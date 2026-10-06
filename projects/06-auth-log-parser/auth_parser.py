"""Summarize a small, fictional authentication log. Standard library only."""

import argparse
from collections import Counter
from datetime import datetime
import ipaddress
import json
import re
import sys


def parse_event(line):
    """Validate one JSON event; raise ValueError for unsupported records."""
    event = json.loads(line)
    fields = {"timestamp", "username", "source_ip", "status"}
    if not isinstance(event, dict) or set(event) != fields:
        raise ValueError("unexpected fields")
    if not all(isinstance(value, str) for value in event.values()):
        raise ValueError("fields must be strings")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", event["timestamp"]):
        raise ValueError("timestamp must use UTC YYYY-MM-DDTHH:MM:SSZ")
    datetime.strptime(event["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,32}", event["username"]):
        raise ValueError("unsupported username")
    event["source_ip"] = str(ipaddress.IPv4Address(event["source_ip"]))
    if event["status"] not in {"success", "failure"}:
        raise ValueError("unsupported status")
    return event


def summarize(lines, threshold=3):
    """Count valid events and failures per source IP across the entire input."""
    if isinstance(threshold, bool) or not isinstance(threshold, int) or threshold < 1:
        raise ValueError("threshold must be a positive integer")
    counts = Counter()
    failures = Counter()
    total = blank = invalid = 0
    for line in lines:
        total += 1
        if not line.strip():
            blank += 1
            continue
        try:
            event = parse_event(line)
        except (ValueError, RecursionError):
            # Never echo rejected records, which could contain sensitive text.
            invalid += 1
            continue
        counts[event["status"]] += 1
        if event["status"] == "failure":
            failures[event["source_ip"]] += 1
    return {
        "total_lines": total,
        "blank_lines": blank,
        "invalid_lines": invalid,
        "valid_events": counts["success"] + counts["failure"],
        "successes": counts["success"],
        "failures": counts["failure"],
        "failure_threshold": threshold,
        "flagged_sources": [
            {"source_ip": ip, "failures": count}
            for ip, count in sorted(failures.items())
            if count >= threshold
        ],
    }


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logfile", help="UTF-8 JSONL file to read")
    parser.add_argument("--threshold", type=positive_int, default=3,
                        help="minimum failures per source IP (default: 3)")
    args = parser.parse_args(argv)
    try:
        with open(args.logfile, encoding="utf-8") as logfile:
            report = summarize(logfile, args.threshold)
    except (OSError, UnicodeError):
        print("Error: cannot read input as a UTF-8 log file.", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
