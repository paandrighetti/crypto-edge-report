# E3 forward test: pre-registration

This document fixes, before the forward window starts, how round two's trend rule E3 is followed forward and
judged: the rule and its code, the data, the window and its two looks, the costs, the statistics, the gates and the
decisions. It is frozen by a commit whose hash and SHA-256 the deployment records; any later change is an amendment,
dated and listed at the end, written before the look it affects.

## 1. Why, and what it can show

E3 is the only design of the project's three rounds of pre-registered backtests that passed. In round two
(crypto-slow-edges, frozen at commit 43a1b35, run once), over January 2021 to September 2026, its timing statistic
earned 1.51% a month with an information ratio of 0.82 (one-sided p = 0.0047, Holm's procedure rejecting at 5%), a
positive mean without its best month and at twice its costs, and a bound of 1.62. Its net Sharpe ratio was 0.99
against 0.68 for holding half in each coin. Round two's section 6 made a pass a candidate for "forward paper
trading, without capital, under a new pre-registration of the same rule". This is that pre-registration.

The test answers two questions, with criteria fixed here.

- **Implementation.** Do the rule's daily signals, computed live, equal those the archive gives afterwards, and
  what do its trades cost on a venue that serves French residents, measured on that venue's order books when the
  rule trades? Binance, whose data define the rule, no longer serves French residents (section 4). Section 8 sets
  three criteria; the implementation is validated if all hold.
- **Persistence, weakly.** A look at 24 months and one at 48 months, at 2.5% each. Section 9 gives their power. If
  E3's true timing edge equals round two's estimate from July 2022, the first criterion of a look holds with
  probability 13% at 24 months and 21-22% at 48; if it equals the full-sample estimate, 32% and 53-56%. A failure at
  the first look is therefore weak evidence against E3, and a pass is strong evidence only of an edge at least as
  large as round two's.

Capital is not decided here.

## 2. Seen before writing it

- Everything round two produced: `REPORT.md`, `POST_RESULTS.md`, `results.json`, `gates.json`, including E3 by
  year (Sharpe ratio 0.50 in 2025 and 0.53 in 2026 to 29 September) and its sub-window from July 2022
  (information ratio 0.37, p = 0.076, not decisional).
- The project's research report of October 2026 on untested strategy families, which proposed this forward test.
- Bitvavo's fee page on 15 October 2026: on its USDC markets (fee category B), 0.05% maker and taker at the lowest
  volume tier; on its EUR markets (category A), 0.15% maker and 0.25% taker. Its market list: BTC-USDC and ETH-USDC
  trade in category B. The AMF's white list of crypto-asset service providers: Bitvavo B.V. holds a licence under
  MiCA (the EU's regulation of crypto-asset markets) from the Dutch AFM and has provided services in France since
  14 July 2025. Kraken Pro's fee page: 0.40% maker and 0.80% taker at its lowest tier.
- Two readings of Bitvavo's books on 15 October 2026: about 14:00 UTC, through a direct request outside the
  operations record (best bid and offer 82,197 and 82,216 USDC, 2.3 bp apart; 2,421.60 and 2,422.60 USDC, 4.1 bp),
  and at 15:42 UTC in job 0112 of the operations repository, three levels of each of the four markets (BTC-USDC
  0.5 bp apart, ETH-USDC 5.4 bp, BTC-EUR and ETH-EUR about 0.1 bp). The same job reached Binance's market-data API
  and archive from the server, whose clock is synchronised.
- No statistic of E3, its benchmark or bitcoin's and ether's returns was computed on any day after
  29 September 2026. The author knows the broad path of prices, as anyone following the market does.

## 3. Rule and code

**The rule is round two's E3, unchanged** (crypto-slow-edges, `PREREGISTRATION.md` section 4): for each coin, the
signal at 00:00 UTC of day k is the share of its 30-, 91- and 365-day returns that are positive (0, 1/3, 2/3 or 1),
from midnight closes. The coin's half of the capital holds the signal times its capital in the coin and the rest in
cash, which earns nothing. At 01:00 UTC each position is brought back to that exposure at constant notional, and the
cost is paid on the notional traded, which includes the daily trimming of the drift since the previous day; the
first interval buys the initial position. The benchmark holds 0.5 in each coin every day without cost.

**The code is round two's.** `collect.py`, `data.py`, `io.py`, `stats.py` and `strategies.py` are copies of
crypto-slow-edges' files at commit 43a1b35, byte for byte (their SHA-256 are checked by the test suite). `config.py`
is round two's with the constants of the looks (marked "forward"), chosen by the environment variable `E3F_LOOK`.
`run.py` takes round two's functions `series`, `timing`, `ci95`, `drop_best_month` and `timing_null` unchanged, and
round two's `evaluate` without the statistics of its thirteen configurations and perpetual books: the monthly test of
the net return, the deflated Sharpe ratio and its benchmark, and the funding and excluded results. `book.py` reads
the live log's books and lines for the looks.

**Decisional code.** The looks' results depend on `book.py`, `collect.py`, `config.py`, `data.py`, `fetch.py`,
`gates.py`, `io.py`, `run.py`, `stats.py`, `strategies.py`, `__init__.py` and `requirements.txt`; their SHA-256 go
into every `gates.json`. The daemon (`live.py`), `status.py` and `report.py` are outside, so that they can be
repaired during the window; each repair is recorded in the operations log. A change to the decisional code is an
amendment and requires a new R2 before the next look. The venue's fees are data (`venue_fees.json`, section 5).

**A check of the copy (R2).** Right after the freeze, the decisional code runs with `E3F_LOOK=R2` on round two's
grid and spot files, and must reproduce, to within 1e-9, the thirteen numbers of `config.ROUND2_E3` taken from
round two's `results.json`: E3's mean net return, Sharpe ratio and turnover; its timing statistic's monthly mean,
information ratio, Newey-West t, p-value, null mean information ratio and the upper end of its 95% interval; the
bound; the two checks (twice the costs, without the best month); and the benchmark's mean return. Its
`reproduction.json` is committed to `results/R2/` after the freeze. A copy of round two's two spot files and their
collection counts is kept on the server for a later R2. If R2 fails, the cause is fixed by a dated amendment and R2
is run again before 1 November 2026.

**The looks' environment.** A look runs in the image saved at the freeze or at the latest R2 (or, if it can no
longer be loaded, one built from the same pinned base image and requirements), with the project's repository at the
look's commit mounted as `/app`. Gate 3 checks that its decisional code is the code R2 ran;
`results/R2/reproduction.json`, `venue_fees.json` and the amendments come from that commit.

## 4. Data, window, looks and live log

**Data.** Prices come from Binance's public archive, as in round two: the monthly files of hourly spot klines of
BTCUSDT and ETHUSDT (`data.binance.vision`), each checked against its published SHA-256, collected by round two's
collector (`fetch.py`). Binance stopped serving French residents on 1 July 2026 (Moneyvox, 25 June 2026), and Binance
France SAS was struck off on 2 July 2026 (Selectra, 1 October 2026, from the AMF's white list); its archive stays
public and its prices are those that define the rule, so it remains the source of signals and returns, while costs
are measured where a French resident can trade (section 5). If the archive's files for the window cannot be
obtained, an amendment may replace them by the candles the daemon saved, provided these equalled the archive on
every month the archive did publish.

**Grid and window.** The grid of a look runs from 00:00 UTC on 31 October 2025, 366 days before the window as in
round two (day 366 is the window's first day in both, so the 365-day signal exists on it), to the end of the look's
last month. The window holds the daily intervals that start from 1 November 2026 to 30 October 2028 for L1 (24
calendar months, the last one with 30 days) and to 30 October 2030 for L2 (48 months).

**Looks.** L1 runs from 8 November 2028, once the archive has published its October 2028 files; L2 from
8 November 2030, only if L1 neither passed nor closed the direction, or if L1 was void; `run.py` refuses an earlier
date. A download that fails is retried once a day for up to 30 days before the completeness gate is computed. Each
look runs once: `run.py` writes `run.started` before reading a price and refuses to run again. As in round two, if a
look crashes before writing `results.json`, `run.started` is renamed `run.started.crashed-1`, the cause is fixed
without changing any rule, and the look is repeated once with the fix disclosed; a second crash
(`run.started.crashed-2`) makes the look void. A look is also void when a dated amendment finds the cause of a gate
failure irremovable (section 7); its folder then holds a `void.json` with `"look": "L1"` and the name of that
amendment. L2 reads L1's folder and authenticates L1's file (`results.json`, `run.started.crashed-2` or
`void.json`) by the SHA-256 that the operations repository recorded when that file was written; it records L1's
pre-registration and code hashes, which amendments made after L1 may have changed. The looks coincide with
round three's study D of the order-flow rule.

**Live log.** From the deployment, a daemon (`live.py`) records every UTC day k:

- at 01:00:00 UTC, the order books of Bitvavo's BTC-USDC, ETH-USDC, BTC-EUR and ETH-EUR markets, up to 1,000
  levels a side, requested together; a missing book is requested again at the daemon's next pass, a minute later,
  until 01:04:00, and the line waits for it. A book counts as on time if the venue's own timestamp (in nanoseconds),
  or the time of receipt when the response has no such timestamp, is between 01:00:00 and 01:05:00; a book missed
  for the day stays missing;
- from 01:00:10, Binance's daily candles of the 367 days before day k (their closes are round two's midnight closes)
  and the hourly candles of 00:00 on days k - 1 and k (their closes are the 01:00 prices), from Binance's public
  market-data API, or from its main API if the first fails or gives incomplete candles. The inputs are complete only
  if every one of these candles exists and is closed, which the next candle proves; incomplete inputs are fetched
  again every minute until 23:00 UTC, when the line is written with `inputs_complete` false;
- each coin's signal and exposure on days k - 1 and k, the return held over day k - 1's interval, day k's trade
  (from cash on 1 November 2026) and its cost at round two's rate and on each book, at paper capitals of 10,000 and
  100,000 in the quote currency.

The line goes to `log/YYYY-MM-DD.json` and the raw responses to `raw/YYYY-MM-DD/`, each file written to a
temporary name, flushed to disk and renamed, so that a crash leaves no partial file; the readers count any
unreadable file instead of stopping. The looks read only these files and fields, which a repaired daemon must keep:
the files `log/YYYY-MM-DD.json` (JSON) and `raw/YYYY-MM-DD/bitvavo_MARKET.json.gz` (gzipped JSON); in a line,
`day`, `inputs_complete` and, for each coin, `exposure`, `midnight_closes["0"]` and `price_0100`; in a saved book,
`received_unix` and the response's `market`, `bids`, `asks` and `timestamp`. The looks use the log for the measured
cost and the checks of section 8 only; the test itself uses the archive.

**Backup.** Every week, the day lines and USDC books not yet archived are copied, with their SHA-256, to a branch
of the operations repository. At a look, the live folder is checked against these manifests, and a lost file is
restored from the archive; a file that differs from its manifest is reported.

## 5. Costs and statistics

**Costs.** The decisional cost, 1x, is round two's 10.5 bp a side (Binance's spot fee of 10 bp plus 0.5 bp). Every
result is also reported at 0, 0.5, 2 and 3 times it.

**Measured cost.** On each window day, each coin's trade from the archive (the same computation as
`strategies.trend`'s turnover, by coin), at a paper capital of 100,000 USDC, is walked through the on-time book of
its USDC market (asks for a purchase, bids for a sale). Its impact is the distance of the average price from the
mid; a part of the trade that the saved levels cannot hold is charged at the last saved level's price moved away
from the mid by the same distance again, and such coin-days are counted. Its all-in cost is the impact plus the
venue's taker fee for USDC markets on that day, from `venue_fees.json`: 0.05% from 15 October 2026 (fee category B,
lowest tier). The measured cost is the mean of the all-in costs weighted by notional over the coin-days with an
on-time book and a trade; it is undefined with fewer than 30 such coin-days. A change of Bitvavo's fees is added to
`venue_fees.json`, with the day it takes effect, by a dated amendment; the fee page is checked at every review of
section 8. Also reported: the shortfall of the same fills against Binance's 01:00 price (fee included). The daemon
also logs, as descriptive, the costs on the EUR markets (0.25% taker) and at a 10,000 capital; the looks do not
compute them.

