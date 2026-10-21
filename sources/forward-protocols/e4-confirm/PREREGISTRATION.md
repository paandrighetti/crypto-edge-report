# E4 round 3: taker order flow beyond its discovery sample

This file fixes, before any of its returns are computed, two tests of round 2's order-flow rule E4. Study B runs now,
on round 2's data, on the Binance perpetual futures ranked 101 to 200 by traded volume, which E4 never traded. Study
D runs on the 100 most traded contracts over months that begin after this freeze, with two looks: D1 in November
2028 on 24 months and, only if D1 decides nothing, D2 in November 2030 on 48 months. The commit that contains this
file is the freeze, and each run records the file's SHA-256.

## 1. Purpose and what was seen

Round 2 (project crypto-slow-edges at commit 43a1b35, deployed by operations commit 7e3722c; PREREGISTRATION.md
SHA-256 b700bfd8d3b69539...) reported E4 without a test. On the 100 most traded USDT-margined Binance perpetuals
from 1 July 2022 to 29 September 2026, the rule earned a net Sharpe ratio of 1.79 and 19.4 basis points (bp) a day,
with a monthly t-statistic of 3.16 (one-sided p of 0.0076 against round 2's calibrated null) and a deflated Sharpe
ratio of 0.97 against 13 trials. Funding payments make up 6.3 of the 19.4 bp a day, and contracts that die during a
hold and funding events of at least 0.5% in absolute value make up 3.8 (the two overlap). The returns are
concentrated in 2025 and 2026 (44.0 and 29.4 bp a day, against 6.0, 3.8 and 9.6 in 2022, 2023 and 2024). E4 was one
of 13 configurations, and its p-value does not pass Holm's procedure over 13 (threshold 0.05 / 13, or 0.0038). Its
source, Anastasopoulos et al., found the effect in aggregate order flow across many exchanges for 82 coins until
June 2022, so round 2's window already followed the source's sample.

Running E4 on other exchanges over the same period would add little: the exchanges trade the same coins at the same
time, arbitrage aligns their prices, and the common component of signed volume across exchanges explains 80% of
bitcoin's returns (Makarov and Schoar, Journal of Financial Economics, 2020). If round 2's result came from luck in
that period, other exchanges would reproduce it. This round therefore tests the rule on contracts (B) or months (D)
it has not run on:

- **Study B**: E4 unchanged on the contracts ranked 101 to 200, from 1 March 2023 to 29 September 2026, on round 2's
  data. These contracts' own returns differ from those of E4's contracts, but factors common to all contracts do
  not (a market-wide regime in 2025, for instance), so luck that E4 had in these months would also favour B. B must
  therefore also earn more than its co-movement with E4 over the same months explains: section 6 requires a
  positive intercept when B's monthly returns are regressed on those of a reference book, E4 rebuilt over B's
  window.
- **Study D**: E4 unchanged on the 100 most traded contracts from 1 November 2026, the first month that starts after
  this freeze, on data that do not exist yet: the only test of whether the effect persists.

What was seen before freezing, beyond round 2's results:

- Operations job 0094 counted, from round 2's data, the contracts ranked 101 to 200 with a finite order-flow signal
  on each formation day of round 2's E4 window. Quarterly medians rose from 35 in the third quarter of 2022 to 61 in
  the second quarter of 2023 and 100 from 2024 to the first quarter of 2026, then fell to 81 and 42; at least 40
  were available on 84.9% of the days from July 2022, and 30 days in a row first ended on 24 February 2023. B's
  window starts on 1 March 2023 because of these counts alone. The cut also leaves out July 2022 to February 2023,
  when E4 earned little (6.0 bp a day in 2022), and raises the share of 2025 and 2026 in the window's days from 41%
  to 49%. Gate 6's threshold (90% of formation days) was set after these counts. The same job listed the public
  trade archives of Bybit (1,108 USDT contracts, delisted ones kept, 0.2 to 3.7 gigabytes a day), OKX (one file a
  day for all perpetual swaps) and Gate (monthly files per contract), which this round does not use.
- Job 0096 listed the archive's best bid and offer files: 315 symbol directories under the USDT-margined futures,
  and, for the four contracts whose files it listed, daily files from 16 May 2023 to 30 March 2024 only. Jobs 0097
  and 0099 found a file for each of the 1,073 contract-days they requested in that range.
- Jobs 0095, 0097 and 0099 measured spreads and depth (section 5); job 0098, an earlier version of 0099, ran out of
  memory before any output. They read prices and quotes; none computed a signal or a strategy return. Job 0095's
  estimator uses hourly price changes.
- No book formed on the contracts ranked 101 to 200 has been computed, and D's window had not begun. Round 2's E4
  results do include such contracts: E4 holds a contract for seven days after trading it at a rank of 1 to 100, and
  contracts move between ranks, so it held some of B's contracts before, during and after they ranked 101 to 200.
  The overlap measure of section 5 and gate 9 report how much.

Expected effects. E4's 1.79 is the best of 13, so it overstates the rule's Sharpe ratio on its own universe.
Applying the decline of published anomalies (26% out of sample and 58% after publication; McLean and Pontiff,
Journal of Finance, 2016) gives a heuristic range of 0.7 to 1.3 for the top 100; that study does not measure the cost
of choosing the best of 13, so the range is a guess, not an estimate. On smaller contracts the effect could be
stronger (less liquid, more information per unit of flow) or weaker (more noise and more manipulated volume); this
file takes no side. Section 8 gives the odds of a pass.

## 2. Data

Study B uses round 2's collection without change: 2,028 files (hourly klines, premium index and funding of the
USDT-margined perpetuals, bitcoin and ether spot klines, the archive listing and exchange information), whose
SHA-256 are listed in `reference/round2_files.json`. That list's own SHA-256 is
e4d2efcfade44dc14eb8b10d50cd0ee28b8394ddfd6cbb1affc8eb7e0f66cda6, fixed in `config.py`. The data are mounted read
only; the gates, the run and the report write to a separate directory. The hourly grid runs from 1 January 2020 to
1 October 2026, as in round 2.

