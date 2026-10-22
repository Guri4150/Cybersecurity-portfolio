# Observed validation

On October 8, 2026, the Linux project preparation environment (Python 3.12.14) ran the detector and
the automated test suite against fictional fixtures. This is not a claim that
Gurdit ran the project on his Mac or operated a SIEM.

Commands, from the repository root:

```bash
python3 projects/07-siem-alert-investigation/detect.py projects/07-siem-alert-investigation/synthetic_auth.jsonl
python3 -m unittest discover -s projects/07-siem-alert-investigation -p 'test_*.py' -v
```

Observed result: **10 tests passed**. The sample CLI output exactly matches
`example_alerts.json`. One Medium alert referenced lines 1, 2, 3 and 4.

Coverage: threshold equality and below-threshold behavior, inclusive
five-minute boundary and one second outside it, exclusion of simultaneous or
future failures, username and IP separation, unsorted inputs, exact tuple
deduplication, invalid and blank input accounting, empty input, no-success
input, repeated success alerts, missing input, and invalid UTF-8.

The dependency was fetched from the current project 06 file and used unchanged.
Only the new project's tests were run; this is not a new validation claim for
the earlier project's complete suite. No SIEM product, live collector, account
action, scan, or network investigation was tested.

## Splunk Cloud follow-up — 22 October 2026

A separate assistant-guided run ingested seven fictional events, reproduced the
one-match result, verified zero matches at threshold 4, and restored threshold 3.
A manual report was saved. See the [dated record and screenshot](../../docs/execution-evidence/2026-10-22-splunk-cloud/README.md).
This does not imply that the Python boundary suite was executed as SPL tests.
