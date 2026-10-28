# T1 forward test: pre-registration

This document fixes, before the forward window starts on Friday 30 October 2026 at 16:00 UTC, how the weekend strangle
T1 of the volatility study is followed forward and judged: the rule, the fills, the data, the window and its three
looks, the costs, the statistics, the gates and the decisions. It is frozen by a commit whose hash and SHA-256 the
deployment records and pushes before the window starts (section 4, Freeze); any later change is an amendment, written
before the look it affects and listed at the end under a numbered heading `### Amendment N (YYYY-MM-DD): title`.
Abbreviations: bp is a basis point (0.01%) of the notional; UTC is coordinated universal time; USDC is the USD Coin
stablecoin in which Deribit's linear options are priced; Black-76 is the option-pricing formula on a forward price that
the volatility study used; RFC 3161 is the published specification of time-stamps signed by a time-stamping authority.

## 1. Why, and what it can show

The volatility study (vol-edges, frozen at commit 4f0d82a, amended once at b36bd84, run once on 18 October 2026)
tested four hypotheses with Holm's procedure at 5%. Only T1 passed: over the 74 weekends from 2 May 2025 to 25
September 2026, selling on Friday at 16:00 UTC the bitcoin call and put whose deltas are nearest 0.35 and -0.35, to
expire on the Sunday at 08:00 UTC, earned 36.6 bp of notional a weekend net of the published cost model (one-sided
p = 0.0062; 0.0070 in the independent recomputation), 25.7 bp at twice the costs, an annual Sharpe ratio of 2.80,
with 81% of weekends won, a worst weekend of -440.7 bp (10 October 2025) and a skewness of -2.9. Its section 6
states: "T1 passes: the next step is a pre-registered forward paper test of the weekend strangle, with the same legal
check; no capital." This is that pre-registration.

The pass is provisional for two reasons the study stated: its bootstrap rejects more often than its level on returns
this skewed, and its fills were modelled, Black-76 prices at Deribit's mark volatilities less 5% of the premium and
0.0003 BTC per option, not measured. The forward test answers two questions with criteria fixed here.

- **Costs (look C, after 12 traded weekends, from January 2027).** What does selling both legs at Deribit's bids at
  16:00 UTC on Friday cost, against the prices the backtest assumed? This is the hypothesis most likely to fail and
  the one the data can settle quickly: the gap between a bid and a model price varies little from week to week.
- **Persistence (looks L1 at 52 weekends, October 2027, and L2 at 104 weekends, October 2028).** Does the rule earn a
  positive mean at the fills the books offered? Section 9 gives the power: about 78% at L1 or L2 together if the
  true mean equals the backtest's, and 27% if it is half of it. L1 can pass only on an overwhelming record; its main
  role is to close the line early when the data rule out half of the backtest's edge.

Capital is not decided here.

## 2. Seen before writing it

- Everything the volatility study produced: `PREREGISTRATION.md`, `REPORT.md`, `POST_RESULTS.md`, `results.json`,
  `verification.json`. Only T1's summary numbers are used here (mean, mean at twice the costs, standard deviation,
  skewness, mean premium); no weekend series was opened again.
- Operations job 0137 of 19 October 2026, 08:54 UTC, a read-only probe of Deribit's public interface: the listing
  schedule (each daily expiry is created four days ahead at 08:00 UTC, so the Sunday expiry appears on Wednesday);
  the fields of instrument lists, book summaries, order books, tickers and delivery prices; tick sizes (0.0001 BTC
  below 0.005 and 0.0005 above for inverse options, 5 USDC below 1,000 and 20 above for linear ones), minimum sizes
  (0.1 contract inverse, 0.01 linear) and the taker fee field (0.0003). The order books of four options of the
  20 October expiry, about 23 hours away. Their best bids lay 2.7% to 7.0% of Deribit's eight-decimal mark below it
  for the inverse options, and 7% to 12% for the linear ones; the inverse books give their own mark to four decimals
  only, up to 2.7% from Deribit's. This is one Monday-morning reading of one-day options, not the weekend options at
  16:00 on a Friday, and is not used by any decision.
- Operations jobs 0138 to 0141 and 0143 to 0145 of 19 October 2026 and 0149 of 20 October 2026: the daemon deployed
  before the freeze, then redeployed five times, and six probes of the nearest expiry with it (54 to 58 books in about
  4 seconds, all usable, the server's clock within 0.07 seconds of Deribit's on the order books), and their timings:
  Deribit serves the instrument list from a cache made 5.4, 4.6, 4.7, 2.9, 7.2 and 10.2 seconds before the request and
  the book summary from one made 0.7 seconds before, while order books are made fresh. The probes of jobs 0143 to 0145
  and 0149 also obtained valid stamps of their folders from the three authorities. Counts and timings only.
