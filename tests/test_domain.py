import unittest
from app.catalog import local_packet
from app.domain import ANALYSES, validate
from app.engine import analyze


class DomainTests(unittest.TestCase):
    def setUp(self):
        self.packet = local_packet("data/current.json")

    def result(self):
        return analyze(self.packet, next(iter(ANALYSES)))["result"]

    def test_caps_and_missingness_are_separate(self):
        self.assertGreater(self.result()["capped_records"], 0)
        self.assertGreater(self.result()["missing_records"], 0)

    def test_original_roster_includes_exited_people(self):
        self.assertGreater(self.result()["roster_size"], len(self.packet["scenario_roster"]))
