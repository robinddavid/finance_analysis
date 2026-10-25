"""Offline smoke tests for the compliance-separated Project Purple bot.
Run: python test_project_purple_compliance.py
Third-party Telegram, Yahoo and DBnomics modules are stubbed; no network calls.
"""
import sys, types, pathlib, importlib.util, unittest
from unittest.mock import Mock, patch
import ast

ROOT = pathlib.Path(__file__).parent
SCRIPT = (ROOT / "project_purple_compliance.py") if (ROOT / "project_purple_compliance.py").exists() else (ROOT / "project_purple.py")

for name in ("telegram", "telegram.ext", "yfinance", "dbnomics"):
    sys.modules[name] = types.ModuleType(name)
telegram = sys.modules["telegram"]
for name in ("BotCommand", "ForceReply", "InlineKeyboardButton", "InlineKeyboardMarkup", "LinkPreviewOptions", "Update"):
    setattr(telegram, name, type(name, (), {}))
ext = sys.modules["telegram.ext"]
for name in ("Application", "CallbackQueryHandler", "CommandHandler", "MessageHandler"):
    setattr(ext, name, type(name, (), {}))
ext.ContextTypes = types.SimpleNamespace(DEFAULT_TYPE=object)
ext.filters = types.SimpleNamespace()
sys.modules["yfinance"].Ticker = Mock()
sys.modules["dbnomics"].fetch_series = Mock()

spec = importlib.util.spec_from_file_location("purple_compliance_for_test", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class ComplianceTests(unittest.TestCase):
    def setUp(self):
        mod._cache.clear()

    def test_newsapi_off_by_default(self):
        mod.NEWS_API_ENABLED = False
        with patch.object(mod.requests, "get", side_effect=AssertionError("NewsAPI called")):
            self.assertEqual(mod.market_news(), [])

    def test_newsapi_explicit_test_only(self):
        mod.NEWS_API_ENABLED = True
        mod.NEWS_API_KEY = "example_for_test"
        mock_resp = Mock(status_code=200)
        mock_resp.json.return_value = {"articles": [{"title": "Example"}]}
        with patch.object(mod.requests, "get", return_value=mock_resp) as req:
            self.assertEqual(len(mod.market_news()), 1)
            self.assertIn("newsapi.org", req.call_args.args[0])
        mod.NEWS_API_ENABLED = False

    def test_fred_not_cached_and_notice_present(self):
        mod.FRED_API_KEY = "test_only_fake_key"
        resp = Mock(status_code=200)
        resp.json.return_value = {"observations": [{"date": "2026-10-25", "value": "4.2"}]}
        with patch.object(mod.requests, "get", return_value=resp) as req:
            self.assertEqual(mod.fred_get_series("VIXCLS")[0]["value"], 4.2)
            self.assertEqual(mod.fred_get_series("VIXCLS")[0]["value"], 4.2)
            self.assertEqual(req.call_count, 2)
        self.assertFalse(any(k.startswith("fred:") for k in mod._cache))
        with patch.object(mod, "fred_macro_data", return_value={"values": {
            "vix": {"value": 20.0}, "spread": {"value": 1.2}, "fed": {"value": 4.0},
            "unemployment": {"value": 4.3}, "cpi": {"value": 320}, "cpi_yoy": .03,
        }, "score": 58, "regime": "Gemischt", "stamp": "today"}):
            msg = mod.macro_text()
            self.assertIn("not endorsed or certified", msg)
            self.assertIn("FRED Terms of Use", msg)

    def test_fred_network_error_never_contains_key(self):
        mod.FRED_API_KEY = "sensitive_fake_secret"
        import requests
        with patch.object(mod.requests, "get", side_effect=requests.RequestException("https://fred.invalid/?api_key=sensitive_fake_secret")):
            with self.assertRaises(RuntimeError) as ctx:
                mod.fred_get_series("VIXCLS")
            self.assertNotIn("sensitive_fake_secret", str(ctx.exception))

    def test_finnhub_network_error_redacts_token(self):
        mod.FINNHUB_API_KEY = "sensitive_finnhub_fake_token"
        import requests
        with patch.object(mod.requests, "get", side_effect=requests.RequestException("https://finnhub.io/?token=sensitive_finnhub_fake_token")):
            with self.assertRaises(RuntimeError) as ctx:
                mod.fh_get("company-news")
            self.assertNotIn("sensitive_finnhub_fake_token", str(ctx.exception))

    def test_newsapi_network_error_redacts_key(self):
        mod.NEWS_API_ENABLED = True
        mod.NEWS_API_KEY = "sensitive_news_fake_key"
        import requests
        with patch.object(mod.requests, "get", side_effect=requests.RequestException("https://newsapi.org/?apiKey=sensitive_news_fake_key")):
            with self.assertRaises(RuntimeError) as ctx:
                mod.market_news()
            self.assertNotIn("sensitive_news_fake_key", str(ctx.exception))
        mod.NEWS_API_ENABLED = False

    def test_scores_dont_include_macro(self):
        subs = {k: 65 for k in mod.COMP_ORDER}
        score, detail = mod.combine(subs)
        self.assertAlmostEqual(score, 65.0)
        self.assertNotIn("macro", detail)
        self.assertAlmostEqual(sum(v["w"] for v in detail.values()), 100)

    def test_ai_request_excludes_fred(self):
        mock_report = {
            "name": "Example Company", "final": 64.0,
            "m": {"pe": 18, "fpe": 17, "peg": 2, "roe": .2, "om": .25, "rev_g": .13, "de": 30, "upside": 12},
            "tech": {"price": 123, "day_chg": .01, "rsi": 53, "sma200": 113},
            "earn_days": 20,
            "detail": {k: {"sub": 64} for k in mod.COMP_ORDER},
        }
        resp = Mock()
        resp.json.return_value = {"content": [{"type": "text", "text": "Test succeeded"}]}
        with patch.object(mod, "build_report", return_value=mock_report), \
             patch.object(mod, "company_news", return_value=[]), \
             patch.object(mod.requests, "post", return_value=resp) as post:
            result = mod.ai_analysis("ABC")
        self.assertEqual(result, "Test succeeded")
        body = post.call_args.kwargs["json"]["messages"][0]["content"]
        self.assertIn("OHNE FRED", body)
        for label in ("VIX", "FEDFUNDS", "Makro/FRED-Score", "Arbeitslosigkeit", "macro_facts"):
            self.assertNotIn(label, body)

    def test_source_data_flows_are_separated(self):
        tree = ast.parse(SCRIPT.read_text())
        fn = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
        for name in ("_build_report", "_light_score", "build_report", "ai_analysis"):
            called = {n.func.id for n in ast.walk(fn[name]) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
            self.assertNotIn("analyze_macro", called, name)
            self.assertNotIn("fred_macro_data", called, name)
            self.assertNotIn("fred_get_series", called, name)
        self.assertNotIn("FRED_SECRET_FILE", SCRIPT.read_text())

if __name__ == "__main__":
    unittest.main(verbosity=2)
