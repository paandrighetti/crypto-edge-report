# After protocol 2

Written on 12 October 2026, after the single run of protocol 2 (`results/followup.started`,
`results/followup.json`, `results/REPORT-2.md`). `PREREGISTRATION-2.md` is unchanged. The numbers are
in `REPORT-2.md` and `exploratory.json`; this note points to them rather than repeating them.

## Outcome

Neither F1 nor F2 passed. Under section 5 of protocol 2, the study of Deribit dealer gamma ends here,
and no further test is run on these data.

## Reading

- **F1.** The exploratory association that motivated it (X3 of `exploratory.json`) does not
  replicate.
  - The estimate on the test sample is close to zero.
  - An effect as negative as the exploratory estimate lies just beyond the one-sided 95 % bound of
    `REPORT-2.md`, but inside the two-sided 95 % interval. Its per-SD units also differ from those of
    X3, so the comparison is approximate.
  - The variants with log V, with gamma in dollars and with G / V are all close to zero. The variant
    without block trades is positive, which is opposite to the prediction.
- **F2.** The estimate has the predicted sign, but it is not significant under either p-value.
  - It rests on a few hours. Without the UTC day of largest |HP x L| (21 August 2026), or without the
    10 largest hours, it is zero or positive.
  - That day carries a large share of the variation of HP over long-gamma hours. The test therefore
    had far less independent information than its number of hours suggests.
  - Its Newey-West standard error is also somewhat too small with these tails (section 4 of the
    protocol).
- **F2 without block trades.** It is one of the six F1 and F2 variants of section 6 of the protocol.
  It is not decisional, because section 6 says so. Its one-sided Newey-West p below 0.05 is weak
  evidence, for three reasons:
  - no correction was made for the six variants;
  - section 4 of the protocol records that this Newey-West p rejects too often when returns are
    heavy-tailed;
  - its regime is different: it has fewer long-gamma hours, and its b_L is positive, so the split
    between regime-wide momentum and a reversal that grows with gamma is not robust.

  It is at most a lead. Testing it would need a new protocol, frozen before use, on data from after
  30 September 2026.
- **Fade rule.** Its gross return is about zero, so it loses its fees. The long-gamma regime as a
  whole shows no reversal.
- **What the nulls exclude.** The one-sided bounds of `REPORT-2.md` exclude effects of the size that
  section 7 of the protocol planned to detect. For F2, this holds subject to the two caveats above:
  a large share of the variation comes from one day, and the standard error is somewhat too small.

## Provenance

- The study ran on a server, through jobs of a private operations repository. Their scripts and logs
  are in `ops/`.
- The commit hashes cited in the reports (`cea1571`, which froze protocol 2, and `4d331e7`, which
  ran it) belong to that repository. `4d331e7` differs from `cea1571` only by the job script.
- The history of this repository is an export of the study's folder from that repository, with the
  same dates and messages and new hashes.
- Git commit dates are set by the author. The order of events can also be checked against the
  timestamps written by the runs themselves (`run_at`, `started_at`) and in the job logs.
