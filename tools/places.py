import requests
from typing import Dict, Any, List
from services.fallback import DynamicCityEstimator, geocode_city
from services.data_normalizer import normalize_response
from config import Config

_PLACES_CACHE = {}

def get_tourist_places(destination: str, interests: List[str] = None) -> Dict[str, Any]:
    """
    Fetches tourist attractions for destination with caching and fast response.
    """
    if interests is None:
        interests = []
    
    city_clean = destination.strip().title()
    cache_key = f"{city_clean.lower()}_{'_'.join(sorted(interests))}"
    if cache_key in _PLACES_CACHE:
        return _PLACES_CACHE[cache_key]

    coords = geocode_city(city_clean)
    lat, lon = coords["lat"], coords["lon"]

    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json][timeout:2];
    (
      node["tourism"~"attraction|museum|viewpoint|artwork|theme_park"](around:10000, {lat}, {lon});
      way["tourism"~"attraction|museum|viewpoint|artwork|theme_park"](around:10000, {lat}, {lon});
    );
    out center 8;
    """

    try:
        resp = requests.post(overpass_url, data={"data": overpass_query}, timeout=1.5)
        if resp.status_code == 200:
            raw_data = resp.json()
            elements = raw_data.get("elements", [])
            
            live_places = []
            seen_names = set()

            for elem in elements:
                tags = elem.get("tags", {})
                name = tags.get("name") or tags.get("name:en")
                if not name or name in seen_names:
                    continue
                seen_names.add(name)

                tourism = tags.get("tourism", "")
                category = "Museum / Culture" if tourism == "museum" else "Attraction"
                p_lat = elem.get("lat") or (elem.get("center", {}).get("lat", lat))
                p_lon = elem.get("lon") or (elem.get("center", {}).get("lon", lon))

                live_places.append({
                    "name": name,
                    "category": category,
                    "rating": 4.5,
                    "address": tags.get("addr:street", f"{city_clean} Center"),
                    "lat": p_lat,
                    "lon": p_lon,
                    "duration": "2 hours",
                    "reason": f"Popular verified location in {city_clean} via OpenStreetMap."
                })

            if len(live_places) >= 2:
                if interests:
                    live_places.sort(key=lambda p: any(i.lower() in p["category"].lower() for i in interests), reverse=True)

                res = normalize_response(
                    status="success",
                    source="LIVE PLACES (OpenStreetMap)",
                    data=live_places[:8],
                    message=f"Fetched live verified places for {city_clean}"
                )
                _PLACES_CACHE[cache_key] = res
                return res
    except Exception:
        pass

    fallback_res = DynamicCityEstimator.get_fallback_places(city_clean)
    places_data = fallback_res["data"]

    if interests:
        places_data.sort(key=lambda p: any(i.lower() in p["category"].lower() for i in interests), reverse=True)

    fallback_res["data"] = places_data
    _PLACES_CACHE[cache_key] = fallback_res
    return fallback_res