**The test is round two's E3 test, unchanged.** The timing statistic is the daily series m = E3's net return minus
the return of a static portfolio holding each coin at E3's mean exposure to it over the window (spot returns from
01:00 to 01:00). The test is one-sided, on the Newey-West t-statistic of its calendar-month sums (Bartlett kernel,
two lags, no small-sample factor), with a p-value calibrated by running the rule without costs on 20,000 paths of
daily return pairs drawn with replacement from all the observed days of the grid (seed 20261014):
p = (1 + number of simulated statistics at or above t) / (1 + 20,000). In the looks the grid's 366 days before the
window make up a third of L1's pool, against 15% in round two; section 9 shows that this keeps the test's size.

**Also reported**, as in round two: E3's and the benchmark's net and gross statistics (Sharpe ratio, mean,
volatility, skewness, kurtosis, maximum drawdown of summed returns), the break-even cost multiple, the stationary
bootstrap interval of the Sharpe ratio (mean block 30 days, 10,000 draws, seed 20261013), the probabilistic Sharpe
ratio against zero, results by calendar year, tails, the alpha and beta of E3's monthly returns on the benchmark's,
and the 95% interval of the timing information ratio.

## 6. Decision rules

At each look, E3 passes if and only if:

1. the timing test's one-sided p-value is at most 2.5%;
2. its timing statistic has a positive mean after dropping its best calendar month;
3. its timing statistic has a positive mean at the cost bound: the larger of twice round two's cost (21 bp a side)
   and the measured cost, so 21 bp when the measured cost is undefined.

