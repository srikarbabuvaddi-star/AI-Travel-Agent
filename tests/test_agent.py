import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent import TravelAgentEngine
from mcp_tools.server import MCPToolBridge
from services.optimizer import optimize_trip_budget

class TestTravelAgentEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.agent = TravelAgentEngine()
        cls.inputs = {
            "destination": "Goa",
            "starting_city": "Hyderabad",
            "start_date": "2026-09-10",
            "end_date": "2026-09-14",
            "num_people": 4,
            "budget": 40000,
            "trip_type": "Friends",
            "travel_style": "Moderate",
            "food_pref": "Seafood",
            "interests": ["Beaches", "Culture"]
        }
        cls.plan = cls.agent.plan_complete_trip(cls.inputs)

    def test_mcp_bridge_calls(self):
        res = MCPToolBridge.call_tool("get_weather", destination="Goa", start_date="2026-09-10", end_date="2026-09-14")
        self.assertIn(res["status"], ["success", "partial"])

    def test_plan_complete_trip(self):
        self.assertIsNotNone(self.plan)
        self.assertEqual(self.plan["destination"], "Goa")
        self.assertTrue(self.plan["ai_score"] > 60)
        self.assertTrue(len(self.plan["itinerary"]) >= 5)
        self.assertIn("budget_breakdown", self.plan)
        self.assertIn("explanations", self.plan)

    def test_optimize_trip_budget(self):
        opt = optimize_trip_budget(self.plan)
        self.assertIn("original_total_cost", opt)
        self.assertIn("optimized_total_cost", opt)
        self.assertTrue(opt["total_savings"] >= 0)

    def test_adapt_itinerary(self):
        adapted_plan = self.agent.adapt_itinerary(self.plan, "Change Day 2 to relaxed pace")
        self.assertIn("adaptation_note", adapted_plan)

    def test_chat_with_trip(self):
        answer = self.agent.chat_with_trip(self.plan, "Which transport option is cheapest?")
        self.assertTrue(len(answer) > 10)

    def test_itinerary_day_uniqueness(self):
        itinerary = self.plan.get("itinerary", [])
        self.assertTrue(len(itinerary) >= 5)

        # Check titles are distinct
        titles = [day.get("title") for day in itinerary if day.get("title")]
        self.assertEqual(len(titles), len(set(titles)), "Each day must have a unique title/theme")

        # Check places visited across consecutive days do not repeat identically
        visited_lists = [tuple(day.get("places_visited", [])) for day in itinerary]
        self.assertEqual(len(visited_lists), len(set(visited_lists)), "Attractions visited per day must be distinct")

if __name__ == "__main__":
    unittest.main()
