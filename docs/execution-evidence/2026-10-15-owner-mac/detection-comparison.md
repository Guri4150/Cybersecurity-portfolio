# Same logs, different detection results

**Guided Mac practice — 15 October 2026.** Commands and outcomes below were reviewed in screenshots supplied by Gurdit Singh. This write-up was prepared with assistant support. All events are fictional. Original screenshots and raw output files are not attached.

[Execution environment and test evidence](README.md)

## Question

Why can an IP-based parser flag a source while an account-and-IP correlation rule produces no alert on the same file?

## Input evidence

Input: [Project 06 sample_auth.jsonl](../../../projects/06-auth-log-parser/sample_auth.jsonl).

| Line | Username | Source IP | Outcome |
|---|---|---|---|
| 1 | demo_owl | 192.0.2.10 | failure |
| 2 | demo_owl | 192.0.2.10 | failure |
| 3 | demo_fox | 192.0.2.10 | failure |
| 4 | demo_owl | 192.0.2.10 | success |
| 5 | demo_badger | 198.51.100.20 | success |
| 6 | demo_fox | 203.0.113.30 | failure |
| 7 | demo_fox | 203.0.113.30 | success |
| 8 | demo_badger | 999.0.0.1 | rejected: invalid IPv4 |
| 9 | — | — | rejected: malformed JSON |

Seven valid events remain: four failures and three successes. The invalid record on line 8 does not count as a valid failure.

## Reproduce the comparisons

Run from `projects/06-auth-log-parser`:

```bash
python3 auth_parser.py sample_auth.jsonl
python3 auth_parser.py sample_auth.jsonl --threshold 4
python3 ../07-siem-alert-investigation/detect.py sample_auth.jsonl
```

### Results observed on the owner's Mac

| Detector and setting | Grouping | Observed result | Explanation |
|---|---|---|---|
| Parser, threshold 3 | Source IP, whole file | 192.0.2.10 flagged with 3 failures | Lines 1–3 share the IP, across two usernames |
| Parser, threshold 4 | Source IP, whole file | Empty flagged_sources | No source reaches four failures |
| Correlation, minimum 3, window 300 seconds | Username + source IP, failures before success | Empty alerts | demo_owl has only two failures before its success; demo_fox has only one failure per source |

The correlation run also reported 9 total lines, 2 invalid lines, 7 unique valid events, 0 blank lines and 0 duplicate events.

These are comparisons on **Project 06's input**. Project 07's own `synthetic_auth.jsonl` is a different dataset and produced one Medium alert in the earlier run. Do not interchange their results.

## Trace a result to source lines

The owner displayed the file with:

```bash
cat -n sample_auth.jsonl
```

Then filtered the source and failures. The final literal-text command observed was:

```bash
grep -nF '"source_ip":"192.0.2.10"' sample_auth.jsonl |
  grep -F '"status":"failure"'
```

It returned original lines **1, 2 and 3**: two failures for demo_owl and one for demo_fox. Earlier filtering without the status condition returned lines 1–4, including the successful login.

- `-n` displays original line numbers.
- `-F` treats the pattern as literal text, including the dots in the IP.
- The pipe passes matching lines to the second filter.
- This exact text pattern relies on the sample's compact JSON formatting. Different spacing can prevent a match. Grep does not validate JSON; the Python parser does.

## Analysis and limitations

Changing a threshold changes the detection result without changing the underlying events. Increasing it can reduce alerts while missing activity worth investigating.

Grouping also changes the question being asked. Three failures for one IP are not necessarily three failures for one account. Multiple usernames may share a source IP.

A successful login does not reset the parser's failure count. The parser does not correlate timing or success; the second project explicitly applies a time-bounded correlation rule.

No alert means this rule's conditions were not met on the accepted records. It does not prove benign activity, particularly when some records were rejected. A flag also does not prove compromise: password mistakes or stale credentials are possible explanations to investigate.

## Practical next checks

For an authorized investigation, examine affected accounts, event timing, device/session context and subsequent actions. This fictional fixture lacks sufficient context to determine intent.

**Skills practised:** running Python CLIs, interpreting validation counters, comparing detection rules, tuning a threshold, reading JSONL, and tracing aggregate results with shell filters.

[Back to portfolio](../../../README.md)
