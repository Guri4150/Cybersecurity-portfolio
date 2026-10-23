# Project 07 — Splunk boundary validation run sheet

Prepared 23 October 2026, before execution. **Expectations below remain preparation, not observations.** See the [subsequent observed execution record](../../../../docs/execution-evidence/2026-10-23-splunk-boundaries/EXECUTION-RECORD.md). This packet contains a static review, copied fictional fixture, runnable searches, expected outcomes and blank observation fields. The local consistency check is not Splunk execution evidence.

## Reviewed baseline

[Draft PR #5](https://github.com/Guri4150/Cybersecurity-portfolio/pull/5), branch `project-07-splunk-boundary-validation`, commit `5aa62c586cf59ef98f09ca2e064357d566655d6c`. Candidate: the SPL block in `projects/07-siem-alert-investigation/splunk/boundary-validation/README.md`. This preparation packet is preserved alongside the later observed execution record. Keep the prior seven-event October 22 lab record separate.

The [detection specification](https://github.com/Guri4150/Cybersecurity-portfolio/blob/5aa62c586cf59ef98f09ca2e064357d566655d6c/projects/07-siem-alert-investigation/detection.md) and Python implementation require, for each success at t:

`same username AND same source_ip AND t−300 <= failure timestamp < t`, with at least 3 unique failures.

This is a rolling interval anchored on each success, not a clock-aligned five-minute bucket. Exact four-field duplicates are removed. Failures at t are excluded. A prior success does not reset the count; each unique success can alert independently.

## Static SPL review

| Element | Finding |
|---|---|
| `dedup timestamp username source_ip status` | Matches the valid fixture's four-field tuple rule, including duplicate successes. Missing fields must be detected before dedup because records can disappear. |
| `eventstats ... BY username source_ip` | Correct grouping; retaining failures until after aggregation is essential. |
| `values(failure epoch)` | Safe for this canonical, second-resolution four-field schema: same group/time/status failures are duplicates. With richer event IDs or alternative timestamp encodings, distinct epochs could collapse legitimate attempts. |
| `mvmap` predicate | Correct inclusive 300-second lower boundary and exclusive success-time upper boundary. Aggregation makes source order irrelevant. |
| `coalesce(mvcount(...),0)` | Intended to turn no qualifying failures into zero; verify behavior in the target Splunk version. |
| Filtering only successes, then threshold | Preserves both `two_successes` results and does not reset at the first success. |
| UTC parsing | Literal `Z` in `%Y-%m-%dT%H:%M:%SZ` does not explicitly consume a timezone directive. Check absolute epoch with search 05. A uniform offset can leave relative counts looking correct, so four matching alerts alone do not establish correct UTC handling. |
| Ingestion versus correlation time | Base search selects indexed `_time`; correlation uses parsed `timestamp`. Validate both. `earliest=0` avoids a historical lower-bound cutoff; use All time in the picker and verify the actual job bounds. |
| Scale and validation | Small trusted batch only. This is not the Python schema validator or a production correlation design. Check job warnings; incomplete `eventstats` output can produce misleading counts. |

Search 06 preserves the PR candidate. Search 09 is a **proposed, unexecuted UTC-explicit variant**, changing only the parse expression to `strptime(replace(timestamp,"Z$","+0000"),"%Y-%m-%dT%H:%M:%S%z")`. Do not silently substitute it or label its output as the original candidate's output. Preserve both queries and observations if investigating a discrepancy.

Splunk references: [mvmap and mvcount](https://help.splunk.com/en/splunk-cloud-platform/spl-search-reference/9.2.2406/evaluation-functions/multivalue-eval-functions), [distinct values](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/10.0/statistical-and-charting-functions/multivalue-stats-and-chart-functions), [time directives including %z](https://help.splunk.com/en/splunk-enterprise/spl-search-reference/9.2/time-format-variables-and-modifiers/date-and-time-format-variables), [eventstats limits](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/9.1/search-commands/eventstats). These document semantics, not execution of this packet.

## 1. Prepare and import

1. Copy `EXECUTION-RECORD-TEMPLATE.md` into a new dated evidence folder; keep this run sheet unchanged. Record operator, actual UTC run time, Splunk version/environment, user display timezone and reviewed commit.
2. Use the included `splunk-boundary-2026-10-23.jsonl` in an authorized trial or isolated lab. Its **event date is 7 October 2026 UTC**, despite the filename's preparation date. The dated execution record fingerprints the uploaded fixture and its published evidence.
3. Upload once: index `main`, source `splunk-boundary-2026-10-23.jsonl`, host `p07-boundary-lab`, sourcetype `_json`. Preview one JSON object per event and UTC extraction from `timestamp`. All addresses are fictional documentation addresses.
4. Select Search & Reporting, All time. Run each `.spl` file separately. If actual labels differ, first identify them from the upload confirmation, then replace the four scope filters consistently in every search and save the exact executed copies. Never remove scope to search unrelated data.
5. Do not enable scheduled alerts or actions. Keep the existing Project 07 report and Project 09 historical replay alert untouched.

## 2. Establish ingestion and time correctness

| Search | Expected only — not observed | Evidence to capture |
|---|---|---|
| `01-ingestion.spl` | One scoped group, raw_events=36 | Result export, actual labels and search job ID |
| `02-quality.spl` | raw_events=36; missing_or_multivalue=0; bad_status=0; bad_time=0; time_mismatch=0; min_epoch=1791363600; max_epoch=1791363901 | Export and job warnings |
| `03-dedup.spl` | unique_tuples=35; failures=25; successes=10 | Export |
| `04-duplicate-detail.spl` | Exactly one row: 2026-10-07T09:02:00Z, dup_check, 192.0.2.17, failure, copies=2 | Export |
| `05-time-probe.spl` | utc_epoch=1791363600 and utc_delta=0. For candidate UTC correctness, candidate_epoch must also be 1791363600 and candidate_delta=0 | Export plus user timezone |

Stop acceptance if a gate fails. Preserve the mismatch before fixing extraction or scope. A count of 72 after repeated upload can deduplicate to 35 and hide a bad import; the raw count gate is mandatory. Do not upload repeatedly to solve zero results: check labels, permissions, historical time range and parsing first. Quality search 02 is a fixture preflight, not comprehensive malformed-schema/IPv4 validation.

## 3. Run the unchanged candidate and inspect every success

Run `06-candidate-threshold3.spl`, wait for job completion, and export all results. Expected exactly these four rows, all failure_count=3:

| timestamp (UTC) | username | source_ip |
|---|---|---|
| 2026-10-07T09:05:00Z | edge_300 | 192.0.2.11 |
| 2026-10-07T09:04:00Z | out_order | 192.0.2.18 |
| 2026-10-07T09:03:00Z | two_successes | 192.0.2.19 |
| 2026-10-07T09:04:00Z | two_successes | 192.0.2.19 |

Then run `07-all-successes.spl`. It uses the same calculation without the threshold filter and exposes matching epochs and their ages. Expect **10 rows**. Compare ages as sets, not display order. Fill `execution-cases.csv` using actual outputs; its observed columns are intentionally empty.

| Success username / UTC time | Expected count | Expected ages in seconds | Required interpretation |
|---|---:|---|---|
| edge_300 / 09:05:00 | 3 | 300,180,60 | Age 300 included; this also crosses a clock-aligned five-minute boundary. |
| edge_301 / 09:05:01 | 2 | 181,61 | Age 301 excluded. |
| same_second / 09:05:00 | 2 | 300,180 | Age 0 excluded even though failure precedes success in file order. |
| ip_split / 09:05:00 | 2 | 300,180 | Failure from 192.0.2.15 must not join success from 192.0.2.14. |
| user_split / 09:05:00 | 2 | 300,180 | `other_user` failure at the same IP must not join. |
| dup_check / 09:05:00 | 2 | 300,180 | Duplicate 09:02 failure counts once. |
| out_order / 09:04:00 | 3 | 240,180,120 | Success appears before failures in input; event time governs. |
| two_successes / 09:03:00 | 3 | 180,120,60 | First independent success alerts. |
| two_successes / 09:04:00 | 3 | 240,180,120 | Second success also alerts; no reset. |
| two_only / 09:05:00 | 2 | 300,180 | Below threshold. |

`other_user` has no success and should have no diagnostic success row. Check exact identities, timestamps, IPs and counts, not merely total result count.

## 4. Threshold control and optional UTC variant

Run `08-candidate-threshold4.spl`: only the threshold differs from search 06. Expect zero result rows. Capture the completed job with zero results and no error; an empty CSV alone cannot distinguish an empty successful search from an unexecuted/failed search. Restore threshold 3 by rerunning search 06 and confirm the same four rows.

If search 05 shows a candidate time offset or you want explicit UTC parsing, run search 09 separately. Expect the same four result rows; label it `UTC-explicit variant`, not baseline. If adopting that variant, repeat searches 07 and 08 with only their parse expression changed to search 09's expression, save the revised SPL, and record them as separate jobs. A proposed change does not become validated until these searches are observed to complete correctly.

## 5. Capture evidence and decide

For each job record UTC start/end, search ID (SID), query filename, exact executed SPL, filters, time bounds, result count, warnings/errors and export/screenshot path. Export tables as CSV/JSON; screenshots should show query identity, completion and results. Retain the zero-row control screenshot. Sanitize credentials and unrelated account/tenant details without changing result fields needed for verification.

Use verdicts `NOT RUN`, `PASS`, `FAIL`, or `BLOCKED`. `PASS` requires an observed match and linked evidence. Blank observed fields mean unknown, never zero. Log deviations before changing a query or import; keep original and revised evidence separately.

Declare boundary validation complete only after all ingestion/time gates, all ten success cases, exact four-row threshold-three output, threshold-four zero-row control, restored threshold-three output and job-completion checks pass for the explicitly identified accepted query. If baseline UTC parsing fails, record that failure even if a revised variant passes. Keep preparation expectations and prior October 22 evidence intact; add a new dated record to the PR only after actual execution.

Coverage is limited to these synthetic cases. No future-failure, zero-failure-success, duplicate-success or malformed-input case is included in this fixture; do not claim those were tested. No production performance, live monitoring, account compromise or general security outcome is established.
