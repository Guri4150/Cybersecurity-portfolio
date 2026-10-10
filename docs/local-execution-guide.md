# Projects 06–08: local execution and evidence guide

Prepared for Gurdit Singh · 10 October 2026 · Mac-first commands, also usable on Linux.

## 1. What is complete, and what remains unperformed

| Project | Completed offline artifacts | Next evidence milestone |
| --- | --- | --- |
| 06: authentication-log parser | Python code, fictional JSONL, 12 tests, example report | Run on your computer; retain environment, test log, report and explanation |
| 07: SIEM-style investigation | Python correlation, fictional JSONL, 10 tests, example alert, investigation | Reproduce offline output on your computer; separately deploy and validate an isolated SIEM |
| 08: vulnerability assessment | Fictional scope, inventory, four findings, severity and remediation/validation plans | Build actual owned lab fixtures; verify isolation; collect observations, apply fixes and retest |

Runnable code and an example report are not evidence that you personally executed them. Running Project 07 is not SIEM deployment. Reading Project 08 is tabletop review, not a scan or completed assessment. Keep the original fictional findings and register unchanged; add actual lab work separately.

During preparation of this guide, the assistant reran Projects 06 and 07 in its Linux preparation environment using Python 3.12.14: all 12 and 10 tests passed, and both parsed JSON reports matched their committed examples. This is preparation evidence only, not Gurdit's Mac evidence. No SIEM was installed and no Project 08 lab was built, scanned, remediated or retested.

## 2. Prerequisites and workspace

For the offline work, use Terminal, Git and Python 3.12 (the verified baseline). There are no third-party Python packages, API keys or privileged commands. Other Python versions should be assessed with the tests rather than assumed compatible. Check:

```bash
git --version
python3 --version
```

If either command is missing, install Git or Python from its official installer before continuing. On Windows with Python installed, use `py -3` instead of `python3`; the shell commands below assume Mac/Linux, so use a Bash environment or translate paths/redirection deliberately.

Use your existing checkout if you have one. Otherwise clone into a new directory:

```bash
git clone https://github.com/Guri4150/Cybersecurity-portfolio.git
cd Cybersecurity-portfolio
```

For an existing checkout, `cd` to its root and inspect `git status --short`. If clean and you want current main, `git pull --ff-only` is sufficient; if it is dirty or diverged, keep it intact and use a separate clone. Do not reset or overwrite your work. Confirm the files:

```bash
ls projects/06-auth-log-parser
ls projects/07-siem-alert-investigation
ls projects/08-vulnerability-assessment-lab
```

Project 07 needs the sibling `projects/06-auth-log-parser/auth_parser.py`; do not download Project 07 alone. All following offline commands start at the repository root and run individually. Do not continue past a failed command.

Create an evidence directory outside the repository so raw captures cannot be committed accidentally. Run this once per session:

```bash
umask 077
PORTFOLIO_EVIDENCE=$(mktemp -d "${TMPDIR:-/tmp}/portfolio-evidence.XXXXXX")
printf '%s\n' "$PORTFOLIO_EVIDENCE"
date -u '+%Y-%m-%dT%H:%M:%SZ' > "$PORTFOLIO_EVIDENCE/run-start-utc.txt"
git rev-parse HEAD > "$PORTFOLIO_EVIDENCE/repository-commit.txt"
git status --short > "$PORTFOLIO_EVIDENCE/working-tree-status.txt"
python3 --version > "$PORTFOLIO_EVIDENCE/python-version.txt" 2>&1
uname -srm > "$PORTFOLIO_EVIDENCE/os-version.txt"
```

Keep the printed path. Temporary evidence may be deleted by the OS: after review, copy selected sanitized files into a permanent evidence folder. Do not upload raw data automatically. If the working-tree status is nonempty, record which modifications affected the run; a commit alone does not identify changed bytes.

## 3. Project 06: reproduce the parser

Run the tests and inspect the captured log:

```bash
python3 -m unittest discover -s projects/06-auth-log-parser -p 'test_*.py' -v > "$PORTFOLIO_EVIDENCE/p06-tests.txt" 2>&1
printf 'test exit code: %s\n' "$?"
cat "$PORTFOLIO_EVIDENCE/p06-tests.txt"
```

