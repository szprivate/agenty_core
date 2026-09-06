"""The log tool has to see the log's errors — and say how old they are.

Two failures, both live in one session:

* **Case.** The markers were matched case-sensitively: ``"Error"``, ``"FAILED"``.
  ComfyUI writes its level as ``[ERROR]`` and its rejections as ``Failed to
  validate prompt``. Neither matched, so no validation failure was ever visible.
* **Staleness.** Something has to be returned, so it fell through to the newest
  line that DID contain "Error" — a four-hour-old ``AttributeError`` from a bug
  fixed that morning — and presented it as the current failure. The agent
  believed it and spent two turns repairing the wrong thing while the real
  reason, ``Value 16 bigger than max of 10: bit_depth``, sat thirty lines below
  it in the same buffer.

A rejection also carries no exception class, so the benign-interrupt filter —
which only looked for one — discarded it whenever it landed near a "Global
interrupt". That is the opposite of benign: the branch never ran.
"""
import json
import unittest

from agenty_core.tools import comfyui as C


def entry(t, m):
    return {"t": f"2026-09-06T{t}.000000", "m": m}


# The morning's crash, then hours later the rejection that actually matters.
LOG = [
    entry("09:39:27", "[ERROR] !!! Exception during processing !!!"),
    entry("09:39:27", "AttributeError: 'int' object has no attribute 'penultimate_hidden_states'"),
    entry("09:39:27", "[INFO] Prompt executed in 357.06 seconds"),
] + [entry("10:00:00", f"[INFO] filler {i}") for i in range(40)] + [
    entry("14:08:05", "[INFO] got prompt"),
    entry("14:08:06", "[INFO] Global interrupt (no prompt_id specified)"),
    entry("14:08:07", "[INFO] Processing interrupted"),
    entry("14:08:13", "[INFO] got prompt"),
    entry("14:08:14", "[ERROR] Failed to validate prompt for output 4:"),
    entry("14:08:14", "[ERROR] * CreateVideo 10:"),
    entry("14:08:14", "[ERROR]   - Value 16 bigger than max of 10: bit_depth"),
    entry("14:08:14", "[ERROR] Output will be ignored"),
    entry("14:08:15", "[INFO] Prompt executed in 0.36 seconds"),
]


class _Client:
    def __init__(self, entries):
        self._entries = entries

    def get(self, path):
        return {"entries": self._entries} if "logs" in path else {}


class FindingTheRealError(unittest.TestCase):
    def setUp(self):
        self._orig = C.get_client

    def tearDown(self):
        C.get_client = self._orig

    def _logs(self, entries=None, **kw):
        C.get_client = lambda: _Client(entries if entries is not None else LOG)
        fn = getattr(C.get_logs, "func", C.get_logs)
        out = fn(**kw)
        return out if out == "None" else json.loads(out)

    def test_it_finds_a_validation_failure(self):
        text = " ".join(self._logs()["lines"])
        self.assertIn("Value 16 bigger than max of 10", text)
        self.assertIn("CreateVideo", text)

    def test_it_does_not_serve_the_morning_traceback_instead(self):
        out = self._logs()
        self.assertEqual(out["at"], "14:08:14")
        self.assertNotIn("penultimate_hidden_states", " ".join(out["lines"]))

    def test_a_rejection_beside_an_interrupt_is_not_benign(self):
        # It has no exception class, so the interrupt filter used to bin it.
        text = " ".join(self._logs()["lines"])
        self.assertIn("Failed to validate", text)

    def test_a_real_interruption_alone_is_still_benign(self):
        quiet = [entry("14:00:00", "[INFO] got prompt"),
                 entry("14:00:01", "[INFO] Global interrupt (no prompt_id specified)"),
                 entry("14:00:01", "[ERROR] !!! Exception during processing !!!"),
                 entry("14:00:01", "comfy.model_management.InterruptProcessingException"),
                 entry("14:00:02", "[INFO] Processing interrupted")]
        self.assertEqual(self._logs(quiet), "None")

    def test_an_uppercase_level_is_matched(self):
        only = [entry("14:00:00", "[ERROR] Something went wrong in a node")]
        self.assertIn("Something went wrong", " ".join(self._logs(only)["lines"]))


class SayingHowOldItIs(unittest.TestCase):
    def setUp(self):
        self._orig = C.get_client

    def tearDown(self):
        C.get_client = self._orig

    def _logs(self, entries):
        C.get_client = lambda: _Client(entries)
        fn = getattr(C.get_logs, "func", C.get_logs)
        return json.loads(fn())

    def test_an_error_from_a_previous_run_is_flagged(self):
        stale = LOG[:3] + [entry("14:20:00", "[INFO] got prompt"),
                           entry("14:20:30", "[INFO] Prompt executed in 30.0 seconds")]
        out = self._logs(stale)
        self.assertTrue(out["from_earlier_run"])
        self.assertIn("BEFORE the most recent submission", out["note"])
        # And it points at what a silent, output-less "success" actually means.
        self.assertIn("node_errors", out["note"])

    def test_an_error_from_the_current_run_is_not_flagged(self):
        fresh = [entry("14:20:00", "[INFO] got prompt"),
                 entry("14:20:01", "[ERROR] Failed to validate prompt for output 4:"),
                 entry("14:20:01", "[ERROR]   - Value 16 bigger than max of 10: bit_depth")]
        out = self._logs(fresh)
        self.assertNotIn("from_earlier_run", out)
        self.assertNotIn("note", out)

    def test_it_always_says_when_the_error_happened(self):
        self.assertEqual(self._logs(LOG)["at"], "14:08:14")


if __name__ == "__main__":
    unittest.main()
