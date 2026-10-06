"""Repeatable unit and CLI tests using fictional data only."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from auth_parser import parse_event, summarize

HERE = Path(__file__).resolve().parent


def record(**changes):
    event = {"timestamp": "2026-10-01T09:00:00Z", "username": "demo_owl",
             "source_ip": "192.0.2.10", "status": "failure"}
    event.update(changes)
    return json.dumps(event)


class ParserTests(unittest.TestCase):
    def cli(self, *args):
        return subprocess.run([sys.executable, str(HERE / "auth_parser.py"), *args],
                              capture_output=True, text=True)

    def test_valid_event(self):
        self.assertEqual(parse_event(record())["source_ip"], "192.0.2.10")

    def test_invalid_records(self):
        bad = ["not json", "[]", "null", "{}", record(extra="demo"),
               record(username=None), record(username="demo name"),
               record(source_ip="999.0.0.1"), record(source_ip="2001:db8::1"),
               record(status="unknown"), record(timestamp="2026-02-30T09:00:00Z"),
               record(timestamp="2026-10-01T09:00:00"), record(timestamp="bad")]
        for line in bad:
            with self.subTest(line=line), self.assertRaises(ValueError):
                parse_event(line)

    def test_empty_and_blank_input(self):
        self.assertEqual(summarize([])["total_lines"], 0)
        result = summarize(["\n", "  \n"])
        self.assertEqual((result["blank_lines"], result["valid_events"]), (2, 0))

    def test_inclusive_threshold(self):
        self.assertEqual(summarize([record()] * 2)["flagged_sources"], [])
        self.assertEqual(summarize([record()] * 3)["flagged_sources"],
                         [{"source_ip": "192.0.2.10", "failures": 3}])

    def test_success_does_not_reset_failures(self):
        result = summarize([record(), record(status="success"), record()], 2)
        self.assertEqual((result["successes"], result["failures"]), (1, 2))
        self.assertEqual(len(result["flagged_sources"]), 1)

    def test_distinct_sources_and_users(self):
        result = summarize([record(), record(username="demo_fox"),
                            record(source_ip="203.0.113.30")], 2)
        self.assertEqual(result["flagged_sources"],
                         [{"source_ip": "192.0.2.10", "failures": 2}])

    def test_invalid_lines_do_not_count_as_events(self):
        result = summarize([record(), "malformed", "\n"])
        self.assertEqual((result["total_lines"], result["valid_events"],
                          result["invalid_lines"], result["blank_lines"]), (3, 1, 1, 1))

    def test_invalid_threshold(self):
        for threshold in [0, -1, True, 1.5, "3"]:
            with self.subTest(threshold=threshold), self.assertRaises(ValueError):
                summarize([], threshold)

    def test_sample_cli_matches_documented_output(self):
        run = self.cli(str(HERE / "sample_auth.jsonl"))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stderr, "")
        self.assertEqual(run.stdout, (HERE / "example_output.json").read_text())

    def test_cli_threshold(self):
        run = self.cli(str(HERE / "sample_auth.jsonl"), "--threshold", "4")
        self.assertEqual(run.returncode, 0)
        self.assertEqual(json.loads(run.stdout)["flagged_sources"], [])
        for value in ["0", "-1", "abc"]:
            self.assertEqual(self.cli(str(HERE / "sample_auth.jsonl"),
                                      "--threshold", value).returncode, 2)

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            run = self.cli(str(Path(directory) / "missing.jsonl"))
        self.assertEqual(run.returncode, 1)
        self.assertEqual(run.stdout, "")
        self.assertIn("cannot read", run.stderr)

    def test_invalid_utf8(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.jsonl"
            path.write_bytes(b"\xff")
            run = self.cli(str(path))
        self.assertEqual(run.returncode, 1)
        self.assertEqual(run.stdout, "")


if __name__ == "__main__":
    unittest.main()
