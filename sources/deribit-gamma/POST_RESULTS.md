# After stage 1

Written on 12 October 2026, after the stage 1 results were known. `PREREGISTRATION.md` is unchanged.

## What happened

- Stage 1 ran on the estimation sample; its outputs are `gate.json` and `stage1.json`. No hypothesis
  passed. Under section 6 of the protocol, H1, H2 and H3 are abandoned and reported as negative
  results.
- Stage 2 was not run. Section 6 re-estimates in stage 2 only the hypotheses that passed stage 1, so
  nothing was left to test. The stage 2 code would also have computed the statistics of section 7 on
  the test sample. They were not computed, so that the returns of the test sample (from 1 April
  2025) stay unexamined for a follow-up. This departs from the reporting the code planned, not from
  the protocol.
- An independent review of the results found no error that changes a decision. It asked for:
  - a check of the taker-side convention for block trades;
  - a check of the timing of the candles;
  - the sign of G by year, and a manifest of the input files;
  - a control for the liquidity channel that dividing G by the perpetual volume creates;
  - R1 to R3 for H3, which the stage code omitted although section 7 does not restrict them;
  - a fuller statement of the limits.

## Done after stage 1

- `src/dgamma/checks.py`, with no return involved: the share of trades in which the taker pays above
  the mark price, by trade type; the timing of the candles; G and G without block trades by year.
  Output: `checks.json`.
- `src/dgamma/exploratory.py`, on the estimation sample only (the hourly file is cut at the end of that
  sample before anything is computed). These analyses were not pre-registered and cannot change a
  decision:
  - X0 reproduces stage 1;
  - X1 adds r(h) / V(h - 1) to H1 and H2;
  - X2 adds log V at the end of the day to H3;
  - X3 runs R1 to R3 for H3.
  Output: `exploratory.json`.
- `src/dgamma/report.py`: everything in `REPORT.md` except the tables of decisions, gates and reported
  analyses was written after the results were known: the signs, intervals, bounds and correlation units,
  the sections on checks and exploratory analyses, the explanatory sentences and the limits. No number
  of the stages changed.
- `manifest.json`: the SHA-256 of every input file.

## Seen of the test sample

The distribution of G by calendar year (`checks.json`) covers the test sample. It involves G only: no
return of the test sample has been loaded into any computation.

## Rule for a follow-up

The test sample may be used only by a new protocol with its own hypotheses and decision rules, frozen
before its returns are loaded.
