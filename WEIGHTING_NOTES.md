# Project Purple — Weighting Update (v2)

This release retains the prior compliance separation of FRED and Anthropic, and NewsAPI developer-only gating. **It does not establish legal compliance** with all data-provider licences.

## Strategy hypothesis

- Indicative horizon: **3–7 years**. Equity risk: **high**, not a quantitative risk rating.
- Style: **quality / growth / value**, with secondary trend and momentum confirmation.
- Purpose: personal, experimental investment research; not financial advice.

## Updated heuristic weights (sum: 100%)

| Factor | Old normalized share (no-FRED v1) | New weight |
| --- | ---: | ---: |
| Valuation | 20.00% | 20% |
| Growth | 20.00% | 22% |
| Profitability | 15.56% | 20% |
| Balance-sheet strength | 15.56% | 15% |
| Trend | 5.56% | 6% |
| Momentum | 5.56% | 7% |
| Analysts | 5.56% | 3% |
| Insider | 5.56% | 2% |
| Sector peer comparison | 6.67% | 5% |

Fundamental indicators now account for **77%**, technical signals for **13%**, external opinions/insider activity for **5%**, and sector peers for **5%**. Lower weights on analysts, insiders and peers aim to reduce noisy and partly overlapping signals, though overlap also remains within fundamentals.

## Important methodological caveats

1. **Not validated**: the weights are an informed design hypothesis, not optimized using historical or out-of-sample returns. Better theoretical interpretation does NOT demonstrate superior investment results.
2. **Data completeness**: missing scores currently contribute neutral 50/100. Results with low coverage can be misleading. A coverage/confidence score is a recommended future improvement.
3. **Sector calibration**: factor thresholds are not uniformly suited to banks, utilities, technology and early-stage companies.
4. **Backtest parity**: historical simulations use only the factors supported by the available historical inputs. The same weights apply to factors that are available, but **the historical and full live scoring models are not identical**. Selection/survivorship biases and data-availability limits remain.
5. **Trading thresholds**: thresholds of 55/70 are unchanged and have not been recalibrated for the new distribution.
6. **History reset**: the next bot startup clears older `history` and `screen` entries from local `purple_data.json` to prevent comparisons between scoring methodologies. Existing watchlists, alerts and peer data are retained. Make a private backup first if you need past records.

## Research basis

Quality-related definitions commonly emphasize profitability, growth and safety; conventional factor research also discusses value and momentum. These publications provide **directional motivation** only, **not a derivation of Project Purple's particular percentages**.

- Asness, Frazzini & Pedersen, *Quality Minus Junk*: https://www.aqr.com/insights/research/working-paper/quality-minus-junk
- MSCI, *Foundations of Factor Investing*: https://www.msci.com/research-and-insights/paper/foundations-of-factor-investing

## How to run

Rename `project_purple_weighted.py` to `project_purple.py` if using the standalone file, or use the already-named version inside the release ZIP. Keep your `.env` local. The score-profile name and weights are defined at the top of the Python script. Run the included offline smoke tests with `python3 test_compliance.py`, then `python3 test_weighting.py`.
