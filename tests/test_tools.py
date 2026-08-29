import unittest
import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.weather import get_weather_forecast
from tools.places import get_tourist_places
from tools.restaurants import get_restaurants
from tools.hotels import get_hotels
from tools.transport import compare_transport_options
from tools.rentals import get_rental_options
from tools.healthcare import get_healthcare_facilities
from tools.maps import get_map_route
from tools.budget import calculate_budget_breakdown
from services.fallback import DynamicCityEstimator

class TestTravelTools(unittest.TestCase):

    def test_weather_forecast(self):
        res = get_weather_forecast("Goa", "2026-09-10", "2026-09-14")
        self.assertIn(res["status"], ["success", "partial"])
        self.assertTrue(len(res["data"]) >= 1)
        self.assertIn("condition", res["data"][0])

    def test_places_lookup_any_city(self):
        # Test custom city (Kyoto) to verify non-hardcoded city support
        res = get_tourist_places("Kyoto", ["Culture", "History"])
        self.assertIn(res["status"], ["success", "partial"])
        self.assertTrue(len(res["data"]) >= 1)

    def test_restaurants_lookup(self):
        res = get_restaurants("Goa", food_pref="Seafood")
        self.assertIn(res["status"], ["success", "partial"])
        self.assertTrue(len(res["data"]) >= 1)

    def test_hotels_lookup(self):
        res = get_hotels("Goa", num_people=4, num_nights=4, budget=40000)
        self.assertIn(res["status"], ["success", "partial"])
        self.assertTrue(len(res["data"]) >= 1)

    def test_transport_comparison(self):
        res = compare_transport_options("Hyderabad", "Goa", num_people=4)
        self.assertEqual(res["status"], "success")
        data = res["data"]
        self.assertIn("cheapest_option", data)
        self.assertIn("best_value_option", data)
        self.assertIn("fastest_option", data)

    def test_rentals(self):
        res = get_rental_options("Goa", num_people=4, num_days=5)
        self.assertEqual(res["status"], "success")
        self.assertTrue(len(res["data"]["rentals"]) >= 2)

    def test_healthcare(self):
        res = get_healthcare_facilities("Goa")
        self.assertIn(res["status"], ["success", "partial"])
        self.assertTrue(len(res["data"]) >= 1)

    def test_maps(self):
        res = get_map_route("Hyderabad", "Goa", "Taj Resort")
        self.assertEqual(res["status"], "success")
        self.assertIn("text_route_summary", res["data"])

    def test_budget_breakdown(self):
        res = calculate_budget_breakdown(
            user_budget=40000,
            num_people=4,
            num_days=5,
            selected_hotel_nightly=3500,
            selected_transport_total=8000
        )
        self.assertEqual(res["status"], "success")
        self.assertIn("total_group_cost", res["data"])
        self.assertIn("cost_per_person", res["data"])

    def test_dynamic_city_estimator_any_city(self):
        # Verify dynamic fallback works for a totally unknown city name
        res = DynamicCityEstimator.get_fallback_places("Reykjavik")
        self.assertEqual(res["status"], "success")
        self.assertTrue(len(res["data"]) >= 3)
        self.assertIn("Reykjavik", res["data"][0]["name"])

if __name__ == "__main__":
    unittest.main()