- Operations job 0142 of 19 October 2026: ten public time-stamping authorities asked to stamp a fixed test digest,
  with no market data. All answered within 1.6 seconds, with clocks within 0.8 seconds of the server's; the
  certificates of DigiCert, Sectigo (which also answers for Entrust's service) and GlobalSign lead to three roots that
  Mozilla's root store also holds, and their responses are the tests of `tsa.py`.
- Deribit's fee page as the volatility study's section 10 states it (14 October 2026): 0.03% of the underlying per
  option, capped at 12.5% of the option's price; no delivery fee on daily options. Deribit's rate limits (its
  documentation, read on 19 October 2026): 20 requests a second by default, and one a second for the instrument list.
- Access from France (section 10): Deribit's list of restricted jurisdictions (updated 6 October 2026) names neither
  France nor the European Union; its onboarding sends some residents to Coinbase by country (page updated 12 October
  2026); Deribit's integration into Coinbase Global Exchange was completed on 7 October 2026.
- Eighteen independent reviews of the drafts of this protocol and its code (19 to 24 October 2026), whose findings led
  to the version frozen here: a heavier reference null, the mark defined as the backtest's model price, partial
  snapshots counted as missing, responses requested again within the window and replaced only by better ones, each
  Friday folder fixed by third-party time-stamps of the daemon's own requests by 16:15, the daemon's records required
  for every Friday, an archive whose history is linear from a pinned first commit and checked against GitHub's record of
  its pushes, each tar.gz read back before it is pushed, a record counting only if its first copy was pushed by a
  deadline eight hours after the entry, under a plain name, and verifies, every input of the archive decided by rules
  fixed in advance and read by a rule of the script's own, which no version of the interpreter changes, the looks
  reading only such copies and checked to have read them, the freeze's record found by a rule on GitHub's record of the
  operations repository, which a force push before the window voids, each look recomputing the looks before it, their
  gates included, and any look's decision recomputable from what GitHub keeps, the look job's steps, attempts and
  records stated, with the script that builds the looks' folder pinned by its SHA-256 in this document, the only one any
  look runs, taken from the freeze's record that each job file states, from GitHub's answers saved once and whole by
  that script in a version of GitHub's interface still served, its job files and any changed code stated by their
  SHA-256 and the image's code hashed from outside it, Deribit's own fees compared with the fee file, a total deadline
  on every request, delivery prices from Deribit's public history, remedies and void rules fixed in advance, numbered
  amendments, and the rehearsal below.
- The rehearsal of Friday 23 October 2026: the daemon deployed by operations job 0149, whose code is the frozen commit's
  (of the 22 files that job and the freeze list, the decisional code, the daemon, the fees, the roots and this document,
  only this document's SHA-256 differs), saved that weekend's snapshot as it will save every other. Operations jobs 0174
  to 0178, 0180 and 0189 and the daily checks until the freeze read it, or its copies in the archive, for counts,
  statuses, stamps, timings, hashes and passes only, and printed its entry line, which names the strikes chosen; no
  price, cost or return of it was computed or looked at. Both kinds traded, each with 60 books listed, made on time and
  usable: Deribit made the inverse books 2.4 to 7.1 seconds after 16:00 and the linear ones 7.7 to 12.3 seconds after,
  the server's clock within 0.034 seconds of Deribit's, and the daemon recorded no error. Each instrument list needed
  two passes: Deribit's first response had been made 1.8 and 1.0 seconds before 16:00 and was kept under `attempts/`,
  and the second, requested 17.3 and 17.5 seconds after 16:00, had been made 9.0 and 10.0 seconds after it; each book
  summary needed one. The three authorities stamped the folder 19 to 20 seconds after 16:00, and gate 1 found it
  stamped, neither response kept under `attempts/` being better than the one at its path. GitHub started the Friday
  job's five scheduled runs at 12:52, 15:28, 17:57, 18:44 and 19:32 UTC, hours after their times: the first, more than
  three hours before 16:21, ended at once; the second waited, copied the 131 records at 16:21 and pushed them at
  16:21:03 UTC, then again at 16:23:05; the three others found nothing new and pushed again. After the deadline all 131
  records counted, the folder built from them was the server's file for file, and gate 1 found it stamped with the same
  digest. On Sunday 25 October the daemon saved both delivery files at its first pass and wrote its settle line at
  08:01:00 UTC; Sunday's daily archive run, which GitHub started at 11:17 UTC, copied them and pushed them at 11:17:32,
  and after their deadline both counted, their first copies equal to the live files (job 0189). It is outside the
  window.
- The planning simulations of section 9, on synthetic returns only.
- No Deribit price after 25 September 2026 was used to compute a T1 return. The author knows the broad path of bitcoin's
  price, as anyone following the market does.

## 3. Rule and fills

**Entry.** Every Friday at 16:00 UTC from 30 October 2026: Deribit's bitcoin inverse options (priced and settled in
BTC, one bitcoin of underlying per contract, names `BTC-DMMMYY-STRIKE-C` or `-P`) that expire on the Sunday at 08:00
UTC, 40 hours later, as the instrument list made on time lists them.

**On time.** A saved response is on time if Deribit made it between 16:00:00 and 16:05:00 UTC, by the `usOut` field
of its envelope (the microsecond at which Deribit made the response; the instrument list and the book summary come
from a cache made seconds earlier, the order books are made fresh), and it does not come from Deribit's test network
(its `testnet` flag is not true). An order book's own `timestamp` is not used: it is the time of the book's last
change, which on a quiet option can precede the request by minutes. An instrument list whose option names do not
follow Deribit's pattern is malformed.

**Complete and usable books.** The snapshot is complete if every option of the Sunday expiry that the list names has
an order book made on time. A book is usable if it was made on time, names that option, is in state `open`, and has
a positive mark volatility (`mark_iv`), a positive underlying price and valid bids (each with a positive price and
size, from the best price down; possibly none).

**Forward and legs.** F is the median of the usable books' underlying prices (Deribit's forward for that expiry).
For every option with a usable book, its Black-76 delta at F, its strike, T = 40 hours over a year of 365 days, and
its own mark volatility (a put's delta is the call's minus one). The call whose delta is nearest +0.35 and the put
whose delta is nearest -0.35 are chosen, the lower strike on a tie (distances equal to nine decimals), each only if
its delta lies within 0.15 of the target.

**Mark.** A leg's mark m is its Black-76 price at its book's own underlying price and mark volatility, T = 40 hours,
divided by that underlying price (BTC per contract): the price the backtest assumed for a sale. Deribit's own marks
are reported beside it: the book's four-decimal `mark_price`, and the eight-decimal mark of the book summary saved
with the books.

**Fill.** Each leg sells one contract (one bitcoin of notional) by walking its book's bids from the best; the average
price p is the fill. A part the bids cannot hold is charged at the last bid minus its distance from the mark, floored
at zero (at the mark itself if the last bid lies above it). Fills at 0.1 and 5 contracts are reported. Latency is not
modelled: the fill is the book as Deribit made it.

**Fees.** Per leg, the smaller of 0.03% of the underlying (0.0003 BTC for an inverse contract) and 12.5% of the
fill price, as `venue_fees.json` gives them by date; no delivery fee on daily options. A change of Deribit's fees is
added to `venue_fees.json` with the day it takes effect, by a dated amendment; a delivery fee on daily options would
need an amendment of the code as well, and the fee gate fails until then.

**Status of a weekend.**

- *Missing*: nothing saved, no instrument list made on time, an empty list, an incomplete snapshot (the daemon, the
  server or the venue failed), a Friday whose records that count are absent or disagree (section 4), a Friday folder
  that none of the daemon's own time-stamps made by 16:15 covers, a Friday folder where the daemon set aside an inverse
  response better than the one it kept, or of the best quality and different from it (section 4), or, for a traded
  weekend, no delivery price in Deribit's history. A missing weekend is left out of the looks, and its reason is
  reported.
- *Not traded*: the list made on time holds bitcoin options but no Sunday expiry, no book of the expiry is open, no
  option lies within the delta tolerance on one side, or a chosen option has no bid. A weekend not traded earns zero,
  as in T1, and its reason is reported.
- *Traded*: both legs chosen and sold.

**Return.** With S Deribit's delivery price of `btc_usd` on the Sunday (its average of the index over the 30 minutes
before 08:00 UTC), as Deribit's public history gives it at the look, P the two fills and f the two fees in BTC, the
weekend's return is (P - f - max(S - Kc, 0) / S - max(Kp - S, 0) / S) x S / F: the dollar profit and loss of the two
legs on one bitcoin of notional at entry, divided by F, as in T1.

**Twice the costs.** Each leg's distance below its mark, floored at zero, and each fee are doubled.

**T1's cost model on the live marks** (reported): the same return with P replaced by the two marks less 5% and f by
0.0003 BTC per option, uncapped. Its difference from the return at the fills is the implementation shortfall.

**Linear options** (reported only): the same rule on the USDC-linear options of the same expiry (`BTC_USDC-...`),
whose books must also give a positive index price; fees at 0.03% of the index in USDC capped at 12.5% of the price;
settled on the delivery price of `btc_usdc` from Deribit's history, the return being
(P - f - max(S - Kc, 0) - max(Kp - S, 0)) / F in USDC.

**Deviations from T1**, all deliberate:

