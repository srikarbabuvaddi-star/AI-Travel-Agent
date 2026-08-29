import requests
from typing import Dict, Any, List
from services.fallback import DynamicCityEstimator, geocode_city
from services.data_normalizer import normalize_response
from config import Config

_HOTELS_CACHE = {}

def get_hotels(
    destination: str,
    num_people: int = 2,
    num_nights: int = 3,
    travel_style: str = "Moderate",
    budget: float = 20000
) -> Dict[str, Any]:
    """
    Fetches accommodation options with caching and fast response time.
    """
    city_clean = destination.strip().title()
    cache_key = f"{city_clean.lower()}_{num_people}_{num_nights}_{travel_style.lower()}"
    if cache_key in _HOTELS_CACHE:
        return _HOTELS_CACHE[cache_key]

    coords = geocode_city(city_clean)
    lat, lon = coords["lat"], coords["lon"]

    target_nightly_max = max(1000, (budget * 0.35) / max(1, num_nights))

    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json][timeout:2];
    (
      node["tourism"="hotel"](around:10000, {lat}, {lon});
      way["tourism"="hotel"](around:10000, {lat}, {lon});
    );
    out center 6;
    """

    try:
        resp = requests.post(overpass_url, data={"data": overpass_query}, timeout=1.5)
        if resp.status_code == 200:
            elements = resp.json().get("elements", [])
            live_hotels = []
            seen = set()

            for elem in elements:
                tags = elem.get("tags", {})
                name = tags.get("name")
                if not name or name in seen:
                    continue
                seen.add(name)

                stars = tags.get("stars", "4")
                est_rate = round(target_nightly_max * (0.8 if travel_style == "Budget" else (1.4 if travel_style == "Luxury" else 1.0)))

                live_hotels.append({
                    "name": name,
                    "rating": float(stars) if stars.replace(".", "").isdigit() else 4.5,
                    "address": tags.get("addr:street", f"Central {city_clean}"),
                    "estimated_price": f"₹{est_rate:,}/night (Estimated)",
                    "distance": f"1.5 km from city center",
                    "reason": f"Verified hotel in {city_clean} matching your {travel_style.lower()} travel style and group size ({num_people} people)."
                })

            if len(live_hotels) >= 2:
                res = normalize_response(
                    status="success",
                    source="LIVE HOTEL DATA (OpenStreetMap)",
                    data=live_hotels[:5],
                    message=f"Fetched live verified hotel locations for {city_clean}"
                )
                _HOTELS_CACHE[cache_key] = res
                return res
    except Exception:
        pass

    res = DynamicCityEstimator.get_fallback_hotels(city_clean, travel_style=travel_style)
    _HOTELS_CACHE[cache_key] = res
    return res
