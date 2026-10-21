#!/usr/bin/env python3
"""Offline DNS TXT burst detector for *synthetic* JSONL records only.

No live collection, packets, network calls, or privileged operations.
"""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import ipaddress
import json
from pathlib import Path
import sys

RULE_ID = "SYN-DNS-TXT-BURST-001"
DOMAIN = "sync.example"
WINDOW_SECONDS = 300
MIN_TXT = 100
MIN_DISTINCT = 80


def parse_event(line):
    obj = json.loads(line)
    if not isinstance(obj, dict):
        raise ValueError("expected object")
    for name in ("event_id", "timestamp", "client_ip", "query_name", "query_type", "message"):
        if not isinstance(obj.get(name), str) or not obj[name].strip():
            raise ValueError("missing or invalid " + name)
    ts = datetime.fromisoformat(obj["timestamp"].replace("Z", "+00:00"))
    if ts.tzinfo is None or ts.utcoffset() is None:
        raise ValueError("timestamp must include timezone")
    ipaddress.ip_address(obj["client_ip"])
    kind = obj["message"].lower()
    if kind not in ("query", "response"):
        raise ValueError("message must be query or response")
    return {
        "event_id": obj["event_id"],
        "timestamp": ts.astimezone(timezone.utc),
        "client_ip": obj["client_ip"],
        "query_name": obj["query_name"].lower().rstrip("."),
        "query_type": obj["query_type"].upper(),
        "message": kind,
    }


def analyze(lines):
    counters = {
        "total_lines": 0,
        "invalid_lines": 0,
        "duplicate_event_ids": 0,
        "unique_events": 0,
        "responses_skipped": 0,
        "eligible_txt_queries": 0,
    }
    seen = set()
    grouped = defaultdict(list)
    for line in lines:
        counters["total_lines"] += 1
        try:
            ev = parse_event(line)
        except (ValueError, TypeError, KeyError, json.JSONDecodeError, OverflowError):
            counters["invalid_lines"] += 1
            continue
        if ev["event_id"] in seen:
            counters["duplicate_event_ids"] += 1
            continue
        seen.add(ev["event_id"])
        counters["unique_events"] += 1
        if ev["message"] == "response":
            counters["responses_skipped"] += 1
            continue
        name = ev["query_name"]
        if ev["query_type"] != "TXT" or not (name == DOMAIN or name.endswith("." + DOMAIN)):
            continue
        counters["eligible_txt_queries"] += 1
        epoch_bucket = int(ev["timestamp"].timestamp()) // WINDOW_SECONDS * WINDOW_SECONDS
        grouped[(ev["client_ip"], epoch_bucket)].append(ev)

    alerts = []
    for (ip, bucket), events in sorted(grouped.items()):
        distinct = len({ev["query_name"] for ev in events})
        if len(events) < MIN_TXT or distinct < MIN_DISTINCT:
            continue
        start = datetime.fromtimestamp(bucket, tz=timezone.utc)
        end = datetime.fromtimestamp(bucket + WINDOW_SECONDS, tz=timezone.utc)
        earliest = sorted(events, key=lambda ev: (ev["timestamp"], ev["event_id"]))
        alerts.append({
            "rule_id": RULE_ID,
            "severity": "Medium",
            "client_ip": ip,
            "domain": DOMAIN,
            "window_start_utc": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "window_end_utc_exclusive": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "txt_query_count": len(events),
            "distinct_query_names": distinct,
            "sample_event_ids": [ev["event_id"] for ev in earliest[:3]],
            "assessment": "Suspicious burst; DNS tunneling and exfiltration unconfirmed",
        })
    return {"rule": {
        "id": RULE_ID,
        "window_seconds": WINDOW_SECONDS,
        "domain": DOMAIN,
        "minimum_txt_queries_inclusive": MIN_TXT,
        "minimum_distinct_names_inclusive": MIN_DISTINCT,
    }, "counters": counters, "alerts": alerts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", help="Path to a synthetic DNS JSONL file")
    args = parser.parse_args()
    try:
        with Path(args.jsonl).open(encoding="utf-8") as stream:
            output = analyze(stream)
    except OSError as exc:
        print("Cannot read input: " + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
