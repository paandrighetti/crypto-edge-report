# Crypto slow edges: interpretation of the single run (round 2)

Written after the run of commit `7e3722c`, so it is not part of the pre-registered analysis; the decisions are those
of REPORT.md. Every number below is filled in by `scripts/post_results.py` from results.json, verification.json (the
independent recomputation, whose daily series give the breakdowns by period), verification/PROVENANCE.txt and the log
of operations job 0093 (`ops/logs`). Returns are in basis points (bp) of capital.

## Outcome

E3, the long-or-cash trend rule on bitcoin and ether spot, passes. The composite of 21-day momentum (E1) and premium
carry (E2) on the 100 most traded Binance perpetuals fails. Holm's procedure rejects E3's null at its first step
(one-sided p = 0.0047, against 2.5%), and E3's two other conditions hold: its timing statistic stays positive without
its best month, 2022-06 (3.79 bp a day), and at twice the costs (4.44 bp a day). The composite fails Holm's procedure
(one-sided p = 0.241), although its other conditions hold. Its bound, 1.51, is above 0.5, so the failure is
inconclusive: the direction is not closed, and the rule is not re-tuned on these data.

| Design | Statistic | Estimate | 95% bootstrap interval | Monthly t | One-sided p | Decision | Bound |
|---|---|---|---|---|---|---|---|
| composite | net Sharpe ratio | 0.38 | [-0.50, 1.51] | 0.81 | 0.241 | fail, inconclusive | 1.51 |
| E3 | timing information ratio | 0.82 | [0.08, 1.48] | 2.09 | 0.0047 | pass | 1.62 |

Under section 6, the pass makes E3 a candidate for forward paper trading, without capital, under a new
pre-registration of the same rule. Holm's step-down keeps the family-wise error at 5%. The pass shows that, over this
window, the rule's exposure covaried with the next day's returns by more than its costs, compared with paths of
independent days. It shows neither that this persists, nor that it is independent of choices made knowing the market's
path, nor how large the edge is. The two other conditions add little, since the timing statistic reaches zero only at
about 10 times the costs. The pass is no basis for committing capital.

## The computations were checked independently

A second implementation (`verification/verify_cse.py`) recomputed the decisional numbers on the same data with its own
random seeds. A separate agent wrote it from PREREGISTRATION.md and its first amendment (the later amendments change
no rule it implements) and, by its author's account, without the project's code; its file was last modified at
2026-10-13 19:25:35 UTC, before the run started at 2026-10-13 20:21:05 UTC, but its hash was first recorded by job
0092, after the run. In the table below, the statistics that do not depend on simulation agree to within 2.2e-15,
except the weekly slope on the premium; the p-values and bounds, which depend on simulation, differ by simulation
error. Both implementations take the same decisions. Spot checks inside the recomputation compared its grid-based
handling of the data with direct timestamp computations from the raw files for 20 random series: 860 comparisons, 0
mismatches. They test the recomputation's own data handling; the agreement of the statistics tests the official
code's.

