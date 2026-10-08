# Gurdit Singh | Cybersecurity Portfolio

**Aspiring SOC Analyst · Junior Cybersecurity Analyst**  
Mohali, Punjab, India · [GitHub: Guri4150](https://github.com/Guri4150)

I am transitioning into cybersecurity after operational work in Canada and international study in business and hospitality. I completed the **Google Cybersecurity Professional Certificate in September 2026**, with a focus on security operations, Linux, SQL, network traffic analysis, and incident response.

I enjoy investigating security problems, documenting findings clearly, and connecting technical risks to business impact. I am seeking an entry-level opportunity in security operations or cybersecurity analysis.

## Featured learning projects

Projects 01–05 reconstruct training exercises and document example investigation methods. They are educational work, not production security engagements. Original screenshots, packet captures, and lab transcripts are not included; examples and expected results are labeled accordingly.

Projects 06 and 07 include runnable Python, fictional input, automated tests, and example output. Project 07 is an offline SIEM-style correlation exercise; an actual SIEM deployment remains a future development goal. These projects do not claim production security experience.

Project 08 is a fictional vulnerability-assessment tabletop case study. Its lab design, evidence and findings are invented; scanning, remediation and validation have not been performed.

| Project | What it demonstrates | Tools / concepts |
|---|---|---|
| [Linux permissions and access control](projects/01-linux-permissions.md) | Reviewing access and applying least privilege | Bash, ls, chmod |
| [SQL for security investigations](projects/02-sql-investigations.md) | Filtering login events and identifying relevant devices | SQL, WHERE, JOIN |
| [Network traffic investigation](projects/03-network-traffic.md) | A repeatable DNS and HTTP analysis workflow | Wireshark, tcpdump |
| [File integrity verification](projects/04-file-integrity.md) | Comparing files using cryptographic hashes | Linux, SHA-256 |
| [SOC incident triage case study](projects/05-incident-triage.md) | Evaluating alerts, preserving evidence, and documenting decisions | Incident response, risk, escalation |
| [Python authentication-log parser](projects/06-auth-log-parser/README.md) | Validating fictional logs and summarizing authentication outcomes | Python, JSONL, unittest |
| [Synthetic SIEM-style alert investigation](projects/07-siem-alert-investigation/README.md) | Time-window correlation, alert triage, severity and response reasoning | Python, detection logic, SOC documentation |
| [Fictional vulnerability assessment](projects/08-vulnerability-assessment-lab/README.md) | Lab scope, asset inventory, sample findings, prioritization and remediation planning | CVSS v3.1-style scoring, least privilege, validation criteria |

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

My SIEM and vulnerability-management knowledge is currently based on training. I am developing hands-on experience and do not claim production SOC experience.

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

## Next development goals

- Add sanitized evidence from repeatable home-lab exercises.
- Run and explain the synthetic parser and alert-correlation projects locally.
- Deploy an isolated SIEM lab, ingest fictional events, reproduce project 07's rule, and document the resulting alert with lab evidence.
- Complete a vulnerability assessment in an isolated, authorized lab.

See the [evidence checklist](docs/evidence-checklist.md) for how projects will be strengthened.

## Scope and ethics

All exercises are intended for owned or explicitly authorized lab systems. Public artifacts should contain only synthetic or sanitized data. No customer data, credentials, or confidential employer information belongs in this repository.
