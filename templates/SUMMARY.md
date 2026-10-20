# Crypto edge research: one-page summary

Pre-registered tests of trading rules on Binance, Deribit and Hyperliquid public data, September and
October 2026. Each study fixed its rules and its decision before computing the statistic the decision
rests on. Full report, with the safeguards of each study: [REPORT.md](REPORT.md).

- **Mechanical flows (round 1).** Funding carry, momentum into the 5pm Eastern Time break, flows into
  United States spot bitcoin exchange-traded funds and a benchmark-window reversal, on bitcoin and
  ether: none passes; net Sharpe ratios from {r1_sr_lo} to {r1_sr_hi}. The carry earned
  {r1_d1_gross_bp} basis points (bp) a day before costs and paid {r1_d1_cost_bp} bp a day to trade.
- **Slow edges (round 2).** Momentum and carry across the hundred most traded perpetual futures
  (futures without expiry) fail (p = {r2_comp_p}). A long-or-cash trend rule on bitcoin and ether spot
  passes a test that strips its average exposure (timing information ratio {r2_e3_ir}, p = {r2_e3_p}).
- **Order flow (round 3).** A rule that follows taker order flow, the buying and selling of orders that
  execute at once against resting quotes, earns a significantly positive mean on the contracts ranked
  101 to 200 (p = {r3_p}), but not significantly more than its returns on the top hundred explain
  (p = {r3_alpha_p}): fail, inconclusive.
- **Dealer gamma.** Dealers' net gamma, the rate at which their option hedges must change as bitcoin
  moves, was rebuilt from Deribit's option trades and was not found to predict bitcoin's next-hour
  returns or next-day volatility: no hypothesis of the two protocols passes.
- **Volatility.** A forecast from realized variance and release calendars does not beat implied
  volatility. Selling a weekend strangle on bitcoin options (an out-of-the-money call and put, sold on
  Friday and expiring on Sunday) passes ({ve_t1_mean_bp} bp a week, p = {ve_t1_p}), with a negatively
  skewed distribution whose worst weekend began on {ve_t1_worst_entry}.
- **Hyperliquid perpetuals.** The best of {hl_trials} long/short cells has a net Sharpe ratio of
  {hl_sr_net} and a deflated Sharpe ratio, which allows for the number of cells tried, of {hl_dsr};
  machine-learning filters on trend signals predict worse than the signals alone. Rejected.
- **Perpetual premia.** Funding carry and time-series momentum against holding bitcoin: {pp_summary}.

The trend rule, the order-flow rule and the weekend strangle will be followed as paper tests from
30 October and 1 November 2026, with looks fixed in advance. Nothing here is traded or advised.
