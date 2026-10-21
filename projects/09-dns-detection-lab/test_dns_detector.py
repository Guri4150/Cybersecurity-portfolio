"""Boundary and data-quality checks for the synthetic DNS rule."""
import importlib.util
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("dns_detector", Path(__file__).with_name("dns_detector.py"))
detector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(detector)


def row(i, *, ts="2026-10-15T08:30:00Z", ip="10.20.5.7", name=None,
        kind="TXT", message="query"):
    return json.dumps({"event_id": "ID-%04d" % i, "timestamp": ts,
                       "client_ip": ip, "query_name": name or "q%04d.sync.example" % i,
                       "query_type": kind, "message": message})


class DNSDetectionTests(unittest.TestCase):
    def test_alert_at_inclusive_thresholds(self):
        lines = [row(i, name="name%03d.sync.example" % (i % 80)) for i in range(100)]
        result = detector.analyze(lines)
        self.assertEqual(1, len(result["alerts"]))
        self.assertEqual(100, result["alerts"][0]["txt_query_count"])
        self.assertEqual(80, result["alerts"][0]["distinct_query_names"])

    def test_99_queries_do_not_alert(self):
        self.assertEqual([], detector.analyze([row(i) for i in range(99)])["alerts"])

    def test_79_distinct_names_do_not_alert(self):
        self.assertEqual([], detector.analyze([
            row(i, name="n%03d.sync.example" % (i % 79)) for i in range(120)
        ])["alerts"])

    def test_deduplication_by_event_id(self):
        lines = [row(i) for i in range(99)] + [row(0)]
        result = detector.analyze(lines)
        self.assertEqual(1, result["counters"]["duplicate_event_ids"])
        self.assertEqual([], result["alerts"])

    def test_response_and_a_record_are_excluded(self):
        lines = [row(i, message="response") for i in range(100)]
        lines += [row(i + 100, kind="A") for i in range(100)]
        result = detector.analyze(lines)
        self.assertEqual(0, result["counters"]["eligible_txt_queries"])
        self.assertEqual(100, result["counters"]["responses_skipped"])
        self.assertFalse(result["alerts"])

    def test_time_window_boundary_is_exclusive(self):
        lines = [row(i, ts="2026-10-15T08:34:59Z") for i in range(60)]
        lines += [row(i + 60, ts="2026-10-15T08:35:00Z") for i in range(60)]
        self.assertEqual([], detector.analyze(lines)["alerts"])

    def test_unsorted_events_same_result(self):
        lines = [row(i) for i in range(100)]
        self.assertEqual(detector.analyze(lines)["alerts"], detector.analyze(list(reversed(lines)) )["alerts"])

    def test_invalid_lines_counted_but_not_alerted(self):
        result = detector.analyze(["not json", row(0), row(1, ts="2026-10-15T08:30:00")])
        self.assertEqual(2, result["counters"]["invalid_lines"])
        self.assertEqual(1, result["counters"]["unique_events"])

    def test_unrelated_domain_is_excluded(self):
        lines = [row(i, name="q%04d.notsync.example" % i) for i in range(100)]
        self.assertEqual([], detector.analyze(lines)["alerts"])

    def test_tz_offset_normalizes_to_utc(self):
        lines = [row(i, ts="2026-10-15T14:00:00+05:30") for i in range(100)]
        alert = detector.analyze(lines)["alerts"][0]
        self.assertEqual("2026-10-15T08:30:00Z", alert["window_start_utc"])


if __name__ == "__main__":
    unittest.main()