Expected: exit code `0`, `Ran 12 tests`, then `OK`. Test duration varies. Zero discovered tests is not a passing reproduction.

Generate the report, with a separate output filename:

```bash
python3 projects/06-auth-log-parser/auth_parser.py projects/06-auth-log-parser/sample_auth.jsonl > "$PORTFOLIO_EVIDENCE/p06-report.json" 2> "$PORTFOLIO_EVIDENCE/p06-stderr.txt"
printf 'parser exit code: %s\n' "$?"
cat "$PORTFOLIO_EVIDENCE/p06-report.json"
```

Expected: exit `0`, no stderr, and these values:

| Field | Expected |
| --- | --- |
| total_lines / blank_lines / invalid_lines | 9 / 0 / 2 |
| valid_events / successes / failures | 7 / 3 / 4 |
| failure_threshold | 3 |
| flagged_sources | One source: `192.0.2.10`, 3 failures |

The two rejected lines are deliberately invalid fixtures. Exit `0` does not mean every line was valid. The parser sums failures by source across the whole file and across usernames; it does not use time windows or correlate a later success.

Try the configurable boundary:

```bash
python3 projects/06-auth-log-parser/auth_parser.py projects/06-auth-log-parser/sample_auth.jsonl --threshold 4 > "$PORTFOLIO_EVIDENCE/p06-threshold4.json"
printf 'threshold run exit code: %s\n' "$?"
cat "$PORTFOLIO_EVIDENCE/p06-threshold4.json"
```

Expected: the same event counts, threshold `4`, and an empty `flagged_sources` list. This is threshold behavior, not proof the account is safe.

Capture the full test log, both JSON reports, the source commit and Python version. Add your own short explanation of why the default flags the source and why the threshold-4 run does not.

## 4. Project 07: reproduce offline correlation

```bash
python3 -m unittest discover -s projects/07-siem-alert-investigation -p 'test_*.py' -v > "$PORTFOLIO_EVIDENCE/p07-tests.txt" 2>&1
printf 'test exit code: %s\n' "$?"
cat "$PORTFOLIO_EVIDENCE/p07-tests.txt"
python3 projects/07-siem-alert-investigation/detect.py projects/07-siem-alert-investigation/synthetic_auth.jsonl > "$PORTFOLIO_EVIDENCE/p07-alerts.json" 2> "$PORTFOLIO_EVIDENCE/p07-stderr.txt"
printf 'detector exit code: %s\n' "$?"
cat "$PORTFOLIO_EVIDENCE/p07-alerts.json"
```

Expected: 10 tests pass; detector exit `0`; 7 unique valid events, no invalid/blank/duplicate events; exactly one Medium alert `SYN-AUTH-001-L004`. It references failure lines `[1, 2, 3]` and success line `4`, for `demo_owl` and `192.0.2.10` at `2026-10-07T09:03:00Z`. Assessment: review required; compromise not established.

Rule: the same username **and** source IP must have at least three failures with `success_time - 300 seconds <= failure_time < success_time`. The five-minute lower boundary is inclusive; same-second failures are excluded. Identical normalized events are deduplicated; events are sorted by event time. Prior successes do not reset the failure count, and multiple successes can produce overlapping alerts.

Compare both generated reports semantically with the examples, from the repository root:

```bash
python3 - "$PORTFOLIO_EVIDENCE" <<'PY'
import json
from pathlib import Path
import sys
evidence = Path(sys.argv[1])
pairs = [
    ('p06-report.json', 'projects/06-auth-log-parser/example_output.json'),
    ('p07-alerts.json', 'projects/07-siem-alert-investigation/example_alerts.json'),
]
for actual, expected in pairs:
    observed = json.loads((evidence / actual).read_text())
    reference = json.loads(Path(expected).read_text())
    if observed != reference:
        raise SystemExit(f'MISMATCH: {actual}; inspect input, options and code')
    print(f'MATCH: {actual}')
PY
```

Expected: two `MATCH` lines and exit `0`. Formatting and trailing newlines do not affect this comparison. Do not edit expected examples to conceal a mismatch.

Optional comparison: feed the Project 07 fixture to Project 06:

```bash
python3 projects/06-auth-log-parser/auth_parser.py projects/07-siem-alert-investigation/synthetic_auth.jsonl > "$PORTFOLIO_EVIDENCE/p06-on-p07-input.json"
cat "$PORTFOLIO_EVIDENCE/p06-on-p07-input.json"
```

