# Deribit dealer gamma and bitcoin returns: results

Protocol: `PREREGISTRATION.md`, SHA-256 `22c16766f1bc7df9922fa72d583f740d82e285eb2c567188683b2bbd6065e777`. Hourly data: `hourly.parquet`, SHA-256 `00974cd8f3b4edaa2236116a5f0786fee76b53b5cd05b702d27408e50463ddf9`. Stage 1 run at 2026-10-12T08:29:51+00:00, stage 2 not run. Every number below is read or derived by `dgamma.report` from the JSON outputs of the build, of stage 1 and of the work done after stage 1 (checks.json, exploratory.json). Everything except the tables of decisions, gates and reported analyses was written after the stage 1 results were known, following an independent review; none of it changes a number of the stages (POST_RESULTS.md).

## 1. Decisions

No hypothesis passed stage 1. Under section 6 of the protocol all three are abandoned and reported as negative results. Stage 2 was not run: no hypothesis was left to test. The stage 2 code would also have computed the statistics of section 4 on the test sample; they were not computed, so that the returns of the test sample stay unexamined for any follow-up, which must be pre-registered before using them (POST_RESULTS.md).

| Hypothesis | Prediction | Stage 1 coefficient (SE) | One-sided p | Passes stage 1 | Stage 2 coefficient (SE) | One-sided p | Replicates |
|---|---|---|---|---|---|---|---|
| H1, hourly hedging pressure | c < 0 | 2.15e-04 (1.50e-04) | 0.9241 | no | not tested | |  |
| H2, hedging pressure after large moves | c < 0 | 1.87e-04 (2.39e-04) | 0.7837 | no | not tested | |  |
| H3, dealer gamma and next-day volatility | k < 0 | -0.0221 (0.0474) | 0.3203 | no | not tested | |  |

Stage 1 decides H1 and H2 together by Holm (smaller one-sided p at most 0.025, larger at most 0.05) and H3 alone at 0.05. Stage 2 re-estimates only what passed; a hypothesis replicates with the predicted sign and a one-sided p at most 0.05. Estimation sample: 23,376 hours, from 2022-08-01 00:00 UTC to 2025-03-31 23:00 UTC (hour h is the end of a clock hour). Test sample: not used.

Estimated signs: H1 is positive, opposite to the prediction (two-sided p 0.1519); H2 is positive, opposite to the prediction (two-sided p 0.4326); H3 is negative, the predicted sign (two-sided p 0.6405).

Stage 3 (trading rule) was not run: it requires H2 to replicate.

## 2. Effect sizes and power

Effects are per standard deviation of the regressor. The detectable effect is the size that a one-sided test at 0.05 detects with 80 % power (2.49 standard errors). The last column is the one-sided 95 % bound: effects more negative than it are rejected by the data, for G as measured under the taker convention. The detectable effect describes the design, the bound where the estimate fell; the bound can be tighter for that reason alone. In correlation units (effect per SD of HP over the SD of the next-hour return), the detectable effect is H1 0.0386 and H2 0.114, larger than the sizes the power analysis of section 8 of the protocol planned for, so the tests had less power than planned. H2 has 499 day clusters.

| Hypothesis | Sample | Observations | Dropped | Unit | Estimated effect of one SD | Two-sided 95 % interval | Detectable with 80 % power | Most negative effect not rejected |
|---|---|---|---|---|---|---|---|---|
| H1 | estimation | 23,376 | 0 | bp of next-hour return per SD of HP | 1.18 | [-0.435, 2.80] | 2.05 | -0.175 |
| H2 | estimation | 1,112 | 0 | bp of next-hour return per SD of HP over qualifying hours | 3.57 | [-5.34, 12.5] | 11.3 | -3.91 |
| H3 | estimation | 974 | 0 | log RV of the next day per SD of g | -0.0140 | [-0.0727, 0.0447] | 0.0745 | -0.0633 |

## 3. Data quality

| Gate | Value | Requirement |
|---|---|---|
| Q1 missing days | 0 | 0 |
| Q1 days without a trade | 0 | 0 |
| Q2 duplicate trades among 20,874,423 | 0 | 0 |
| Q3 share of hours without a candle | 0.0 % | at most 0.5 % |
| Q4 sample hours with a live option created before the data | 0 | 0 |
| Q5 days downloaded twice, all identical | 30, yes | 30, yes |
| Q6 options with a gap in trade_seq, of 73,554 | 0 | 0 |
| Q7 trades without metadata | 0 | 0 |
| Q8 trades before creation | 0 | 0 |
| Q8 trades one hour or more after expiry | 0 | 0 |
| Q8 traded options expiring off the hour | 0 | 0 |
| All gates pass | yes | yes |

Reported only: 6 trades in the hour after expiry, 65,461 trades whose `iv` counts as missing, 3 sample hours with a zero-volume candle.

## 4. Reported analyses, not decisional