Each look of study D collects a new data directory with round 2's collector once the last month of its window is
published: D1 with the last month October 2028 and the grid extended to 1 November 2028, D2 with October 2030 and 1
November 2030. Round 2's collector classifies contracts with Binance's live exchange information, which drops
delisted contracts: an equity or commodity contract delisted during D's window would pass for a coin. From the
freeze, a daemon (`e4c.snapshot`) saves the exchange information once a day, and D's collector adds, for each symbol
that the live list no longer has, its entry in the latest snapshot that lists it (`raw/exchangeInfo.json` holds the
merged list, `raw/exchangeInfo_live.json` the live response). Gate 1 fails if a band member has a class in neither,
unless round 2's data held it.

The fields used are each perpetual's hourly close, high, low, number of trades, quote volume and taker-buy quote
volume, and its funding events. Candidates, the split of relaunched symbols and the treatment of bars without trades
are round 2's (its sections 2 and 3, with its amendments 1 to 4, which also apply to these data).

## 3. Universe, books and windows

Eligibility on day k is round 2's, with its amendment 1: first traded at least 60 days before day k and traded on at
least 54 of the 60 days before it; a funding event recorded on day k - 1; traded in the last hour of day k - 1; and a
median daily quote volume over days k - 30 to k - 1 of at least US$5 million. Eligible contracts are ranked by that
median volume, ties broken by symbol order, and the first 200 keep their ranks (round 2 kept 100). Bands and costs
use the rank of the day concerned.

| Study | Book | Ranks on the formation day | Role |
|---|---|---|---|
| B | E4-next100 | 101 to 200 | primary, tested |
| B | E4-next100-fresh | 101 to 200, without the contracts ranked 1 to 100 on any of the previous 30 days | descriptive |
| B | E4-top100 | 1 to 100 | reference: round 2's E4 over B's window |
| D1, D2 | E4 | 1 to 100 | primary, tested |
| D1, D2 | E4-next100 | 101 to 200 | descriptive |