| Statistic | Depends on simulation | Official run | Recomputation | Absolute difference |
|---|---|---|---|---|
| Composite: mean net return, bp a day | no | 4.10109 | 4.10109 | 1.8e-15 |
| Composite: net Sharpe ratio | no | 0.376036 | 0.376036 | 2.2e-16 |
| Composite: monthly Newey-West t | no | 0.809647 | 0.809647 | 1.1e-16 |
| Composite: mean without its best month, bp a day | no | 2.91414 | 2.91414 | 4.4e-16 |
| Composite: mean without deaths and extreme funding, bp a day | no | 2.52875 | 2.52875 | 2.2e-15 |
| Composite: weekly slope on the 21-day return | no | 0.0024434 | 0.0024434 | 0 |
| Composite: net Sharpe ratio at twice the costs | no | 0.108809 | 0.108809 | 9.7e-17 |
| E3: mean net return, bp a day | no | 11.7158 | 11.7158 | 0 |
| E3: timing information ratio | no | 0.815464 | 0.815464 | 0 |
| E3: timing monthly Newey-West t | no | 2.08593 | 2.08593 | 0 |
| E3: timing without its best month, bp a day | no | 3.78832 | 3.78832 | 0 |
| E3: timing at twice the costs, bp a day | no | 4.43794 | 4.43794 | 0 |
| Benchmark: net Sharpe ratio | no | 0.67894 | 0.67894 | 0 |
| E1: mean net return, bp a day | no | 6.9135 | 6.9135 | 1.8e-15 |
| E2: mean net return, bp a day | no | 1.46932 | 1.46932 | 4.4e-16 |
| Composite: weekly slope on the premium | no | -9.23803e-05 | -9.26668e-05 | 2.9e-07 |
| Composite: one-sided p | yes | 0.240729 | 0.239459 | 0.0013 |
| Composite: bound (upper end of the Sharpe ratio's interval) | yes | 1.50588 | 1.50728 | 0.0014 |
| E3: one-sided p | yes | 0.00474976 | 0.00564972 | 0.0009 |
| E3: null's mean information ratio | yes | -0.137156 | -0.135993 | 0.0012 |
| E3: bound (interval's upper end minus the null's mean) | yes | 1.61921 | 1.6151 | 0.0041 |

Two differences remain. For E1, E2 and the composite, the split of the net result between price and funding differs by
up to 0.11 bp a day while the net agrees. In the interval in which a sub-portfolio is liquidated, the official code
books the funding accrued in that interval before the liquidation hour as funding, and the recomputation books the
whole loss as price. The whole gap falls in September 2025, the month of all eight liquidations: the composite's gap
equals E1's and E2's at that month's weight on E1, 0.472. And the weekly slope on the premium differs in its third
significant digit (-9.238e-05 against -9.267e-05, t = -0.0276 against -0.0277): both are negative, as the composite's
condition requires, and both are indistinguishable from zero.

## E3: what the pass rests on

1. The timing statistic, the rule's net return minus a static holding of its mean exposures (0.28 in bitcoin and 0.28
   in ether), earned 1.51% a month. By calendar year (sums of the daily statistic, in % of capital): 2021 54.2%, 2022
   14.1%, 2023 0.4%, 2024 19.1%, 2025 10.9%, 2026 5.5%.
2. It is concentrated at the start. The window opens with the rule at exposures of 0.50 and 0.50 on 1 January 2021,
   early in that year's rally: January to April 2021 give 47% of the statistic's total, and its best month, 2022-06,
   another 25%. Only 35 of 69 months are positive. Dropping the statistic's first two or four months gives t = 1.88 or
   1.50, against the critical value of 1.53 that section 8 computed for 69 months (not recalibrated for the shorter
   windows). Of the total, 77% accrued from January 2021 to June 2022, the 18 months that overlap Harvey et al.'s
   sample. From July 2022, the pre-registered sub-window gives an information ratio of 0.37, t = 1.00, one-sided p =
   0.076: positive, not significant on its own. That sub-window lies outside Harvey et al.'s sample, but not outside
   what was known when the rule was chosen.
3. The margin covers the test's measured liberal bias. Section 8 measured the calibrated test's rejection rate, at a
   nominal 2.5%, between 2.4% and 3.3% depending on the volatility model. The p-values of the two implementations,
   0.0047 and 0.0056, are about 19% and 23% of 2.5%, so that bias cannot overturn the rejection; the bias further in
   the tail was not measured.
4. The test is not blind to the market's path (section 1): the rule was chosen knowing that 2022 had a deep drawdown.
   Its horizons, 30, 91 and 365 days, long or cash, come from Hurst, Ooi and Pedersen and were not tuned.
5. The variants that share the signal agree in sign, so they are not independent evidence: with a 30% volatility
   target the timing information ratio is 0.64 (t = 1.69), on the perpetuals 0.43 (t = 1.39), which pay 2.6 bp a day
   of funding. The one-week moving-average rule, another signal, has -0.38.
6. Against its own static holding, the rule added return rather than cut risk. The static holding of its mean
   exposures, 56% of capital on average, earns 6.7 bp a day at 36% annualised volatility (the benchmark's Sharpe
   ratio, 0.68); the rule earns 11.7 at 43%. Its lower risk than the benchmark holding half in each coin (volatility
   43% against 65%, maximum drawdown in sums of returns 56% against 124%) comes from being 56% invested on average.
7. Deflated for the 13 trials, E3's net Sharpe ratio of 0.99 has a deflated Sharpe ratio of 0.82, below the 0.95 that
   a stand-alone claim would need.
