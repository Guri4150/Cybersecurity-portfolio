# Project 07 — Splunk boundary-validation preparation

**Prepared 23 October 2026. This fixture has NOT been run in Splunk Cloud.**

The [22 October Project 07 Splunk lab](../../../../docs/execution-evidence/2026-10-22-splunk-cloud/README.md) was assistant-operated and verified only against the original seven fictional records and a threshold variation. This additional dataset is for a future owner-executed, authorized, synthetic-data validation run. Do not relabel expected outputs as observed results.

## Prepared fixture and cases

- [`splunk-boundary-2026-10-23.jsonl`](splunk-boundary-2026-10-23.jsonl): 36 fictional JSONL lines, 35 distinct four-field tuples, one exact duplicated failure. All IPv4 addresses are from documentation ranges.
- [`expected-boundary-results.json`](expected-boundary-results.json): four qualifying successes expected from the five-minute Python rule. This is an offline semantic check, **not an observed Splunk result**.
- Every synthetic event timestamp is 7 October 2026 UTC, *not* the October 23 preparation date.

| Case | Purpose | Expected rows |
| --- | --- | ---: |
| `edge_300` | 300-second-old failure counts; lower boundary inclusive | 1 |
| `edge_301` | 301-second-old failure excluded; two remaining | 0 |
| `same_second` | Failure at success timestamp excluded | 0 |
| `ip_split` | Third failure from different source IP | 0 |
| `user_split` | Third failure from different username | 0 |
| `dup_check` | Identical failure tuple deduplicated | 0 |
| `out_order` | Input order differs from event-time order | 1 |
| `two_successes` | Two qualifying successes both alert | 2 |
| `two_only` | Two failures are below threshold | 0 |

## Import safely

Use an authorized Splunk Cloud trial or isolated non-production instance. The input is fictional; do not upload real authentication logs or enable scheduled alerts/actions. Leave the existing Project 07 report and disabled Project 09 historical replay alert untouched.

Upload the fixture as source `splunk-boundary-2026-10-23.jsonl`, host `p07-boundary-lab`, sourcetype `_json`, index `main`; parse `timestamp` in UTC. Verify the preview has one record per line. In Search & Reporting select **All time** (historical 2026-10-07 events). If the instance assigns a different source, host, index or sourcetype, first verify actual values and replace the filters; do not search unscoped data.

Raw-ingestion check:

```spl
index="main" source="splunk-boundary-2026-10-23.jsonl" host="p07-boundary-lab" sourcetype="_json" earliest=0
| stats count AS raw_events
```

Expect `raw_events=36`. Deduplicated check:

```spl
index="main" source="splunk-boundary-2026-10-23.jsonl" host="p07-boundary-lab" sourcetype="_json" earliest=0
| dedup timestamp username source_ip status
| stats count AS unique_tuples
```

Expect `unique_tuples=35`. Resolve ingestion mismatches/repeated uploads before claiming a rule match.

## Candidate SPL to run and document

```spl
index="main" source="splunk-boundary-2026-10-23.jsonl" host="p07-boundary-lab" sourcetype="_json" earliest=0
| dedup timestamp username source_ip status
| eval event_epoch=strptime(timestamp,"%Y-%m-%dT%H:%M:%SZ")
| eventstats values(eval(if(status="failure",event_epoch,null()))) AS failure_times BY username source_ip
| where status="success"
| eval matching_failures=mvmap(failure_times,if(failure_times>=event_epoch-300 AND failure_times<event_epoch,failure_times,null()))
| eval failure_count=coalesce(mvcount(matching_failures),0)
| where failure_count>=3
| table timestamp username source_ip failure_count
| sort 0 username timestamp
```

Expected **four** rows (not yet observed): `edge_300` 09:05:00Z (3); `out_order` 09:04:00Z (3); `two_successes` 09:03:00Z (3) and 09:04:00Z (3). See the JSON for precise IPs. As a negative control, change only `failure_count>=3` to `>=4`: expect zero rows; then restore 3.

## Required execution evidence before declaring validation complete

Record the operator, UTC run date, environment, Git commit, actual Splunk field mapping and source labels, executed SPL, ingestion count, dedup count, screenshot/redacted result export, threshold-four control, and any mismatches. Do not change this preparation note into a fake run record. Add a new dated execution note once results are actually observed.

**Limitations:** this query presumes valid UTC four-field records; unlike Python it does not fully validate malformed schemas. Its `values` / `mvmap` approach is for a small batch; it has search-memory limits, doesn't establish general timezone handling or production readiness, and is not proof of account compromise. No scheduled alert was configured as part of this preparation.
