from typing import Dict, Any, List
from services.data_normalizer import normalize_response

METRO_CITIES = {"tokyo", "paris", "london", "new york", "delhi", "singapore", "kyoto", "mumbai", "berlin"}

def get_rental_options(
    destination: str,
    num_people: int = 2,
    num_days: int = 3,
    budget: float = 20000
) -> Dict[str, Any]:
    """
    Calculates car, bike, and transit rental options for local commuting in destination.
    Provides estimated daily costs, totals, and group suitability.
    """
    city_clean = destination.strip().title()
    dest_lower = city_clean.lower()

    # Car Rental Estimates
    hatchback_daily = 1600
    suv_daily = 2800
    
    # Bike Rental Estimates
    scooter_daily = 450
    royal_enfield_daily = 900

    car_recommended = suv_daily if num_people > 4 else hatchback_daily
    car_model = "7-Seater SUV (Ertiga/Innova)" if num_people > 4 else "5-Seater Hatchback/Sedan (Swift/i20)"
    car_total = car_recommended * num_days

    # Bikes required
    bikes_needed = (num_people + 1) // 2
    scooter_total = (scooter_daily * bikes_needed) * num_days

    rentals = []

    if dest_lower in METRO_CITIES:
        metro_pass_daily = 350
        metro_total = (metro_pass_daily * num_people) * num_days
        rentals.append({
            "vehicle_type": "🚇 Unlimited Metro & Transit Pass",
            "model": f"{city_clean} Travel Tourist Pass ({num_people} pass{'es' if num_people>1 else ''})",
            "daily_rate": f"₹{metro_pass_daily:,}/day per person",
            "total_estimated": f"₹{metro_total:,}",
            "suitable_group_size": "Unlimited travelers",
            "reason": f"Fastest, most economical way to beat traffic in {city_clean} with direct access to major attractions.",
            "is_recommended": True
        })

    rentals.append({
        "vehicle_type": "🚗 Car Rental (Self-Drive)",
        "model": car_model,
        "daily_rate": f"₹{car_recommended:,}/day",
        "total_estimated": f"₹{car_total:,}",
        "suitable_group_size": f"Up to {7 if num_people > 4 else 5} people",
        "reason": f"Ideal for comfortable group sightseeing across {city_clean} with luggage and AC comfort.",
        "is_recommended": (dest_lower not in METRO_CITIES and num_people >= 3)
    })

    rentals.append({
        "vehicle_type": "🏍️ Scooter / Gearless Bike",
        "model": f"Honda Activa / Vespa ({bikes_needed} bike{'s' if bikes_needed>1 else ''} needed)",
        "daily_rate": f"₹{scooter_daily:,}/day per bike",
        "total_estimated": f"₹{scooter_total:,}",
        "suitable_group_size": "1-2 people per scooter",
        "reason": "Perfect for budget travelers, quick parking, and navigating narrow coastal or city lanes.",
        "is_recommended": (dest_lower not in METRO_CITIES and num_people <= 2)
    })

    rentals.append({
        "vehicle_type": "🏍️ Cruiser Bike",
        "model": f"Royal Enfield Classic 350 ({bikes_needed} bike{'s' if bikes_needed>1 else ''} needed)",
        "daily_rate": f"₹{royal_enfield_daily:,}/day per bike",
        "total_estimated": f"₹{(royal_enfield_daily * bikes_needed) * num_days:,}",
        "suitable_group_size": "1-2 people per bike",
        "reason": "Great for scenic highway rides and thrill-seeking road trips.",
        "is_recommended": False
    })

    recommended = next((r for r in rentals if r.get("is_recommended")), rentals[0])

    return normalize_response(
        status="success",
        source="LOCATION MATCHED COMMUTE OPTIONS",
        data={
            "destination": city_clean,
            "duration_days": num_days,
            "rentals": rentals,
            "recommended_choice": recommended
        },
        message=f"Commute estimates generated for {city_clean}"
    )
