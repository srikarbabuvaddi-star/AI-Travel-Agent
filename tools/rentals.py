from typing import Dict, Any, List
from services.data_normalizer import normalize_response

def get_rental_options(
    destination: str,
    num_people: int = 2,
    num_days: int = 3,
    budget: float = 20000
) -> Dict[str, Any]:
    """
    Calculates car and bike rental options for local commuting in destination.
    Provides estimated daily costs, totals, and group suitability.
    """
    city_clean = destination.strip().title()

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

    rentals = [
        {
            "vehicle_type": "🚗 Car Rental (Self-Drive)",
            "model": car_model,
            "daily_rate": f"₹{car_recommended:,}/day",
            "total_estimated": f"₹{car_total:,}",
            "suitable_group_size": f"Up to {7 if num_people > 4 else 5} people",
            "reason": f"Ideal for comfortable group sightseeing across {city_clean} with luggage and AC comfort.",
            "is_recommended": num_people >= 3
        },
        {
            "vehicle_type": "🏍️ Scooter / Gearless Bike",
            "model": f"Honda Activa / Vespa ({bikes_needed} bike{'s' if bikes_needed>1 else ''} needed)",
            "daily_rate": f"₹{scooter_daily:,}/day per bike",
            "total_estimated": f"₹{scooter_total:,}",
            "suitable_group_size": "1-2 people per scooter",
            "reason": "Perfect for budget travelers, quick parking, and navigating narrow coastal or city lanes.",
            "is_recommended": num_people <= 2
        },
        {
            "vehicle_type": "🏍️ Cruiser Bike",
            "model": f"Royal Enfield Classic 350 ({bikes_needed} bike{'s' if bikes_needed>1 else ''} needed)",
            "daily_rate": f"₹{royal_enfield_daily:,}/day per bike",
            "total_estimated": f"₹{(royal_enfield_daily * bikes_needed) * num_days:,}",
            "suitable_group_size": "1-2 people per bike",
            "reason": "Great for scenic highway rides and thrill-seeking road trips.",
            "is_recommended": False
        }
    ]

    return normalize_response(
        status="success",
        source="ESTIMATED RENTAL OPTIONS",
        data={
            "destination": city_clean,
            "duration_days": num_days,
            "rentals": rentals,
            "recommended_choice": rentals[0] if num_people >= 3 else rentals[1]
        },
        message=f"Rental estimates generated for {city_clean}"
    )
