from typing import Dict, Any, List
from services.data_normalizer import normalize_response

def calculate_budget_breakdown(
    user_budget: float,
    num_people: int,
    num_days: int,
    selected_hotel_nightly: float,
    selected_transport_total: float,
    selected_rental_total: float = 0.0,
    travel_style: str = "Moderate"
) -> Dict[str, Any]:
    """
    Calculates detailed itemized budget breakdown, cost per person, and budget status.
    Provides automated savings suggestions if over budget.
    """
    num_nights = max(1, num_days - 1)
    accommodation_total = selected_hotel_nightly * num_nights

    # Daily food estimate per person based on travel style
    daily_food_per_person = 400 if travel_style == "Budget" else (1200 if travel_style == "Luxury" else 750)
    food_total = daily_food_per_person * num_people * num_days

    # Local sightseeing / entry tickets estimate
    activities_total = 350 * num_people * num_days

    # Miscellaneous & emergency reserve (approx 5% of subtotal)
    subtotal = accommodation_total + selected_transport_total + food_total + selected_rental_total + activities_total
    misc_reserve = round(subtotal * 0.05)
    emergency_reserve = round(subtotal * 0.05)

    total_estimated_cost = subtotal + misc_reserve + emergency_reserve
    cost_per_person = round(total_estimated_cost / max(1, num_people))
    remaining_balance = user_budget - total_estimated_cost

    is_within_budget = total_estimated_cost <= user_budget
    status_label = "Within budget ✅" if is_within_budget else "Budget exceeded ⚠️"

    # Savings suggestions
    savings_suggestions = []
    if not is_within_budget:
        excess = abs(remaining_balance)
        savings_suggestions.append(f"⚠️ Your budget is exceeded by ₹{excess:,}. Consider the following optimizations:")
        if selected_hotel_nightly > 2000:
            potential_hotel_save = round((selected_hotel_nightly - 1800) * num_nights)
            savings_suggestions.append(f"• Switch to a budget lodge/homestay: Save ~₹{potential_hotel_save:,}")
        if selected_transport_total > 5000:
            savings_suggestions.append("• Switch intercity travel to AC Express Train or Sleeper Bus: Save ~₹3,500")
        if selected_rental_total > 2000:
            savings_suggestions.append("• Replace private SUV rental with scooter rental or public transit: Save ~₹2,000")
    else:
        savings_suggestions.append(f"✅ Great job! You are ₹{remaining_balance:,} under your allocated budget of ₹{user_budget:,.0f}.")

    breakdown = {
        "user_budget": user_budget,
        "total_group_cost": total_estimated_cost,
        "cost_per_person": cost_per_person,
        "remaining_balance": remaining_balance,
        "status": status_label,
        "is_within_budget": is_within_budget,
        "categories": {
            "Accommodation": accommodation_total,
            "Intercity Transportation": selected_transport_total,
            "Food & Dining": food_total,
            "Local Rentals": selected_rental_total,
            "Activities & Entry Tickets": activities_total,
            "Miscellaneous": misc_reserve,
            "Emergency Reserve": emergency_reserve
        },
        "savings_suggestions": savings_suggestions
    }

    return normalize_response(
        status="success",
        source="ESTIMATED BUDGET CALCULATOR",
        data=breakdown,
        message="Budget calculation and comparison completed."
    )