The fresh variant uses past ranks only; leaving out the contracts that ever ranked 1 to 100 would use future ranks
and drop the contracts whose rank rose.

Windows, given as the first and last days on which a daily interval starts (intervals run from 01:00 to 01:00 UTC):
B, 1 March 2023 to 29 September 2026 (43 months); D1, 1 November 2026 to 30 October 2028 (24 months); D2, 1 November
2026 to 30 October 2030 (48 months). Formation days run from a window's first day to six days before its last, so
that every sub-portfolio exits inside the window. A study's members are the contracts that hold a rank of one of its
books' bands on some formation day.

## 4. Design

The rule is round 2's E4, unchanged. For each day d, x = ln(taker-buy quote volume / (quote volume - taker-buy
quote volume)), divided by the standard deviation of x over days d - 30 to d - 1 (at least 20 present). The signal on
day k is the sum over days k - 7 to k - 1, all seven present.

The book is round 2's cross-sectional machine (its section 4). On each formation day k, the band's contracts with a
finite signal that traded in the entry bar (00:00 to 01:00) are sorted on the signal (ties by symbol order). With N
contracts and q = floor(N / 5), the q highest are bought and the q lowest sold, each at a weight of 1 / q of the
sub-portfolio's capital; no sub-portfolio is formed on a day with fewer than 40. Entry is at the 01:00 price of day k
and the scheduled exit at the 01:00 price of day k + 7, without rebalancing. Each sub-portfolio holds one seventh of
the book's capital; capital that no live sub-portfolio holds (in a window's first and last six days, and for seven
days after a formation day without a sub-portfolio) earns nothing. Funding, exits at a delisting, the liquidation
rule, the netting of same-day trades and the results excluded for the robustness condition are round 2's, and so is
the treatment of hours missing from the archive (its amendments 2 to 4).

## 5. Costs and statistics

**Costs** per side, by the contract's volume rank on the trade day (for an exit at a delisting, on the day the
sub-portfolio formed, as in round 2): 6 bp for ranks 1 to 20, 8 bp for 21 to 50, and 12 bp for 51 to 200 and for
contracts outside the ranking. These are round 2's tiers; ranks 101 to 200 pay its last one, as contracts outside
its universe did. Results are reported at 0, 0.5, 1, 2 and 3 times the costs.

Measured before the run, from the archive's best bid and offer files, on the 15th of each month from June 2023 to
March 2024 for the contracts ranked 101 to 200 that day (833 contract-days, 166 contracts) and, on three of those
days, for ranks 21 to 100:

- Over whole days (job 0097), the time-weighted half-spread by contract, in bp, has a median of 1.49, a 75th
  percentile of 2.34 and a 90th of 3.99 for ranks 101 to 200, against 1.10, 2.13 and 3.58 for ranks 51 to 100 and
  0.78, 1.99 and 3.19 for ranks 21 to 50.
- From 00:30 to 01:30, around the books' trades (job 0099), the same measure has a median of 1.46, a 75th
  percentile of 2.30 and a 90th of 3.98 for ranks 101 to 200 (1.10, 2.11 and 3.61 for ranks 51 to 100; 0.79, 2.00
  and 3.21 for ranks 21 to 50), close to the whole-day values. Depth at the best quote is thin: the time-weighted
  median of the smaller side, in US$, has a median of 274 by contract for ranks 101 to 200 and a 90th percentile of
  2,579 (701 and 7,631 for ranks 51 to 100; 1,366 and 13,755 for ranks 21 to 50). A trade of more than a few hundred
  dollars a name goes past the best quote for most of these contracts: the tiers hold for small capital only, and
  capacity is not estimated.
- Binance's taker fee is 5 bp, so 12 bp per side leaves 7 bp for the half-spread and price impact. D's top tiers
  are thinner: 6 and 8 bp leave 1 and 3 bp, against 75th to 90th percentile half-spreads of 1.99 to 3.19 bp for
  ranks 21 to 50; rule 4 of section 6 (positive at twice the costs) guards against this.
