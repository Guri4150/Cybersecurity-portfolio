# Project 09 — Synthetic DNS detection: Python and Splunk Cloud

**Status:** Owner-local Mac execution is documented in the [2026-10-21 screenshot-reviewed execution record](mac-execution-2026-10-21.md), including evidence provenance and limits. Raw artifacts remain on the owner's Mac and are not published here. The [Splunk Cloud trial lab](splunk/README.md) now has observed ingestion, native search validation and scheduled historical alert firing; the replay alert was disabled after testing. This extends the [original Project 09 DNS triage tabletop](../09-dns-anomaly-triage.md) without replacing its reasoning.

## Objective and scope

Use a deterministic fictional DNS JSONL stream to generate and investigate a suspicious TXT-query burst. Every event, address and name is fabricated. `sync.example` and `portal.example` use the reserved `.example` namespace. The Python programs process files locally and **do not** send DNS queries, capture packets, monitor the Mac, connect to a SIEM, or prove tunneling/exfiltration.

The fictional `ws-07` (`10.20.5.7`) has **480 queries** in `[2026-10-15 08:30, 08:35) UTC`: 450 distinct TXT questions for `*.sync.example` and 30 A questions for `portal.example`. Synthetic DNS responses, duplicate telemetry and two other clients are included as controls. Names such as `q0001` are *not* evidence of high entropy.

## Files

- `generate_fixture.py` — prints deterministic synthetic JSONL to standard output.
- `dns_detector.py` — validates events, deduplicates by `event_id`, buckets TXT queries into fixed UTC five-minute windows, and outputs JSON alerts.
- `test_dns_detector.py` — ten automated tests of thresholds, time boundaries, deduplication, UTC normalization and false-positive controls.
- `example_alerts.json` — expected example output from the prepared fixture, not owner-generated evidence.
- `analyst_handoff_template.md` — worksheet for an analyst's own assessment and Mac evidence.

## Run on your Mac (Python 3.9+; no external packages)

Open Terminal in the repository root. Use `main` after PR #1, or the recorded source revision when reproducing that exact run:

```bash
python3 --version
git status --short
umask 077
LAB_EVIDENCE="$(mktemp -d "${TMPDIR:-/tmp}/p09-evidence.XXXXXX")"
printf 'Evidence folder: %s\n' "$LAB_EVIDENCE"
python3 projects/09-dns-detection-lab/generate_fixture.py > "$LAB_EVIDENCE/synthetic_dns.jsonl"
python3 projects/09-dns-detection-lab/dns_detector.py "$LAB_EVIDENCE/synthetic_dns.jsonl" > "$LAB_EVIDENCE/alerts.json"
python3 -m unittest discover -s projects/09-dns-detection-lab -p 'test_*.py' -v > "$LAB_EVIDENCE/tests.txt" 2>&1
cat "$LAB_EVIDENCE/tests.txt"
cat "$LAB_EVIDENCE/alerts.json"
```

**Check each command for an error before continuing.** Record run metadata:

```bash
date -u '+%Y-%m-%dT%H:%M:%SZ' > "$LAB_EVIDENCE/run-utc.txt"
git rev-parse HEAD > "$LAB_EVIDENCE/source-commit.txt"
python3 --version > "$LAB_EVIDENCE/python-version.txt"
```

Check report equivalence without modifying the expected example:

```bash
python3 - "$LAB_EVIDENCE/alerts.json" <<'PY'
import json, sys
with open(sys.argv[1], encoding='utf-8') as f:
    actual = json.load(f)
with open('projects/09-dns-detection-lab/example_alerts.json', encoding='utf-8') as f:
    expected = json.load(f)
if actual != expected:
    raise SystemExit('MISMATCH: compare counters and alert fields')
print('MATCH: generated report equals prepared example')
PY
```

## Expected result (prepared in assistant Linux environment)

- `Ran 10 tests` and `OK` (test run success is not automatic evidence of Mac execution).
- `total_lines: 628`, `duplicate_event_ids: 1`, `invalid_lines: 0`, `unique_events: 627`.
- `eligible_txt_queries: 595` (450 from ws-07, 110 repeated from ws-08, 35 from ws-09).
- **One Medium alert** for `10.20.5.7`, window `[08:30, 08:35) UTC`, `txt_query_count: 450`, `distinct_query_names: 450`.
- Second client has 110 TXT queries but only one distinct query name and should not alert; the third client has only 35 TXT queries and should not alert.

## Exact detection rule and limitations

Filter to unique, valid DNS `query` events whose type is `TXT` and whose lowercased name is `sync.example` or ends in `.sync.example`. Group by normalized UTC five-minute fixed bucket and `client_ip`. Alert when **TXT count >= 100 AND distinct question names >= 80**. Windows include their start and exclude their end. Event IDs deduplicate globally by first occurrence.

These illustrative thresholds are **not a production recommendation**. The program does not calculate entropy, determine registered domains dynamically, measure a real baseline, correlate processes, inspect responses, identify sensitive data, or track network egress. Missing/invalid lines are counted, but validation is limited; duplicate IDs with differing content are silently treated as first-wins. Fixed buckets can miss bursts straddling windows, and there is no ingestion-delay handling. A match is an **investigation lead**, not proof of compromise.

Do not upload actual system/network logs or identifiers. Only publish evidence after review for real personal data. The generator never accesses the network or machine logs, so there is no reason to run it using `sudo`.

## Recommended evidence to collect

After running the code yourself, save the executed Git commit, UTC run date, Python version, full test log, generated alerts, and a short analyst note distinguishing the suspicious signal from unsupported exfiltration claims. Use `analyst_handoff_template.md`. The generated fixture and report are fictional; the **execution transcript on your Mac** is the actual hands-on evidence.

**Splunk lab milestone completed — 2026-10-21 UTC:** the owner uploaded the fictional fixture to a Splunk Cloud trial; the assistant configured parsing and ran native validation/searches through the owner's browser, then verified scheduled historical alert triggers. See the [evidence summary](splunk/evidence-2026-10-21.md) and [reproduction guide](splunk/README.md). This is assisted lab work, not independent production SIEM deployment. Next evidence improvement: retain redacted exports of scheduled-job results before cleanup.
