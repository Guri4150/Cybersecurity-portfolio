# Synthetic SIEM-style alert investigation

An offline SOC learning project using entirely fictional authentication events.
It extends project 06 with event-time correlation, reproducible alert output,
and an evidence-based investigation. It does not deploy a SIEM, ingest live
telemetry, establish a real incident, or demonstrate production SOC experience.

## Scenario and result

The invented account `demo_owl` records three failed logins from
`192.0.2.10`, followed by a success at 09:03 UTC on October 7, 2026.
The rule emits one **Medium** alert. The simulated analyst disposition is
**suspicious authentication; compromise unconfirmed**.

Read [the investigation](investigation.md) for the timeline, competing
explanations, triage, severity, and proposed response. Read
[the detection specification](detection.md) for exact rule semantics.

## Repository structure

```text
projects/
    06-auth-log-parser/
        auth_parser.py                 # existing dependency, unchanged
    07-siem-alert-investigation/
        README.md
        detection.md
        investigation.md
        detect.py
        synthetic_auth.jsonl
        example_alerts.json
        test_detect.py
        validation.md
```

The existing project's other files remain in place. This project imports its
`parse_event` function using a path relative to this script. No copying or
modification of project 06 is required in the repository.

## Run on Mac or Linux

Use Python 3 with the standard library; no packages, API keys, elevated access,
network requests, or security product account are required.
From the repository root:

```bash
python3 projects/07-siem-alert-investigation/detect.py projects/07-siem-alert-investigation/synthetic_auth.jsonl
python3 -m unittest discover -s projects/07-siem-alert-investigation -p 'test_*.py' -v
```

Optional comparison with the earlier parser:

```bash
python3 projects/06-auth-log-parser/auth_parser.py projects/07-siem-alert-investigation/synthetic_auth.jsonl
```

Project 06 flags the source's three failures across the whole file.
Project 07 additionally requires a later success for the same username and IP
within a bounded interval. Neither output establishes an attack.

The complete observed JSON is in [example_alerts.json](example_alerts.json).
Its key results are seven unique valid events, zero rejected records, zero
duplicates, and one alert `SYN-AUTH-001-L004`, referencing failure lines
1, 2, 3 and success line 4. Line numbers are one-based input references.
The other three events do not meet the rule.

To save another report, redirect to a new filename, never the input filename.
Exit code 0 means processing completed, including when bad records were skipped;
1 means the dependency or input could not be read; 2 means CLI arguments are
invalid. Inspect data-quality counters even if the alert list is empty.

## Safe data and honest portfolio use

All names, dates, addresses, events, and case context are invented. The IPv4
addresses use documentation ranges. No real account was accessed and no
containment action was performed. Do not add real logs, secrets, tokens,
customer details, employer information, or screenshots containing private data.
Validation checks structure, not whether data is safe to publish.

Suggested interview description after reviewing and running it yourself:

> I studied an offline SIEM-style authentication investigation using fictional
> logs. The project correlates repeated failures with a later success, tests
> rule boundaries, and distinguishes an alert match from confirmed compromise.

Do not describe this as operating a production SIEM or responding to a real
breach. Execution evidence from project preparation is recorded separately in
[validation.md](validation.md); your own local run has not been assumed.

## Limitations and next lab

This is a small batch correlation exercise, not a SIEM installation.
The input schema has no host, application, session, event ID, device, MFA, or
endpoint fields. It assumes one authentication service and one UTC clock.
See detection.md for deduplication, false positives, false negatives, and
performance limits. The simulated investigation deliberately leaves uncertainty
unresolved instead of inventing user interviews or endpoint findings.

Next: ingest only this fictional dataset into an isolated SIEM lab, implement
the same rule, compare results, and capture your own sanitized screenshots.
That deployment remains future work.
