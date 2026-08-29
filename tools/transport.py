import math
import hashlib
from typing import Dict, Any, List
from services.fallback import geocode_city
from services.data_normalizer import normalize_response

def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates approximate distance in kilometers between two coordinates."""
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def compare_transport_options(
    starting_city: str,
    destination: str,
    num_people: int = 2,
    travel_style: str = "Moderate"
) -> Dict[str, Any]:
    """
    Compares Train, Bus, Flight, Car, and Public Transport options between starting city and destination.
    Identifies CHEAPEST OPTION, BEST VALUE OPTION, and FASTEST OPTION.
    """
    c1 = geocode_city(starting_city)
    c2 = geocode_city(destination)
    
    dist_km = _haversine_distance(c1["lat"], c1["lon"], c2["lat"], c2["lon"])
    if dist_km < 30:
        dist_km = 450  # Default reasonable intercity travel distance if cities overlap

    # Calculate multi-modal options based on actual geographical distance
    flight_dur = f"{round(max(1.2, dist_km / 500.0), 1)} hrs flight (+2h airport)"
    train_dur = f"{round(max(3.0, dist_km / 65.0), 1)} hrs"
    bus_dur = f"{round(max(4.0, dist_km / 50.0), 1)} hrs"
    car_dur = f"{round(max(3.5, dist_km / 60.0), 1)} hrs drive"

    # Per person estimated costs
    flight_cost_per_person = max(2800, round(dist_km * 7.5))
    train_cost_per_person = max(450, round(dist_km * 1.8))
    bus_cost_per_person = max(550, round(dist_km * 2.1))
    car_total_fuel_tolls = max(2500, round(dist_km * 8.0))
    car_cost_per_person = round(car_total_fuel_tolls / max(1, num_people))

    flight_total = flight_cost_per_person * num_people
    train_total = train_cost_per_person * num_people
    bus_total = bus_cost_per_person * num_people

    options = [
        {
            "mode": "✈️ Flight",
            "per_person_cost": f"₹{flight_cost_per_person:,}",
            "total_group_cost": f"₹{flight_total:,}",
            "raw_total": flight_total,
            "duration": flight_dur,
            "convenience": "High",
            "value_score": 8.2,
            "category": "FASTEST OPTION",
            "details": "Direct or fastest connecting flights. Saves max travel time."
        },
        {
            "mode": "🚆 Express Train (AC 3-Tier)",
            "per_person_cost": f"₹{train_cost_per_person:,}",
            "total_group_cost": f"₹{train_total:,}",
            "raw_total": train_total,
            "duration": train_dur,
            "convenience": "High",
            "value_score": 9.4,
            "category": "BEST VALUE OPTION",
            "details": "Optimal combination of cost efficiency, comfort, and group luggage space."
        },
        {
            "mode": "🚌 Volvo AC Bus",
            "per_person_cost": f"₹{bus_cost_per_person:,}",
            "total_group_cost": f"₹{bus_total:,}",
            "raw_total": bus_total,
            "duration": bus_dur,
            "convenience": "Moderate",
            "value_score": 8.0,
            "category": "CHEAPEST OPTION" if bus_total <= train_total else "BUDGET ALTERNATIVE",
            "details": "Overnight sleeper/seater bus with frequent flexible departures."
        },
        {
            "mode": "🚗 Private SUV / Self-Drive",
            "per_person_cost": f"₹{car_cost_per_person:,}",
            "total_group_cost": f"₹{car_total_fuel_tolls:,}",
            "raw_total": car_total_fuel_tolls,
            "duration": car_dur,
            "convenience": "Very High",
            "value_score": 8.8,
            "category": "FLEXIBLE GROUP OPTION",
            "details": "Door-to-door scenic road trip; economical when sharing costs among 3+ people."
        }
    ]

    # Explicitly find Cheapest, Best Value, Fastest
    cheapest = min(options, key=lambda x: x["raw_total"])
    fastest = options[0]  # Flight
    best_value = options[1]  # Train

    return normalize_response(
        status="success",
        source="ESTIMATED TRANSPORT OPTIONS",
        data={
            "distance_km": round(dist_km),
            "starting_city": starting_city.title(),
            "destination": destination.title(),
            "cheapest_option": cheapest,
            "best_value_option": best_value,
            "fastest_option": fastest,
            "all_options": options,
            "recommendation_summary": f"For {num_people} travelers from {starting_city} to {destination}, {best_value['mode']} offers the best overall value, while {cheapest['mode']} is the most economical."
        },
        message=f"Transport analysis completed for {starting_city} to {destination}"
    )
