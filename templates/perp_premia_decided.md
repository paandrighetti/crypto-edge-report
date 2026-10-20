The protocol, frozen on 8 September 2026 and run on 20 October 2026, tests two documented premia
on Binance USDT-margined perpetuals against holding bitcoin: delta-neutral funding carry, long spot
and short perpetual on the contracts with the highest funding (Schmeling, Schrimpf and Todorov 2023),
and time-series momentum on the sign of the two-week return, sized to a volatility target (Moskowitz,
Ooi and Pedersen 2012). A premium is retained only if, for its primary configuration, it beats
bitcoin's Sharpe ratio out of sample (from 2023), its alpha against bitcoin has a Newey-West t above
two, its deflated Sharpe ratio is at least 0.95 over the thirteen declared configurations, its
maximum drawdown stays under 50% and its annual return after a 30% tax on positive years is positive.

| Premium | Out-of-sample Sharpe | Bitcoin's | Alpha t | Deflated Sharpe | Maximum drawdown | Annual return after tax | Verdict |
|---|---|---|---|---|---|---|---|
| Funding carry | {pp_carry_oos_sr} | {pp_btc_oos_sr} | {pp_carry_t} | {pp_carry_dsr} | {pp_carry_dd} | {pp_carry_cagr} | {pp_carry_verdict} |
| Time-series momentum | {pp_mom_oos_sr} | {pp_btc_oos_sr} | {pp_mom_t} | {pp_mom_dsr} | {pp_mom_dd} | {pp_mom_cagr} | {pp_mom_verdict} |

Both premia are rejected. The carry earned in sample and stopped earning afterwards: its primary
configuration had a Sharpe ratio of {pp_carry_is_sr} before 2023 and {pp_carry_oos_sr} after, and the
out-of-sample Sharpe ratio is negative for {pp_carry_negative_oos} carry configurations.

The universe is the contracts listed at the time of the run, so delisted contracts are missing, a
survivorship bias the protocol states in advance; it favours momentum. A first attempt stopped before
computing any statistic: a paging error in the collection script had cut the spot price series short,
which left the bitcoin benchmark without values from June 2022. The script was fixed, spot prices were fetched
again and the run was started a second and last time
([PROVENANCE.md](sources/perp-premia/PROVENANCE.md)). Outputs:
[results.csv](sources/perp-premia/results.csv), [verdict.txt](sources/perp-premia/verdict.txt),
[protocol](sources/perp-premia/PROTOCOL.md).
