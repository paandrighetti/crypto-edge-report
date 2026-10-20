# Provenance

perp-premia-test was delivered on 8 September 2026 as `perp-premia-test.zip` (`PROTOCOL.md`, `fetch_data.py`,
`backtest.py`, `tests/`, `README.md`, `requirements.txt`), with its protocol frozen before any run on real data. It
had not been run on real data before 20 October 2026.

These files were reconstructed on 20 October 2026 from the delivery transcript: the original texts and the three
edits made before delivery (`hold_between_rebalances`, the guard on `n_trials` in `deflated_sharpe`, the annual
turnover column). The reconstruction reproduces the delivery's own checks: the 6 tests pass, and the synthetic run
rejects both hypotheses, its primary carry turning over 47 times a year and losing 4.5% a year after tax, the
figures the delivery reported (about 46 and 4.5%).

Added for the run, outside the decisional code: `Dockerfile`, `run_fetch.py` and this file. `run_fetch.py` calls
`fetch_data.main()` unchanged, with ccxt's request spacing raised to 1,000 ms for both Binance clients. The default
spacing would send funding-history requests far faster than Binance's limit of 500 per five minutes per address, and
the server's running daemons (`e4c-snapshots`, `e3f-live`) use Binance from the same address. The data requested
are unchanged; only the pace is.

`PROTOCOL.md` is unchanged and its section 9 (amendments) stays empty. Seen before the run and not used by it: the
results of `crypto-flow-edges` (D1, delta-neutral funding carry on bitcoin and ether, failed) and
`crypto-slow-edges` (E2, premium carry, failed), which test related designs. No parameter of this protocol changed
after 8 September 2026.

## 20 October 2026: the first attempt stopped, spot pagination fixed

The single run (vps-ops job 0156, 18:04 UTC) stopped with an exception in `alpha_beta` before printing any
statistic. Cause: `fetch_all_ohlcv` stopped paging at the first page shorter than 1,500 rows, the futures page
size. Binance spot pages hold 1,000 rows, so every spot series ended after 1,000 days (BTC on 5 June 2022). Perp
prices, volumes and funding were complete. The benchmark had no value after June 2022, which raised the exception;
without it, the carry legs, which use spot returns, would have been computed on missing data.

Fix: `fetch_all_ohlcv` pages until an empty batch (`tests/test_fetch.py`). `refetch_spot.py` fetched the spot closes
again for the same perp symbols, at the same pace; the truncated file is kept as `spot_close.truncated.csv`. The
restarted run checks, before running, that the BTC benchmark covers the whole panel and lists spot series ending
more than three days before it. The run was then started a second and last time. No result of the first attempt
existed or was seen; the protocol and `backtest.py` are unchanged.
