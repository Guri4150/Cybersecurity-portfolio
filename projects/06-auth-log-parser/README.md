# Python authentication-log parser

## Objective and scope

A beginner-sized educational Python project: read synthetic authentication
events, validate records, summarize successes and failures, and identify source
IPs meeting a configurable failure threshold. This demonstrates JSON parsing,
validation, counters, command-line arguments, error handling, and automated tests.
It is not evidence of production SOC experience or a confirmed attack detector.

All input was invented for this exercise. No system was accessed or attacked;
the script only reads a user-selected local file and prints a report. It makes
no network requests, changes no accounts, and takes no blocking action.

## Files

Place this directory at `projects/06-auth-log-parser/` in the portfolio:

```text
projects/06-auth-log-parser/
    README.md
    auth_parser.py
    sample_auth.jsonl
    example_output.json
    test_auth_parser.py
```

No third-party dependencies or installation step are needed. Tested with
Python 3.12.14 on Linux on October 6, 2026 in the project preparation environment.
This is an observed test run, not a claim that the portfolio owner ran it locally.

## Input format

UTF-8 JSON Lines: one JSON object per line, with exactly four string fields:

| Field | Accepted format |
|---|---|
| `timestamp` | Valid UTC date and time, exactly `YYYY-MM-DDTHH:MM:SSZ` |
| `username` | 1–32 ASCII letters, digits, underscores, or hyphens |
| `source_ip` | Valid IPv4 address |
| `status` | Exactly `success` or `failure` |

Blank lines are counted separately. Malformed JSON, missing or extra fields,
wrong types, invalid dates/IPs, and unsupported values count as invalid lines;
processing continues. Rejected contents are never printed. The supplied file
has nine lines, including an intentionally invalid IP and a non-JSON record.
The demo usernames are fictional and the valid addresses use documentation ranges.

## Usage

From the repository root:

```bash
cd projects/06-auth-log-parser
python3 auth_parser.py sample_auth.jsonl
python3 auth_parser.py sample_auth.jsonl --threshold 4
python3 -m unittest discover -s . -p 'test_*.py' -v
```

On Windows, substitute `py -3` for `python3` if needed.
To save a report, use a new output filename:

```bash
python3 auth_parser.py sample_auth.jsonl > report.json
```

Do not redirect output to the input filename: shell redirection would overwrite
the input before the parser reads it.

Exit codes: `0` means the file was processed (even if it contained invalid lines);
`1` means the file could not be read or decoded as UTF-8; `2` means invalid CLI
arguments. Always check `invalid_lines` and `valid_events` before interpreting
results. An empty or entirely invalid file produces no flagged sources, but
does not establish that authentication activity is safe.

## Observed example output

The default command produced exactly the following, also stored in
`example_output.json` and checked by an automated CLI test:

```json
{
  "total_lines": 9,
  "blank_lines": 0,
  "invalid_lines": 2,
  "valid_events": 7,
  "successes": 3,
  "failures": 4,
  "failure_threshold": 3,
  "flagged_sources": [
    {
      "source_ip": "192.0.2.10",
      "failures": 3
    }
  ]
}
```

Interpretation: three failures from `192.0.2.10` meet the default threshold.
That source also has a successful login in the fictional input. The report
does not correlate that success or declare compromise. A real authorized
investigation would review timing, affected accounts, and additional evidence.
At threshold `4`, the sample produces an empty `flagged_sources` list.

## How the code works

1. `parse_event` decodes and validates one line.
2. `summarize` counts valid outcomes and failures grouped by source IP.
3. Sources with failures **greater than or equal to** the threshold appear in
   the report, sorted lexicographically by IP string for stable output.
4. `main` handles arguments, reads the file, and prints JSON.

The threshold applies to the **entire file**, across all usernames. A success
does not reset the failure count. Timestamps are validated, but not used for
time windows or event ordering.

## Test evidence

Observed result: **12 tests passed** using Python 3.12.14. The suite covers
valid and invalid records, empty/blank input, threshold boundaries, aggregation
across users and sources, success handling, malformed-line accounting, invalid
thresholds, exact sample CLI output, missing files, and invalid UTF-8 input.
All test data is fictional. Temporary files are removed by the test suite.

## Limitations

- Only this custom JSONL schema is supported, not raw Linux auth.log,
  Windows events, SIEM exports, IPv6, or arbitrary timezone formats.
- Repeated failures are a review signal, not proof of brute force. Shared IPs,
  ordinary mistakes, and long collection periods can cause false positives;
  distributed attempts below the threshold can be missed.
- No time windows, success-after-failure correlation, deduplication, enrichment,
  geolocation, live monitoring, alert delivery, or automated response.
- Duplicate input events count again. Python's JSON decoder uses the last
  value for duplicate object keys; this is not a forensic validation tool.
- Reads one line at a time, but stores a counter per distinct failing IP;
  line length and file size are not bounded. Use small trusted lab files.
- Validation cannot determine whether data is fictional or safe to publish.
  Reports may include source IPs, so reports require review too.

## Safe-data guidance

Keep public examples wholly fictional. Use invented usernames and documentation
IPv4 ranges (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`). Do not paste
real authentication logs into this repository or include credentials, tokens,
email addresses, private hostnames, customer details, or employer information.
Do not assume replacing one name makes a real log anonymous.

Use only owned or explicitly authorized lab systems for future exercises.
Before committing anything, inspect the input, generated reports, screenshots,
and staged Git changes. This project needs no real data, elevated permissions,
network access, scanning, or login attempts.

## Suggested portfolio README edits

Add this row to the root README's featured-projects table:

```markdown
| [Python authentication-log parser](projects/06-auth-log-parser/README.md) | Validating synthetic logs, summarizing outcomes, and testing a CLI | Python, JSONL, unittest |
```

Keep the existing Python skills description modest. After reviewing and running
the project yourself, replace the original parser development goal with:

```markdown
- Extend the synthetic authentication-log parser with a tested time-window rule.
```

The existing five write-ups and ethics note can remain. These edits are supplied
for review; no changes have been pushed to GitHub.
