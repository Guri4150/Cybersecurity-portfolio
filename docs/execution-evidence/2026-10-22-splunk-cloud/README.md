# Project 07 — Splunk Cloud execution

Executed 22 October 2026 through Safari on the owner's Mac, using the owner's logged-in Splunk Cloud trial. The assistant operated the upload and search UI with the owner's authorization and read the displayed results. This record is a transcription of observed UI results, not a raw Splunk export or a claim of independent owner execution.

## Ingestion

- File: `synthetic_auth.jsonl` from Project 07 in the local Cybersecurity-portfolio checkout.
- All seven records are fictional authentication events.
- Source: `synthetic_auth.jsonl`; source type: `_json`; index: `main`; host label: `project07-fictional-lab`.
- Preview showed seven separate records with timestamps from 2026-10-07T09:00:00Z to 2026-10-07T09:06:00Z.
- Upload completed successfully. The initial All time search returned exactly **7 events**.

## Correlation result

Run the [executed SPL](../../../projects/07-siem-alert-investigation/splunk-search.spl) in Search & Reporting with All time selected. The executed search returned **one statistics row**:

| Success timestamp (UTC) | Username | Source IP | Preceding failures | Severity |
|---|---|---|---|---|
| 2026-10-07T09:03:00Z | demo_owl | 192.0.2.10 | 3 | medium |

Assessment displayed: **Review required; compromise unconfirmed**.

The search deduplicates the four input fields, collects failure times for each username/IP pair, and counts failures with `success_time - 300 <= failure_time < success_time`. Prior successes do not reset the count.

The assistant also ran the existing Python detector on the same Mac and input. It reported seven valid unique events, zero invalid/duplicate records, and one matching alert with the same account, IP, time, failure count, and severity. Its input-line alert ID is `SYN-AUTH-001-L004`; the Splunk search does not reconstruct input line IDs.

## Threshold check and saved report

On 22 October 2026, the assistant changed only `where failure_count>=3` to `where failure_count>=4` and ran the search. Splunk completed with **0 events**, **Statistics (0)**, and **No results found**. Restoring the threshold to 3 and rerunning returned the original single `demo_owl` row with failure_count 3.

Saved the restored search as **Project 07 - Synthetic Authentication Correlation**. Splunk confirmed “Your Report Has Been Created”; opening the report displayed the saved title, All time selection, and one matching result. No schedule or notification was configured. The owner captured the threshold-3 screenshot at 17:32 on 22 October 2026. The assistant reviewed it and copied it unchanged as `splunk-threshold-3.png`. It shows the query and one match; the threshold-4 test and saved-report confirmation are recorded from direct UI observations, not from this screenshot.

![Threshold-3 query and result](splunk-threshold-3.png)

## Scope and limitations

This completes a manual Splunk ingestion and correlation run on the supplied seven-event fixture. No scheduled Splunk alert or notification was configured. This is a synthetic learning lab; it does not establish a real compromise or production SOC experience.

This SPL was verified against this fixture only, not against the full Python boundary-test suite. The batch `eventstats`/multivalue approach is intended for this small lab and is subject to Splunk search-memory limits. The timestamp format treats the literal Z as text; relative comparisons are sufficient for this UTC fixture, but broader use should explicitly parse timezone offsets. The query does not replicate Python's complete schema validation.

The project documentation, executed SPL, and reviewed screenshot were added to the local portfolio after the run. No code changes, commit, push, or public publication are part of this update.

Reference for multivalue evaluation: [Splunk multivalue eval functions](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/10.2/evaluation-functions/multivalue-eval-functions).
