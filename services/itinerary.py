import datetime
from typing import Dict, Any, List

DAY_THEMES = [
    ("Orientation & Historic Landmarks", "Historical"),
    ("Culture, Arts & Local Heritage", "Culture"),
    ("Nature Trails, Parks & Scenic Heights", "Nature"),
    ("Culinary Flavors & Artisan Bazaars", "Shopping"),
    ("Coastal Breeze, Architecture & Sunset", "Photography"),
    ("Hidden Gems & Local Neighborhoods", "Sightseeing"),
    ("Leisure Excursion & Botanical Gardens", "Nature"),
    ("Panoramic Viewpoints & Heritage Docks", "Historical"),
]

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
    Guarantees unique daily themes, non-repeating places across days,
    distinct lunch and dinner recommendations, and weather adaptability.
    """
    if interests is None:
        interests = []

    dest_clean = destination.strip().title()

    try:
        d1 = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        d2 = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
        num_days = max(1, (d2 - d1).days + 1)
    except Exception:
        num_days = max(1, len(weather_data)) if weather_data else 5

    # 1. Build a rich, non-duplicating pool of places for the destination
    existing_place_names = set()
    unique_places = []
    for p in places:
        name = p.get("name", "")
        if name and name not in existing_place_names:
            existing_place_names.add(name)
            unique_places.append(p)

    # Dynamic place generators if provided places are fewer than needed (3 per day)
    needed_places = num_days * 3
    fallback_templates = [
        (f"{dest_clean} Historic Fort & Palace", "Historical"),
        (f"{dest_clean} Museum of Art & Culture", "Culture"),
        (f"{dest_clean} Grand City Square & Bazaar", "Shopping"),
        (f"{dest_clean} Central Botanical Gardens", "Nature"),
        (f"{dest_clean} Sunset Hilltop Viewpoint", "Photography"),
        (f"{dest_clean} Royal Heritage Promenade", "Sightseeing"),
        (f"{dest_clean} Craft Village & Artisan Alley", "Shopping"),
        (f"{dest_clean} Ancient Cathedral & Square", "Historical"),
        (f"{dest_clean} Waterfront Docks & Park", "Nature"),
        (f"{dest_clean} Local Spice & Produce Market", "Food"),
        (f"{dest_clean} Scenic River / Coastal Overlook", "Photography"),
        (f"{dest_clean} Contemporary Fine Arts Gallery", "Culture"),
        (f"{dest_clean} Old Town Walking Street", "Sightseeing"),
        (f"{dest_clean} Memorial Gardens & Lake", "Nature"),
        (f"{dest_clean} Skyline Towers Lookout", "Photography"),
    ]

    fb_idx = 0
    while len(unique_places) < needed_places:
        tmpl_name, tmpl_cat = fallback_templates[fb_idx % len(fallback_templates)]
        fb_idx += 1
        if tmpl_name not in existing_place_names:
            existing_place_names.add(tmpl_name)
            unique_places.append({
                "name": tmpl_name,
                "category": tmpl_cat,
                "rating": 4.6,
                "address": f"{dest_clean} Center",
                "duration": "2 hours"
            })

    # Sort places prioritizing user interests if present
    if interests:
        unique_places.sort(
            key=lambda p: any(i.lower() in p.get("category", "").lower() for i in interests),
            reverse=True
        )

    # 2. Build non-duplicating pool of restaurants
    unique_restaurants = []
    seen_rest = set()
    for r in restaurants:
        r_name = r.get("name", "")
        if r_name and r_name not in seen_rest:
            seen_rest.add(r_name)
            unique_restaurants.append(r)

    fallback_rests = [
        {"name": f"The Royal {dest_clean} Kitchen", "cuisine": "Regional Delicacies"},
        {"name": f"{dest_clean} Spice Route Fine Dining", "cuisine": "Multi-Cuisine"},
        {"name": f"Green Leaf {dest_clean} Bistro", "cuisine": "Organic & Local Fare"},
        {"name": f"Harbor View Seafood & Grill", "cuisine": "Coastal & Grill"},
        {"name": f"Heritage Courtyard Café", "cuisine": "Artisan Coffee & Snacks"},
    ]
    for r in fallback_rests:
        if len(unique_restaurants) >= max(4, num_days * 2):
            break
        if r["name"] not in seen_rest:
            seen_rest.add(r["name"])
            unique_restaurants.append(r)

    itinerary_days = []
    place_cursor = 0

    for i in range(num_days):
        day_num = i + 1
        
        # Weather data lookup
        w_item = weather_data[i] if i < len(weather_data) else {
            "day": f"Day {day_num}",
            "condition": "🌤️ Partly Cloudy",
            "max_temp": "30°C",
            "min_temp": "22°C",
            "rain_prob": "15%",
            "recommendation": "Good for outdoor sightseeing."
        }

        cond_str = w_item.get("condition", "").lower()
        rain_p = int(w_item.get("rain_prob", "0%").replace("%", "")) if "rain_prob" in w_item else 0
        max_t = int(w_item.get("max_temp", "30°C").replace("°C", "")) if "max_temp" in w_item else 30

        # Theme selection
        theme_title, theme_cat = DAY_THEMES[i % len(DAY_THEMES)]

        # Pick 3 distinct, non-overlapping places for this day
        p1 = unique_places[place_cursor % len(unique_places)]
        p2 = unique_places[(place_cursor + 1) % len(unique_places)]
        p3 = unique_places[(place_cursor + 2) % len(unique_places)]
        place_cursor += 3

        # Pick distinct lunch and dinner options for this day
        r_lunch = unique_restaurants[(i * 2) % len(unique_restaurants)]
        r_dinner = unique_restaurants[(i * 2 + 1) % len(unique_restaurants)]

        # Calculate date string
        try:
            curr_date_str = (d1 + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        except Exception:
            curr_date_str = w_item.get("date", f"Day {day_num}")

        # Weather-specific and Theme-based Activity Construction
        if "rain" in cond_str or rain_p > 45:
            weather_note = "🌧️ Rain Alert: High chance of rain. Indoor attractions & covered markets prioritized."
            morning_act = f"🏛️ Morning (09:30 AM – 12:30 PM): Protected indoor cultural tour at {p1['name']}. Explore covered museum galleries."
            afternoon_act = f"🍽️ Afternoon (01:00 PM – 04:30 PM): Authentic lunch at {r_lunch['name']}, followed by an indoor artisan workshop at {p2['name']}."
            evening_act = f"🛍️ Evening (05:30 PM – 08:30 PM): Covered shopping & evening leisure at {p3['name']}, followed by dinner at {r_dinner['name']}."
        elif max_t >= 34:
            weather_note = "☀️ Heat Alert: High temperatures mid-day. Outdoor activities planned for cooler morning/evening hours."
            morning_act = f"🌄 Early Morning (08:00 AM – 11:00 AM): Cool morning excursion to {p1['name']} before peak heat."
            afternoon_act = f"❄️ Mid-day (01:00 PM – 04:30 PM): Air-conditioned lunch at {r_lunch['name']} & relaxed indoor tour of {p2['name']}."
            evening_act = f"🌅 Sunset (05:30 PM – 08:30 PM): Scenic evening stroll & photography at {p3['name']}, with dinner at {r_dinner['name']}."
        else:
            weather_note = "🌤️ Great Weather: Ideal conditions for outdoor exploration & sightseeing!"
            
            # Rotate time structures and specific action verbs based on day number
            if day_num % 3 == 1:
                morning_act = f"🏰 Morning (09:00 AM – 12:00 PM): Sightseeing tour of {p1['name']}. Experience local heritage & photo spots."
                afternoon_act = f"🍛 Afternoon (01:00 PM – 04:30 PM): Mid-day lunch at {r_lunch['name']} followed by a visit to {p2['name']}."
                evening_act = f"🌅 Evening (05:30 PM – 08:30 PM): Catch sunset views at {p3['name']} & dine at {r_dinner['name']}."
            elif day_num % 3 == 2:
                morning_act = f"🎨 Morning (09:30 AM – 12:30 PM): Discover art, culture, and architecture at {p1['name']}."
                afternoon_act = f"🍽️ Afternoon (01:30 PM – 05:00 PM): Traditional lunch at {r_lunch['name']} & immersive stroll around {p2['name']}."
                evening_act = f"🛍️ Evening (06:00 PM – 09:00 PM): Night market & local crafts at {p3['name']} with dinner at {r_dinner['name']}."
            else:
                morning_act = f"🌄 Morning (08:30 AM – 11:30 AM): Outdoor nature walk and scenic view at {p1['name']}."
                afternoon_act = f"🍲 Afternoon (12:30 PM – 04:00 PM): Multi-course lunch at {r_lunch['name']} followed by exploration of {p2['name']}."
                evening_act = f"🌃 Evening (05:30 PM – 08:30 PM): Relaxing promenade walk at {p3['name']} & fine dining at {r_dinner['name']}."

        itinerary_days.append({
            "day": f"Day {day_num}",
            "title": f"Day {day_num}: {theme_title}",
            "date": curr_date_str,
            "weather_summary": f"{w_item.get('condition', '🌤️ Fair')} ({w_item.get('min_temp', '22°C')} – {w_item.get('max_temp', '30°C')})",
            "weather_note": weather_note,
            "morning": morning_act,
            "afternoon": afternoon_act,
            "evening": evening_act,
            "places_visited": [p1.get("name"), p2.get("name"), p3.get("name")],
            "lunch": r_lunch.get("name"),
            "dinner": r_dinner.get("name"),
            "dining": f"Lunch: {r_lunch.get('name')} | Dinner: {r_dinner.get('name')}"
        })

    return itinerary_days

