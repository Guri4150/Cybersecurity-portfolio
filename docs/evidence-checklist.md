# Project evidence checklist

Use this checklist before adding or describing a cybersecurity portfolio result. **Lab execution is not production SOC experience.** Every claim must name the performer, environment, data provenance, and limits of the evidence.

## Evidence categories

| Label | Meaning | Permitted claim |
| --- | --- | --- |
| **Owner-executed, screenshot-reviewed** | The portfolio owner ran commands locally; the assistant reviewed shared screenshots or owner-provided summaries. | "Ran on my Mac; screenshots show X." Do not claim an independent rerun or unpublished raw artifacts were checked. |
| **Assistant-executed on owner's Mac** | The assistant operated an authorized local lab on the owner's Mac. | "Assistant-operated Mac lab during guided practice; X checks passed." Do not imply independent owner execution. |
| **Assistant-guided/operated Splunk Cloud** | The assistant used the owner's authorized trial session and observed UI results. | "Assisted synthetic Splunk Cloud validation observed X." Do not claim production monitoring or independent deployment. |
| **Assistant Linux preparation** | Code or lab executed in the assistant's preparation environment. | "Assistant-environment test result"; do not relabel it as Mac execution. |
| **Synthetic or simulated tabletop** | Invented events, modeled findings, expected output or proposed actions without real execution. | "Fictional case study," "simulated finding," or "expected result," as appropriate. |

## Current project evidence — 23 October 2026

| Project | Verified or documented evidence | Boundaries / what is **not** established |
| --- | --- | --- |
| **01–05: foundational exercises** | Reconstructed educational workflows and example reasoning in the project write-ups. | Original course screenshots, packet captures and raw lab transcripts are not included. Do not claim independent execution of every example. |
| **06: authentication-log parser** | 12 Python tests passed on the owner's Mac on 15 October, as recorded from reviewed screenshots; example report comparison showed no differences. Separate assistant Linux preparation tests were recorded on 10 October. | Original owner screenshots and generated files are not committed; the numeric `diff` exit status was not separately recorded. Fictional inputs, not real accounts. |
| **07: synthetic authentication correlation** | 10 Python tests passed on the owner's Mac on 15 October, screenshot-reviewed. An assistant-operated Splunk Cloud trial run on 22 October ingested seven fictional events; threshold 3 produced one row, threshold 4 none, and a manual report was saved. | Splunk was checked against this fixture and threshold variation, not every Python boundary case. No scheduled Project 07 alert, real compromise, production SIEM, or independent owner-operated Splunk run. |
| **08: fictional vulnerability assessment + separate micro-lab** | Original four findings remain simulated and open. A separate assistant-operated Mac loopback HTTP lab on 22 October passed eight before/after checks, with a JSON execution record. | No real multi-asset assessment, no real backup exposure, and no closure of the original four findings. The lab fix is not a persistent production deployment. |
| **09: synthetic DNS detection** | Owner-Mac Python run on 21 October: screenshots directly support 10 tests passing and a comparison-success message; reported event/alert counts have a separately stated owner-summary basis. Assistant-operated Splunk Cloud trial observed 628 events, 627 unique IDs, one matching synthetic client and excluded controls; scheduled historical trigger entries were seen. | Owner raw Mac artifacts are not publicly attached. Splunk scheduled-job payloads were not exported; the replay alert was disabled after testing. No live capture, proven DNS tunneling/exfiltration or production detection. |

Source records:

- [Owner-Mac Projects 06–07 execution — 15 October](execution-evidence/2026-10-15-owner-mac/README.md)
- [Assistant Linux preparation — 10 October](execution-evidence/2026-10-10-assistant-linux/README.md)
- [Project 07 assistant-operated Splunk Cloud — 22 October](execution-evidence/2026-10-22-splunk-cloud/README.md)
- [Project 08 assistant-operated Mac micro-lab — 22 October](../projects/08-vulnerability-assessment-lab/hands-on/mac-execution-2026-10-22.md)
- [Project 09 owner-Mac record — 21 October](../projects/09-dns-detection-lab/mac-execution-2026-10-21.md)
- [Project 09 assisted Splunk Cloud observation record — 21 October](../projects/09-dns-detection-lab/splunk/evidence-2026-10-21.md)

## Checklist for future runs

- [ ] **Scope and authorization:** record the task, owned/authorized lab boundary, synthetic input source and whether the test touched any real system.
- [ ] **Performer and context:** state owner-executed, assistant-operated, or jointly guided; capture date/time with timezone, OS, tool versions and exact Git revision.
- [ ] **Commands and queries:** preserve the actual commands, SPL, configuration, thresholds and time range. Separate executed search text from untested alternatives.
- [ ] **Results:** record both passing and failing checks, counts, positive/negative controls and exact acceptance criteria. Distinguish observations from reference output and hypotheses.
- [ ] **Evidence strength:** say whether results come from screenshots, directly viewed UI, raw exported artifacts, logs or an owner's recollection. Record missing source artifacts and uncertain exit codes.
- [ ] **Analysis:** add the owner's own explanation of the signal, one plausible benign explanation, what remains unproven, and the practical security implication.
- [ ] **Remediation claims:** require a before/after record for the exact tested asset and control. Never close separate fictional findings because a narrow lab test passed.
- [ ] **Privacy and ethics:** inspect every artifact for usernames, local paths, tokens, credentials, private URLs, customer data and employer information; redact before publishing. Use only authorized synthetic or sanitized data.
- [ ] **Reproducibility:** provide a safe command sequence and expected results, without claiming a fresh run when only documentation was changed.
- [ ] **Resume/interviews:** match every bullet to its dated record. Describe skills demonstrated by educational labs without suggesting commercial SOC duties, confirmed attacks, independent Splunk deployment or full vulnerability assessments.

## Next evidence improvements

1. Independently rerun the Project 07 SPL against additional boundary fixtures and record both successes and mismatches.
2. Independently reproduce the Project 08 local micro-lab; keep it distinct from the still-pending broader assessment.
3. Preserve sanitized owner-executed test logs and generated JSON for Projects 06 and 09, plus exact revisions, if reviewed and safe to publish.
4. Write original analyst interpretations for the synthetic alerts, including alternative explanations, uncertainty and next investigative steps.
5. For future scheduled SIEM tests, save redacted scheduled-job result exports **before** disabling or cleaning up alerts, where authorized.

Do not publish secrets or live customer data. Update this checklist when new dated evidence is available; do not turn a plan or example into a completed milestone.
