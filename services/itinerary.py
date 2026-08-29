import datetime
from typing import Dict, Any, List

def build_weather_aware_itinerary(
    destination: str,
    start_date_str: str,
    end_date_str: str,
    weather_data: List[Dict[str, Any]],
    places: List[Dict[str, Any]],
    restaurants: List[Dict[str, Any]],
    interests: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Constructs a weather-aware, day-by-day travel itinerary.
    Dynamically adjusts schedule based on daily weather forecast (rain, heat, clear skies).
    """
    if interests is None:
        interests = []
    
    num_days = max(1, len(weather_data))
    place_idx = 0
    num_places = len(places)

    itinerary_days = []

    for i in range(num_days):
        w_item = weather_data[i] if i < len(weather_data) else {
            "day": f"Day {i+1}",
            "condition": "🌤️ Partly Cloudy",
            "max_temp": "30°C",
            "rain_prob": "15%",
            "recommendation": "Good for outdoor sightseeing."
        }

        day_num = i + 1
        cond_str = w_item.get("condition", "").lower()
        rain_p = int(w_item.get("rain_prob", "0%").replace("%", "")) if "rain_prob" in w_item else 0
        max_t = int(w_item.get("max_temp", "30°C").replace("°C", "")) if "max_temp" in w_item else 30

        # Select Morning, Afternoon, and Evening activities
        morning_activity = ""
        afternoon_activity = ""
        evening_activity = ""

        # Fetch places from list
        p1 = places[place_idx % num_places] if num_places > 0 else {"name": f"{destination} City Tour", "category": "Sightseeing"}
        p2 = places[(place_idx + 1) % num_places] if num_places > 0 else {"name": f"{destination} Local Market", "category": "Shopping"}
        p3 = places[(place_idx + 2) % num_places] if num_places > 0 else {"name": f"{destination} Sunset Point", "category": "Photography"}
        place_idx += 2

        # Restaurant selection
        r1 = restaurants[i % len(restaurants)] if restaurants else {"name": "Local Restaurant", "cuisine": "Regional"}

        # WEATHER ADAPTABILITY RULES
        if "rain" in cond_str or rain_p > 45:
            weather_note = "🌧️ Weather Alert: High chance of rain today. Indoor & covered attractions prioritized."
            morning_activity = f"🏛️ Morning: Visit {p1['name']} ({p1.get('category', 'Indoor')}) - Protected indoor sightseeing."
            afternoon_activity = f"🍽️ Lunch & Cultural Workshop at {r1['name']}, followed by indoor gallery tour."
            evening_activity = f"🛍️ Evening: Explore covered handicrafts & shopping arcade at {p2['name']}."
        elif max_t >= 34:
            weather_note = "☀️ Weather Alert: High temperatures expected mid-day. Early morning & evening outdoors."
            morning_activity = f"🌄 Early Morning (8:00 AM): Cool outdoor excursion to {p1['name']}."
            afternoon_activity = f"❄️ Mid-day Rest: Lunch at {r1['name']} & relaxed indoor shopping at {p2['name']}."
            evening_activity = f"🌅 Sunset (5:30 PM): Scenic evening breeze & photography at {p3['name']}."
        else:
            weather_note = "🌤️ Pleasant Weather: Perfect for full-day outdoor exploration!"
            morning_activity = f"🏰 Morning (9:00 AM): Explore famous landmark {p1['name']}."
            afternoon_activity = f"🍛 Afternoon (1:00 PM): Authentic lunch at {r1['name']} followed by visit to {p2['name']}."
            evening_activity = f"🌅 Evening (5:30 PM): Sunset views and evening leisure at {p3['name']}."

        itinerary_days.append({
            "day": f"Day {day_num}",
            "date": w_item.get("date", f"Day {day_num}"),
            "weather_summary": f"{w_item.get('condition', '🌤️ Fair')} ({w_item.get('min_temp', '22°C')} – {w_item.get('max_temp', '30°C')})",
            "weather_note": weather_note,
            "morning": morning_activity,
            "afternoon": afternoon_activity,
            "evening": evening_activity,
            "places_visited": [p1.get("name"), p2.get("name"), p3.get("name")],
            "dining": r1.get("name")
        })

    return itinerary_days
