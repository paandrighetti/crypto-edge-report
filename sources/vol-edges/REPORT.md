# Forecast against implied volatility: results of the single run

Commit b36bd84; pre-registration SHA-256 0ec4603cb56033df1ec03924ca7f8f78b393758fa39d26568a847a534a3b4643; run started 2026-10-18T11:28:57+00:00, finished 2026-10-18T11:30:07+00:00; gates written 2026-10-16T05:48:50+00:00.

## Decision

| Test | Statistic | Estimate | One-sided p | Holm rejects | Necessary conditions | Pass |
|---|---|---|---|---|---|---|
| V1 | coefficient of the forecast gap, controlling for log DVOL^2 | -0.127 | 0.7345 | no | beta positive each asset: no, daily overlapping beta positive: no | **no** |
| V2 | weekly rule: mean return, and mean return beyond always selling (larger p) | -34.2 bp | 0.9907 | no | mean positive at 2x costs: no | **no** |
| V3 | log(realised / implied variance), event days against controls | -0.078 | 0.2848 | no | negative before 2024: yes, negative from 2024: yes | **no** |
| T1 | mean weekly return of the weekend strangle | 36.6 bp | 0.0062 | yes | mean positive at 2x costs: yes | **yes** |

T1 passes: the next step is a pre-registered forward paper test of the weekend strangle, with the same legal check; no capital.

## V1: does the forecast gap predict the 30-day premium beyond DVOL?

Pooled over bitcoin and ether on 57 non-overlapping 30-day windows (114 rows), with log DVOL^2 as a control: coefficient -0.127, standard error 0.191 (Driscoll-Kraay scores, equal-weighted cosine variance), t = -0.66 with 6 degrees of freedom, one-sided p = 0.7345; coefficient on log DVOL^2 -0.334. By asset: BTC -0.170, ETH -0.102. Daily overlapping regression: -0.158 (t = -1.16, descriptive). Without the DVOL control the slope would be 0.092 (t = 0.38). Rows dropped for missing inputs: 0 daily, 0 decisional. GARCH fits (total, unconverged): BTC 248, 0, ETH 248, 0.

| Asset | Mean log(RV30 / DVOL^2) | DVOL minus realised (vol points) | QLIKE HAR | QLIKE GARCH | QLIKE forecast | QLIKE DVOL | Encompassing: log forecast (t) | log DVOL^2 (t) | Daily-return over 5-minute variance |
|---|---|---|---|---|---|---|---|---|---|
| BTC | -0.189 | 4.43 | 0.171 | 0.204 | 0.174 | 0.131 | -0.226 (-1.59) | 0.817 (6.17) | 0.90 |
| ETH | -0.087 | 2.14 | 0.174 | 0.215 | 0.176 | 0.133 | -0.106 (-0.68) | 0.766 (4.79) | 0.97 |

Mean log premium by year (daily rows): BTC 2022 -0.364, 2023 -0.176, 2024 -0.201, 2025 -0.139, 2026 -0.005; ETH 2022 -0.220, 2023 -0.086, 2024 -0.074, 2025 0.033, 2026 -0.089.

## V2: does trading the weekly gap pay beyond selling?

239 of 246 Fridays priced. Median decision volatility 46.5, median pricing volatility 46.7, median 7-day forecast 54.5, median half-spread 0.00022 BTC. Gap: mean -7.10 points, SD 7.02, correlation with the short straddle's return 0.132. The rule sold 16 weeks, bought 193 and stayed out 37. Studentised bootstrap: mean p = 0.9907, beyond always selling p = 0.9892; 95% interval of the rule's annual Sharpe ratio [-2.28, -0.19]. Worst week: 2022-05-13 08:00 (-583.7 bp). Median gap between the hedge's unwind price and the delivery price: 0.00053.

| Series | Weeks | Mean (bp of notional) | SD (bp) | Annual Sharpe | Worst week (bp) | Max drawdown (bp) | Skewness | Positive weeks (%) |
|---|---|---|---|---|---|---|---|---|
| Rule, c = 2 (decisional) | 246 | -34.2 | 206.8 | -1.19 | -583.7 | 9647.3 | 0.55 | 32 |
| Rule at twice the costs | 246 | -50.5 | 206.7 | -1.76 | -603.4 | 13478.3 | 0.51 | 28 |
| Rule, c = 1 | 246 | -39.6 | 213.8 | -1.34 | -583.7 | 10987.0 | 0.53 | 33 |
| Rule, c = 3 | 246 | -38.0 | 190.6 | -1.44 | -583.7 | 10585.1 | 0.47 | 28 |
| Rule minus always short | 246 | -62.3 | 391.6 | -1.15 | -1127.9 | 18537.4 | 0.70 | 33 |
| Always short | 246 | 28.2 | 218.0 | 0.93 | -702.4 | 2193.2 | -0.60 | 59 |
| Always short at twice the costs | 246 | 9.5 | 219.0 | 0.31 | -724.2 | 2534.8 | -0.61 | 54 |
| Always long | 246 | -65.6 | 216.2 | -2.19 | -596.4 | 17652.6 | 0.58 | 30 |

Mean weekly contribution to the rule (bp of notional): option -16.3, hedge -12.5, hedge cost 6.1, funding 0.8.

By year, rule and always short (mean bp per week): 2022 -64.6 and 43.0; 2023 -29.8 and 7.1; 2024 27.0 and 28.5; 2025 -54.2 and 29.4; 2026 -54.7 and 34.8.

## V3: do daily options overprice event days?

149 of 149 event days used (149 with an implied volatility; 1.83 controls on average) in 125 clusters. log(sum RV / sum IV^2) on event days minus the same on their controls: -0.078 (delta-method SE 0.122, t = -0.64, studentised cluster bootstrap one-sided p = 0.2848); before 2024 -0.029, from 2024 -0.147. Realised part log(sum RV event / sum RV control) 0.262, implied part 0.340. Mean of the per-event log differences (descriptive, biased by the shape of event-day variance): -0.146.

| Event | Days | Statistic | Realised part | Implied part |
|---|---|---|---|---|
| CPI | 56 | 0.023 | 0.356 | 0.334 |
| NFP | 56 | 0.016 | 0.095 | 0.079 |
| FOMC | 38 | -0.364 | 0.295 | 0.659 |

## T1: Deribit's weekend strangle, unpublished window

74 of 74 weekends priced; mean premium 0.0098 BTC; mean deltas 0.35 and -0.34; 81% of weekends won. Studentised bootstrap one-sided p = 0.0062; 95% interval of the annual Sharpe ratio [1.00, 7.04]. Worst weekend: 2025-10-10 16:00 (-440.7 bp); the weekend of 10 October 2025: -440.7 bp.

| Series | Weeks | Mean (bp of notional) | SD (bp) | Annual Sharpe | Worst week (bp) | Max drawdown (bp) | Skewness | Positive weeks (%) |
|---|---|---|---|---|---|---|---|---|
| Strangle | 74 | 36.6 | 94.3 | 2.80 | -440.7 | 524.0 | -2.90 | 81 |
| Strangle at twice the costs | 74 | 25.7 | 94.0 | 1.97 | -451.4 | 544.4 | -2.93 | 76 |

By year (mean bp per weekend): 2025 37.2 (35), 2026 36.0 (39).

## Data-quality gates

| Gate | Pass |
|---|---|
| trades | yes |
| minutes | yes |
| funding | yes |
| dvol | yes |
| events | yes |
| listing | yes |
| iv_V2 | yes |
| iv_V3 | yes |
| iv_T1 | yes |
| settlement_V2 | yes |
| settlement_T1 | yes |

Void tests: none.