- The forward is Deribit's (the books' underlying price), where T1 used Binance's USDT perpetual at 16:00 as a stand-in
  (the volatility study's section 11). A 0.05% basis moves a delta by about 0.01.
- Each listed option has its own live mark volatility, where T1 interpolated trade marks up to four hours old across
  strikes; calls and puts share `mark_iv` at every strike of the probe's book summary.
- The sale is at the bids, and twice the costs doubles the measured distance and the capped fee, where T1 charged 5%
  of the premium and 0.0003 BTC (10% and 0.0006 at twice the costs).
- Inverse options decide, as in the backtest; the volatility study's section 11 expected a forward test on the
  USDC-linear options, which are reported here because they may be the product an account in France can trade
  (section 10).
- Missing weekends are left out; T1 had none.

## 4. Data, window, looks and live log

**Live log.** A daemon (`live.py`) on the operations server, whose clock is synchronised, one daemon per folder,
records:

- on Fridays from 16:00:02 UTC, for the inverse options and then the linear ones: the instrument list, the book
  summary, and the order book (20 levels a side) of every listed option of the Sunday 08:00 expiry, one request at a
  time, nearest the money first, calls and puts alternating. The books are requested at once from the names of the
  first list that comes back, even one made before 16:00, while the list is requested again until one made after
  16:00:00 arrives. Each response is saved whole with the times at which it was requested and received. A response
  that failed, or came back early, late or unusable, is requested again at the next pass, every 5 seconds, and no
  request starts in the last second before 16:05:00; a request still unanswered after 15 seconds in all counts as
  failed. A response replaces the saved one only if its quality is better:
  unreadable, then readable but not made on time (or, for an instrument list, made on time but malformed), then made
  on time (for an order book, made on time but unusable), then, for an order book, usable. The response at a path is
  thus the first made of the best quality; every other response is kept under `attempts/`, the saved one being linked
  there before it is replaced, so that a crash leaves it at its path. The linear options wait while no inverse list
  has come back. Then a monitoring line (`log/entry-DATE.json`) with the counts, the weekend's status, the chosen
  strikes, the server's clock offset from Deribit's on the order books and the Friday folder's digest, without any
  price, cost or return;
- right after that line, the time-stamps of the folder's digest (below), and a line `log/pin-DATE.json` with the
  digest and the seconds after 16:00 of each authority's stamp;
- for every Friday from the rehearsal's, an entry line once its window is over and a stamp line once its stamps'
  phase is over, even for a Friday the daemon missed (its entry line then says it saved nothing, and the stamp line of
  an empty folder holds no digest and no stamp);
- on Sundays from 08:01 UTC, Deribit's delivery prices of `btc_usd` and `btc_usdc`, requested every five minutes
  until the Sunday's price appears (until Monday 08:00), and a line `log/settle-DATE.json`. They are compared with
  Deribit's history at the looks and reported; they decide nothing.

Files are written to a temporary name, flushed to disk and renamed, so that a crash leaves no partial file. The
daemon is outside the decisional code and may be repaired during the window; each repair is recorded in the
operations log. The looks check from `attempts/` that no response set aside is better than the one at its path, or of
the best quality and different from it, which a correct daemon never leaves; a Friday where an inverse response
breaks this is missing, and the linear options' and the summaries' cases are reported. This checks the record the
daemon keeps, not a daemon that keeps none, which only the deployment record guards against. No deployment job runs on
a Friday between 15:55 and 16:20 UTC. A scheduled GitHub workflow cannot take the snapshot: the operations
repository's daily check, scheduled at 07:17 UTC, ran as late as 14:39 UTC.

**What the looks read.** Only the saved responses at their paths (`attempts/` only to verify them), the saved stamps and
the entry and stamp lines, and only these fields: in a saved response, the envelope's `usOut` and `testnet`; in an
instrument list, each instrument's `instrument_name`, `strike`, `option_type`, `kind` and `expiration_timestamp`; in an
order book, `instrument_name`, `state`, `mark_iv`, `underlying_price`, `index_price` (linear options) and `bids`, and
for the report `mark_price`, `asks` and `greeks.delta`; in a book summary, for the report, `instrument_name` and
`mark_price`; in a saved delivery file, for the report, `result.data[].date` and `delivery_price`; in a saved stamp,
`response_b64`, the authority's response, and the request's `folder_sha256` and `nonce`; in an entry line,
`folder_sha256`; in a stamp line, `folder_sha256` and `stamps_seconds_after_entry`.

**Delivery prices.** A traded weekend's S is the delivery price of its Sunday in Deribit's public history, which
`collect.py` downloads whole at L1 and L2 and which anyone can download again; without it, the weekend is missing.
Where the daemon's saved price differs from the history's by more than a relative 1e-9, the difference is reported.

**Time-stamps.** Once the entry line is written, the daemon computes the Friday folder's digest, a SHA-256 over one line
per saved response (its path in the folder and its own SHA-256, sorted by path), and asks three public time-stamping
authorities, DigiCert, Sectigo and GlobalSign, to stamp it (RFC 3161, SHA-256, with a nonce and their certificates); it
asks again every 15 seconds while a stamp is missing, until 16:14:00, and gives up on a request after 10 seconds, so
that the last answer comes by 16:14:10. An answer is kept as the daemon's own stamp, under `raw/pins/DATE/`, only if it
is a valid stamp of the digest and the nonce asked for, made between 16:00:00 and 16:15:00 by the authority's clock; any
other answer goes under `raw/pins/DATE/other/`, which no look reads. A stamp is valid under the rules `tsa.py` states.
It is signed by a certificate for time-stamping only, issued under one of three roots that `tsa.py` pins by their
SHA-256 fingerprints: DigiCert Trusted Root G4, USERTrust RSA Certification Authority (under which Sectigo issues) and
GlobalSign Root CA - R6. Every certificate between the two is a certification authority for time-stamping that signed
the one below it, the authorities' current intermediates being kept in `tsa_roots/intermediates/` for answers that lack
them; every certificate was valid at the stamped time; revocation is not checked. A token's certificates are not signed:
duplicates are dropped, every candidate is tried for the signer and at each step of the chain, and a token with more
than 16 certificates is refused. The requests use plain HTTP: a stamp is signed, so whoever is on the path can withhold
or spoil one, as dropping the traffic would under encryption, but not forge one. Mozilla's root store holds these roots
for websites and e-mail, not for time-stamping: a valid stamp is one that a time-stamping certificate issued under them
signed, which the CA/Browser Forum's code-signing requirements leave to the roots' certification authorities and the
parties they delegate.

**Records.** Gate 1 reads each Friday's records together, in the folder that the look job builds from the archive
(below): the entry line, whose digest must be the folder's (none for an empty folder); for a folder with responses, the
stamp line, with that digest, and every stamp it counts; and the daemon's own stamps, none of which may be of another
digest. A Friday whose records are absent or disagree is missing, with the reason; so is a folder with responses but
none of the daemon's own stamps made by 16:15:00, and a Friday whose daemon saved nothing. The stamps settle by 16:15,
by clocks the operator does not control, what a folder held; which records count is settled by the copy deadline below,
the Saturday at 00:00 UTC. Until then, deleting them, or keeping them from the archive, can still make a weekend
missing, since the daemon then writes lines saying that nothing was saved or that no stamp was obtained (section 12).
Job 0142 found the three authorities answering in 0.3 to 0.6 seconds.

**Backup.** The files of the live folder not yet archived, stamps and lines included, are copied with their SHA-256 to
the branch `t1f-archive` of the operations repository (GitHub's repository id 1384225891), whose history only ever grows
by commits that add files: every Friday from 16:21 UTC, by a job that GitHub is asked to start at 07:47, 10:47, 13:47,
14:47 and 15:47 UTC and that, started in the three hours before 16:21, waits on the server until then, and that pushes
the branch again two minutes after its copy, or at once if nothing was new, each push tried three times a minute apart;
and every day at 06:13 UTC. GitHub starts scheduled jobs late: from 16 to 19 October 2026 the daily check started 4 h 18
min to 7 h 22 min after its time. A Friday whose copy starts after 16:21 is copied then; a copy made from the Saturday
at 00:00 UTC, the next daily run's included, comes after the copy deadline, so that the weekend is missing. A Sunday's
files are copied by Monday's daily run. The archive does not run on Fridays between 15:55 and 16:20 UTC, and leaves out
that Friday's records whenever it lists files on a Friday before 16:21. Each run copies the new files once, hashes and
archives the copies in GNU tar's format, and reads the tar.gz back against its manifest, by GNU tar and by the rule
below that the looks apply (`ops/t1f-history.py --check-copy`), before pushing them; a file that the runner cannot read,
or that no look could count, its name not plain (below) or its size over 50 MB, is not archived and fails the run, the
others being archived; new files too large together for one tar.gz under GitHub's limit of 100 MiB for a file stop the
run until the script is repaired. A file's first copy is the one of the earliest commit that archived it. Each run
checks that the branch's history is whole and linear from its first commit, 784230ecd51e (19 October 2026), without
merges, and that each commit only adds files under `t1f/`, so that every copy ever archived is still there; and it
checks the files archived before against their first copies: a history that is not linear and made of added files, or a
changed or missing file, fails the run, and a changed file's new version is archived beside the first. GitHub records
each push, force push and deletion of the branch in the repository's activity, which GitHub gives the repository's owner
no means to edit; on 19 October 2026 it still held a repository's pushes of 13 February 2024, 32 months earlier, and it
had missed one push of the operations repository out of about 300 and repeated another. GitHub offers no rule against
force pushes on a private repository of a free account, so that record is what detects one. Every day, the operations
check runs these checks of the history and verifies it against that record, and from Saturday to Monday checks that
every record of the last Friday counts under the copy deadline (`ops/t1f-history.py`). The archive decides nothing by
itself.

**Copy deadline.** A record of a Friday (a response of its folder, a stamp or another answer under `raw/pins/DATE/`,
each a file `*.json.gz`, its entry line or its stamp line) counts only if its first copy was pushed to the archive
before the Saturday at 00:00 UTC, eight hours after the entry, by the time of the earliest push in GitHub's record that
holds it (a push holds every commit up to its own, the history being linear; a push the record missed can only make that
time later, and one it repeats changes nothing); if that copy names it once, under a plain name (at most 99 characters,
in parts of ASCII letters, digits and `_ . = + -`, each starting with a letter or a digit); if the tar.gz committed with
that copy's manifest is readable and holds exactly one member of that name, of at most 50 MB, whose SHA-256 is the
manifest's; and if no other record that counts so has a name of which its own is a folder, or the reverse. Manifests and
tar.gz are the regular files a commit adds under `t1f/`; any other entry, a link or a submodule's, names nothing and
holds no record. A tar.gz is readable only if it is one gzip member, its CRC-32 and length checked, with nothing after
it, of at most 200 MB of tar made of 512-byte blocks: headers, each followed by its data padded to whole blocks, then
nothing but zero bytes, a part of a block included. Each header holds, from its 258th byte, the eight bytes of GNU tar's
magic (`ustar`, two spaces and a NUL), the type `0`, nothing but zero bytes from its 346th byte on, a checksum and a
size each written as octal digits from the field's first byte and followed only by NUL or space bytes, the checksum
being the sum of the header's 512 bytes as unsigned numbers with its checksum field counted as eight spaces, and a name:
the bytes of its name field before the first NUL, not empty and followed only by NUL bytes. `ops/t1f-history.py` reads
the tar.gz by this rule itself, with zlib for the gzip and no tar library, so that no version of the interpreter changes
which records count. A Sunday's files (the delivery prices the daemon saved, which L1 and L2 read for the report only)
count on the same terms by the Tuesday at 00:00 UTC. Any other record is left out of the looks, as if it had never been
archived, and reported; a manifest line that does not parse, or a manifest over 50 MB, names nothing. A record held back
and shown later, a stamp obtained privately, a file put in a folder after its deadline, a later copy of a file, or a
copy that does not verify thus has no effect. These rules decide every input the archive can hold, and the script that
applies them is the one the freeze records (below): no amendment, and no change of a script, can make a record count or
not. A Friday whose entry line or stamp line does not count, or whose records that count disagree, is missing under gate
1. Whoever can push to the archive before the deadline (the server, or the repository's owner from any machine) can keep
a record from counting, by not copying it, by copying it wrong, or by pushing another first copy of it, which is the
exposure section 12 states; GitHub can too, by starting none of the Friday's copy runs before midnight or missing every
entry of its pushes, a failure unrelated to the outcome. Either way the weekend is missing.

**Freeze.** The freeze is the operations job, generated for this document's commit, that deploys it and records: the
SHA-256 of this document, `venue_fees.json`, `requirements.txt`, the decisional code, the daemon and the certificates of
`tsa_roots/` (`freeze_sha256.txt`), of `ops/t1f-history.py` and `ops/t1f-archive.sh` (`freeze_ops_sha256.txt`), the
image's ID, its configuration digest, Docker's version and storage and the pinned base image (`freeze_image.txt`), its
Python packages (`pip_freeze.txt`), the saved image's SHA-256 (`t1f-PROJECTCOMMIT7.tar.gz.sha256`) and the commit
(`freeze_commit.txt`). The reading script `ops/t1f-history.py` is frozen with the SHA-256
`d4817fb83bb004e0f435fa348eb52a06661c4a6b70d928619d1ba55caa6ffb4f`, which no amendment changes. It refuses to run from
Friday 30 October 2026 at 15:20 UTC on, once any commit of the operations repository's branch `main` has held
`results/t1-forward/freeze_commit.txt`, unless `main` and GitHub's record of it agree as the rule below requires
(`ops/t1f-history.py --main-record`), and unless its `ops/t1f-history.py` has the SHA-256 above. Only once its tests in
the image, the daemon's restart on it, a probe with three valid stamps, the saved image and its copy fetched back from
GitHub have all passed, it commits these files to `results/t1-forward/` on `main`, only if that `main` holds the frozen
commit's tree under `projects/t1-forward` and the scripts that `freeze_ops_sha256.txt` names (otherwise it pushes
nothing and stops), pushes them, pushes `main` again two minutes later, and checks that the rule gives as the freeze's
record a commit that holds these files, that tree and those scripts; it prints that commit, which every look's job file
states. The freeze's record is these files as they are in the commit of `main` that adds
`results/t1-forward/freeze_commit.txt` (its tree holds the file and none of its parents' does) and that the earliest
entry of GitHub's record of `main` holds (an entry holds a commit if its pushed commit is that commit or one after it in
`main`'s history), provided that this entry is dated before Friday 30 October 2026 at 16:00 UTC and holds no other such
commit, and that GitHub's record of `main` before that time holds `main`'s creation, no other entry than pushes and that
creation (no force push and no deletion), and no pushed commit that `main`'s history no longer holds; otherwise there is
no freeze's record, and no look is run. `ops/t1f-history.py --freeze-record` applies this rule, on `main` fetched whole.
A later change of these files, or of `main`'s history, changes nothing: a commit added later is held only by later
entries, and a rewrite of `main` that removes the freeze's record leaves no freeze's record.

**The look job.** Each look's operations job is written and tested before C, outside the decisional code. Each version
of a job file is stated by its SHA-256 in a dated amendment, on a line `jobs/NAME SHA-256: HEX`, before it runs; the job
stops before anything else unless the operations repository's current document states its own SHA-256 so, each job file
states the freeze's record's commit, and each line of a look's record names the SHA-256 of the job file that wrote it,
which a later look checks against the document of the commit that pushed that line. The job does not run
`ops/t1f-archive.sh`, which, like the daemon, may be repaired during the window, each repair recorded
(`ops/t1f-archive-test.sh` tests both scripts; it does not test which days `ops/health.sh` checks): no look reads the
live folder. It takes `ops/t1f-history.py` from the stated commit only if that record's SHA-256 of it is the one frozen
above, which it reads in this document's text before its Amendments section, checks the copy against it when it copies
it into the attempt's folder and before each use, and runs that copy for every step: it saves GitHub's answers for
`main` and for the archive's branch once, in the attempt's folder (`--save-record`: asked in GitHub's REST API version
2026-03-10, or, if GitHub refuses it, in 2022-11-28, or else in none, each page saved whole with its Link header, the
version asked and the one GitHub reports having served, the pages followed by GitHub's own next-page links, and a link
that is not this repository's record of the branch, oldest first, stopping it with nothing saved), gives these answers
to every later step (`--record`), and stops unless the rule above, on them, gives the stated commit. No step runs the
operations repository's current script, and neither an amendment nor a stated commit can make a step run another reading
script. The frozen script reads the answers only if the repository's id is an integer and each entry is of the branch
asked and names one of GitHub's documented kinds, the commits before and after it and a time with its zone; if GitHub
changes the form of its answers so that the frozen script refuses them, an amendment states how the answers that the
frozen copy saved whole map to the form it reads, and the job applies that mapping to them. The build's report records
the SHA-256 of the script that wrote it and of the answers it read, and the versions of the interpreter and of zlib.
Every container the job runs is of the image it loaded (Image, below), with `PYTHONPYCACHEPREFIX` set to a folder
outside the image's code, so that no cached bytecode runs instead of its source. The job runs only after the deadline of
the last record the look reads (for C, of the last Friday it reads, its twelfth traded weekend's; for L1 and L2, the
Tuesday at 00:00 UTC after their last Sunday), with absolute paths under `/opt/t1-forward/looks/`, a folder the freeze
makes for the runner's user, and stops at the first step that fails. At its N-th attempt for look LOOK (N one more than
the largest number among the folders `looks/LOOK-*` and the reports `results/t1-forward/LOOK-*-build.json` in `main`) it
does, in this order: it checks its own SHA-256, loads the saved image of the stated record, hashes its decisional code
and checks the files it mounts (Image), copies the script from that record and checks it against the SHA-256 frozen
above, saves GitHub's answers with that copy and checks that the rule gives the stated record (Freeze, above); it
builds, in `looks/LOOK-N/build`, the look's Fridays from their records that count (`--build`; for C, every window Friday
up to the 26th whose deadline has passed; for L1 and L2, all of theirs, with their Sunday folders), after checking, as
above, that the repository's id is the one above, that GitHub's record holds the branch's creation and no force push or
deletion of it, that every commit the record lists as pushed is still in the branch's history, and that this history is
whole, linear from its first commit and made of added files; the build's report, `results/t1-forward/LOOK-N-build.json`,
lists the Fridays built, every record written with its SHA-256, the records left out by reason, GitHub's record as read
and the script's SHA-256. It compares, for every Friday built, the `taker_commission` of each option of that Friday's
Sunday expiry (those the rule can trade) in the saved inverse instrument list with the `option_share_of_underlying` that
`venue_fees.json` gives for that Friday, and continues only if they are equal for each of those options on every Friday
built: an amendment can add a dated entry to `venue_fees.json` (stated by that file's line, Image), never make the job
continue where the fee that file gives differs from Deribit's for those options; a list without that field is reported,
and if Deribit changes the field's form, an amendment states how it maps to the form the job reads, as for GitHub's
answers. For L1 and L2 it collects the delivery prices into `looks/LOOK-N/data`. It runs `gates.py` on the build into
`looks/LOOK-N/gates`; checks that this `gates.json` is of the look, names only Fridays built (for L1 and L2, all of
them) and records as the files it read exactly the records the build wrote for those Fridays and their Sundays
(`--check-gates`); copies it into the look's one output folder `looks/LOOK`, noting the attempt's number in
`looks/LOOK.attempt`, unless `run.py` has started there; and commits the output folder's record. A void `gates.json`
ends the look, void, once its record is on `main`: a later run of the job records it if `main` holds no line with that
record, and makes no attempt; one whose gates failed stops it until an amendment (section 7). The copy and its record
are skipped for C when its `gates.json` is not void and its only gate not passed is the twelfth traded weekend: C's time
has not come, the job stops as for a deadline still to come, and C's job is run again every Monday from 18 January 2027
until its `gates.json` passes or is void. Otherwise the job recomputes the prior looks (Looks, below), runs `run.py` in
the output folder on attempt N's build and delivery files, and commits the output folder's record again whatever
`run.py`'s exit. Once `run.py` has started in the output folder, its `gates.json` is not changed: a repeat after a crash
runs `run.py` on that `gates.json` and on the build and delivery files of the attempt that `looks/LOOK.attempt` names,
collecting nothing. Such a repeat runs the same, stated job file again (by `workflow_dispatch`); it can repair only a
cause outside the decisional code, this document and `venue_fees.json`, whose SHA-256 `run.py` requires to be those that
`gates.json` records, and the repair is disclosed in a commit outside `projects/t1-forward`, and in an amendment of this
document only after the look has run. The attempts' folders are kept until the test ends. Each record is committed and
pushed from the job, three tries a minute apart, as a line of `results/t1-forward/LOOK-records.txt` (the job's clock
time, the attempt, the job file's SHA-256, the record, the folder's files, the operations commit the job ran on and the
SHA-256 of every file it mounts), with the output folder's files, which replace those under `results/t1-forward/LOOK/`
(the copy's `run.record_of` checked against the line's), the attempt's delivery files under
`results/t1-forward/LOOK-N-data/` and the GitHub answers it saved under `results/t1-forward/LOOK-N-record/`; a record
line is dated by the earliest first push to `main` among the commits that add it, by ancestry (a commit adds a line if
its file holds the line and none of its parents' files does; `--pushed`: the earliest entry of GitHub's record of `main`
whose pushed commit is that commit or one after it in `main`'s history), and a later look takes the record it is given
from every line ever added to that file in `main`'s history, by these dates (below). If the build exits 1 (a check of
the history or of the record failed), nothing is built and the look is not run, and a look not run within its eight
weeks closes the line (below). Any other stop of the job (the record unreadable or in a form the frozen script refuses,
a clone not whole, a folder or a report that exists, a deadline still to come, a fee to state, a `gates.json` that the
check refuses, an error of a script) decides nothing, and the job is run again as its next attempt: once the deadlines
have passed, the build gives the same folder whenever it runs, as long as GitHub's answers are unchanged.

**Window.** The Fridays from 30 October 2026.

**Looks.**

- **C** reads the window's first 12 traded weekends, in order, and nothing after their entries: no delivery price
  and no return. It runs from the Monday after the Friday of the twelfth traded weekend (18 January 2027 if every
  weekend is traded). If the twelfth traded weekend comes after the 26th Friday (23 April 2027), C is void, which its
  `gates.json` records, and the test goes on to L1.
- **L1** reads the 52 Fridays from 30 October 2026 to 22 October 2027 and runs from Monday 25 October 2027, its job
  from the Tuesday at 00:00 UTC, the copy deadline of its last Sunday's files.
- **L2** reads the 104 Fridays to 20 October 2028 and runs from Monday 23 October 2028, its job from the Tuesday at
  00:00 UTC, only if neither C nor L1 closed the line and L1 did not pass.

Each look's operations job is scheduled at its earliest date, and a look runs within eight weeks of it; **a look not run
by then closes the line**. L1 runs only if C did not close the line; L2 only if C did not close the line and L1 neither
passed nor closed it; a void look counts as not having closed the line. After each `gates.json` it copies into a look's
output folder, and after each run of `run.py`, a look's operations job commits to the operations repository that
folder's record: the SHA-256 of each of its files and of their list, `void.json` left out (`run.record_of`). A later
look is given each prior look's folder (C's for L1; C's and L1's for L2) with its record: of every line ever added to
the prior's `LOOK-records.txt` in `main`'s history, each dated as above, the one dated earliest among those listing a
`results.json`, or else the one dated latest before that look's latest instant, eight weeks after its earliest, after
which `run.py` refuses to run it, and `run.py` requires the folder to match it. Each recomputation of a prior look by
the later look's job mounts the files mounted for the prior's run (this document, `venue_fees.json` and `tsa_roots/`) as
the prior's record line names them: taken from `main`'s history at the operations commit it names, each with the SHA-256
it names. A prior look made void by its gates is recomputed so on the folder that the later look's job builds, and on
the history, and must still be void; `run.py` recomputes it too, with the later look's files, and must find it void,
with the Fridays and files that its `gates.json` records (section 7). One made void by an amendment after gates that
failed is recomputed so at the job's clock time that the record line written right after its gates states, and the
gates' results and the Fridays and files they read (`gates`, `fridays` and `raw_files`) must equal those its
`gates.json` records. A prior look with results is recomputed too, by the later look's job, with the inputs the prior
ran with: in an image whose decisional code, hashed from outside it as for the look's own (Image), has the SHA-256 that
the prior's `gates.json` records, with the files mounted for the prior's run, on the folder the later job builds and,
for L1, on L1's delivery files as committed with its record. Its gates are recomputed first (`gates.record` at the
prior's latest instant, as for a void prior) and must give the prior's Fridays, exclusions and files read; then its
results with them (`run.c_look` for C, `run.l_look` for L1), each value equal, in the JSON form `run.py` writes, to the
one in the prior's `results.json`; otherwise the later look is not run. A look's decision is the one this computation
gives on these inputs, which the archive, `main`, the image's branch, GitHub's record and Deribit's public history keep:
anyone with access to the operations repository can recompute it, reading GitHub's record itself and requiring every
entry of the answers a job saved to appear in it unchanged (`activity_type`, `before`, `after`, `ref`, `timestamp`),
GitHub's own record deciding where they differ, and a recomputation that differs from the recorded results decides. The
look that ends the line is recomputed so by a closing job, written, tested and stated with the look jobs before C, which
runs the frozen script, checked as the look job checks it, and reads GitHub's record itself and the delivery files
committed with that look's record, within the eight weeks of that look; its decision is reported once the closing job
agrees, or as not recomputed if the closing job could not run in that time. A prior look's `void.json` is refused beside
a `results.json`, and must name by its number an amendment of this document titled `C is void` (or `L1 is void`), dated
no later than the run that reads it and than the void look's latest date. `run.py` reads that date from the amendment's
heading; the look job also checks, from GitHub's record, that a commit holding the amendment was pushed to the
operations repository by the end of that date, and that the record it gives `run.py` was committed as stated above. The
void look's folder must show the amendment's cause: two crashed starts (its `attempts.json`, `run.started.crashed-1` and
`run.started`), or gates that failed. A look that simply was not run has no `gates.json` and cannot be voided.
Amendments are numbered 1, 2, 3 and so on, in order. Before computing anything, `run.py` recomputes the gates and
refuses to run unless they equal `gates.json`. Each look runs once: `run.py` writes `run.started`, then appends its
start to `attempts.json`, before computing any fill or return, refuses to run again, and writes `results.json` at the
end. If a look crashes before `results.json`, the operator renames `run.started` to `run.started.crashed-1`, the cause
is fixed without changing any rule, and the look is repeated once with the fix disclosed; `attempts.json` refuses a
third start. After a second crash the line is closed, unless a dated amendment finds the cause irremovable and voids the
look, which its `void.json` then names. A crash prints the frames of the traceback only, never the exception's message,
which could carry a number computed before it. A look is also void when a dated amendment finds the cause of a gate
failure irremovable. Report-only computations that fail are recorded in `results.json` as errors and cannot stop a look.

**Image.** A look runs in the image saved at the freeze (`t1f-PROJECTCOMMIT7.tar.gz`, named after this project's frozen
commit, which is never deleted and of which a copy is kept in parts on the branch `t1f-image-PROJECTCOMMIT7` of the
operations repository; the look job loads it after checking its SHA-256 against the freeze's record, and rebuilds it
from that branch when the server's copy fails that check), or, if it can no longer be loaded, one built from the same
pinned base image and requirements. Before running anything in it, the job hashes from outside it (`docker create` and
`docker cp`) every file of the freeze's record (`freeze_sha256.txt`) and checks each against that record or, in a new
image (below), against the last amendment line `image PATH SHA-256: HEX` that states it; the certificates and files that
amendments state for the mount (below) are checked there. The look job mounts over the image's, read-only, the
operations repository's current `PREREGISTRATION.md`, `venue_fees.json` and `tsa_roots/`, so that amendments reach the
look, after three checks against the frozen files, read from `projects/t1-forward` in the freeze's record's commit,
never from the image. This document must be the frozen one with its Amendments section's "None." replaced by numbered
amendments, in order. `venue_fees.json` must hold every entry of the frozen file unchanged and have the frozen file's
SHA-256 or, if an amendment changes it, the one that the last such amendment states on a line
`venue_fees.json SHA-256: HEX`. `tsa_roots/` must hold the frozen certificates unchanged and no other certificate than
those an amendment names, each on a line `tsa_roots/NAME SHA-256: HEX` or `tsa_roots/intermediates/NAME SHA-256: HEX`.
Otherwise the job stops before the build and is run again with the files that the amendments give. `gates.json` records
the SHA-256 of the document, of `venue_fees.json` and of the frozen certificates; the job records those of every file it
mounts. An amendment that adds an intermediate reaches the look by this mount. Any other change of the decisional code,
a new root included (`tsa.py` pins the roots by their SHA-256), is a new image, built `FROM` the frozen image with only
the changed files copied in, each stated by an amendment on a line `image PATH SHA-256: HEX`, and saved under
`/opt/t1-forward/image/` as the file that the amendment names on a line `image file NAME SHA-256: HEX`; the look job
loads that file instead, after checking its SHA-256, records it, and compares it with the frozen image from outside
both: every entry of their file systems (`docker export`) but those in a `__pycache__` folder, which no container of a
look reads, must have the same path, type, mode, owner and link target and, for a regular file, the same SHA-256, and
their configurations (`docker image inspect`'s `Config`) must be equal, the frozen side read from its saved file if need
be, except the files those lines state, which must hash so.

## 5. Costs and statistics

**Look C.** A traded weekend's slippage is the two legs' sum(m - p) over sum(m), at one contract. C's statistic is
the mean of the 12 weekly slippages. Its standard error is their standard deviation over sqrt(12), multiplied by
1.3628 = sqrt(1.3 / 0.7) to allow a lag-one autocorrelation of up to 0.3 between weeks, and its bounds are the mean
minus and plus 2.201 (Student's 97.5% quantile at 11 degrees of freedom) standard errors. Also reported: the lag-one
autocorrelation of the 12 slippages, the pooled slippage, by leg and at 0.1 and 5 contracts, without the three holiday
Fridays (27 November 2026, 25 December 2026, 1 January 2027), against the books' four-decimal marks and against
Deribit's eight-decimal marks; the half-spread at the best level over the mark; the size at the best bid; the seconds
after 16:00 at which the chosen books were made; Deribit's delta against the rule's; the counts of listed, made and
usable books; the reasons of the weekends not traded or missing; and the slippage of the linear options.

**Looks L1 and L2.** x is the series of weekend returns at the fills over the look's window (missing weekends left
out, weekends not traded at zero), n its length, its mean and standard deviation m and sd. Each look has its level:
1% for L1 and 4% for L2, 5% in all.

1. *Calibrated test.* t = m / (sd / sqrt(n)), and p = (1 + #{t* >= t}) / (1 + 100,000), where t* is the same
   statistic on 100,000 samples of n returns from a reference null: zero mean and skewness -5.6, the shape on which
   the volatility study checked T1's size (its section 9), as a negated standardised gamma distribution of shape
   (2 / 5.6)^2 (seed 20261024). The scale does not matter to t. A short option that has not met its crash shows a
   high t: a sample with no edge passes Student's test at 5% about 11% of the time at 52 weekends on T1's own shape,
   and 17% on this one. T1's sample skewness (-2.9, from 74 weekends with one crash) is not used, because a sample
   skewness of heavy-tailed returns is biased toward zero.
2. *Anchored statistic.* m / (scale / sqrt(n)), with scale the larger of sd and 1.206 times the mean premium of the
   traded weekends (the sum of the two marks). 0.965 is T1's standard deviation per unit of mean premium
   (0.0094271 / 0.0097675), and 1.206 raises it by a quarter: a window without a crash then cannot show a standard
   deviation far below what the premium implies.
3. *Twice the costs.* The mean of the returns at twice the costs.

The upper bound is m + 1.959964 x scale / sqrt(n).

**Also reported**: the returns' summary (mean, standard deviation, annual Sharpe ratio on 52 weekends, skewness,
worst and best weekends, share positive, maximum drawdown of summed returns), the same at twice the costs and under
T1's cost model, the implementation shortfall, the pooled slippage over all traded weekends, results by calendar
year, the worst weekend, the statuses and their reasons, the differences between the daemon's and the history's
delivery prices, and the linear options' returns.

## 6. Decision rules

**C.** If the lower bound of the mean weekly slippage exceeds 0.23724, **the line closes**: at Deribit's bids, T1's
backtest mean would be at most halved (0.23724 = 0.05 + 0.5 x 0.0036577 / 0.0097675, where 0.0036577 is T1's mean and
0.0097675 its mean premium, so that each point of slippage above the modelled 5% costs about 0.98 bp). L1 and L2 are
then not run. Otherwise the test goes on, and C reports whether the upper bound is at most 0.10, twice the modelled
slippage, T1's own stress level.

**L1 and L2.** T1 passes a look if and only if:

1. the calibrated test's p-value is at most the look's level (1% at L1, 4% at L2);
2. the anchored statistic is at least the standard normal's quantile at that level (2.326348 at L1, 1.750686 at L2);
3. the mean at twice the costs is positive.

The two looks share a 5% error rate (1% and 4%, the same data being read twice). At L1, a failure whose upper bound
is below 18.29 bp (half of T1's mean) **closes the line**; any other failure leads to L2. At L2, a failure closes the
line.

**Pre-commitment.** A closed line means no further test of T1 or of its variants on Deribit's bitcoin weekend options:
other deltas, entry hours or weekend expiries.

**Pass.** A pass is forward evidence of T1's edge at the fills the books offered at 16:00. It is not a decision to
commit capital, which also depends on access from France and on the tax treatment (section 10) and on the drawdown
the account's owner accepts.

## 7. Data-quality gates

Computed by `gates.py` before any return, and written to `gates.json` with the look, the SHA-256 of the
pre-registration, of the decisional code, roots and intermediates, of `venue_fees.json`, of the collected delivery
files and of every saved file of the look's weekends (their Friday folders, stamps and lines, and for L1 and L2 their
Sunday folders), with each Friday's records, the weekends made missing by gate 1 or by a response set aside, the
statuses of the inverse and linear entries and, for L1 and L2, the delivery prices' differences.

1. **Stamps** (every look): the three pinned roots load. A Friday read whose records that count are absent or
   disagree, or that none of the daemon's own stamps made by 16:15 covers, is missing (section 4).
2. **Fees** (every look): `venue_fees.json` gives complete terms, and no delivery fee, on every Friday read.
3. **C**: twelve traded weekends among the Fridays up to the 26th; without them once the 26th has passed, C is void.
   **L1, L2**: the collected `btc_usd` history is readable and holds the window's last Sunday, and at least 40 (L1)
   or 80 (L2) weekends are valid (traded with a delivery price in the history, or not traded); with fewer, the look
   is void, without an amendment.

A look is void only if the other gates pass. The decisional code is `collect.py`, `config.py`, `gates.py`, `io.py`,
`options.py`, `run.py`, `snapshot.py`, `stats.py`, `tsa.py`, `__init__.py`, `requirements.txt` and the certificates of
`tsa_roots/`; the daemon `live.py` is outside. A change to the decisional code is an amendment. If a gate fails, nothing
is run; the failure is diagnosed without computing any return, any change is a dated amendment before the look, after
which the gates are computed again. A look is void only if an amendment finds the cause irremovable, such as data that
do not exist. The remedies of the foreseeable failures are fixed above, and none needs an amendment: the looks read the
first copies, so a file lost or changed on the server has no effect; a record that does not count under the copy
deadline is left out; a weekend whose records that count disagree or lack a line, not stamped by 16:15, whose daemon
saved nothing, with a better inverse response set aside, or without a delivery price in the history is missing; too few
valid weekends make the look void; a failed check of the archive's history or of GitHub's record leaves the look not
run. If an authority's genuine stamps stop being valid because its hierarchy changed, an amendment may pin its new root
or intermediate, taken from its own repository; it applies to every stamp of that authority saved under `raw/pins/` at
every look run after it, a void prior's recomputation by `run.py` included (section 4), which then stops the later look
if the amendment would make a void look not void; and it makes gate 1 also read the answers kept under
`raw/pins/DATE/other/` that count under the copy deadline and are stamps of the digest and nonce asked for, which no
stamp line counts.

## 8. Operational checks and implementation criteria

**Monitoring.** The operations repository's daily check verifies that the daemon is running; from Saturday to Monday,
that the previous Friday's entry line exists, with the inverse weekend traded, every listed book made on time and
usable, and the median clock offset on the order books within 0.5 seconds, that its stamp line shows a stamp from each
authority, that gate 1 finds that Friday stamped in the deployed image, that every record of that Friday counts under
the copy deadline, and that gate 1 also finds it stamped in the folder a look would read, built from the archive, and it
prints the folder's digest; on Monday and Tuesday, that the previous Sunday's delivery prices were saved; that the
archive's last copy is at most eight days old, that its history is whole and linear from its pinned first commit and
only adds files, and that it agrees with GitHub's record of its pushes; and that the disk has room. A failure is
e-mailed to the account. The monitoring prints counts, statuses, strikes, offsets and digests, never a price, a cost or
a return, so that no one sees C's statistic before C. A missed weekend stays missing; none of this changes the rule, the
window or the tests.

**Implementation criteria**, reported by L1 and L2 apart from the decision: at least 95% of the window's weekends are
valid; on at least 95% of the traded weekends, both chosen books were made within 10 seconds of 16:00; the delivery
prices' differences.

## 9. Power and size

`scripts/size.py` (output in `scripts/size_output.txt`) runs the decision rules of L1 and L2 on 20,000 synthetic
histories of 104 weekends per row. Returns are either a negated standardised gamma (the skewness shown, a standard
deviation as a multiple of T1's, T1's mean premium unless stated, some weekends not traded where stated), or a
strangle priced at its expected payoff, with weekend moves Student t of 3 or 4 degrees of freedom, plus the edge
shown. The condition at twice the costs is simulated by lowering the mean by T1's own difference between its two cost
levels (10.9 bp). The calibrated test's critical values (quantiles of the reference null at each look's level) are
6.361 at L1 and 2.937 at L2.

| Returns (mean) | Standard deviation / T1's | L1 passes | L1 closes | L2 passes, if reached | Passes, L1 or L2 |
|---|---|---|---|---|---|
| no edge, gamma, skewness -2.9 | 1.0 | 0.0% | 12.6% | 0.9% | 0.8% |
| no edge, gamma, skewness -2.9 | 3.0 | 0.0% | 2.8% | 1.3% | 1.3% |
| no edge, gamma, skewness -5.6 | 2.0 | 1.0% | 2.4% | 3.8% | 4.6% |
| no edge, gamma, skewness -5.6 | 3.0 | 1.0% | 1.0% | 3.7% | 4.7% |
| no edge, gamma, skewness -5.6, premium 0.6x T1's | 1.0 | 0.9% | 17.9% | 4.5% | 4.5% |
| no edge, gamma, skewness -5.6, 25% of weekends not traded | 1.7 | 0.7% | 3.1% | 4.7% | 5.2% |
| no edge, fair pricing, t3 moves, sd 2.0% | 1.5 | 0.1% | 8.1% | 2.8% | 2.6% |
| no edge, gamma, skewness -8 | 2.5 | 3.6% | 0.9% | 6.3% | 9.7% |
| T1's mean, gamma, skewness -2.9 | 1.0 | 6.4% | 0.0% | 76.0% | 77.6% |
| T1's mean, gamma, skewness -2.9 | 1.5 | 2.0% | 0.0% | 44.4% | 45.5% |
| T1's mean, fair pricing plus the edge, t4 moves | 1.7 | 1.5% | 0.0% | 39.3% | 40.2% |
| half T1's mean, gamma, skewness -2.9 | 1.0 | 1.0% | 0.6% | 26.8% | 27.4% |

The rules keep the chance of a false pass at or below 4.7% in every no-edge row of the output, except with 10% or 25%
of weekends not traded (5.1% and 5.2%) and for tails heavier than the reference null's: at a skewness of -8 it reaches
10%. At 52 weekends, Student's t-test at 2.5% on a zero mean passes 7% of the time on T1's shape and 13% with a
skewness of -5.6 (the output's first line). The power is that of a test of an edge as large as the backtest's: an
edge halved is found about a quarter of the time, and a failure at L1 is weak evidence against T1.

For look C, the output's last table: at a true slippage equal to the threshold, the rule closes the line 0.6% of the
time with independent normal weekly slippages, 0.1% to 0.2% with right-skewed ones, 2.6% to 2.7% with a lag-one
autocorrelation of 0.3 and 6.3% to 6.5% with one of 0.5. At 0.30 it closes the line in 83% to 100% of the samples
when the weekly slippage varies with a standard deviation of 0.05 or less, and in 20% to 39% at 0.10; at 0.20 it
almost never does.

## 10. Legal check (outside the decision)

Before any use of a pass, the account's owner checks whether Deribit's onboarding from France leads to an account
that can trade daily options as an individual, or sends the applicant to a Coinbase entity that does not offer them;
the tax treatment in France of gains on cash-settled crypto options; and the annual declaration of accounts held
abroad (article 1649 bis C of the French general tax code). The results are recorded at each look and decide
nothing here.

## 11. Outside this study

Capital; ether; the linear options as a decision; other deltas, hours, expiries or sizes; hedging; any change to the
rule. Each would be a new pre-registration.

## 12. Limitations known in advance

- The books at 16:00 show displayed liquidity. A real order may move the quotes, and market makers may adjust to a
  seller who comes back every Friday; neither is modelled.
- The mark is the backtest's model price at Deribit's mark volatility, not a traded price; the cost measured against
  it is a cost against the price the backtest assumed. Deribit's own marks are reported beside it.
- Three of C's first twelve Fridays may be holidays (Thanksgiving Friday, Christmas, New Year's Day), when books are
  thinner; C reports its slippage without them as well.
- The on-time rule for the instrument list rests on Deribit refreshing its cache within the window. Six probes outside a
  Friday afternoon found caches made 2.9 to 10.2 seconds before the request; at the rehearsal each list needed a second
  pass, its cache being made 9.0 and 10.0 seconds after 16:00. One Friday does not show how late a refresh can come.
- Missing weekends are left out, which is neutral only if the cause of a miss is unrelated to the outcome. A venue
  outage on a stressed Friday would not be; the reasons are reported. The stamps settle by 16:15 what a folder held, and
  the copy deadline which records count. Whoever controls the server can still make a weekend missing in ways that no
  code detects: stopping the daemon, or blocking its traffic to the authorities, from 16:00 to 16:15, when Deribit's
  books, and so C's slippage, can be seen on its site; or deleting the Friday's records, or keeping them from the
  archive, before the deadline, the daemon itself then writing lines saying that nothing was saved or that no stamp was
  obtained; or holding the stamps back, or blocking the daemon's requests while obtaining a stamp privately, and showing
  them before the deadline only if the weekend has gone well so far. The copy leaves when the operations server, the
  repository's only runner, makes it: at 16:21 when GitHub starts the Friday job in time, as its schedule allows hours
  for, otherwise with the next run, and whoever controls the server can postpone it. The copy deadline bounds all of
  this: a record first pushed at or after the Saturday at 00:00 UTC never counts, so such a choice can use at most the
  weekend's first eight hours. For L1 and L2, they hold about a fifth of the delivery price's variance from 16:00 if the
  index follows a random walk, and no information of the Sunday; C's statistic is in the books by 16:05, so for C the
  deadline stretches to eight hours the exposure from 16:00 to 16:15 named above, with no more information. After the
  deadline, nothing done on the server changes what the looks read, the first copies that count, which the look job
  checks `gates.py` read: a deletion, a change, a later copy or a malformed file has no effect, and dropping a weekend
  would require rewriting the archive's history, which GitHub's record of the pushes shows and which leaves the look not
  run. That holds as long as GitHub keeps the record unchanged, the operations repository exists, and the look job,
  written before C, builds the folder with the frozen script and checks it as section 4 states; if GitHub stops keeping
  the record, or answering the frozen script's requests in every version of its interface that the script asks for
  (2026-03-10, 2022-11-28 and none), the looks cannot be run, and if it answers them only in a form the script refuses,
  they run only through the mapping that an amendment states for the answers the script saved whole (section 4); a
  next-page link that the script refuses saves nothing, and the looks then cannot be run. Whoever can push to the
  archive or the operations repository can also keep a look from running, by inputs that make its build outlast a job's
  time limit or by rewriting `main`; a look not run within its eight weeks closes the line, so this can end the test. It
  cannot change a look's decision unseen: each decision can be recomputed by anyone with access to the operations
  repository from what the archive, `main`, the image's branch, GitHub's record and Deribit's public history keep, and a
  recomputation that differs decides (section 4, Looks). The closing job runs on the same server and engine as the look:
  it checks the look against GitHub's record and the archive, not against the server, which only a recomputation
  elsewhere does. A job file stating another commit than the freeze's record stops at the reading script that this
  document freezes, unless that commit also holds another text of this document, which the freeze's record, found by the
  rule on GitHub's record, shows. The operator does not watch the books at 16:00, and the daily check prints the last
  Friday's counts and digest from Saturday to Monday.
- A stamp is as good as the authorities' keys and hierarchies. Revocation is not checked. A hierarchy that changes
  before L2 can make an authority's stamps invalid, which the daily check reports, with the remedy of section 7; the
  three authorities answer for each other's availability, while the gate needs only one stamp.
- No 104-weekend test can resolve tails heavier than the reference null's (section 9); 104 weekends may hold no
  crash, or one, and the forward test cannot measure the left tail better than the backtest did.
- Deribit's move into Coinbase Global Exchange may change its interface, its products or who may use them during the
  window; any such change is handled by a dated amendment.

## Amendments

None.