- Abdi and Ranaldo's estimator from hourly close, high and low prices (job 0095) had a median of zero in every rank
  band, as expected when spreads are small against hourly volatility, and is not used.

Not measured before the run: the spreads of the contracts the book actually trades, whose extreme order flow may
come with wider quotes, and spreads after March 2024, when E4 earned most. For study B's primary book, the run
records the notional traded at 01:00, by contract, on the ten days above; `scripts/traded_spreads.py` then reads
their quotes from 00:30 to 01:30 and reports the notional-weighted half-spread, its percentiles, the share of traded
notional whose half-spread exceeds 7 bp, and the capital at which a trade equals the depth at the best quote. These
results are descriptive.

**The monthly test** is round 2's: the calendar-month sums of the primary design's daily net returns at 1x costs over
the window, a Newey-West t-statistic with two lags (Bartlett weights, no small-sample factor), and a one-sided
p-value against round 2's simulated null: mean-zero daily returns from a generalised autoregressive conditional
heteroskedasticity model, GARCH(1,1) (alpha 0.10, beta 0.88), with standardised Student t(4) innovations, plus
compensated negative jumps (six a year, exponential sizes with a mean of six times the GARCH part's daily standard
deviation), 300 days of burn-in, summed over the window's calendar months; 200,000 draws, seed 20261013; p = (1 +
the number of draws with t at least the observed) / (1 + 200,000). The null's daily standard deviation is 1.48 (the
jumps add 1.18 to the GARCH part's unit variance); the t-statistic does not depend on the scale.

**The intercept test** (study B): the primary book's monthly net returns y, regressed by ordinary least squares on
the reference book's x over the same months, y = a + b x + e. The statistic is the Newey-West t of a (two lags,
Bartlett weights, no small-sample factor). Its one-sided p-value is computed as above against 200,000 draws of the
monthly test's null for y, each regressed on the observed x (seed 20261018). The t of a does not depend on b, so this
null holds for any loading on the reference's realised path. It does not cover luck that the two books share without
moving together, such as a window with few squeezes for both (section 8). The run also reports b, a in percent a
month, and the correlation of the two books' returns, daily and monthly.

