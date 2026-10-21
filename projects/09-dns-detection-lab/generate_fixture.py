#!/usr/bin/env python3
"""Print deterministic, purely fictional DNS JSONL to standard output."""
from datetime import datetime, timedelta, timezone
import json

START = datetime(2026, 10, 15, 8, 30, tzinfo=timezone.utc)


def emit(event_id, second, ip, name, record_type, message="query"):
    obj = {
        "event_id": event_id,
        "timestamp": (START + timedelta(seconds=second)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "client_ip": ip,
        "query_name": name,
        "query_type": record_type,
        "message": message,
    }
    print(json.dumps(obj, sort_keys=True))


def main():
    # ws-07: exactly 480 DNS queries in five minutes, 450 unique TXT + 30 A.
    for i in range(450):
        emit("W07-TXT-%04d" % i, i % 300, "10.20.5.7", "q%04d.sync.example" % i, "TXT")
    for i in range(30):
        emit("W07-A-%04d" % i, i * 10, "10.20.5.7", "portal.example", "A")
    # Another client has high TXT volume but only one name: no alert.
    for i in range(110):
        emit("W08-TXT-%04d" % i, i % 300, "10.20.5.8", "metadata.sync.example", "TXT")
    # Low-volume TXT names on a third client: no alert.
    for i in range(35):
        emit("W09-TXT-%04d" % i, i, "10.20.5.9", "m%04d.sync.example" % i, "TXT")
    for i in range(2):
        emit("DNS-RSP-%04d" % i, i, "10.20.5.7", "q%04d.sync.example" % i, "TXT", "response")
    # Deliberately duplicated ID and content: detector must not count it twice.
    emit("W07-TXT-0000", 0, "10.20.5.7", "q0000.sync.example", "TXT")


if __name__ == "__main__":
    main()
