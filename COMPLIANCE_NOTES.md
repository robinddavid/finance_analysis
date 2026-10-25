# Project Purple – Compliance and Setup Notes

This version retains the original Telegram bot features while separating third-party restricted data flows. It is a personal research prototype, not financial advice or a licensed market-data redistribution service. **No software change can guarantee legal compliance; the owner must follow each provider's current terms and the rights of underlying data providers.**

## Changes in this version

- **FRED:** No caching of FRED API observations, no persistence of FRED content or FRED-derived stock scores, no scheduled FRED requests, and no FRED inputs in Anthropic prompts. The explicit `/macro` function and the macro button in a stock report request a fresh, short-lived response from FRED; the macro view includes the required FRED attribution and Terms link. Do not forward, archive or redistribute output without rights.
- **Stock scoring:** The former **10% FRED macro factor is removed** from the stored/reporting scoring formula. The remaining nine weights (total 90) are normalized to 100%. Consequently **scores are not directly comparable with earlier releases**. FRED is still accessible separately as live context. The strategy/backtesting methodology remains experimental and has not been independently validated.
- **Existing user data:** On first successful bot startup, older `history` and `screen` entries are discarded because they may include FRED-derived scores. Watchlists, alert preferences and peer data are preserved. You should review backups of legacy `purple_data.json` separately.
- **Claude/Anthropic:** Optional analysis is built solely from a non-FRED stock report plus company-specific Finnhub headlines. No FRED raw values or FRED-derived aggregate scores are sent to Claude.
- **NewsAPI:** Free Developer plan access is disabled by default. A NewsAPI request is possible *only* if `APP_ENV=development` AND `NEWS_API_DEV_MODE=true` AND `NEWS_API_KEY` is set. **Do not enable these flags in a running private/production deployment.** Company news via Finnhub continues independently and may have separate restrictions.
- **Secrets:** All API keys are read from local environment variables; the FRED key is no longer accepted via Telegram chat or saved to `purple_secrets.json`. The `/fredkey` command now displays safe setup instructions only. The Telegram bot is restricted to `ALLOWED_USER_IDS`; `/id` remains accessible for initial setup.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
cp .env.compliance.example .env
# Edit .env locally to supply fresh keys and YOUR numeric Telegram user ID.
python project_purple_compliance.py
```

Create a bot through [Telegram BotFather](https://t.me/BotFather). Do not share your token.

To update an existing GitHub repository, upload `project_purple_compliance.py` and update the README/start command to reference it, or rename this file to `project_purple.py` before uploading and keep the original command unchanged. **Do not upload `.env`.**

## Licensing references (verified 2026-10-25)

- FRED Terms: https://fred.stlouisfed.org/legal/terms/
- NewsAPI pricing/developer limitations: https://newsapi.org/pricing
- NewsAPI terms: https://newsapi.org/terms
- Yahoo Finance / yfinance data are subject to separate rights. Finnhub news and financial data may have provider-specific distribution rights; verify your account permissions. Anthropic API use is subject to its API terms.

### Required FRED attribution

> This product uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis.

**Testing limitations:** Source code syntax and offline mocked behavior are tested. Live Telegram authentication, full yfinance/Finnhub/FRED/NewsAPI/Anthropic API integration, rate limits and provider licensing for a specific account have not been independently verified in a running deployment.
