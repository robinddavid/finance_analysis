# Project Purple — Stock Analysis & Screening Bot

Eigenständig entwickelter Telegram-Bot zur datenbasierten Analyse und zum Screening von Aktien. **Private Portfolio- und Zugangsdaten sind nicht im Repository enthalten.**

## Funktionen

- Mehrfaktorielles Aktien-Scoring (Bewertung, Wachstum, Profitabilität, Bilanz, Trend, Momentum, Analysten, Insider, Branchenvergleich und Makroumfeld)
- Technische Indikatoren wie RSI, MACD und gleitende Durchschnitte
- Unternehmenskennzahlen, Branchenvergleich und Makrodaten (u. a. FRED)
- Automatisiertes Aktienscreening, Watchlist und Kursalarme
- Morgen-Briefings und interaktive Navigation im Telegram-Bot
- Historische Backtests und laufende Erfassung für einen Forward-Test
- Optionale generative KI-Einordnung über die Anthropic API

Die Scores sind **regelbasiert**, nicht das Ergebnis eines trainierten Machine-Learning-Modells. Die Ergebnisse sind keine Anlageempfehlung. Historische Backtests haben methodische Einschränkungen und garantieren keine zukünftigen Ergebnisse.

## Technischer Aufbau

Python, pandas, NumPy, Matplotlib, python-telegram-bot, yfinance, Finnhub, NewsAPI, DBnomics und FRED. Die optionale KI-Integration nutzt Anthropic. API-Zugangsdaten werden über lokale Umgebungsvariablen geladen.

## Lokales Setup

1. Virtuelle Umgebung erstellen: `python -m venv .venv` und aktivieren.
2. Abhängigkeiten installieren: `pip install -r requirements.txt`.
3. `.env.example` lokal nach `.env` kopieren und mit **neu generierten** API-Keys füllen.
4. `ALLOWED_USER_IDS` mit deiner Telegram-ID belegen. Ohne eine ID ist der Bot absichtlich für Analysefunktionen gesperrt; der Befehl `/id` ist verfügbar, um die ID zu ermitteln.
5. Starten: `python project_purple.py`.

Die lokale `.env`, `purple_secrets.json` sowie die Datei `purple_data.json` mit Nutzerdaten gehören **nicht** ins Repository.

## Veröffentlichung und Sicherheit

Die frühere Entwicklungsdatei enthielt direkt eingebettete Keys. **Alle früheren Tokens und API-Keys vor einer Veröffentlichung beim Anbieter widerrufen/rotieren.** Das Entfernen aus einer Datei macht einen früher bereits hochgeladenen Key nicht wieder geheim; auch öffentliche Git-History und alte Commits müssen geprüft werden.

Diese öffentliche Version ist ein bereinigter Projektstand für Portfolio-/Demozwecke. Vor einem produktiven Betrieb sind Integrationstests, Monitoring, API-Limits und die Verarbeitung von Nutzerdaten gesondert zu prüfen.
