import unittest
from app.catalog import local_packet
from app.contributions import contribution_profile as profile


class ContextTests(unittest.TestCase):
    def setUp(self):
        self.packet = local_packet("data/current.json")

    def test_exited_people_are_not_removed(self):
        result = profile(self.packet)
        self.assertEqual(len(result["people"]), result["current_roster"])
        self.assertGreater(result["current_roster"], result["next_roster"])

    def test_person_and_team_recorded_totals_agree(self):
        result = profile(self.packet)
        self.assertAlmostEqual(sum(row["lower_recorded_hours"] for row in result["people"]), sum(row["recorded_hours"] for row in result["teams"]))
