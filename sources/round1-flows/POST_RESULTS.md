# Crypto flow edges: interpretation of the single run

Written after the run of commit `b3c3fcd`, so it is not part of the pre-registered analysis. The decisions
are those of REPORT.md. Every number below is filled in by `scripts/post_results.py` from results.json and
verification.json.

## Outcome

No design passes. All four fail Holm's test, and none keeps a positive Sharpe ratio at twice the costs.

| Design | Sharpe before costs (daily) | Net Sharpe (daily) | 95% bootstrap interval | Monthly t | One-sided p | Criteria failed |
|---|---|---|---|---|---|---|
| D1 | 5.06 | -1.96 | [-4.84, 1.43] | -1.07 | 0.837 | Holm, necessary condition, 2x costs |
| D2 | 0.21 | -1.92 | [-2.74, -1.17] | -5.33 | 1.000 | Holm, 2x costs |
| D3 | -0.15 | -0.42 | [-1.91, 0.84] | -0.72 | 0.736 | Holm, necessary condition, 2x costs |
| D4 | 0.30 | -2.55 | [-3.53, -1.61] | -6.49 | 1.000 | Holm, 2x costs |

For D2 and D4 the whole bootstrap interval of the net Sharpe ratio lies below zero: trading these rules as a taker
loses money with high confidence. For D1 and D3 the intervals include zero, so a net Sharpe ratio up to their upper
bounds cannot be excluded, but nothing points to a positive one.

## The computations were checked independently

A second implementation, written from PREREGISTRATION.md without the project's code or results, recomputed the daily
means of the four primary rules (D1 through its bitcoin sleeve) on the same data. The largest absolute difference
across price, funding and cost components is 0.000009 bp a day, and the trade counts match.
The residual difference in D1 comes from the SOFR value applied to the hour that ends at midnight, which the two
implementations date differently.

## D1. Funding carry earned too little to pay for its own trading

- Before costs, the carry earned 0.32 bp a day on capital in excess of SOFR
  (1.16% a year). Costs took 0.54 bp a day, so the net
  mean is -0.22 bp a day. Costs would have to fall to
  59% of the assumed level to break even.
- The rule was not "always in". Funding printed at Binance's 0.01% default on
  21% of bitcoin settlements and
  21% of ether settlements. The rule was in position
  47% (bitcoin) and 43%
  (ether) of the time, over 46 round trips, each costing 32 bp of notional.
- The carry paid in 2024 only: net 0.33 bp a day in 2024, -0.46 in 2025 and -0.45 in
  2026. This fits Borri et al.'s finding of a negative carry before costs in 2025.
- Holding the carry throughout (D1-always) lost money even before costs (Sharpe -1.86,
  -0.14 bp a day): over the window, the carry did not cover SOFR on a
  capital of 1.5 times the notional.
- The returns hide a tail risk: the perpetual rose by up to 61% during a
  trade. With collateral of half the notional and no top-up, the short leg would have been liquidated.

## D2. Momentum into the 5pm ET break did not survive publication

- Before costs, the combined rule's Sharpe ratio is 0.21 over 2021-2026, against 1.72
  in Shen, Urquhart and Wang's sample to 2020. Its mean is 0.33 bp a day, or
  0.87 bp per round trip at break-even, against a 9 bp taker round trip. Even
  Deribit's maker fee (1.5 bp a side) exceeds that.
- The signs of the predictive regression are the paper's: the first signal predicts positively
  (t = 1.90) and the second negatively (t = -0.37). Both are weak.
- The net return is negative in every year.

## D3. Fund flows did not predict bitcoin two days later

- Before costs, the Sharpe ratio is -0.15. With the return before entry as a control, the
  coefficient on the flow signal is negative (t = -0.54).
- With 17 months, the test had little power: a true Sharpe ratio of 1.5 would have passed Holm's first step about
  one time in four (PREREGISTRATION.md, section 7). The null result is weak evidence, not proof of absence.

## D4. The 3-4pm ET window does not reverse enough to trade

- Before costs, the Sharpe ratio is 0.30, worth 0.94 bp
  per round trip at break-even.
- The slope of the traded hour on the window's return is -0.0057 (t = -0.12) on
  NYSE trading days and +0.2856 (t = 0.97) on other days. The necessary
  condition holds on point estimates only; there is no measurable reversal.

## Secondary configurations

None of the 14 configurations has a positive mean net return.
Before costs, the highest Sharpe ratios are D1 (5.06), D1-ETH (4.65) and
D1-BTC (4.42). The carry sleeves look high only because their volatility is tiny. Among the
intraday variants, D2-ETH reaches 0.71 and D4-placebo 0.65 before costs, within
the range that 14 trials produce by chance. The largest DSR of any configuration is
0.02.

## What the run says, and what it does not

The run fits the literature review: edges from mechanical flows are worth about one spread and pay whoever supplies
liquidity, so a taker paying 4.5 bp a side loses on the intraday rules. The funding carry was a real source of
return in 2024 and disappeared after, at least for a rule that crosses the spread on both legs.

The run does not test maker execution, which needs order-book data to model fills; fee tiers below the base tier;
other venues or coins; or the period after September 2026. Any of these, chosen after seeing these results, can
only be tested on new data under a new pre-registration.

Decision, as pre-registered: the four designs are closed in this form, and none goes to paper trading.
