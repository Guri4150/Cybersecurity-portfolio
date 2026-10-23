# Project 07 — interview practice

## About 60 seconds

> My Project 07 explores how repeated login failures followed by a success can
> become a useful investigation lead. It uses fictional authentication logs,
> an offline Python detector and an assisted Splunk Cloud lab.
>
> The rule checks each success for at least three unique failures from the same
> account and source IP in the preceding five minutes. Exactly 300 seconds
> earlier counts; a failure at the same timestamp does not.
>
> The assistant operated the Splunk searches in my authorized trial. The
> 36-record fixture reduced to 35 unique events, and all ten success diagnostics
> matched the expected counts and ages. Threshold three returned four matches;
> threshold four returned none. Restoring three brought back the same four.
>
> The evidence includes exported results, screenshots and exact queries, with
> expectations kept separate from observations. This validates the supplied
> synthetic cases. A match is an investigation lead, not proof of compromise.

Practice this in your own words after reviewing the query and evidence.
Do not describe the assisted Splunk execution as an independent run.

## Questions to prepare for

**Why a rolling window?** Each success has its own five-minute lookback.
Fixed clock buckets could separate a failure and success that are only seconds
apart. The interval is `t - 300 <= failure_time < t`.

**What makes an event unique?** This fixture deduplicates the tuple of timestamp,
username, source IP and status. One duplicate raw record is removed. Without
an event ID, two genuinely distinct events sharing those fields could be
collapsed; that is a limitation of this schema.

**What did the boundary cases establish?** The observed diagnostics include
age 300 and exclude ages 301 and zero. Other cases check account/IP isolation,
duplicates, unsorted input, only two failures and multiple successes. A success
does not reset the failure history; each success is evaluated separately.

**Why raise the threshold?** Threshold four is a negative control for this
fixture. Zero results, followed by the original four when restoring threshold
three, checks that the observed output responds to the configured threshold.

**Does an alert prove an attack?** No. Legitimate retries can also match.
An investigation would seek authorized context such as user confirmation,
MFA outcomes, device and session details, and related activity. Those findings
were not collected in this synthetic exercise.

**What did you execute yourself?** The repository records an owner-local Python
run on 15 October with ten correlation tests passing. The 23 October Splunk
boundary run was assistant-operated after owner login. An independent owner
Splunk rerun remains a next step.

**What would you improve?** Independently repeat the run and explain each result;
then test richer event identity, timestamp handling and larger datasets before
considering operational use. This small fixture does not establish production
performance or live detection coverage.

## Evidence to open during a walkthrough

- [Detection specification](detection.md)
- [Candidate SPL](splunk/boundary-validation/06-candidate-threshold3.spl)
- [Observed execution record](../../docs/execution-evidence/2026-10-23-splunk-boundaries/EXECUTION-RECORD.md)
- [Run sheet](splunk/boundary-validation/RUN-SHEET.md)
- [Owner-local Python record](../../docs/execution-evidence/2026-10-15-owner-mac/README.md)