Expected: 7 valid events, 4 failures and 3 successes; `192.0.2.10` has 3 failures. Project 06 flags the IP across the file; Project 07 correlates three failures and a later success for one account/IP pair. Neither establishes who logged in or whether compromise occurred.

Capture tests, alerts, comparison output, and an annotated four-event timeline. Explain one benign possibility (mistyped password), one suspicious possibility, and the additional endpoint/session/MFA evidence that would distinguish them. Do not invent that additional evidence.

## 5. Optional next milestone: an actual isolated SIEM

This is a separate deployment, not a prerequisite for the Python runs. No SIEM product or deployment files are supplied in this repository. Choose a product compatible with your computer/VM architecture and check its current official installation instructions and resource requirements before provisioning. Record product/version, guest OS, CPU/RAM/disk, rule configuration and network layout. Do not treat this section as a product-specific installation script.

Use an internal-only VM network with no host adapter, bridge, NAT, gateway, external DNS, or internet route while the lab is operating. Prestage trusted installers and dependencies before isolation. Operate the SIEM UI from another guest on that internal network. Capture hypervisor adapters and guest routes before ingestion; avoid production connectors and real logs.

1. Install the selected SIEM using its official instructions; record its configuration and startup/health checks.
2. Import only Project 07's seven fictional JSONL events, mapping `timestamp` to UTC event time, `username`, `source_ip`, and `status`. Use one service/dataset. Configure the search time range to cover **7 October 2026, 09:00–09:06 UTC**; these are historical fixture events, not today's ingestion time.
3. Confirm all seven events arrived and inspect field mappings before creating a rule. Repeated imports can duplicate events; record and control this.
4. Translate `detection.md` into the product's native query/rule. Preserve exact deduplication, account/IP grouping, inclusive five-minute boundary, strict exclusion of same-second failures and one result per qualifying success. A bucketed five-minute count alone is not an equivalent rule.
5. Run the query against historical event time, using replay/backfill support if available. A real-time schedule may not alert on an old fixture. Distinguish a search match from a generated SIEM alert and capture both if claiming alert generation.
6. Compare with the offline result: seven unique events, one match for `demo_owl`/`192.0.2.10`, three preceding failures and the 09:03 success. Vendor alert identifiers may differ; retain your original input line references as separate traceability metadata rather than altering the four-field Python schema.
7. Create separate fictional boundary fixtures from the test cases: exactly 300 seconds (match), 301 seconds (no match), same-second failures (no match), different username/IP (no match), duplicate tuple (count once), and unsorted input (same result). Record observed results, including discrepancies.

Evidence: isolation checks; installation/version and health; dataset mapping; exact native query/rule export; ingestion counts/time range; raw sanitized result and actual alert screenshot; boundary results; explanation of any semantic difference. A screenshot of a dashboard alone does not prove the correlation was reproduced. Until deployment and rule evidence exist, keep “isolated SIEM deployment” pending.

## 6. Project 08: tabletop review, then a separate hands-on lab

### Stage A — review the existing documentation

Read the README and files 01–05 in order. No scanner or executable fixture is included. Explain the priority order VA-001, VA-002, VA-003, VA-004 and distinguish illustrative CVSS severity from scenario priority. The current register remains `Open — simulated`, fix `No`, validation `Not performed`.

### Stage B — create real owned fixtures before any network check

The “Lantern” products and versions are invented; there is nothing real to download under those labels. Implement disposable training services yourself or select an authorized training application and document differences. Do not claim the original four findings were verified merely because another application has similar weaknesses.

Prerequisites: a hypervisor supporting your host CPU; supported guest OS images; staged tools; enough resources for the guests; restorable snapshots; disposable accounts; dummy data; and an actual scope record naming the operator, ownership, exact target allowlist, methods, time window, stop conditions and recovery steps.

Use the designed internal-only `portfolio-lab` network only after verifying it. Proposed assets are analyst A-01 `10.77.0.10`, app A-02 `.20`, files A-03 `.30`, worker A-04 `.40`. Addresses are proposed, not observed. If unsuitable, record a revised allowlist and substitute actual lab addresses in all commands. Do not scan a subnet. The assessment source and hypervisor are not targets.

