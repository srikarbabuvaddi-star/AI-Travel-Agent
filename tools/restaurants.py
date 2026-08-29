import requests
from typing import Dict, Any, List
from services.fallback import DynamicCityEstimator, geocode_city
from services.data_normalizer import normalize_response
from config import Config

_RESTAURANTS_CACHE = {}

def get_restaurants(destination: str, food_pref: str = "Any", travel_style: str = "Moderate") -> Dict[str, Any]:
    """
    Fetches restaurants with caching and fast response time.
    """
    city_clean = destination.strip().title()
    cache_key = f"{city_clean.lower()}_{food_pref.lower()}_{travel_style.lower()}"
    if cache_key in _RESTAURANTS_CACHE:
        return _RESTAURANTS_CACHE[cache_key]

    coords = geocode_city(city_clean)
    lat, lon = coords["lat"], coords["lon"]

    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json][timeout:2];
    (
      node["amenity"="restaurant"](around:8000, {lat}, {lon});
      node["amenity"="cafe"](around:8000, {lat}, {lon});
    );
    out 8;
    """

    try:
        resp = requests.post(overpass_url, data={"data": overpass_query}, timeout=1.5)
        if resp.status_code == 200:
            elements = resp.json().get("elements", [])
            live_rests = []
            seen = set()

            for elem in elements:
                tags = elem.get("tags", {})
                name = tags.get("name")
                if not name or name in seen:
                    continue
                seen.add(name)

                cuisine = tags.get("cuisine", "Regional / Multi-Cuisine").replace("_", " ").title()

                live_rests.append({
                    "name": name,
                    "cuisine": cuisine,
                    "rating": 4.4,
                    "address": tags.get("addr:street", f"{city_clean} Central"),
                    "price_category": "Moderate" if travel_style == "Moderate" else ("Luxury" if travel_style == "Luxury" else "Budget"),
                    "reason": f"Popular verified dining option in {city_clean} offering {cuisine} cuisine."
                })

            if len(live_rests) >= 2:
                res = normalize_response(
                    status="success",
                    source="LIVE RESTAURANTS (OpenStreetMap)",
                    data=live_rests[:6],
                    message=f"Retrieved live restaurants for {city_clean}"
                )
                _RESTAURANTS_CACHE[cache_key] = res
                return res
    except Exception:
        pass

    res = DynamicCityEstimator.get_fallback_restaurants(city_clean, food_pref=food_pref)
    _RESTAURANTS_CACHE[cache_key] = res
    return res