Descriptive statistics: the daily Sharpe ratio (annualised with the square root of 365) and its 95% interval from a
stationary bootstrap (10,000 draws, mean block of 30 days), the probabilistic Sharpe ratio against zero, results by
year, tails, the decomposition into price, funding and costs, the skewness of the monthly returns (against the
null's, section 8), liquidations, formation days without a sub-portfolio, and the median number of contracts in each
band by month. In study B, the share of each book's absolute net weight by contract and day that sits in contracts
the reference book holds on the same day in the same direction.

## 6. Decision rules

Study B's primary design passes if and only if:

1. its one-sided p-value in the monthly test is at most 5%;
2. its intercept on the reference book has a one-sided p-value of at most 5%;
3. its necessary conditions hold: the mean weekly slope on the order flow is positive with a Fama-MacBeth t of at
   least 1.0, in cross-sectional regressions (on every seventh formation day from the first) of the seven-day
   forward return, winsorised at its 1st and 99th percentiles (linear interpolation), on the ranks of the order flow
   and of the 7- and 21-day returns (ties take their average rank) scaled as (rank - 1) / (N - 1) - 0.5, among the
   band's contracts that traded in the entry bar and have all three signals finite (at least 40); its mean net
   return stays positive without its best calendar month; and it stays positive without the results of contracts
   that die during a hold and of funding events with an absolute rate of at least 0.5%;
4. its net Sharpe ratio at twice the costs is positive.

Each look of study D passes if and only if rules 1, 3 and 4 hold over its window, with 2.5% in rule 1. D1 runs in
November 2028. D2 runs in November 2030 only if D1 neither passes nor closes the direction (below), or is void; the
run refuses to start without D1's results showing this or D1's failed gates. The two looks share 5% by Bonferroni's
inequality; under the skewed null, the design passes with probability 0.045 (section 8). D passes if D1 or D2
passes, fails if a look closes the direction or D2 does not pass, and is pending in between. If a gate of a D look
fails and no data-access amendment repairs it, the look is void and spends none of the 5%: a void D1 leaves D2 at
2.5%, and a void D2 leaves D inconclusive. If the verification below voids a pass of D1, the code that produced it
is in doubt: D2 is not run and D is inconclusive.

| B | D | What it shows | Consequence |
|---|---|---|---|
| pass | pass | E4's ordering predicts returns beyond the top 100, beyond its co-movement with E4 over the same years, and the effect persists after round 2 | a candidate for a pre-registered test with small capital, on both bands |
| pass | fail or pending | predictive power beyond the top 100 over round 2's years; persistence not shown | no capital |
| fail | pass | the effect persists on the top 100; it does not reach ranks 101 to 200, B's returns are spanned by E4's, or B lacked power | D suffices for a pre-registered test with small capital on the top 100; B is reported beside it |
| fail | fail | no evidence for E4 | closed where the bound below applies, inconclusive otherwise |

The two studies answer different questions and are not corrected for each other: if neither has an edge, the
chance that at least one passes is at most about 10%, or 18% if B's false-pass risk is 14% (section 8). B alone
commits no capital.

**Verification.** Decisions use the official run. The independent recomputation of section 9, with at least
200,000 draws in each simulated null, must agree with it on: the t-statistics of rules 1 and 2, and the two means
and the Sharpe ratio of rules 3 and 4, to within 1e-9; the sign of the mean Fama-MacBeth slope and the side of 1.0
of its t (round 2's recomputations differed by 2.9e-7 on such a slope); and each p-value to within 0.002, since its
simulated null is its own (round 2's differed by up to 0.0013). Otherwise the difference is reported and the study
counts as not passed.

**Pre-commitment.** If a study fails and the upper end of its Sharpe ratio's 95% bootstrap interval is below 0.5, the
direction is closed for this project: E4 on contracts ranked beyond 100 after B, E4 on Binance perpetuals after a
look of D (and D2 is then not run). A failure with a higher bound is inconclusive and reported as such; after D2,
nothing further is run on E4 without a new pre-registration. Section 8 shows that these rules rarely fire unless the
Sharpe ratio is negative.

**Discipline for D.** No return, statistic sorted on the signal, or paper trade of E4 or of any variant is computed
for D's window before D1's run, nor for the months after October 2028 before D2's. Amendments to D after the freeze
may concern data access only (a moved archive, a changed file format, the class of a contract that gate 1 finds
without one); they are dated and written before the run of the look concerned.

## 7. Data-quality gates

The gates run before the run and write gates.json, with the study, the SHA-256 of each data file, of every module of
the code and of the pinned requirements. The run refuses to start if gates.json is for another study, if any of
those differs, if a data file appeared since, or if an installed package differs from its pinned version, and does
not start unless every gate passes. The gates compute no return, except gate 2's reference book.

1. Data: in B, every data file equals round 2's (its SHA-256 against the pinned reference list, and no file missing
   or added); in D, round 2's classification and completeness gates, and no band member without a class (section 2).
2. Reference (B): the reference book, computed by the run's code, reproduces round 2's mean net return of E4 in 2024,
   2025 and 2026 (9.61, 43.96 and 29.39 bp a day; 2023 differs because B's window starts in March), and E4 rebuilt by
   the same library over round 2's whole window, 1 July 2022 to 29 September 2026, reproduces round 2's monthly
   t-statistic (3.1579389494196013) and mean net return (19.378521863635857 bp a day), all to within 1e-9. A
   failure points to a change in the code or the data; it is diagnosed, fixed by a dated amendment and the gates
   rerun, before any other book is computed. The run repeats the comparison by year and reports it.
3. Hourly coverage (round 2's gate 3 with its amendments 1 and 2): over the members' lives, at most 0.1% of bars
   missing outside suspensions; runs of a day or more are reported.
4. Survivorship: at least one contract dies inside the window after holding a band's rank on one of the 30 days
   before its death.
5. Deaths (round 2's gate 5): every contract settled with a delivery date from the window's first day to the end of
   the grid is checked, at least 100 in B (125 contracts in round 2's exchange information have such dates) and 20
   in D; the median distance between death and delivery date is at most 48 hours, at least 80% die between seven
   days before that date and an hour after it, and no member's death is a possible truncation.
6. Band size: on at least 90% of the window's formation days, at least 40 contracts of the primary band with a
   finite signal that traded in the entry bar.
7. Funding coverage: at least 99% of the primary band's member-days, on formation days, have funding events with no
   gap above eight hours and fifteen minutes over the next seven days.
8. Funding exclusions: the funding rule removes at most 1% of the member-days of the 200-contract ranking built
   without it.
9. Reported, not a gate: the share of the member-days of the band ranked 101 to 200, on formation days, on which the
   contract ranked 1 to 100 within seven days before or after.

If a gate fails, nothing is run; the failure is diagnosed without computing any return, and any change is recorded
as a dated amendment before the run.

## 8. Power

From `scripts/power.py` (output in `scripts/power_output.txt`; 20,000 simulated windows per cell, seed 20261016):
daily net returns follow the test's skewed null model, with its daily standard deviation of 1.48, or independent
normals with the same standard deviation, plus a drift giving the stated annual Sharpe ratio, and are tested as in
section 5. The other conditions of section 6 are ignored, which can only overstate the probability of a pass. (The
draft reviewed before this freeze added the drift as if the standard deviation were 1, which understated the power
of its skewed rows.)

The monthly test of study B alone (43 months, critical t 2.07):

| Annual Sharpe ratio | 0 | 0.5 | 0.75 | 1.0 | 1.25 | 1.5 | 1.79 |
|---|---|---|---|---|---|---|---|
| Probability of p at most 5%, skewed returns | 0.049 | 0.221 | 0.364 | 0.521 | 0.665 | 0.783 | 0.880 |
| Same, normal returns | 0.029 | 0.164 | 0.300 | 0.469 | 0.642 | 0.795 | 0.912 |

Study B's two tests together. Given the reference's path, the regression removes the reference's luck: the
intercept is B's true mean less b times the reference's true mean. What matters is therefore E4's true Sharpe ratio
over B's window, not its realised value of about 1.94 (from round 2's years, with 2023 standing in for its last ten
months). B's daily returns are modelled as rho times the reference's noise plus the square root of (1 - rho squared)
times their own, plus a drift, so that the intercept's information ratio is (S - rho S_true) / sqrt(1 - rho^2).
Probability that both tests give p at most 5% (the monthly test alone in brackets), for a reference whose true
Sharpe ratio is 1.0:

| B's annual Sharpe ratio | rho 0 | rho 0.3 | rho 0.5 | rho 0.7 |
|---|---|---|---|---|
| 0.5 | 0.18 (0.23) | 0.09 (0.22) | 0.04 (0.21) | 0.01 (0.21) |
| 1.0 | 0.45 (0.53) | 0.33 (0.53) | 0.24 (0.52) | 0.16 (0.51) |
| 1.5 | 0.72 (0.79) | 0.62 (0.79) | 0.56 (0.79) | 0.52 (0.79) |
| 2.0 | 0.88 (0.93) | 0.84 (0.93) | 0.82 (0.93) | 0.82 (0.94) |
| 2.5 | 0.96 (0.98) | 0.94 (0.98) | 0.94 (0.98) | 0.95 (0.98) |

and for a reference whose true Sharpe ratio is 1.94:

| B's annual Sharpe ratio | rho 0 | rho 0.3 | rho 0.5 | rho 0.7 |
|---|---|---|---|---|
| 0.5 | 0.15 (0.23) | 0.03 (0.22) | 0.01 (0.21) | 0.00 (0.21) |
| 1.0 | 0.38 (0.53) | 0.17 (0.53) | 0.06 (0.52) | 0.01 (0.51) |
| 1.5 | 0.64 (0.79) | 0.41 (0.79) | 0.24 (0.79) | 0.09 (0.79) |
| 2.0 | 0.82 (0.93) | 0.66 (0.93) | 0.53 (0.93) | 0.38 (0.94) |
| 2.5 | 0.92 (0.98) | 0.83 (0.98) | 0.76 (0.98) | 0.70 (0.98) |

When B's own noise is independent of the reference's, the intercept test holds its size by construction (4.8% and
5.0% in these simulations, with B's mean exactly rho times the reference's true mean). B passes only if the band's
Sharpe ratio clearly exceeds rho times E4's true Sharpe ratio over the window. If the band moves with E4 as closely
as the common regime of 2025 suggests, B will rarely pass at a Sharpe ratio near the heuristic 0.7 to 1.3: that is
the price of testing on the same months, and the reason why a pass of D suffices without B.

The test does not remove luck that the two books share without moving together. In 1,200,000 simulated windows
with no edge in either book and the null's squeezes (its jumps) shared by both, the intercept test passes 4.1% of all
windows, but 12.7% of those in which the reference's monthly t is at least 3.0 and 14.1% of those in which it is at
least 3.5 (E4's was 3.16 in round 2; 2,000 windows tested in each case, standard errors under one point). With half
the squeezes shared, the rates are 4.8%, 8.2% and 8.4%. A reference that looks lucky is mostly one that had few
squeezes, and if the band ranked 101 to 200 shares that luck, the regression does not remove it. A pass of B
therefore carries a false-pass risk of about 8 to 14%, not 5%, if the two bands share their squeeze risk, which
cannot be measured before the run.

Study D (D1 on 24 months, critical t 2.89 at 2.5%; D2 on 48 months, critical t 2.49):

| Annual Sharpe ratio | D1 passes | D passes (D1, or D2 after D1 neither passes nor closes) | Closed at D1 | Closed at D2 | Inconclusive after D2 |
|---|---|---|---|---|---|
| -0.5 | 0.003 | 0.004 | 0.27 | 0.29 | 0.44 |
| 0 | 0.027 | 0.045 | 0.07 | 0.10 | 0.78 |
| 0.5 | 0.099 | 0.197 | 0.02 | 0.01 | 0.77 |
| 0.75 | 0.163 | 0.336 | 0.01 | 0.00 | 0.65 |
| 1.0 | 0.246 | 0.494 | 0.00 | 0.00 | 0.50 |
| 1.25 | 0.337 | 0.639 | 0.00 | 0.00 | 0.36 |
| 1.5 | 0.434 | 0.765 | 0.00 | 0.00 | 0.23 |
| 1.79 | 0.547 | 0.868 | 0.00 | 0.00 | 0.13 |

At a Sharpe ratio of 1.0, D1 alone passes with probability 0.246 and the two looks with 0.494; at zero, the design
passes with probability 0.045.

Under the null, the skewness of the monthly returns has a median of -1.07 over 43-month windows (10th and 90th
percentiles -2.14 and -0.10), -0.97 over 24 months (-2.08 and 0.10) and -1.11 over 48 months (-2.14 and -0.13): the
comparators for section 5's monthly skewness.

The pre-commitment's operating characteristics (normal approximation, upper bound = estimate + 1.96 / sqrt(years)):
B closes the direction with probability 0.49 if the true Sharpe ratio is -0.5, 0.14 if it is zero and 0.02 if it is
0.5; D's columns above give the same for its looks.

## 9. Procedure

1. This file and the code are committed; the commit is the freeze. A job deploys the frozen project, builds its
   image from the base image pinned by digest, runs the test suite for B, D1 and D2 inside it, and saves the image
   (`docker save`) with the archive's SHA-256 and the list of installed packages (`pip freeze`) for D's looks;
   Python 3.12 reaches its end of life in October 2028, and a current certificate bundle may be mounted
   (`SSL_CERT_FILE`) if the image's has expired by then.
2. A job starts the snapshot daemon of section 2 from that image (with E4C_STUDY=D1). At each look, a job lists the
   snapshot dates and any gaps.
3. Study B: a job runs the gates on round 2's data (read only) into B's output directory. A job then checks that the
   deployed project equals the freeze commit, runs the test suite (the dry run, on synthetic data), the single run,
   the report and `scripts/traded_spreads.py`. `run.started` is written before any price is read and records the
   commit, the study and the library versions; the run refuses to start twice.
4. REPORT.md is generated from results.json and gates.json only. Interpretation goes in a separate, labelled file.
   An independent recomputation, written from this file and round 2's by someone who has not seen the run's code,
   checks every decisional quantity of section 6 with its tolerances.
5. D1 runs in November 2028 and, if section 6 calls for it, D2 in November 2030, each from the saved image (or, if it
   cannot be loaded, from the freeze commit rebuilt on the pinned base image): collection with the snapshots into a
   new data directory, gates, the single run (for D2, with D1's results.json, or its gates.json if D1 was void), the
   report and the recomputation, as in steps 3 and 4.
6. If a run crashes before writing results.json, `run.started` is renamed `run.started.crashed-1`, the cause is
   fixed without changing any rule, and the run is repeated once with the fix disclosed. A completed run is final.

## 10. Limitations known in advance

- B's intercept removes the part of B's return that moves with E4's realised returns. If the effect is real and
  common to both bands, the intercept shrinks with it: a failure of B then says little against E4, which is why a
  pass of D suffices. Conversely, luck that the two bands share without moving together, such as few squeezes in
  both, survives the regression and can raise B's false-pass risk to between 8% and 14% (section 8).
- D decides nothing half the time at a Sharpe ratio of 1.0, after four years (section 8).
- Costs rest on ten days of quotes from June 2023 to March 2024 and an allowance for price impact that is not
  measured; liquidity beyond rank 100 varies widely, and capacity is not estimated.
- The band ranked 101 to 200 is thin at times (job 0094's median of 42 in the third quarter of 2026): with 40 names,
  each name is 12.5% of its side, so a short squeeze can liquidate a sub-portfolio. Liquidations and the skewness of
  the monthly returns are reported.
- Smaller contracts are delisted more often: exits at a delisting use the last traded close, and the cost of
  marking longs held into a delisting down 30% is reported.
- Binance's reported volume can include wash trading, which would distort both the ranking and the signal.
- Round 2's other limitations apply (its section 10): the liquidation rule ignores maintenance margin, and Binance
  may stop serving French residents under the European Union's crypto-asset regulation, which affects a live book,
  not the backtest. Binance's archive may change or close before 2030; amendments to D may then only restore access
  to the same data.

## Amendment 1 (15 October 2026, before any return of study B's books)

Study B's gates (operations job 0104, on the freeze's code) passed except gate 5: AERGOUSDT, a member of the band
ranked 101 to 200, is a possible truncation, its series in round 2's data ending with a trade in the last hour of
June 2026, where its monthly kline files stop. Gate 2 reproduced round 2's E4 exactly (differences of 0.0). Jobs 0105
and 0106 diagnosed the failure without computing any signal or return: the archive holds daily klines of AERGOUSDT
with trades in every hour up to 23 July 2026 but no monthly file for July 2026, and neither round 2's nor the live
exchange information lists the contract. It was delisted after 23 July, and round 2's collector, which reads monthly
files, missed its last 23 days.

Study B must use round 2's data unchanged (gate 1) and its reference book must reproduce round 2 (gate 2), so the
data are not changed. AERGOUSDT is treated as dying at its last bar in those data, as the code treats any contract,
and gate 5 lists it as a known truncation instead of failing (`config.KNOWN_TRUNCATIONS`, study B only; empty for
D). Consequences: B's books exit an AERGOUSDT position at its close of 30 June 2026 instead of holding it into July,
count that exit among the deaths of the robustness condition, and do not consider the contract from 1 to 23 July
2026: at most 23 formation days of one of about 100 contracts in the band. No other rule changes. The gates are run
again on the amended code before the run.
