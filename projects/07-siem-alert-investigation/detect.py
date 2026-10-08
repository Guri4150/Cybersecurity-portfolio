"""Offline educational correlation using project 06's input validator."""

import argparse
from datetime import datetime
import importlib.util
import json
from pathlib import Path
import sys

PARSER = Path(__file__).resolve().parents[1] / "06-auth-log-parser/auth_parser.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("portfolio_auth_parser", PARSER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_event


def investigate(lines, parse_event):
    events = []
    seen = set()
    total = blank = invalid = duplicates = 0
    for number, line in enumerate(lines, 1):
        total += 1
        if not line.strip():
            blank += 1
            continue
        try:
            event = parse_event(line)
        except (ValueError, RecursionError):
            invalid += 1
            continue
        key = tuple(event[k] for k in ("timestamp", "username", "source_ip", "status"))
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        events.append((datetime.strptime(event["timestamp"], "%Y-%m-%dT%H:%M:%SZ"),
                       number, event))
    events.sort(key=lambda row: (row[0], row[1]))
    alerts = []
    for time, number, event in events:
        if event["status"] != "success":
            continue
        failures = [
            (t, n, e) for t, n, e in events
            if e["status"] == "failure"
            and e["username"] == event["username"]
            and e["source_ip"] == event["source_ip"]
            and 0 < (time - t).total_seconds() <= 300
        ]
        if len(failures) >= 3:
            alerts.append({
                "alert_id": f"SYN-AUTH-001-L{number:03d}",
                "rule_id": "SYN-AUTH-001",
                "severity": "medium",
                "success_time": event["timestamp"],
                "username": event["username"],
                "source_ip": event["source_ip"],
                "failure_count": len(failures),
                "failure_lines": [n for _, n, _ in failures],
                "success_line": number,
                "assessment": "Review required; compromise not established",
            })
    return {
        "synthetic": True,
        "total_lines": total,
        "blank_lines": blank,
        "invalid_lines": invalid,
        "duplicate_events": duplicates,
        "unique_valid_events": len(events),
        "window_seconds": 300,
        "minimum_failures": 3,
        "alerts": alerts,
    }


def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("logfile")
    args = cli.parse_args(argv)
    try:
        validator = load_validator()
        with open(args.logfile, encoding="utf-8") as source:
            report = investigate(source, validator)
    except (OSError, UnicodeError, ImportError):
        print("Error: cannot load project 06 validator or read UTF-8 input.", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
