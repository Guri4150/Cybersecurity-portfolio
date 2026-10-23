# Project 07 — observed Splunk boundary validation

**PASS for the supplied synthetic fixture. Executed by the assistant through Safari on the owner's Mac, with the owner's authorization. This is not a claim of independent owner execution.**

The original candidate and the separately labeled UTC-explicit variant each returned the four expected successes. All ten success-event failure counts and age sets matched expectations. Each threshold-four control completed with zero rows, and restoring threshold three returned four rows.

## Run identity and scope

- Run date: 23 October 2026. Initial pre-upload search at 17:26:40 UTC; validation searches at 17:29–17:32 UTC (22:59–23:02 IST); evidence collection continued afterward.
- Environment: owner's Splunk Cloud trial, Splunk 10.6.1.0, Search & Reporting, account `sc_admin`.
- UI operator: Codex assistant via Safari; owner performed login.
- Reviewed baseline: [PR #5](https://github.com/Guri4150/Cybersecurity-portfolio/pull/5), commit `5aa62c586cf59ef98f09ca2e064357d566655d6c`.
- Fixture: `splunk-boundary-2026-10-23.jsonl`, 36 fictional JSONL records. Event date is 7 October 2026 UTC.
- Fixture SHA-256: `a87e397a52d9647664ce8f71b2d8e4f671ed86e2bf8276e0f165dca7658e97bd`.
- Actual scope: index `main`, source `splunk-boundary-2026-10-23.jsonl`, host `p07-boundary-lab`, sourcetype `_json`.
- Search settings: All time, `earliest=0`, latest blank in the UI, Smart Mode, No Event Sampling. The UI completion line showed an upper bound at each dispatch time. Job inspector for the final UTC run confirms earliest_time=0, latest_time blank, sample_ratio=1.
- Search timestamps displayed in UTC, while the Mac is on IST; the named user-profile timezone preference was not inspected or changed. The explicit epoch and `_time` checks below establish the timestamps used for this fixture.
- Ingestion: the initial scoped search completed with zero events (SID `1792776400.13022`). Uploaded the supplied file once. Preview showed 36 events, 1 line each; confirmed `_json`, host and index before submission. Splunk confirmed upload success. The resulting base search showed 36 events (SID `1792776535.13031`).

## Expected versus observed

| Check | Expected | Observed | Verdict / evidence |
|---|---|---|---|
| Raw scoped ingestion | 36, one scope group | 36, correct four scope labels | PASS — [original CSV](p07-01-ingestion-observed.csv) |
| Fields and timestamps | Four quality error counts all 0 | missing_or_multivalue=0, bad_status=0, bad_time=0, time_mismatch=0 | PASS — [original CSV](p07-02-quality-observed.csv) |
| UTC extent | 1791363600–1791363901 | 1791363600–1791363901 | PASS — same quality CSV |
| Unique tuples | 35; 25 failures, 10 successes | 35; 25 failures, 10 successes | PASS — [original CSV](p07-03-dedup-observed.csv) |
| Duplicate | dup_check / 192.0.2.17 / 09:02Z failure, copies=2 | Exactly that one duplicate row | PASS — [original CSV](p07-04-duplicate-detail-observed.csv) |
| UTC parser probe | Both epochs 1791363600; both deltas 0 | Both epochs 1791363600; both deltas 0 | PASS in this session — [original CSV](p07-05-time-probe-observed.csv) |
| Original candidate, threshold 3 | Four exact matches, each count=3 | Four exact matches, each count=3 | PASS — [original CSV](p07-06-candidate-threshold3-observed.csv), [screenshot](06-candidate-threshold3.png) |
| Original candidate, all successes | 10 rows with expected counts and ages | All 10 rows and age sets matched | PASS — [original CSV](p07-07-all-successes-observed.csv), [comparison](07-all-successes-case-comparison.csv) |
| Original candidate, threshold 4 | 0 rows with completed job | Complete, Statistics (0), No results found | PASS — [screenshot](08-candidate-threshold4.png) |
| Original candidate, restored threshold 3 | Original four matches | Original four matches | PASS — [restored result snapshot](10-candidate-threshold3-restored-ax.txt) |
| UTC-explicit variant, threshold 3 | Same four matches | Same four matches | PASS — [original CSV](p07-09-utc-explicit-threshold3-observed.csv) |
| UTC-explicit variant, all successes | Same 10 rows/counts/ages | Same 10 rows/counts/ages | PASS — [original CSV](p07-11-utc-all-successes-observed.csv), [comparison](11-utc-all-successes-case-comparison.csv) |
| UTC-explicit variant, threshold 4 | 0 rows with completed job | Complete, Statistics (0), No results found | PASS — [screenshot](12-utc-threshold4.png), [UI snapshot](12-utc-threshold4-ax.txt) |
| UTC-explicit variant, restored threshold 3 | Four matches | Four matches; inspector DONE, isDone=true, 36 events scanned, 4 results | PASS — [snapshot](13-utc-threshold3-restored-ax.txt), [inspector](13-job-inspector-ax.txt) |

All downloaded CSV values were compared locally against the prepared expectations after execution. This comparison is a check of actual Splunk exports, separate from the earlier offline fixture check.

## Observed qualifying successes

| UTC timestamp | Username | Source IP | Observed failure count |
|---|---|---|---:|
| 2026-10-07T09:05:00Z | edge_300 | 192.0.2.11 | 3 |
| 2026-10-07T09:04:00Z | out_order | 192.0.2.18 | 3 |
| 2026-10-07T09:03:00Z | two_successes | 192.0.2.19 | 3 |
| 2026-10-07T09:04:00Z | two_successes | 192.0.2.19 | 3 |

The diagnostics observed age 300 included; age 301 excluded; age 0 excluded; username/IP groups kept separate; the duplicated tuple counted once; unsorted input handled by event time; and both successive successes independently qualified. The two-failure negative control stayed below threshold. The comparison CSVs preserve separate expected and observed columns.

## Query identity, completion and evidence provenance

Every `.spl` file in this directory is the exact text supplied for that named run. Search 06 preserves the reviewed candidate. Search 09 changes only timezone parsing. Searches 11 and 12 apply that same explicit UTC parse to the diagnostics and threshold-four control. Searches 10 and 13 restore threshold three for their respective variants. Neither variant was silently substituted for the other.

All listed jobs visibly reached Complete. No query error or warning was visible in their search result views. The final UTC job inspector additionally reported DONE, isDone=true, status=success, 36 scanned events and 4 results in 0.122 seconds. Full search.log files were not audited; do not interpret this as a claim that every internal log entry is warning-free. The existing notification badge was not treated as a query failure.

- `p07-*-observed.csv`: unchanged files downloaded using Splunk's Export Results → CSV action.
- `*-case-comparison.csv`: locally generated comparisons using those original exports, with separate expected and observed values.
- `*-ax.txt`: accessibility text read directly from the rendered UI; these are sanitized UI snapshots, not Splunk raw exports. Browser chrome is omitted and textual trial hostnames/local paths are replaced; result values and search IDs are preserved. Some snapshots were captured by reopening the already-completed SID.
- PNGs: unaltered Safari screenshots. They contain the trial hostname and non-sensitive browser chrome; no credentials are visible.
- `jobs.json`: search IDs and observation times. Dispatch times are explicitly labeled as inferred from SID epoch and agree with the displayed completion bounds; observation time is not the server's exact completion time. Final inspector createTime independently confirms its dispatch timestamp.
- During evidence assembly, a helper reused a snapshot filename and job label. Labels were reconciled against the observed SIDs, and ingestion/quality/dedup/duplicate/time-probe snapshots were recaptured from the original completed jobs. No query results or expected values were altered.

| Query file stem | SID | Dispatch UTC (from SID) | Completion observed UTC |
|---|---|---|---|
| 01-ingestion | `1792776547.13033` | 2026-10-23T17:29:07+00:00 | 2026-10-23T17:29:15.289Z |
| 02-quality | `1792776565.13034` | 2026-10-23T17:29:25+00:00 | 2026-10-23T17:29:30.183Z |
| 03-dedup | `1792776580.13035` | 2026-10-23T17:29:40+00:00 | 2026-10-23T17:29:44.591Z |
| 04-duplicate-detail | `1792776590.13036` | 2026-10-23T17:29:50+00:00 | 2026-10-23T17:29:54.080Z |
| 05-time-probe | `1792776605.13037` | 2026-10-23T17:30:05+00:00 | 2026-10-23T17:30:08.772Z |
| 06-candidate-threshold3 | `1792776619.13039` | 2026-10-23T17:30:19+00:00 | 2026-10-23T17:30:23.530Z |
| 07-all-successes | `1792776643.13040` | 2026-10-23T17:30:43+00:00 | 2026-10-23T17:30:49.649Z |
| 08-candidate-threshold4 | `1792776663.13041` | 2026-10-23T17:31:03+00:00 | 2026-10-23T17:31:07.289Z |
| 10-candidate-threshold3-restored | `1792776678.13043` | 2026-10-23T17:31:18+00:00 | 2026-10-23T17:31:21.227Z |
| 09-utc-explicit-threshold3 | `1792776690.13044` | 2026-10-23T17:31:30+00:00 | 2026-10-23T17:31:33.552Z |
| 11-utc-all-successes | `1792776704.13045` | 2026-10-23T17:31:44+00:00 | 2026-10-23T17:31:48.435Z |
| 12-utc-threshold4 | `1792776719.13046` | 2026-10-23T17:31:59+00:00 | 2026-10-23T17:32:04.771Z |
| 13-utc-threshold3-restored | `1792776734.13048` | 2026-10-23T17:32:14+00:00 | 2026-10-23T17:32:41.835Z |

## Limits and completion statement

Boundary validation is complete for this 36-record fixture in this trial session. No detection mismatch was observed. The UTC-explicit variant is preferable for an explicit timezone contract, but the baseline parser also returned the correct absolute epoch in this environment; no offset failure is claimed.

No malformed-schema, future-failure, zero-failure-success or duplicate-success case was added or tested. This does not establish production performance, general timezone portability, live monitoring, account compromise or production SOC experience. The batch query retains its documented memory and schema limitations.

The owner authorized the run; the assistant operated it. Preparation files remain labeled as preparation, and the October 22 seven-event run remains separate. No scheduled alert/action was created and no prior report was changed. The PR was unchanged during execution; this evidence is now being added in a subsequent documentation update. No merge is part of that update.
