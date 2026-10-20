# Crypto edge research: one-page summary

Pre-registered tests of trading rules on Binance, Deribit and Hyperliquid public data, September and
October 2026. Each study fixed its rules and its decision before computing the statistic the decision
rests on and ran once. Full report: [REPORT.md](REPORT.md).

- **Mechanical flows (round 1).** Funding carry, momentum into the 5pm ET break, spot-fund flows and a
  benchmark-window reversal on bitcoin and ether: none passes; net Sharpe ratios from {r1_sr_lo} to
  {r1_sr_hi}. The carry earned {r1_d1_gross_bp} bp a day before costs and paid {r1_d1_cost_bp} bp a day
  to trade.
- **Slow edges (round 2).** Momentum and carry across the hundred most traded perpetuals fail
  (p = {r2_comp_p}). A long-or-cash trend rule on bitcoin and ether spot passes a test that strips its
  average exposure (timing information ratio {r2_e3_ir}, p = {r2_e3_p}).
- **Order flow (round 3).** The taker order-flow rule earns a positive mean on the contracts ranked
  101 to 200 (p = {r3_p}), but not significantly more than its returns on the top hundred explain
  (p = {r3_alpha_p}): fail, inconclusive.
- **Dealer gamma.** Rebuilt from Deribit's option trades, dealers' gamma predicts neither bitcoin's next
  hour nor its next day: no hypothesis of the two protocols passes.
- **Volatility.** A forecast from realized variance and release calendars does not beat implied
  volatility. A weekend option strangle passes ({ve_t1_mean_bp} bp a week, p = {ve_t1_p}), with a
  negatively skewed tail whose worst weekend began on {ve_t1_worst_entry}.
- **Hyperliquid alts.** The best of {hl_trials} long/short cells has a net Sharpe ratio of {hl_sr_net}
  and a deflated Sharpe ratio of {hl_dsr}; machine-learning filters on trend signals predict worse than
  the signals alone. Rejected.
- **Perpetual premia.** Funding carry and time-series momentum against holding bitcoin: {pp_summary}.

The passing rules run as frozen paper tests from 30 October and 1 November 2026, with looks fixed in
advance. Nothing here is traded or advised.

Tools: Python, pandas, statsmodels, Docker on a self-hosted server, public exchange archives and
APIs, pre-registration with hashed protocols, Holm's procedure, deflated Sharpe ratios, stationary
bootstrap, independent recomputation, reports generated from outputs.
