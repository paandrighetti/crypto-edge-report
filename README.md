# crypto-edge-report

What can a small, slow participant earn on liquid crypto markets? This repository synthesises
pre-registered tests of trading rules on public Binance, Deribit and Hyperliquid data, run in
September and October 2026: rules tied to mechanical flows, momentum and carry across perpetuals,
trend timing on spot, taker order flow, option dealers' gamma, volatility forecasts against implied
volatility, a weekend option strangle, machine-learning filters, and funding carry against holding
bitcoin.

- [SUMMARY.md](SUMMARY.md): one page.
- [REPORT.md](REPORT.md): the full synthesis, with the method, each study's decision, what runs
  forward, limitations and references.
- `sources/<study>/REPORT.md`: each study's own generated report, with every configuration.

Its companion on prediction markets is [pm-edge-report](https://github.com/paandrighetti/pm-edge-report).

## How the figures are produced

No figure in REPORT.md or SUMMARY.md is typed by hand.

1. `sources/` holds each study's outputs as its single run wrote them, with a `MANIFEST.sha256` per
   folder; [SOURCES.md](SOURCES.md) gives where each was copied from.
2. `src/cedge/facts.py` reads every printed figure from those files and checks each statement the
   text makes about a decision or a sign; if a source no longer supports one, the build fails.
3. `templates/` holds the prose, with a placeholder for each figure; a test fails if a template
   contains a measured figure.
4. `facts.json` lists every printed figure with its raw value and its source file.

## Reproduce

```
pip install -e ".[dev]"
python -m cedge.build      # regenerate REPORT.md, SUMMARY.md and facts.json
pytest -q                  # fails if they are out of date, if a claim no longer holds or if a checksum differs
```

## License

The code is under the MIT License ([LICENSE-CODE.md](LICENSE-CODE.md)). The report, the summary and the
study outputs are under the Creative Commons Attribution 4.0 International License
([LICENSE-CONTENT.md](LICENSE-CONTENT.md)).

## Disclaimer

Research on public market data. No rule here is traded, and nothing here is investment advice.