Build and record: app service on 443 and administration on 8443; archive on 443 with only the planted `training-backup.txt`; worker dummy notes owned by `labsvc`; and your actual diagnostics route. For HTTPS, stage a lab CA and certificates matching the chosen lab hostnames. Use only fictional record markers. These services must exist before the examples below make sense.

In each Linux guest, inspect these locally:

```bash
ip -brief address
ip route show
ip -6 route show
sysctl net.ipv4.ip_forward net.ipv6.conf.all.forwarding
```

Expected design: only the internal lab NIC plus loopback, no IPv4/IPv6 default route, and forwarding disabled. Also inspect hypervisor settings and guest firewall rules; route output alone is insufficient. Verify no NAT, bridge, shared folders, host access or secondary NIC. Do not test isolation by probing public/home/work systems. If isolation fails, disconnect the guest and resolve it before testing.

### Stage C — bounded discovery and benign observations

The following commands are conditional examples for the **actually built and authorized** lab. Run from the Linux analyst guest, never from your host or against public systems. Stage Nmap and curl beforehand. Save versions with `nmap --version` and `curl --version`; create a new evidence folder in that guest. Set `LAB_EVIDENCE` to that folder, for example:

```bash
umask 077
LAB_EVIDENCE=$(mktemp -d /tmp/portfolio-va.XXXXXX)
```

If your actual target allowlist matches the design, check only the named ports:

```bash
nmap -sT -Pn -n --max-retries 1 --host-timeout 30s -p 22,443,8443 -oA "$LAB_EVIDENCE/app-ports" 10.77.0.20
nmap -sT -Pn -n --max-retries 1 --host-timeout 30s -p 22,443 -oA "$LAB_EVIDENCE/files-ports" 10.77.0.30
nmap -sT -Pn -n --max-retries 1 --host-timeout 30s -p 22 -oA "$LAB_EVIDENCE/worker-ports" 10.77.0.40
```

These are limited TCP connection checks without vulnerability scripts, exploitation or broad discovery. No sudo is required. Record actual open/closed/filtered results; the inventory's ports are expectations, not guaranteed results. A timeout makes coverage incomplete. An open port is not proof of a vulnerability.

Use a trusted lab CA at the recorded path, and adapt routes to your actual fixtures. The names below are local labels; `--resolve` pins each request to the approved IP, and `--noproxy '*'` avoids a configured proxy. Do not use redirects or bypass certificate verification to hide TLS errors.

```bash
curl --noproxy '*' --connect-timeout 3 --max-time 10 --cacert ./lab-ca.pem --resolve app-01.lab:8443:10.77.0.20 -D "$LAB_EVIDENCE/admin-headers.txt" -o "$LAB_EVIDENCE/admin-body.txt" https://app-01.lab:8443/
curl --noproxy '*' --connect-timeout 3 --max-time 10 --cacert ./lab-ca.pem --resolve files-01.lab:443:10.77.0.30 -D "$LAB_EVIDENCE/archive-headers.txt" -o "$LAB_EVIDENCE/archive-body.txt" https://files-01.lab/training-backup.txt
curl --noproxy '*' --connect-timeout 3 --max-time 10 --cacert ./lab-ca.pem --resolve app-01.lab:443:10.77.0.20 -D "$LAB_EVIDENCE/diagnostics-headers.txt" -o "$LAB_EVIDENCE/diagnostics-body.txt" https://app-01.lab/diagnostics
```

Make at most one request per shown route per test stage. Check exit codes and inspect the saved status, headers and dummy content. curl success means transfer success, not authorization success; a denial can still be exit `0`. A redirect is evidence to investigate, not permission to follow an unknown destination. A login page returned with HTTP 200 is not administrative access.

For VA-001, additionally review effective authentication/role configuration and, only if implemented, perform a harmless disposable administrative operation. Do not stop the application or delete data to demonstrate impact. For VA-002, confirm the direct object returns exactly the planted markers, not merely a listing. For VA-004, determine whether actual non-public details are exposed rather than treating a generic public version string as confirmation.

On worker-01 locally, if the dummy fixture exists:

```bash
stat -c '%U %G %a %n' /srv/lantern/demo-notes.txt
namei -l /srv/lantern/demo-notes.txt
getfacl -p /srv/lantern /srv/lantern/demo-notes.txt
```

