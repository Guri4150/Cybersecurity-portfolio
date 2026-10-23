# Project 07 — execution record (fill in after running)

**Status: NOT RUN. No Splunk observations have been entered.**

Do not copy expected values into observed fields. Use `NOT RUN`, `PASS`, `FAIL`, or `BLOCKED`; a PASS requires recorded observations and evidence. Keep failures and reruns as separate entries.

## Run identity

- Operator: ______
- Actual UTC start/end: ______ / ______
- Splunk product/version, environment and app: ______
- User display timezone: ______
- PR: https://github.com/Guri4150/Cybersecurity-portfolio/pull/5
- Reviewed commit: 5aa62c586cf59ef98f09ca2e064357d566655d6c
- Actual fixture revision and SHA-256: ______
- Actual index / source / host / sourcetype: ______
- Upload time, preview evidence and upload count: ______
- Picker and job time bounds: ______
- Accepted query, if any (baseline or UTC-explicit variant): ______
- Exact executed SPL directory / hashes, including scope edits: ______

## Observations

| Check | Expected | Observed (leave blank until run) | Verdict | SID / evidence |
|---|---|---|---|---|
| 01 raw scoped count | 36, one scope group | | NOT RUN | |
| 02 quality | 36 raw; all four error counts 0; epochs 1791363600–1791363901 | | NOT RUN | |
| 03 dedup | 35 unique, 25 failures, 10 successes | | NOT RUN | |
| 04 duplicate | One dup_check failure at 09:02Z, copies=2 | | NOT RUN | |
| 05 UTC-explicit probe | epoch 1791363600, delta 0 | | NOT RUN | |
| 05 baseline UTC probe | epoch 1791363600, delta 0 | | NOT RUN | |
| 06 baseline threshold 3 | Exact four rows from expected JSON | | NOT RUN | |
| 07 diagnostic | All 10 cases match execution-cases.csv expectations | | NOT RUN | |
| 08 baseline threshold 4 | 0 rows; completed job without error | | NOT RUN | |
| 06 threshold 3 restored | Same exact four rows | | NOT RUN | |
| 09 optional UTC variant | Exact four rows; separate execution identity | | NOT RUN | |
| Revised 07/08 if adopting UTC variant | 10 diagnostic rows / 0 threshold-four rows | | NOT RUN | |

Attach the completed `execution-cases.csv`, raw result exports and screenshots. Record each search invocation below; duplicate this section for every run or rerun.

## Individual search job

- Query filename / variant / hash: ______
- Exact executed SPL attachment: ______
- UTC start/end and SID: ______
- Actual scope and time bounds: ______
- Job completed? ______
- Actual result count: ______
- Warnings/errors (write “none observed” only after inspection): ______
- Result export / screenshot: ______
- Expected comparison and verdict: ______

## Deviations and retests

| Original SID | Actual mismatch / error | Suspected cause (label as hypothesis) | Change made | Retest SID and evidence | Outcome |
|---|---|---|---|---|---|
| | | | | | |

## Completion statement — fill only from evidence

- Final status: NOT RUN
- Accepted query revision: ______
- Observed results and evidence links: ______
- Failed or blocked checks: ______
- Checks not performed: ______
- Remaining limitations: synthetic small batch; other limits: ______
- Operator sign-off / UTC time: ______

Suggested wording after a completed run: “On [actual UTC date], [operator] executed [exact query revision] against [fixture hash] in [environment]. Observed [actual results], supported by [evidence links]. [Checks] passed; [deviations/unperformed checks] remain. This validates only the documented synthetic cases.”

Until then retain: “Boundary-validation preparation complete; Splunk execution pending.”