8. A forward test cannot confirm the edge in a useful horizon. At an information ratio r, a t-statistic of 2 is an
   even bet after about (2 / r) squared years: 6 years at the full window's 0.82, 29 at the sub-window's 0.37. Odds of
   80% need 12 years at 0.82, the estimate that passed the test and so is more likely too high than too low. The
   forward statistic must also fix its static exposures in advance or calibrate its own null, because the small-sample
   term grows as the window shortens (the null's mean information ratio is -0.14 over 69 months and -0.18 over 51).
   Forward paper trading, the protocol's only holdout (section 2), can check the implementation, not the edge.

## The composite: no detectable edge, and one ruinous squeeze

1. Neither leg shows a detectable edge net of costs: E1's net Sharpe ratio is 0.45, E2's 0.11, the composite's 0.38.
   By year, E1's net Sharpe ratio was negative in 2022 and 2023 and E2's in 2025 and 2026; the composite's was 2.84 in
   2021. E1 sits inside the 0.4 to 0.7 that section 1 expected; E2's Sharpe ratio before costs, 0.34, is far below the
   1.8 implied by Chi et al.'s sample. The mechanism conditions held in sign only: the weekly slope on the 21-day
   return has t = 0.54, the slope on the premium t = -0.03.
2. E2 earned its carry as funding and lost it on price (-7.2 bp a day of price against 11.6 of funding): the contracts
   it shorted for their rich premiums outperformed those it bought, so the price effect that section 4 expected to
   point the same way pointed the other.
3. On 2025-09-08 the composite lost 48% in a day, 84% over the seven days to 2025-09-13, and 71% in September 2025.
   All 8 sub-portfolios of E1 and E2 formed from 2025-09-04 to 2025-09-07 were liquidated. MYXUSDT was short in every
   one of them, in E1 as a 21-day loser and in E2 as one of the richest premiums, and its highest price during those
   holds reached 14.4 to 16.5 times its entry price (job 0093). With 20 names a side at equal weights, that rise alone
   cost 67% to 78% of a sub-portfolio's capital. Without September 2025, the composite's monthly t would be 1.88,
   still below the 2.37 needed at Holm's first step. The composite's daily skewness of -6.1 reflects such events: the
   short legs of equal-weight crypto cross-sections may need per-name loss limits, but such a rule is another design,
   testable only on other data.

## Descriptive results that deserve their own test

- E4 (seven-day taker order flow, long the highest): net Sharpe ratio 1.79, monthly t = 3.16 over 51 months, deflated
  Sharpe ratio 0.97 against 13 trials. It was reported without a test, so no decision follows. Its returns are
  concentrated in 2025 and 2026 (44.0 and 29.4 bp a day, against 3.8 to 9.6 in 2022 to 2024); 3.8 of its 19.4 bp a day
  come from names that die during a hold and from extreme funding events, and funding contributes 6.3 (the two
  overlap). Testing it needs data it has not seen: a forward period, or another exchange's taker flows.
- E1-14d's one-sided p of 0.048 comes before any allowance for the 13 trials; it is not evidence.

## What follows under the protocol

1. E3: a new pre-registration of the same rule for forward paper trading without capital, aimed at the implementation:
   the daily signal, the 01:00 rebalancing, spot fills and costs, and the quote asset. Costs matter little (the
   break-even cost multiple is 23), but Binance stopped offering USDT spot pairs to users in the European Economic
   Area on 31 March 2025, under the European Union's Markets in Crypto-Assets regulation (The Block). A European
   implementation would hold USDC or euros: euros add EUR/USD exposure, and for a French taxpayer a sale for legal
   tender is a taxable disposal while an exchange between digital assets is deferred (BOFiP, BOI-RPPM-PVBMC-30-10,
   paragraphs 70 and 80).
2. The composite: closed in this form, inconclusive; its rules are not re-tuned on these data.
3. E4: a candidate for a new pre-registered test on independent data.

## Sources

- The Block, "Binance to delist Tether and other non-MiCA compliant stablecoins for EEA users", 3 March 2025:
  https://www.theblock.co/post/344182/binance-delist-tether-other-non-mica-compliant-stablecoins
- BOFiP, BOI-RPPM-PVBMC-30-10 (actifs numériques, champ d'application): https://bofip.impots.gouv.fr/node/12857
