# Project 09 — Splunk Cloud trial lab

**Status:** Assisted synthetic ingestion, native SPL validation and scheduled historical alert firing observed on 2026-10-21 UTC. Replay alert disabled after testing. Documentation prepared on 2026-10-22 IST.

The owner created the trial and uploaded the fictional JSONL file. The assistant used the owner's Safari session to correct parsing, run searches, save a report, configure and verify a scheduled alert, and disable it with approval. This is not a claim of independent production SOC work or Splunk Enterprise Security deployment.

## Evidence and reusable searches

- [Observed evidence and cleanup](evidence-2026-10-21.md)
- [Ingestion validation](validate-ingestion.spl)
- [All three clients and negative controls](validate-controls.spl)
- [Matching detection results](detect-txt-burst.spl)

The SPL files reproduce the searches actually executed, with line breaks added for readability. They have not been rerun as repository files. Select **All time** in Splunk; the fixture's timestamps are October 15, not the upload date. Change the base filters only if you intentionally use another lab index/source/host. These files are search text, not a deployable Splunk app.

## Reproduce ingestion

1. Generate `synthetic_dns.jsonl` using [the existing Python generator](../generate_fixture.py) and the [Mac instructions](../README.md). Upload only the fictional fixture once.
2. In Add Data, choose JSON parsing. Set timestamp field `timestamp`, format `%Y-%m-%dT%H:%M:%SZ`, and GMT/UTC. Save as `p09:dns:json`.
3. Check the preview shows 628 events, one line per event, and October 15 08:30–08:34:59 UTC. Fix parsing before submitting.
4. In the dedicated trial used here, select index `main`, host `p09-synthetic-lab`, source `synthetic_dns.jsonl`. This guide is not a recommendation to upload lab fixtures to a production index.
5. Run the validation searches before the detection. Expected ingestion: 628 records, 627 unique IDs, one duplicate, zero timestamp mismatches and zero multi-valued IDs. Repeated uploads change counts; investigate rather than treating expected numbers as evidence.
6. Controls: 10.20.5.7 = 450 TXT / 450 names (match); 10.20.5.8 = 110 / 1 (no match); 10.20.5.9 = 35 / 35 (no match). The detection returns one Medium-labeled row for the first client.

The executed ingestion validation used a literal `Z` in `strptime`, with the session displaying UTC. For other session timezones, explicitly parse the timezone (for example replace the trailing Z with +0000 and use %z) before comparing epoch values. Displayed result times follow the session timezone. The observed UTC window is [08:30,08:35).

## Recorded alert configuration

| Setting | Tested value |
| --- | --- |
| Name | Project 09 - DNS TXT Burst - Historical Replay Test |
| Permissions | Private |
| Type | Scheduled |
| Temporary cron | `* * * * *` (every minute) |
| Search | detect-txt-burst.spl |
| Time range | All time, scoped to the synthetic source |
| Trigger | Number of results > 0, once per search |
| Action | Add to Triggered Alerts |
| Severity | Medium |
| Trigger record expiry | 24 hours |
| Final state | Disabled |

The report is named **Project 09 - Synthetic DNS TXT Burst Detection**. The alert was a short historical replay, not a live monitoring schedule. Record expiry does not stop scheduling. There were no email or webhook actions.

If reproducing the schedule, supervise the test, capture the trigger history and export the scheduled result before cleanup. Splunk warned that disabling deletes trigger history and related results. The owner approved that deletion here after a written summary was saved. The retained summary records observed trigger entries; individual scheduled-job payloads and raw screenshots were not archived in this repository.

## Interpretation and limits

The match is an investigation lead in invented data. No tunneling, exfiltration or compromise is established. The thresholds are illustrative; fixed buckets miss some boundary-straddling bursts. The SPL is validated against this fixture, not every Python validation edge case. Splunk dedup keeps a record according to search order; it is not guaranteed to reproduce Python's first-input-occurrence behavior for conflicting duplicate IDs. Counts matching the Python example do not mean full JSON equivalence or complete validation parity.

Future work: retain redacted scheduled-job exports, test SPL threshold/window edge cases, and design a bounded recent-time schedule with appropriate ingestion-delay handling for an authorized lab. Project 07's separate SIEM milestone and Project 08's assessment work remain pending.
