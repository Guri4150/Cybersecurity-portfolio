"""Fictional fixtures; tests exercise rule boundaries and CLI evidence."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from detect import investigate, load_validator

HERE = Path(__file__).resolve().parent
VALIDATE = load_validator()


def row(second, status="failure", **changes):
    event = dict(timestamp=f"2026-10-07T09:{second // 60:02d}:{second % 60:02d}Z",
                 username="demo_owl", source_ip="192.0.2.10", status=status)
    event.update(changes)
    return json.dumps(event)


class DetectionTests(unittest.TestCase):
    def run_rule(self, lines):
        return investigate(lines, VALIDATE)

    def test_sample_cli(self):
        result = subprocess.run([sys.executable, str(HERE / "detect.py"),
                                 str(HERE / "synthetic_auth.jsonl")],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, (HERE / "example_alerts.json").read_text())
        report = json.loads(result.stdout)
        self.assertEqual(len(report["alerts"]), 1)
        self.assertEqual(report["alerts"][0]["failure_lines"], [1, 2, 3])

    def test_threshold(self):
        self.assertEqual(self.run_rule([row(0), row(60), row(180, "success")])["alerts"], [])
        self.assertEqual(len(self.run_rule([row(0), row(60), row(120),
                                           row(180, "success")])["alerts"]), 1)

    def test_inclusive_window_boundary(self):
        failures = [row(0), row(60), row(120)]
        self.assertEqual(len(self.run_rule(failures + [row(300, "success")])["alerts"]), 1)
        self.assertEqual(self.run_rule(failures + [row(301, "success")])["alerts"], [])

    def test_strictly_before_success(self):
        for final in [180, 181]:
            self.assertEqual(self.run_rule([row(0), row(60), row(final),
                                           row(180, "success")])["alerts"], [])

    def test_grouping(self):
        for change in [dict(username="demo_fox"), dict(source_ip="203.0.113.30")]:
            self.assertEqual(self.run_rule([row(0), row(60), row(120, **change),
                                           row(180, "success")])["alerts"], [])

    def test_unsorted(self):
        result = self.run_rule([row(180, "success"), row(120), row(0), row(60)])
        self.assertEqual(result["alerts"][0]["failure_lines"], [3, 4, 2])

    def test_deduplication_and_bad_data(self):
        result = self.run_rule([row(0), row(0), row(60), row(180, "success"),
                                "not json", "", row(240, source_ip="999.0.0.1")])
        self.assertEqual((result["duplicate_events"], result["invalid_lines"],
                          result["blank_lines"], result["unique_valid_events"]), (1, 2, 1, 3))
        self.assertEqual(result["alerts"], [])

    def test_empty_and_no_success(self):
        for lines in [[], [row(0), row(60), row(120)], ["invalid"]]:
            self.assertEqual(self.run_rule(lines)["alerts"], [])

    def test_multiple_successes_not_suppressed(self):
        result = self.run_rule([row(0), row(60), row(120),
                                row(180, "success"), row(240, "success")])
        self.assertEqual(len(result["alerts"]), 2)

    def test_cli_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.jsonl"
            for content in [None, b"\xff"]:
                if content is not None:
                    path.write_bytes(content)
                result = subprocess.run([sys.executable, str(HERE / "detect.py"), str(path)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
