# Owner-local execution — 15 October 2026

## Provenance and scope

Gurdit Singh ran Projects 06 and 07 on his Mac during a guided practice session on 15 October 2026 (Asia/Kolkata). The assistant reviewed user-supplied Terminal screenshots showing commands and results, then prepared this transcription. This is separate from the assistant's Linux preparation tests on 10 October.

The screenshots and original generated report files are not committed here. This page is a summary of screenshot evidence, not a raw terminal transcript or an independently rerun verification. The exercises use the repository's fictional inputs.

## Environment and revision

- Mac terminal with zsh; exact macOS version and hardware architecture were not captured.
- Python: 3.9.6.
- Git: 2.50.1 (Apple Git-155).
- Reported checkout HEAD: `07daa32ca26b56883f12f30cd06dbff16d2ac373`.
- Project 07 followed Project 06 in the same checkout; no revision change was shown.
- A tracked-file cleanliness check was not captured.

## Project 06: authentication-log parser

Commands run from `projects/06-auth-log-parser`:

```bash
python3 -m unittest discover -s . -p 'test_*.py' -v
python3 auth_parser.py sample_auth.jsonl > mac-report.json
cat mac-report.json
diff -u example_output.json mac-report.json
git rev-parse HEAD
```

Observed: **12 tests passed**, with the suite reporting 0.223 seconds and OK.

The displayed report contained 9 total lines, 0 blank lines, 2 invalid lines, 7 valid events, 3 successes and 4 failures. With failure threshold 3, source `192.0.2.10` was flagged with 3 failures.

The comparison returned to the prompt without differences or an error displayed. Its numeric exit status was not separately recorded.

## Project 07: offline correlation

Commands run from `projects/07-siem-alert-investigation`:

```bash
python3 -m unittest discover -s . -p 'test_*.py' -v
python3 detect.py synthetic_auth.jsonl > mac-alerts.json
cat mac-alerts.json
diff -u example_alerts.json mac-alerts.json
```

Observed: **10 tests passed**, with the suite reporting 0.098 seconds and OK.

The displayed report contained:

| Field | Result |
|---|---|
| Total lines / unique valid events | 7 / 7 |
| Blank / invalid / duplicate events | 0 / 0 / 0 |
| Window | 300 seconds |
| Minimum failures | 3 |
| Alerts | 1 |
| Alert ID | SYN-AUTH-001-L004 |
| Severity | medium |
| Username | demo_owl |
| Source IP | 192.0.2.10 |
| Failure lines / success line | 1, 2, 3 / 4 |
| Success time in fictional input | 2026-10-07T09:03:00Z |
| Assessment | Review required; compromise not established |

The comparison returned to the prompt without differences or an error displayed. Its numeric exit status was not separately recorded.

## Interpretation reviewed during guided practice

Repeated failures can reflect password mistakes or software using stale credentials. A later success adds investigation context but does not establish malicious intent. Review account, timing and related activity before classifying an incident.

This explanation was supplied during coaching; it is not presented as an independently authored analyst finding by the portfolio owner.

## What this milestone establishes

The screenshot evidence records owner-local execution of both existing Python projects and successful tests on Python 3.9.6, plus generated outputs consistent with the committed examples.

It does not establish production SOC experience, independent code authorship, a deployed SIEM, live telemetry ingestion, or a real compromise. Project 08 scanning/remediation/validation and Project 09 packet-capture execution remain unperformed in this record.

Future evidence improvements: attach reviewed original test logs and reports, record the precise OS version and tracked-file status, and add the owner's own explanation after further practice.

[Back to portfolio](../../../README.md)