Expected *only for an intentionally matching fixture*: owner/group `labsvc`, mode `666`, traversable parents and effective ordinary-user access. Record what actually appears. In a disposable ordinary-account terminal, check `test -r /srv/lantern/demo-notes.txt` and `test -w /srv/lantern/demo-notes.txt`, then print `$?` immediately after each. Exit `0` means permission is granted; `1` means it is not. A permission predicate is supporting evidence, not a complete runtime access test: validate reading and a reversible append on a separate dummy copy with matching owner/mode/ACLs, then restore the dummy copy. Keep content and credentials out of public captures.

### Stage D — remediation and retest

Snapshot first. Use Project 08's `04-remediation-and-validation.md` as the acceptance plan. Apply one recorded configuration change at a time to the actual fixture. Never paste generic firewall/authentication changes into an unidentified service.

| Finding | Required rejection evidence | Required positive control |
| --- | --- | --- |
| VA-001 | Anonymous and ordinary-user administration denied; other lab guests blocked from 8443 | Authorized admin harmless operation and normal 443 workflow succeed |
| VA-002 | Anonymous and unauthorized direct object reads denied; listing disabled | Approved reader retrieves exact dummy backup; a newly seeded object inherits restrictions |
| VA-003 | Ordinary user cannot read or modify; parent traversal and ACLs checked | `labsvc` can read/write; normal creation yields appropriately protected new notes |
| VA-004 | Anonymous/ordinary diagnostics and benign error path expose no internal details | Normal app works and authorized operators retain necessary restricted diagnostics |

For the matching Linux notes fixture only, after recording ownership/ACLs and snapshotting, the planned mode correction is `sudo chmod 0600 /srv/lantern/demo-notes.txt`, executed in worker-01's console. Confirm ownership is actually `labsvc`; review and remove unintended ACL grants using the recorded ACL configuration. chmod alone is not complete validation. Keep a recovery console; use service-specific instructions for other fixes.

Repeat the exact benign before-checks with new `after-` output filenames, and perform both rejection and positive tests. A 401/403 or deliberately non-disclosing response may be an appropriate rejection; a 200 response requires content/operation review. Network containment alone does not fix missing authentication. A failed or incomplete retest leaves the finding open. Rollback that restores a weakness must occur with the service isolated.

Publish separate actual-lab records, for example `projects/08-vulnerability-assessment-lab/local-follow-up/`, only after review. Map new observed evidence to scenario IDs where supported; revise impact/scoring for differences. Do not overwrite invented evidence with actual results or invent a CVE for a fictional fixture.

## 7. Evidence to retain and troubleshooting

For each milestone retain: operator, date/time/timezone, environment/tool versions, source commit and modified files, exact commands/options, exit codes, raw private evidence, sanitized public copies, expected vs observed results, limitations and your own explanation. For the offline inputs/code, optionally record hashes on Mac with `shasum -a 256 FILE` (Linux: `sha256sum FILE`) to identify exact bytes. Hashes identify files; they do not prove an investigation was authentic.

A compact run record:

```markdown
## Local run — [actual date/time/timezone]
Operator: [actual operator]
Environment / Python or tool version: [observed]
Repository commit / modifications: [observed]
Scope and input: [actual files or authorized lab targets]
Command and exit code: [recorded]
Expected: [reference]
Observed: [result with evidence link]
Interpretation and limitation: [your explanation]
SIEM installed / scan performed / fix applied / retest: [only facts]
```

