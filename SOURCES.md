# Sources

Each folder of `sources/` holds outputs copied, unchanged, from where the study ran (protocols, for
`forward-protocols`). `MANIFEST.sha256`
in each folder gives their SHA-256; the test suite checks them.

| Folder | Study | Copied from |
|---|---|---|
| `round1-flows` | Round 1, mechanical flows (crypto-flow-edges) | operations repository, `results/crypto-flow-edges/`, commit `ca0dfeca7254` |
| `round2-slow` | Round 2, slow edges (crypto-slow-edges) | same, `results/crypto-slow-edges/` and `projects/crypto-slow-edges/results/POST_RESULTS.md` |
| `round3-e4b` | Round 3, study B (e4-confirm) | same, `results/e4-confirm/B/` and `results/e4-confirm/freeze_commit.txt` |
| `deribit-gamma` | Deribit dealer gamma | same, `results/deribit-gamma/` and `projects/deribit-gamma/POST_RESULTS-2.md` |
| `vol-edges` | Volatility forecasts and the weekend strangle | same, `results/vol-edges/` |
| `hl-alts-ml` | Hyperliquid alts long/short and meta-labeling | research repository, branch `research/managed-beta-92k`, commit `cb264d75a531`, `research/reports/`, `research/PROTOCOL_ALTS_ML.md` and `research/results/` |
| `perp-premia` | Funding carry and time-series momentum | operations repository, `results/perp-premia-test/` and `projects/perp-premia-test/`, commit 6513bb1cec35 |
| `forward-protocols` | Protocols of the forward tests of E3 (e3-forward) and E4 (e4-confirm, study D) | operations repository, `projects/e3-forward/PREREGISTRATION.md` at its freeze, commit `099e130` of 15 October 2026, and `projects/e4-confirm/PREREGISTRATION.md` with its amendment 1, commit `dfee587` of 15 October 2026 |

What each study records about its run:

- rounds 1 to 3 and the volatility study: the commit of the code that ran and the SHA-256 of the protocol, at the
  top of `REPORT.md` and in `results.json`;
- dealer gamma: the SHA-256 of the first protocol (`REPORT.md`, `stage1.json`), without the code's commit; the
  commit and the SHA-256 of the second protocol (`REPORT-2.md`, `followup.json`);
- Hyperliquid: the commit of the protocol, in `ALTS_ML.md` (in French);
- perpetual premia: the SHA-256 of the protocol, the code and the data at the restart, in `source.restart.sha256`
  and `data.restart.sha256`;
- forward protocols: E4's SHA-256 is the `prereg_sha256` that study B's `results.json` and `gates.json` record;
  E3's is the one its freeze commit states. Each look records the SHA-256 of the protocol it runs under; a dated
  amendment, written into the protocol, changes it.
