# Deribit dealer gamma, protocol 2: follow-up on the test sample

Protocol: `PREREGISTRATION-2.md`, SHA-256 `b8173c166e67b50343c78ffd086bc4914165986dc5516b9e1de9ff32fabfc3c1`. Hourly data: `hourly.parquet`, SHA-256 `00974cd8f3b4edaa2236116a5f0786fee76b53b5cd05b702d27408e50463ddf9`. Code commit `4d331e7dc83ee84f3970385ca554c4ffcb08d3f9`. Started at 2026-10-12T11:40:03+00:00, run once. Test sample: 13,152 hours, from 2025-04-01 00:00 UTC to 2026-09-30 23:00 UTC; F1 uses 548 days. Every number below is read or derived by `dgamma.report` from `followup.json`.

## Decisions

Neither F1 nor F2 passed. Under section 5 of protocol 2, the study of Deribit dealer gamma ends here; no further test is run on these data.

| Hypothesis | Prediction | Coefficient (SE) | One-sided p, decisional | Two-sided p | Observations | Dropped | Passes |
|---|---|---|---|---|---|---|---|
| F1, next-day volatility on dealer gamma in BTC (G / P) | k < 0 | 3.76e-07 (6.98e-05) | 0.5021 | 0.9957 | 548 | 0 | no |
| F2, next-hour reversal growing with dealers' long gamma, beyond the regime's autocorrelation | c_L < 0 | -1.66e-04 (1.78e-04) | 0.2489 | 0.4978 | 13,152 | 0 | no |

Holm over F1 and F2: smaller one-sided p at most 0.025, larger at most 0.05. F2's decisional p is a wild bootstrap with the null imposed (9,999 draws, Rademacher weights by UTC day); its Newey-West p is 0.1753. Estimated signs: F1 is positive, opposite to the prediction; F2 is negative, the predicted sign.

## Effect sizes

Unadjusted: computed at one-sided 5 % from the Newey-West standard errors, without Holm.

| Hypothesis | Unit | Estimated effect of one SD | Two-sided 95 % interval | Detectable with 80 % power, unadjusted | Most negative effect not rejected, unadjusted |
|---|---|---|---|---|---|
| F1 | log RV of the next day per SD of G / P | 1.61e-04 | [-0.0586, 0.0589] | 0.0745 | -0.0491 |
| F2 | bp of next-hour return per SD of HP over long-gamma hours | -1.26 | [-3.91, 1.39] | 3.36 | -3.48 |

F2 uses 4,527 hours in which dealers were long gamma at h - 1 (34.4 % of the test sample), in 220 runs of consecutive hours (median 5.00 hours, longest 335). With standard errors clustered by UTC day, c_L has a one-sided p of 0.1596.

## Reported, not decisional

| Analysis | Coefficient (SE) | One-sided p, Newey-West | Two-sided p | Effect of one SD | Observations |
|---|---|---|---|---|---|
| F1 with log V at the end of the day added | -8.45e-06 (7.53e-05) | 0.4554 | 0.9107 | -0.00363 | 548 |
| F1 with gamma in dollars, G (exploratory X3 variable) | 1.26e-10 (7.67e-10) | 0.5651 | 0.8698 | 0.00483 | 548 |
| F1 with g = G / V (H3 of protocol 1) | 0.00316 (0.0196) | 0.5638 | 0.8724 | 0.00500 | 548 |
| F1 without block trades, G_nb / P | 3.07e-04 (1.70e-04) | 0.9642 | 0.0715 | 0.0572 | 548 |
| F2 without block trades (regime, g and HP from G_nb) | -0.00147 (6.84e-04) | 0.0156 | 0.0313 | -3.87 | 13,152 |
| F2 with r(h) L(h - 1) / V(h - 1) added | -2.54e-04 (2.29e-04) | 0.1335 | 0.2669 | -1.93 | 13,152 |
| F2 without the UTC day of largest sum of abs(HP L) | 4.95e-06 (1.98e-04) | 0.5100 | 0.9801 | 0.0306 | 13,128 |
| F2 without the 10 hours of largest abs(HP L) | 2.23e-04 (3.29e-04) | 0.7505 | 0.4989 | 1.28 | 13,142 |
| F2, slope when dealers are short gamma, c_S | 5.20e-06 (1.23e-04) | 0.5168 | 0.9663 | 0.0331 | 13,152 |
| F2, extra autocorrelation in long-gamma hours, b_L | 0.0167 (0.0450) | 0.6445 | 0.7110 | n/a | 13,152 |

Fade rule: after each long-gamma hour, hold -sign(r(h)) for one hour, paying the taker fee on entry and exit: 4,521 trades, mean gross -0.154 bp and net -7.15 bp per trade, t-statistic of the net mean -11.5 (one-sided p 1.0000). It measures the reversal of the whole long-gamma regime, not c_L.

## Limits

- The caveats of protocol 1 apply: dealers are inferred from the taker side, Deribit is one venue, and only next-hour or next-day effects are tested.
- F1 was suggested by an exploratory analysis that tried several variants on the estimation sample, and G / P itself was never estimated before this test. F2 was chosen after stage 1 of protocol 1 failed and after the number of long-gamma hours in the test sample was known.
- The long-gamma regime rests largely on block trades; the no-blocks variants show how much.
- Section 7 of protocol 2 gives the power computed before the test.
