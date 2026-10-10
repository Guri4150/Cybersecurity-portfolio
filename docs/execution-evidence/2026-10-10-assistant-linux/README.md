# Offline verification — 10 October 2026

Operator: ChatGPT assistant. Environment: Linux, Python 3.12.14.
Run timestamp (UTC): 2026-10-10T08:36:26.596829+00:00.
Source commit: `d6b92b968126f9be7865b1ad1136f2738e23039e`.
All tested code, test files, fixtures and committed example bytes were verified against that commit's Git blob hashes.

This is an actual offline run in the assistant execution environment. It is **not Gurdit Singh's Mac run**, a deployed SIEM, production SOC experience, or a vulnerability assessment.

## Commands

Commands are shown relative to the repository root; the runner used the equivalent absolute paths and Python 3.12.14 interpreter. Output was captured separately from input.

```bash
python3 -m unittest discover -s projects/06-auth-log-parser -p 'test_*.py' -v
python3 projects/06-auth-log-parser/auth_parser.py projects/06-auth-log-parser/sample_auth.jsonl
python3 -m unittest discover -s projects/07-siem-alert-investigation -p 'test_*.py' -v
python3 projects/07-siem-alert-investigation/detect.py projects/07-siem-alert-investigation/synthetic_auth.jsonl
```

## Observed results

| Check | Result | Evidence |
| --- | --- | --- |
| Project 06 tests | 12 passed; exit 0 | [Test log](06-auth-log-parser-tests.txt) |
| Project 06 sample CLI | Exit 0; JSON semantically equal to committed example | [Generated report](06-auth-log-parser-report.json) |
| Project 07 tests | 10 passed; exit 0 | [Test log](07-siem-alert-investigation-tests.txt) |
| Project 07 sample CLI | Exit 0; JSON semantically equal to committed example | [Generated report](07-siem-alert-investigation-report.json) |

[Environment and result metadata](verification.json).

Project 06 observed nine lines, seven valid events, two intentionally invalid records, three successes and four failures. The default threshold flags 192.0.2.10 for three failures across the file; it does not establish an attack.

Project 07 observed seven unique valid events with no invalid, blank or duplicate events and one Medium alert for demo_owl/192.0.2.10. Failure lines 1–3 precede success line 4 within the rule's five-minute window. The alert is a review signal; compromise remains unconfirmed.

## Remaining milestones

- Gurdit's own local run and explanation remain pending.
- Actual SIEM installation, ingestion, native rule validation and alert evidence remain pending.
- Project 08 remains a fictional tabletop exercise. No guest lab, scan, remediation or retest was performed during this verification.

The tests establish behavior on small fictional fixtures in this environment. They do not establish performance on real logs, compatibility with every Python/OS version, or detection efficacy in a live service.
