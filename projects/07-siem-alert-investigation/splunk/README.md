# Project 07 — Splunk authentication correlation follow-up

**Status: prepared, not executed in Splunk.** Python checks and live Splunk evidence are separate milestones. Existing offline and Mac execution records remain unchanged.

Use the existing owner-created Splunk Cloud trial from Project 09, if available. Upload only [synthetic_auth.jsonl](../synthetic_auth.jsonl), once, with JSON line parsing, timestamp field `timestamp`, format `%Y-%m-%dT%H:%M:%SZ` and UTC. Use source type `p07:auth:json`, host `p07-synthetic-lab`, source `synthetic_auth.jsonl` and the dedicated trial's `main` index. Do not use a workplace instance. Preview must show seven separate events on **7 October 2026**, not the upload date. Select **All time** for these historical fixtures.

1. Run [validate-ingestion.spl](validate-ingestion.spl). Expected: 7 records, 0 timestamp mismatches, 4 failures, 3 successes and 3 usernames. These are expectations, not observed Splunk results. Check for multivalue fields and search warnings before proceeding.
2. Run [detect-failure-success.spl](detect-failure-success.spl). Expected: one Medium row for `demo_owl`, `192.0.2.10`, success `2026-10-07T09:03:00Z`, failure count 3. `demo_fox` and `demo_badger` must not match. Export actual CSV and retain a redacted screenshot with search, time range and results.
3. Compare those fields with [example_alerts.json](../example_alerts.json), then record the actual outcome in [execution-template.md](execution-template.md). This query does not reproduce Python input-line references or alert IDs.
4. Only after successful interactive validation, save a private report named `Project 07 - Synthetic Authentication Correlation`. A recurring alert is optional and not necessary to prove search execution. Do not schedule an all-time replay indefinitely.

## Preserved semantics and limits

The query deduplicates identical four-field tuples. For each success it counts failures for the same username AND IPv4 address satisfying `success-300 <= failure < success`. It excludes failures at exactly the success second, includes the five-minute lower boundary, allows overlapping alerts and does not reset counts at a prior success. It uses explicit UTC parsing rather than session-dependent display time. It uses `eventstats` and multivalue expansion rather than fixed five-minute buckets.

This search is intended for this tiny, valid fixture. It is not a port of Project 06's complete schema validator and has not been parsed or run by Splunk in this preparation. Unique failure timestamps are sufficient only because deduplication and the original four-field schema leave at most one failure per account/IP/second. Eventstats/mvexpand memory limits can cause incomplete output on larger data; inspect warnings. No host/service field exists in the original event schema; scope to this one fictional service only. No production tuning, continuous scheduling or live incident claim is made.

Before claiming boundary parity, run separate controlled fixtures for 300-second inclusion, 301-second exclusion, same-second exclusion, different username/IP, duplicates and overlapping successes. Keep results per fixture; do not mix test cases without distinct identities.

Official command references used during preparation: [eventstats](https://help.splunk.com/en/splunk-enterprise/spl-search-reference/9.1/search-commands/eventstats) and [mvexpand](https://splunk.portal.heretto.com/en/splunk-enterprise/spl-search-reference/9.0/search-commands/mvexpand). Documentation review is not runtime validation.
