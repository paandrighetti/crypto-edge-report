The protocol, written in French and frozen on 8 September 2026, tests two documented premia on
Binance perpetuals margined in USDT against holding bitcoin: delta-neutral funding carry, long spot
and short the perpetual on the contracts with the highest funding (Schmeling, Schrimpf and Todorov
2023), and time-series momentum on the sign of the two-week return, sized to a volatility target
(Moskowitz, Ooi and Pedersen 2012). It was delivered that day with its code, its tests and a run on
synthetic data, and was not run on real data before 20 October 2026. That day, its files were
rebuilt from the delivery transcript, reproduced the delivery's own checks and were committed before
the run ([PROVENANCE.md](sources/perp-premia/PROVENANCE.md)).

A premium is retained only if its primary configuration meets five criteria: its Sharpe ratio out of
sample (from 2023) exceeds bitcoin's over the same period; the t-statistic of its alpha against
bitcoin out of sample, with Newey-West standard errors (which allow for autocorrelation), is above
two; its deflated Sharpe ratio over the full sample, with the thirteen declared configurations
counted as trials, is at least 0.95; its maximum drawdown stays under 50%; and its annual return
after a 30% tax on positive years is positive. The protocol does not say over which sample the last
two criteria are measured; the code measures them over the full sample.

| Premium | Out-of-sample Sharpe | Bitcoin's, same period | Out-of-sample alpha t | Deflated Sharpe, full sample | Maximum drawdown, full sample | Annual return after tax, full sample | Verdict |
|---|---|---|---|---|---|---|---|
| Funding carry | {pp_carry_oos_sr} | {pp_btc_oos_sr} | {pp_carry_t} | {pp_carry_dsr} | {pp_carry_dd} | {pp_carry_cagr} | {pp_carry_verdict} |
| Time-series momentum | {pp_mom_oos_sr} | {pp_btc_oos_sr} | {pp_mom_t} | {pp_mom_dsr} | {pp_mom_dd} | {pp_mom_cagr} | {pp_mom_verdict} |

Both premia are rejected. The carry earned before 2023 and lost afterwards: its primary configuration
had a Sharpe ratio of {pp_carry_is_sr} before 2023 and {pp_carry_oos_sr} after, and the out-of-sample
Sharpe ratio is negative for {pp_carry_negative_oos} carry configurations.

The universe is the contracts listed at the time of the run, so delisted contracts are missing: a
survivorship bias that the protocol states in advance and expects to overstate momentum slightly. The
run was started twice. The first attempt stopped before printing any statistic: a paging error in the
collection script had cut every spot price series short, leaving the bitcoin benchmark without values
after 5 June 2022. The script was fixed, spot prices were fetched again and the run was started a
second and last time, with the protocol and the backtest code unchanged. Outputs:
[results.csv](sources/perp-premia/results.csv), [verdict.txt](sources/perp-premia/verdict.txt)
(in French), [protocol](sources/perp-premia/PROTOCOL.md) (in French).