Section 7 of the protocol. The stage code computed R1 to R3 for H1 and H2 only, although the protocol does not restrict them; for H3 they are in section 6.

| Analysis | Sample | Coefficient (SE) | One-sided p | Observations |
|---|---|---|---|---|
| R1, H1 without block trades | estimation | 4.76e-04 (3.30e-04) | 0.9253 | 23,376 |
| R1, H2 without block trades | estimation | 5.18e-04 (5.92e-04) | 0.8094 | 1,112 |
| R2, H1 with per-option IV | estimation | 1.90e-04 (1.37e-04) | 0.9179 | 23,376 |
| R2, H2 with per-option IV | estimation | 1.75e-04 (2.26e-04) | 0.7803 | 1,112 |
| R3, H1 with standardised G | estimation | 8.95e-05 (1.05e-04) | 0.8030 | 23,376 |
| R3, H2 with standardised G | estimation | -1.54e-05 (1.94e-04) | 0.4684 | 1,112 |
| R4, H2 at the 5th/95th percentiles | estimation | 2.71e-04 (2.04e-04) | 0.9085 | 2,230 |
| R4, H2 at the 1st/99th percentiles | estimation | 3.55e-04 (3.46e-04) | 0.8472 | 433 |
| R5, H1 without 07:00-09:00 | estimation | 1.91e-04 (1.62e-04) | 0.8814 | 20,454 |
| R5, H2 without 07:00-09:00 | estimation | 1.70e-04 (2.52e-04) | 0.7495 | 1,037 |
| R6, H1 with every trade iv | estimation | 2.13e-04 (1.50e-04) | 0.9228 | 23,376 |
| R6, H2 with every trade iv | estimation | 1.86e-04 (2.39e-04) | 0.7814 | 1,112 |
| R6, H3 with every trade iv | estimation | -0.0222 (0.0473) | 0.3196 | 974 |

| Statistic | Estimation sample | Test sample |
|---|---|---|
| P1 placebo, share of draws at least as negative, H1 | 0.893 | not run |
| P1 placebo, share of draws at least as negative, H2 | 0.755 | not run |
| Every-hour rule, hours | 23,376 | not run |
| Every-hour rule, gross bp per hour | -0.722 | not run |
| Every-hour rule, net bp per hour | -4.47 | not run |
| Every-hour rule, gross annualised Sharpe ratio | -1.27 | not run |
| Every-hour rule, net annualised Sharpe ratio | -7.86 | not run |
| Share of hours with dealers long gamma | 0.0466 | not run |
| Median G, million dollars per 1 % move | -14.1 | not run |
| 5th percentile of G, same unit | -49.6 | not run |
| 95th percentile of G, same unit | -0.273 | not run |
| Median abs(g), G over mean hourly perpetual volume | 0.816 | not run |
| Mean abs(G minus G without blocks) over mean abs(G) | 0.627 | not run |
| Median number of options held | 635 | not run |
| Most options held without implied volatility in an hour | 0 | not run |
| Hours without sigma_near | 0 | not run |

The every-hour rule holds -sign(HP) for one hour, paying the taker fee per unit of position traded, so twice on a reversal. With dealers short gamma in most hours, it is close to hourly momentum; its result reflects the autocorrelation of hourly returns more than the coefficient c.

## 5. Checks after stage 1, no return involved

### Taker side by trade type

A taker who buys should pay above the mark price and one who sells should receive below it.

| Trade type | Trades | Share of traded BTC | Share where the taker pays | Share where the taker receives | Taker pays, amount-weighted |
|---|---|---|---|---|---|
| block | 281,242 | 34.2 % | 80.9 % | 19.1 % | 83.9 % |
| block RFQ | 46,054 | 4.7 % | 77.8 % | 22.2 % | 77.5 % |
| combo leg | 106,747 | 0.4 % | 43.5 % | 56.5 % | 49.9 % |
| order book | 20,426,446 | 60.7 % | 62.7 % | 37.3 % | 64.4 % |

For block, block RFQ and order book trades, the recorded side pays the spread more often than not: Deribit's field behaves as the taker's side, block trades included. This validates the field, not the assumption that takers are customers.

### Candle timing

Median absolute log gap between a candle's close and the index of the last option trade before h, over 8,760 hours of 2023: 0.00165 for the candle ending at h - 1h, 3.18e-04 for the candle ending at h, 0.00169 for the candle ending at h + 1h. The closest is the candle ending at h, as the code assumes.

### Dealer gamma by year, no return involved

| Year | Sample | Hours | Share of hours with dealers long gamma | Same without block trades | Same sign with and without blocks | Median G, million dollars per 1 % move | Same without block trades |
|---|---|---|---|---|---|---|---|
| 2022 | estimation | 3,672 | 1.6 % | 17.4 % | 83.5 % | -4.76 | -1.58 |
| 2023 | estimation | 8,760 | 11.0 % | 23.0 % | 84.9 % | -11.1 | -3.16 |
| 2024 | estimation | 8,784 | 0.6 % | 8.8 % | 91.5 % | -19.8 | -7.83 |
| 2025 | estimation and test | 8,760 | 36.2 % | 22.4 % | 70.2 % | -11.9 | -12.2 |
| 2026 | test | 6,552 | 20.9 % | 13.6 % | 83.9 % | -16.8 | -11.6 |

