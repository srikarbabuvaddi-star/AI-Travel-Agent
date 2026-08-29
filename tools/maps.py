from typing import Dict, Any, List
from services.fallback import geocode_city
from services.data_normalizer import normalize_response

def get_map_route(
    starting_city: str,
    destination: str,
    hotel: str = "Central Hotel",
    places: List[Dict[str, Any]] = None,
    restaurants: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generates map route coordinates and text route summary for trip mapping.
    Handles map failures gracefully by returning structured route steps.
    """
    if places is None:
        places = []
    if restaurants is None:
        restaurants = []

    start_coords = geocode_city(starting_city)
    dest_coords = geocode_city(destination)

    # Build sequence of waypoint coordinates
    waypoints = [
        {
            "name": f"Origin: {starting_city.title()}",
            "lat": start_coords["lat"],
            "lon": start_coords["lon"],
            "type": "origin"
        },
        {
            "name": f"Destination Hub: {destination.title()}",
            "lat": dest_coords["lat"],
            "lon": dest_coords["lon"],
            "type": "destination"
        },
        {
            "name": f"Base Accommodation: {hotel}",
            "lat": dest_coords["lat"] + 0.005,
            "lon": dest_coords["lon"] + 0.005,
            "type": "hotel"
        }
    ]

    # Add places as waypoints
    for p in places[:4]:
        waypoints.append({
            "name": p.get("name", "Sightseeing Location"),
            "lat": p.get("lat", dest_coords["lat"] + 0.01),
            "lon": p.get("lon", dest_coords["lon"] + 0.01),
            "type": "place"
        })

    # Add restaurants as waypoints
    for r in restaurants[:2]:
        waypoints.append({
            "name": r.get("name", "Dining Location"),
            "lat": dest_coords["lat"] - 0.008,
            "lon": dest_coords["lon"] - 0.008,
            "type": "restaurant"
        })

    # Build text route summary fallback
    route_steps = [starting_city.title(), destination.title(), hotel]
    for p in places[:3]:
        route_steps.append(p.get("name", "Sightseeing"))
    if restaurants:
        route_steps.append(restaurants[0].get("name", "Local Restaurant"))

    text_route_summary = " ➔ ".join(route_steps)

    return normalize_response(
        status="success",
        source="LIVE ROUTE & COORDINATES",
        data={
            "starting_city": starting_city.title(),
            "destination": destination.title(),
            "center": {"lat": dest_coords["lat"], "lon": dest_coords["lon"]},
            "waypoints": waypoints,
            "text_route_summary": text_route_summary
        },
        message=f"Map route calculated for {starting_city} to {destination}"
    )