The two looks share a 5% error rate (2.5% each). **Pre-commitment.** If E3 fails a look and its bound is below 0.5,
the direction is closed: no further test on bitcoin and ether of long-or-cash rules that hold each coin in
proportion to the share of positive returns over fixed past horizons. The bound is round two's: the upper end of
the 95% interval of the timing information ratio minus the mean information ratio of the null's paths. A failure
with a higher bound is inconclusive, and after L1 it leads to L2.

A pass is forward evidence of the edge that round two found, net of a cost that a French resident can obtain if the
implementation is validated (section 8). It is not a decision to commit capital, which also depends on what the
owner of the account accepts in drawdown.

## 7. Data-quality gates

Computed by `gates.py` before any return, and written to `gates.json` with the look, the SHA-256 of the
pre-registration, of the decisional code, of every data file and of every file of the live log that the look reads
(the window's lines and USDC books):

1. **Completeness**: every monthly file of both coins from October 2025 to the look's last month was listed,
   downloaded and verified against its published checksum, without a gap.
2. **Hourly coverage**: at most 0.1% of the grid's hourly closes missing, for each coin (round two's spot gate,
   without its comparison with the perpetuals, which this study does not load).
3. **Reproduction**: `results/R2/reproduction.json` passed, under the same decisional code, on round two's spot
   files (their SHA-256, recorded by round two's gates).
4. **Live log**: the live folder holds at least one readable line of the window (an empty or wrong folder fails).
5. **Fees**: `venue_fees.json` gives a USDC taker fee between 0 and 1% on every day of the window.

If a gate fails, nothing is run. As in round two, the failure is diagnosed without computing any return, and any
change is recorded as a dated amendment before the look, after which the gates are computed again. The look is
void only if an amendment finds the cause irremovable, such as data that do not exist, and says so in the look's
`void.json`. A void L1 leads to L2, and a void L2 ends the study without a decision.

## 8. Operational checks and implementation criteria

**Monitoring.** A scheduled workflow of the operations repository checks every day at 07:17 UTC that the daemon is
running, that it wrote the day's line with complete inputs and both USDC books on time, and that the disk has room;
a failure is e-mailed to the account. If the server itself is down, the check waits in GitHub's queue and fails
after 24 hours. `status.py` summarises the log at each review: 1 February 2027, then every six months, and at each
look; each review also checks Bitvavo's fee page. A failure of the daemon is repaired and recorded in the operations
log; the days it missed stay missing. None of this changes the rule, the window or the test.

**Implementation criteria**, computed by the looks and reported apart from the decision:

1. at least 95% of the window's days were logged with complete inputs, and on at least 99% of those the log's
   exposures equal the archive's (the days that differ are listed, as are the days whose midnight closes or 01:00
   prices differ, and their causes are diagnosed in the look's interpretation);
2. both USDC books were on time on at least 95% of the window's days;
3. the measured cost is defined and at most 21 bp a side.

The implementation is validated if all three hold. If it is not, a pass still stands as evidence about the rule,
but not about trading it on this venue.

## 9. Power and size

`scripts/power.py` (output in `scripts/power_output.txt`) runs the test's own machinery on synthetic pools of the
grid's length (Student t returns with 4 degrees of freedom, daily volatilities of 3.3% and 4.3%, correlation 0.8,
drift 0 or 12 bp a day), 20,000 paths each. Power is that of a location shift of the timing series above the null's
mean, for criterion 1 alone (criteria 2 and 3 can only lower it). Round two's estimates map to such shifts after
removing their own null's mean: 0.8155 + 0.1372 = 0.95 for the full sample, 0.37 + 0.18 = 0.55 from July 2022.