| Symptom | Check and resolution |
| --- | --- |
| `python3` missing or unsupported behavior | Check executable/version; install official Python, then rerun both suites |
| File not found | `pwd`; return to repo root; verify exact filenames and case |
| Project 07 validator error | Restore the complete sibling Project 06 directory; do not modify imports merely to mask missing files |
| Zero tests / import failure | Use the project-specific discovery paths shown; inspect full stderr; expect 12 and 10 tests |
| Report empty or JSON decode fails | Check exit code/stderr and input encoding; do not treat an empty report as no alerts |
| Project 06 has 2 invalid lines | Expected for the supplied fixture; a different count requires input comparison |
| JSON differs from example | Check commit, local edits, selected fixture and threshold; compare parsed objects, not formatting |
| Output accidentally redirected to input | Stop; recover the tracked fixture from an untouched checkout after preserving other work; use separate output paths |
| No SIEM match | Check historical event-time range, UTC parsing, field mapping, ingestion count and rule grouping before changing thresholds |
| Extra SIEM alerts | Check repeat imports, deduplication, overlapping windows and product scheduling; retain discrepancies |
| VM cannot reach another lab guest | Check internal-switch membership, actual guest IP, listening service and guest firewall locally; do not add NAT/bridge |
| curl certificate failure / timeout | Check staged CA, certificate name, approved IP and service; fix the fixture instead of disabling verification |
| Port open but finding unproven | Inspect authorization and benign behavior; label discovery separately from confirmed configuration weakness |
| chmod seems ineffective | Check ACLs, ownership, parent traversal, test-account privileges and whether you changed the intended guest/file |
| Positive control fails after a fix | Keep finding open; inspect dependency/configuration and use the isolated rollback plan |

Before publishing, review input, reports, screenshots and staged diff for secrets, tokens, private hostnames, personal identifiers and employer data. Screenshots should show useful commands/results without unrelated account details. Add a sanitized evidence link only after the run exists; never relabel the committed example JSON as your own capture.

## 8. Concise root README update (ready to paste)

Keep the existing project disclaimers. Replace the current `## Next development goals` section (through the evidence-checklist sentence, before `## Scope and ethics`) with the following. If this guide is added to the repo, place it at `docs/local-execution-guide.md` so its relative link works. This update claims no personal execution.

```markdown
## Execution status and next milestones

- **Completed offline artifacts:** Projects 06–07 contain runnable Python,
  fictional inputs, automated tests and example output. Project 07 is an
  offline SIEM-style exercise, not a deployed SIEM. Project 08 is a fictional
  tabletop assessment; its findings and validation remain simulated.
- **Owner-local reproduction pending:** Run Projects 06–07 and publish dated,
  sanitized test logs, generated reports, environment details and explanations.
  Preparation-environment tests and committed examples do not establish that
  I ran these projects locally.
- **Hands-on lab evidence pending:** Deploy an isolated SIEM and reproduce
  Project 07's rule with ingestion, query and alert evidence. Separately build
  an owned isolated assessment lab, record observations, apply fixes and retest;
  Project 08's planned scanning, remediation and validation are not completed.

Follow the [local execution guide](docs/local-execution-guide.md) and
[evidence checklist](docs/evidence-checklist.md). Update a milestone only after
its dated evidence exists; this portfolio does not claim production SOC work.
```

After your actual offline run, replace only the owner-local bullet with a factual date, environment, observed test counts/output comparison and link to your sanitized run record. Do not mark SIEM or assessment work complete at that point. For an actual lab, document coverage and unresolved findings; completion of testing is distinct from closure of every finding.

The root README uses the status block above; future changes must be supported by recorded evidence. The generic status sentence in `docs/evidence-checklist.md` could later be refreshed to distinguish Projects 01–05 reconstructed write-ups, Projects 06–07 executable offline artifacts, and Project 08's fictional tabletop records.

## Sources reviewed

Current main was read on 10 October 2026. Reviewed root README, evidence checklist, all Project 06–08 files, executable code, fixtures and tests. The guide's commands use those exact paths.

- [Root README](https://github.com/Guri4150/Cybersecurity-portfolio/blob/main/README.md)
- [Project 06](https://github.com/Guri4150/Cybersecurity-portfolio/tree/main/projects/06-auth-log-parser)
- [Project 07](https://github.com/Guri4150/Cybersecurity-portfolio/tree/main/projects/07-siem-alert-investigation), especially `detection.md` and `validation.md`
- [Project 08](https://github.com/Guri4150/Cybersecurity-portfolio/tree/main/projects/08-vulnerability-assessment-lab), especially scope and remediation/validation plans
- User-supplied provenance commits: [parser af98081](https://github.com/Guri4150/Cybersecurity-portfolio/commit/af980819f19c0a3abcdd64067185083bf4acf596), [correlation 0810c40](https://github.com/Guri4150/Cybersecurity-portfolio/commit/0810c406d9a3c4db8394e38c6c9a857bea8f091b), [tabletop 78b0834](https://github.com/Guri4150/Cybersecurity-portfolio/commit/78b083456a2d5c521de0647cee8576e7cda72223).
