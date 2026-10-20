# Sources

Each folder of `sources/` holds outputs copied, unchanged, from where the study ran. `MANIFEST.sha256`
in each folder gives their SHA-256; the test suite checks them.

| Folder | Study | Copied from |
|---|---|---|
| `round1-flows` | Round 1, mechanical flows (crypto-flow-edges) | operations repository, `results/crypto-flow-edges/`, commit `ca0dfeca7254` |
| `round2-slow` | Round 2, slow edges (crypto-slow-edges) | same, `results/crypto-slow-edges/` and `projects/crypto-slow-edges/results/POST_RESULTS.md` |
| `round3-e4b` | Round 3, study B (e4-confirm) | same, `results/e4-confirm/B/` and `results/e4-confirm/freeze_commit.txt` |
| `deribit-gamma` | Deribit dealer gamma | same, `results/deribit-gamma/` and `projects/deribit-gamma/POST_RESULTS-2.md` |
| `vol-edges` | Volatility forecasts and the weekend strangle | same, `results/vol-edges/` |
| `hl-alts-ml` | Hyperliquid alts long/short and meta-labeling | research repository, branch `research/managed-beta-92k`, commit `cb264d75a531`, `research/reports/`, `research/PROTOCOL_ALTS_ML.md` and `research/results/` |
| `perp-premia` | Funding carry and time-series momentum | operations repository, `results/perp-premia-test/` (after its single run) |

Each study's own `REPORT.md` records the commit of the code that ran and the SHA-256 of its protocol.
