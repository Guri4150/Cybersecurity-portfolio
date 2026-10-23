# Gurdit Singh | Cybersecurity Portfolio

**Aspiring SOC Analyst · Junior Cybersecurity Analyst**  
Mohali, Punjab, India · [GitHub: Guri4150](https://github.com/Guri4150)

I am transitioning into cybersecurity after operational work in Canada and international study in business and hospitality. I completed the **Google Cybersecurity Professional Certificate in September 2026**, with a focus on security operations, Linux, SQL, network traffic analysis, and incident response.

I enjoy investigating security problems, documenting findings clearly, and connecting technical risks to business impact. I am seeking an entry-level opportunity in security operations or cybersecurity analysis.

## Featured learning projects

Projects 01–05 reconstruct training exercises and document example investigation methods. They are educational work, not production security engagements. Original screenshots, packet captures, and lab transcripts are not included; examples and expected results are labeled accordingly.

Projects 06 and 07 include runnable Python, fictional input, automated tests, and example output. Project 07 also includes assistant-operated Splunk Cloud validation: a 36-record fictional fixture produced four qualifying successes, and all 10 success-event diagnostics matched expected failure counts and ages. The [execution record](docs/execution-evidence/2026-10-23-splunk-boundaries/EXECUTION-RECORD.md) separates observed results from expectations and includes CSV exports, screenshots and executed SPL. These projects do not claim production security experience.

Project 08 retains its fictional vulnerability-assessment tabletop and adds a separate loopback backup-exposure lab. An assistant-operated Mac run passed eight before/after HTTP checks; the original four simulated findings remain open.

Project 09 combines a fictional DNS triage tabletop, Mac-tested Python detection, and an assisted Splunk Cloud trial lab. Synthetic ingestion, native search results and scheduled historical alert firing were observed; the replay alert was disabled after testing. The [dated evidence summary](projects/09-dns-detection-lab/splunk/evidence-2026-10-21.md) distinguishes observations from retained raw evidence. No live capture, Wireshark execution or production detection is claimed.

| Project | What it demonstrates | Tools / concepts |
|---|---|---|
| [Linux permissions and access control](projects/01-linux-permissions.md) | Reviewing access and applying least privilege | Bash, ls, chmod |
| [SQL for security investigations](projects/02-sql-investigations.md) | Filtering login events and identifying relevant devices | SQL, WHERE, JOIN |
| [Network traffic investigation](projects/03-network-traffic.md) | A repeatable DNS and HTTP analysis workflow | Wireshark, tcpdump |
| [File integrity verification](projects/04-file-integrity.md) | Comparing files using cryptographic hashes | Linux, SHA-256 |
| [SOC incident triage case study](projects/05-incident-triage.md) | Evaluating alerts, preserving evidence, and documenting decisions | Incident response, risk, escalation |
| [Python authentication-log parser](projects/06-auth-log-parser/README.md) | Validating fictional logs and summarizing authentication outcomes | Python, JSONL, unittest |
| [Synthetic SIEM-style alert investigation](projects/07-siem-alert-investigation/README.md) | Rolling five-minute correlation, boundary validation, evidence handling and alert triage | Python, Splunk Cloud, SPL, SOC documentation |
| [Fictional vulnerability assessment](projects/08-vulnerability-assessment-lab/README.md) | Lab scope, asset inventory, sample findings, prioritization and remediation planning | CVSS v3.1-style scoring, least privilege, validation criteria |
| [DNS detection lab and triage](projects/09-dns-detection-lab/README.md) | Mac-tested Python; assisted Splunk ingestion, SPL validation, negative controls and scheduled historical alert testing | DNS, Python, Splunk Cloud, SPL, evidence handling |

## Skills and current depth

| Area | Training and practice |
|---|---|
| Linux | File navigation, permissions, users and groups, text filtering |
| SQL | SELECT, filtering, sorting, and joins for investigation exercises |
| Networking | TCP/IP, DNS, HTTP/HTTPS; introductory Wireshark and tcpdump analysis |
| Security operations | SIEM concepts, alert triage, incident-response workflows, log analysis |
| Security fundamentals | CIA triad, least privilege, authentication, defense in depth, NIST CSF concepts |
| Cryptography | SHA-256 comparisons and introductory OpenSSL exercises |
| Python | Fundamentals; continuing to build scripting skills |

My SIEM practice includes assistant-guided Splunk Cloud labs using synthetic authentication and DNS data. Vulnerability-management practice also includes an assistant-operated local backup-route remediation lab. I do not claim production SOC experience.

## Education and certification

- **Google Cybersecurity Professional Certificate** — completed September 26, 2026; training began May 28, 2026.
- **Postgraduate Certificate, Global Business Management** — Conestoga College, Canada.
- **Postgraduate Certificate, Global Hospitality Management** — Conestoga College, Canada.
- **Bachelor's degree** — Chandigarh Group of Colleges, India.

## Transferable professional experience

**Sixt Car Rental, Canada — Vehicle Service Agent**  
July 2023–January 2024; May 2024–April 2025.

**Routes Car Rental, Canada — Vehicle Detailer / Rental Operations**  
November 2025–May 2026.

These roles developed my attention to detail, procedure adherence, discrepancy reporting, time management, and communication in multicultural teams. I bring those habits to security investigations and documentation.

## Execution status and next milestones

[Recorded offline verification — 10 October 2026](docs/execution-evidence/2026-10-10-assistant-linux/README.md):
12 parser tests and 10 correlation tests passed in the assistant's Linux
preparation environment; generated JSON matched both committed examples.
This is separate from my own local execution and the pending lab milestones.

- **Completed offline artifacts:** Projects 06–07 contain runnable Python,
  fictional inputs, automated tests and example output. Project 07 also has a
  separately recorded manual Splunk Cloud lab run. Project 08 retains a fictional
  tabletop assessment and adds the separately scoped executed micro-lab below.
- **Owner-local runs completed — 15 October 2026:** On my Mac with Python
  3.9.6, all 12 parser tests and 10 correlation tests passed. Generated reports
  matched the committed examples with no differences displayed by `diff`.
  See the [screenshot-reviewed execution record](docs/execution-evidence/2026-10-15-owner-mac/README.md)
  for commands, revision, results and evidence limitations. Original screenshots
  and generated report files are not included in that record; attaching reviewed
  raw artifacts and adding my own interpretation remain evidence improvements.
- **Project 09 Splunk Cloud trial lab completed — 21 October 2026 UTC:**
  verified 628 records / 627 unique IDs, one 450-query / 450-name match and
  two excluded control clients. Scheduled historical triggers were observed;
  the alert is disabled. See the [lab guide](projects/09-dns-detection-lab/splunk/README.md)
  for reusable searches, assistance disclosure and evidence limits.
- **Splunk Cloud lab completed — 22 October 2026:** An assistant-guided run
  ingested seven fictional Project 07 events. Threshold 3 returned one match;
  threshold 4 returned none; restoring 3 returned the original match. A report
  was saved, with no scheduled alert configured. See the [execution record and
  screenshot](docs/execution-evidence/2026-10-22-splunk-cloud/README.md).
- **Project 08 micro-lab completed — 22 October 2026:** An assistant-operated
  Mac run passed eight checks before and after disabling a fictional backup
  route. See the [Mac execution evidence](projects/08-vulnerability-assessment-lab/hands-on/mac-execution-2026-10-22.md).
  The original four tabletop findings remain simulated and open.
- **Project 07 Splunk boundary validation completed — 23 October 2026:**
  An assistant-operated run ingested 36 fictional events (35 unique tuples).
  All 10 success-event diagnostics matched expectations; threshold 3 returned
  four matches, threshold 4 returned none, and restoring 3 returned four.
  See the [execution record](docs/execution-evidence/2026-10-23-splunk-boundaries/EXECUTION-RECORD.md)
  and [repeatable run sheet](projects/07-siem-alert-investigation/splunk/boundary-validation/RUN-SHEET.md).
- **Further lab work:** Independently repeat Project 07's boundary run and the
  Project 08 micro-lab. The broader multi-asset assessment remains pending.

Follow the [local execution guide](docs/local-execution-guide.md) and
[evidence checklist](docs/evidence-checklist.md). Update a milestone only after
its dated evidence exists; this portfolio does not claim production SOC work.

## Scope and ethics

All exercises are intended for owned or explicitly authorized lab systems. Public artifacts should contain only synthetic or sanitized data. No customer data, credentials, or confidential employer information belongs in this repository.
