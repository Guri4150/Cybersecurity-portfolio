# Detection specification: SYN-AUTH-001

## Purpose

Identify a successful authentication preceded by at least three failures
for the same username and source IPv4 address in the previous five minutes.
This is a review signal for possible password guessing or account misuse;
it also matches ordinary password mistakes followed by a correct password.
Three is an illustrative lab threshold, not a production recommendation.

## Data contract and processing

Input is UTF-8 JSONL, one event per line, with exactly four string fields:
`timestamp` (UTC `YYYY-MM-DDTHH:MM:SSZ`), `username` (1–32 ASCII letters,
digits, underscores or hyphens), `source_ip` (IPv4), and `status`
(`failure` or `success`). Project 06's validator enforces this contract.

1. Count all input lines, including blank and invalid lines.
2. Skip invalid and blank records, exposing their counts without printing
   rejected text.
3. Deduplicate identical normalized four-field tuples across this input.
   Retain the first line reference.
4. Sort unique valid events by timestamp, then original line number.
5. Evaluate every success independently using the rule below.

For success S at time t, count failures F satisfying:

```text
F.username = S.username
AND F.source_ip = S.source_ip
AND t - 300 seconds <= F.timestamp < t
```

Emit one Medium alert per success if that count is at least three.
The lower boundary is inclusive; failures at the same second as the success
are excluded because the records do not establish their temporal order.
A prior success does not reset the count. Multiple later successes may emit
multiple alerts using overlapping failures; there is no incident grouping or
cooldown. The alert ID uses the success input line and is only local to this
file, not a global or persistent identifier.

This is a rule specification implemented in Python, not executable SPL, KQL,
Sigma, or another vendor query. Porting it requires preserving these semantics.

## Why the grouping matters

Source-only aggregation could combine failures for unrelated accounts behind
a shared address. This rule also requires username equality. That still cannot
identify a person: IPs can be shared, and a username does not prove who used it.
Because there is no destination field, do not combine exports from different
services or hosts. A future schema should group by service and asset too.

## Known tradeoffs

| Issue | Consequence / future improvement |
|---|---|
| Mistyped password, stale client password, shared IP | Possible false positives; check account owner, device, session, and baseline |
| Distributed attempts or success from a different IP | False negatives; add separate account-centric rules |
| Slow attempts or fewer than three failures | Missed by design; evaluate longer windows separately |
| Failed-only attempts | No alert; add a distinct failure-burst rule |
| Repeated identical events within one second | Deduplication can remove legitimate separate attempts; use stable source event IDs in a real pipeline |
| Clock skew or coarse timestamps | Incorrect correlation; validate source time synchronization |
| Malformed or missing logs | Incomplete evidence; monitor ingestion quality |
| Multiple input files/reruns | No persistent deduplication or suppression; may repeat alerts |
| Small trusted inputs only | All events are held in memory; nested scanning can take quadratic time |
| Existing JSON parser behavior | Duplicate JSON keys use the last value; no forensic authenticity guarantee |

No enrichment, geolocation, threat-intelligence lookup, live collection,
network activity, account modification, or automated blocking is implemented.
The absence of an alert does not prove that the input or account is safe.