| Look | Null 97.5% quantile of t | Shift 0.37 | 0.55 (round two from July 2022) | 0.82 | 0.95 (round two, full sample) | 1.5 | Closing without edge |
|---|---|---|---|---|---|---|---|
| L1, 24 months | 1.38-1.44 | 8% | 13% | 25% | 32% | 66-67% | 11% |
| L2, 48 months | 1.51-1.55 | 11-12% | 21-22% | 42-44% | 53-56% | 90-92% | 17-18% |

The null's mean information ratio is about -0.36 at 24 months and -0.19 at 48, the small-sample covariance between
the rule's exposure and its sample's own drift that round two described. The bound rarely closes the direction: an
edge of zero closes it with probability 11% at L1.

`scripts/size.py` (output in `scripts/size_output.txt`) checks the size of L1's test as it will run: 1,500
simulated histories, each tested against its own null of 1,000 draws from all its days, under three models. The
test rejects 2.3% of independent Student t histories at a nominal 2.5% (4.5% at 5%), 2.2% (4.5%) when the year
before the window falls by 10 bp a day while the window rises by 12 bp, and 2.2% (4.4%) under a GARCH(1,1), with a
standard error of about 0.4 point at 2.5% (0.56 at 5%). An independent review of this protocol found 2.4% to 2.6%
with a pool of the window's own days only, so the pool does not change the size.

## 10. Outside this study

Capital, round two's variants (volatility target, perpetuals, seven-day average), other coins, other venues and
any change to the rule. Each would be a new pre-registration.

## Amendments

None.