In the years of the estimation sample alone, dealers are long gamma in 0.6 % to 11.0 % of hours; without block trades the share is 8.8 % to 23.0 %: block trades deepen dealers' short gamma, which remains the norm without them. In the years that include the test sample, the share is 36.2 % (2025) and 20.9 % (2026); these figures involve G only, no return.

## 6. Exploratory analyses after stage 1, not pre-registered

Chosen after the stage 1 results, following an independent review, and run on the estimation sample only: the hourly file is cut at the end of that sample before anything is computed. They cannot change a decision. Dividing G by the perpetual volume V puts 1/V(h - 1) into HP, so if hourly returns reverse more when volume is low, c is pushed upwards; X1 controls for it. X2 does the same for H3, and X3 runs R1 to R3 for H3.

| Analysis | Coefficient (SE) | One-sided p | Two-sided p | Observations |
|---|---|---|---|---|
| H1 as in stage 1 | 2.15e-04 (1.50e-04) | 0.9241 | 0.1519 | 23,376 |
| H1 with r(h) / V(h - 1) as a control | 2.16e-04 (1.50e-04) | 0.9241 | 0.1517 | 23,376 |
| H2 as in stage 1 | 1.87e-04 (2.39e-04) | 0.7837 | 0.4326 | 1,112 |
| H2 with r(h) / V(h - 1) as a control | 1.79e-04 (2.44e-04) | 0.7678 | 0.4644 | 1,112 |
| H3 as in stage 1 | -0.0221 (0.0474) | 0.3203 | 0.6405 | 974 |
| H3 with log V at the end of the day as a control | 0.0299 (0.0523) | 0.7159 | 0.5682 | 974 |
| H3 without block trades, R1 for H3 | -0.0548 (0.0803) | 0.2476 | 0.4951 | 974 |
| H3 with per-option IV, R2 for H3 | -0.0246 (0.0399) | 0.2684 | 0.5369 | 974 |
| H3 with G standardised and no volume, R3 for H3 | -0.0514 (0.0244) | 0.0174 | 0.0349 | 974 |

With the liquidity control, c moves by +0.4 % in H1 and -4.7 % in H2: the liquidity channel does not explain the stage 1 estimates. For H3 the sign of k depends on how volume enters: -0.0221 (H3 as in stage 1), 0.0299 (H3 with log V at the end of the day as a control), -0.0514 (H3 with G standardised and no volume, R3 for H3). The smallest one-sided p, 0.0174 (H3 with G standardised and no volume, R3 for H3), is nominal: with a Bonferroni correction it becomes 0.0697 over the 4 H3 variants chosen after the results and 0.1046 over all 6 H3 specifications of this report. G in dollars also rises with the bitcoin price for given positions, so this regressor carries the price trend. It is a hypothesis for a test on the test sample, under a new protocol that fixes the scaling of G in advance (for example G divided by the price); no further variant is run on the estimation sample.

## Limits

- Deribit does not identify dealers. The study takes the taker of each trade as the customer and the maker as the dealer. Dealers also take liquidity from each other, customers also post limit orders, and directional funds also make markets; each case puts the wrong sign on part of G. Misclassified sides do not only add noise: they shrink G, can reverse it, and can bias the coefficients either way, so the bounds of section 2 hold for G as measured, not for true dealer gamma.
- In the estimation sample G rarely changes sign: dealers are long gamma in 4.7 % of the hours. H1 and H2 therefore test mainly whether momentum grows with the size of dealers' short gamma; the reversal predicted for dealers long gamma is barely tested (section 5 gives the later years).
- Only next-hour effects are tested. The protocol assumes that dealers on Deribit hedge continuously; an effect inside hour h, or one concentrated at a fixed time as in the equity setting of the protocol's reference, would be missed.
- Implied volatility is one value per expiry, amount-weighted, which ignores the smile; R2 and R6 report two alternatives.
- V is the volume of Deribit's perpetual only. Dealers also hedge with futures, spot and other venues, so g overstates the hedge relative to the liquidity that absorbs it, and V moves with Deribit's market share.
- HP uses the gamma of the hour before, a linear approximation of the hedge that overstates it for large moves and for options close to expiry.
- H3 controls for implied volatility, so an effect already priced into implied volatility is absorbed.
- Black-76 uses the perpetual price as the forward of every expiry, while Deribit quotes each option's `iv` against that expiry's own forward; the delta of premiums and margin held in BTC is ignored.
- One venue. Deribit's share of listed bitcoin option open interest fell over the period (protocol, section 2), so G misses a growing part of dealer gamma, in particular IBIT and CME options.
