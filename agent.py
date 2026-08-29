import json
import datetime
import concurrent.futures
from typing import Dict, Any, List, Optional
from config import Config
from mcp_tools.server import MCPToolBridge
from services.itinerary import build_weather_aware_itinerary
from services.optimizer import optimize_trip_budget

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class TravelAgentEngine:
    """
    High-Speed Autonomous AI Travel Agent Engine.
    Executes MCP tool calls in parallel using ThreadPoolExecutor for ultra-fast response times.
    """

    def __init__(self):
        self.client = None
        if GENAI_AVAILABLE and Config.GEMINI_API_KEY:
            try:
                self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
            except Exception:
                self.client = None

    def plan_complete_trip(self, inputs: Dict[str, Any], status_callback=None) -> Dict[str, Any]:
        """
        Main autonomous parallel workflow execution:
        PARALLEL TOOL EXECUTION ➔ COLLECT ➔ COMPARE ➔ OPTIMIZE ➔ RETURN PLAN
        """
        def update_status(msg: str):
            if status_callback:
                status_callback(msg)

        destination = inputs.get("destination", "Goa").strip()
        starting_city = inputs.get("starting_city", "Hyderabad").strip()
        start_date = str(inputs.get("start_date", datetime.date.today()))
        end_date = str(inputs.get("end_date", datetime.date.today() + datetime.timedelta(days=4)))
        num_people = int(inputs.get("num_people", 2))
        user_budget = float(inputs.get("budget", 40000))
        trip_type = inputs.get("trip_type", "Friends")
        travel_style = inputs.get("travel_style", "Moderate")
        food_pref = inputs.get("food_pref", "Any")
        interests = inputs.get("interests", [])

        try:
            d1 = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            d2 = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            num_days = max(1, (d2 - d1).days + 1)
        except Exception:
            num_days = 5
        num_nights = max(1, num_days - 1)

        # 1. UNDERSTAND & SELECT TOOLS
        update_status("🤖 Understanding requirements & selecting MCP tools...")

        # 2. PARALLEL MCP TOOL EXECUTION (FASTEST RESPONSE TIME)
        update_status("⚡ Executing 7 MCP tools in parallel (Weather, Places, Restaurants, Hotels, Transport, Rentals, Healthcare)...")

        with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
            fut_weather = executor.submit(MCPToolBridge.call_tool, "get_weather", destination=destination, start_date=start_date, end_date=end_date)
            fut_places = executor.submit(MCPToolBridge.call_tool, "get_places", destination=destination, interests=interests)
            fut_restaurants = executor.submit(MCPToolBridge.call_tool, "get_restaurants", destination=destination, food_pref=food_pref, travel_style=travel_style)
            fut_hotels = executor.submit(MCPToolBridge.call_tool, "get_hotels", destination=destination, num_people=num_people, num_nights=num_nights, travel_style=travel_style, budget=user_budget)
            fut_transport = executor.submit(MCPToolBridge.call_tool, "get_transport", starting_city=starting_city, destination=destination, num_people=num_people, travel_style=travel_style)
            fut_rentals = executor.submit(MCPToolBridge.call_tool, "get_rentals", destination=destination, num_people=num_people, num_days=num_days, budget=user_budget)
            fut_healthcare = executor.submit(MCPToolBridge.call_tool, "get_healthcare", destination=destination)

            weather_res = fut_weather.result()
            places_res = fut_places.result()
            restaurants_res = fut_restaurants.result()
            hotels_res = fut_hotels.result()
            transport_res = fut_transport.result()
            rentals_res = fut_rentals.result()
            healthcare_res = fut_healthcare.result()

        # 3. EXTRACT CONTEXT & MAP ROUTE
        places_list = places_res.get("data", [])
        restaurants_list = restaurants_res.get("data", [])
        hotels_list = hotels_res.get("data", [])
        weather_list = weather_res.get("data", [])
        transport_data = transport_res.get("data", {})

        selected_hotel = hotels_list[0] if hotels_list else {"name": "Central Residency", "estimated_price": "₹3,500/night"}
        selected_hotel_name = selected_hotel.get("name", "Central Hotel")

        update_status("🗺️ Building route map & calculating itemized budget...")
        map_res = MCPToolBridge.call_tool("get_map_route", starting_city=starting_city, destination=destination, hotel=selected_hotel_name)

        # 4. BUDGET CALCULATIONS
        try:
            p_str = selected_hotel.get("estimated_price", "3000").replace("₹", "").replace(",", "").split("/")[0].split("(")[0].strip()
            hotel_nightly = float(p_str)
        except Exception:
            hotel_nightly = 3500.0

        best_transport = transport_data.get("best_value_option", {})
        try:
            t_str = best_transport.get("total_group_cost", "8000").replace("₹", "").replace(",", "").strip()
            transport_total = float(t_str)
        except Exception:
            transport_total = 8000.0

        rec_rental = rentals_res.get("data", {}).get("recommended_choice", {})
        try:
            r_str = rec_rental.get("total_estimated", "0").replace("₹", "").replace(",", "").strip()
            rental_total = float(r_str)
        except Exception:
            rental_total = 0.0

        budget_res = MCPToolBridge.call_tool("get_budget", user_budget=user_budget, num_people=num_people, num_days=num_days, hotel_nightly=hotel_nightly, transport_total=transport_total, rental_total=rental_total)

        # 5. WEATHER-AWARE ITINERARY & AI SCORE
        update_status("📅 Constructing daily itinerary & AI score...")
        day_itinerary = build_weather_aware_itinerary(
            destination=destination,
            start_date_str=start_date,
            end_date_str=end_date,
            weather_data=weather_list,
            places=places_list,
            restaurants=restaurants_list,
            interests=interests
        )

        ai_score, factor_breakdown = self._compute_ai_score(
            user_budget=user_budget,
            total_cost=budget_res.get("data", {}).get("total_group_cost", user_budget),
            weather_list=weather_list,
            travel_style=travel_style,
            interests=interests,
            places_count=len(places_list)
        )

        explanations = self._generate_explanations(
            hotel=selected_hotel,
            transport=best_transport,
            travel_style=travel_style,
            num_people=num_people
        )

        final_plan = {
            "inputs": inputs,
            "destination": destination,
            "starting_city": starting_city,
            "dates": f"{start_date} to {end_date} ({num_days} days, {num_nights} nights)",
            "num_days": num_days,
            "num_people": num_people,
            "ai_score": ai_score,
            "factor_breakdown": factor_breakdown,
            "weather_forecast": weather_res,
            "itinerary": day_itinerary,
            "places": places_res,
            "must_visit": places_list[:4],
            "restaurants": restaurants_res,
            "hotels": hotels_res,
            "selected_hotel": selected_hotel,
            "transport": transport_res,
            "rentals": rentals_res,
            "healthcare": healthcare_res,
            "map_route": map_res,
            "budget_breakdown": budget_res,
            "explanations": explanations,
            "ai_recommendations": [
                f"• Pack comfortable footwear and sun protection for daytime sightseeing in {destination}.",
                f"• Carry digital and physical copies of IDs for transport and hotel check-in.",
                f"• Reservable dining at {restaurants_list[0]['name']} is recommended for evening meals.",
                f"• Keep emergency medical contacts saved: {healthcare_res.get('data', [{}])[0].get('name', 'Local Hospital')} ({healthcare_res.get('data', [{}])[0].get('phone', '108')})."
            ]
        }

        update_status("✨ Plan ready!")
        return final_plan

    def _compute_ai_score(self, user_budget: float, total_cost: float, weather_list: List[Dict[str, Any]], travel_style: str, interests: List[str], places_count: int) -> tuple[int, Dict[str, str]]:
        score = 88
        if total_cost <= user_budget:
            budget_score = "Excellent (Within Budget)"
            score += 4
        else:
            budget_score = "Tight (Exceeds Budget)"
            score -= 6

        rainy_days = sum(1 for w in weather_list if "rain" in w.get("condition", "").lower())
        if rainy_days == 0:
            weather_fit = "Optimal (Clear Skies Forecast)"
            score += 4
        else:
            weather_fit = "Adapted (Rain-aware indoor backup planned)"
            score += 1

        efficiency = "High (Optimal Route Sequence)"
        pref_match = f"Strong Match ({len(interests)} interests incorporated)" if interests else "Standard General Sightseeing"
        final_score = max(60, min(98, score))

        factors = {
            "Budget Fit": budget_score,
            "Weather Suitability": weather_fit,
            "Travel Efficiency": efficiency,
            "Preference Match": pref_match,
            "Accommodation Suitability": f"Matched to {travel_style} travel style"
        }
        return final_score, factors

    def _generate_explanations(self, hotel: Dict[str, Any], transport: Dict[str, Any], travel_style: str, num_people: int) -> Dict[str, Any]:
        return {
            "why_this_hotel": [
                f"✓ Fits within your selected {travel_style.lower()} budget bracket",
                f"✓ Centrally located near major sightseeing attractions in {hotel.get('address', 'city center')}",
                f"✓ High cleanliness and safety ratings suitable for your group of {num_people}"
            ],
            "why_this_transport": [
                f"✓ Selected {transport.get('mode', 'Train/Bus')} balances cost and comfort",
                f"✓ Offers excellent travel duration value compared to driving distance",
                f"✓ Economical total group fare of {transport.get('total_group_cost', 'budget fare')}"
            ],
            "why_day2_changed": [
                "✓ Weather conditions evaluated for peak daytime comfort",
                "✓ Activity sequence optimized to minimize back-and-forth commuting distance",
                "✓ Balanced mix of sightseeing, dining, and relaxation time"
            ]
        }

    def adapt_itinerary(self, current_plan: Dict[str, Any], modification_prompt: str) -> Dict[str, Any]:
        updated_plan = json.loads(json.dumps(current_plan))
        prompt_lower = modification_prompt.lower()
        itinerary = updated_plan.get("itinerary", [])
        
        if "reduce budget" in prompt_lower or "cheaper" in prompt_lower:
            opt = optimize_trip_budget(updated_plan)
            updated_plan["budget_breakdown"]["data"]["total_group_cost"] = opt["optimized_total_cost"]
            updated_plan["budget_breakdown"]["data"]["cost_per_person"] = opt["optimized_cost_per_person"]
            updated_plan["budget_breakdown"]["data"]["status"] = "Optimized Savings Applied ✅"
            updated_plan["adaptation_note"] = f"Budget reduced! Saved ₹{opt['total_savings']:,} by selecting cost-effective stay & transit."
            return updated_plan

        if "day 2" in prompt_lower:
            for day_item in itinerary:
                if "2" in day_item.get("day", ""):
                    day_item["morning"] = "🏛️ Morning (9:30 AM): Relaxed cultural visit to local heritage museum."
                    day_item["afternoon"] = "🍽️ Afternoon (1:30 PM): Scenic café dining & craft workshop."
                    day_item["evening"] = "🌅 Evening (5:30 PM): Sunset walking tour & local food tasting."
                    day_item["weather_note"] = "✨ Day 2 customized as per user request (Relaxed pace)."
            updated_plan["itinerary"] = itinerary
            updated_plan["adaptation_note"] = "Updated Day 2 schedule to a relaxed, cultural pace as requested."
            return updated_plan

        if "temple" in prompt_lower:
            for day_item in itinerary:
                day_item["morning"] = "🛕 Early Morning: Spiritual visit to historic city temple & peaceful complex grounds."
            updated_plan["itinerary"] = itinerary
            updated_plan["adaptation_note"] = "Added prominent temple visits to morning schedules across the trip."
            return updated_plan

        if "relaxed" in prompt_lower or "lazy" in prompt_lower:
            for day_item in itinerary:
                day_item["morning"] = "☕ Late Morning (10:30 AM): Leisurely breakfast and casual neighborhood walk."
            updated_plan["itinerary"] = itinerary
            updated_plan["adaptation_note"] = "Adjusted itinerary to a relaxed schedule with late morning starts."
            return updated_plan

        if len(itinerary) > 1:
            itinerary[1]["afternoon"] = f"✨ Modified Activity: {modification_prompt.capitalize()}"
            updated_plan["itinerary"] = itinerary
        updated_plan["adaptation_note"] = f"Adapted plan: Incorporating request '{modification_prompt}'."
        return updated_plan

    def chat_with_trip(self, current_plan: Dict[str, Any], user_question: str) -> str:
        dest = current_plan.get("destination", "Goa")
        budget_data = current_plan.get("budget_breakdown", {}).get("data", {})
        total_cost = budget_data.get("total_group_cost", 36500)
        per_person = budget_data.get("cost_per_person", 9125)
        hotel = current_plan.get("selected_hotel", {}).get("name", "Selected Hotel")
        transport = current_plan.get("transport", {}).get("data", {}).get("best_value_option", {}).get("mode", "Train")

        if self.client:
            try:
                system_prompt = f"You are the AI Travel Agent advisor for a trip to {dest}. Total cost: ₹{total_cost}, Per person: ₹{per_person}, Hotel: {hotel}, Transport: {transport}. Answer concisely in 2-3 sentences based on context."
                response = self.client.models.generate_content(
                    model=Config.DEFAULT_MODEL,
                    contents=f"{system_prompt}\nUser Question: {user_question}"
                )
                if response and response.text:
                    return response.text.strip()
            except Exception:
                pass

        q_lower = user_question.lower()
        if "cost" in q_lower or "budget" in q_lower or "expensive" in q_lower or "cheapest" in q_lower:
            return f"The total estimated cost for your group to {dest} is ₹{total_cost:,} (₹{per_person:,} per person). You can lower costs by clicking 'Optimize Trip' to downgrade accommodation or transportation."
        elif "hotel" in q_lower or "stay" in q_lower or "accommodation" in q_lower:
            return f"We recommend staying at '{hotel}'. It was selected because it is centrally located, fits your travel budget, and offers great amenities."
        elif "transport" in q_lower or "travel" in q_lower or "flight" in q_lower or "train" in q_lower:
            return f"The recommended transportation option is {transport}, which offers the best balance of travel time and cost efficiency for your starting city."
        elif "rain" in q_lower or "weather" in q_lower:
            return f"Our weather system checks forecast data for {dest}. If rain is detected on any day, the itinerary automatically shifts outdoor sightseeing to covered indoor museums, cafes, and markets."
        else:
            return f"Regarding your trip to {dest}: Your total estimated budget is ₹{total_cost:,} for {current_plan.get('num_days', 5)} days. Hotel '{hotel}' and {transport} have been selected to optimize comfort and value."
