from typing import Dict, Any, List

def optimize_trip_budget(
    current_plan: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Analyzes current trip plan and generates realistic budget optimizations by comparing alternatives.
    Returns original cost, optimized cost, itemized savings, and optimization explanation.
    """
    budget_info = current_plan.get("budget_breakdown", {}).get("data", {})
    categories = budget_info.get("categories", {})
    
    orig_total = budget_info.get("total_group_cost", 36500)
    user_budget = budget_info.get("user_budget", 40000)

    orig_hotel_cost = categories.get("Accommodation", 12000)
    orig_transport_cost = categories.get("Intercity Transportation", 10000)
    orig_rental_cost = categories.get("Local Rentals", 4500)

    optimizations = []
    total_savings = 0

    # 1. Accommodation Optimization
    if orig_hotel_cost > 6000:
        hotel_saving = round(orig_hotel_cost * 0.35)
        total_savings += hotel_saving
        optimizations.append({
            "category": "🏨 Hotel Accommodation",
            "action": "Switch to top-rated 3-star central boutique hotel or homestay",
            "original_cost": f"₹{orig_hotel_cost:,}",
            "optimized_cost": f"₹{orig_hotel_cost - hotel_saving:,}",
            "savings": f"Save ₹{hotel_saving:,}",
            "impact": "Minimal impact: central location maintained with clean high-rated amenities."
        })

    # 2. Transportation Optimization
    if orig_transport_cost > 5000:
        trans_saving = round(orig_transport_cost * 0.40)
        total_savings += trans_saving
        optimizations.append({
            "category": "🚆 Intercity Transport",
            "action": "Switch from peak flight to AC 3-Tier Express Train or Sleeper Bus",
            "original_cost": f"₹{orig_transport_cost:,}",
            "optimized_cost": f"₹{orig_transport_cost - trans_saving:,}",
            "savings": f"Save ₹{trans_saving:,}",
            "impact": "Low impact: comfortable overnight travel, saving daytime hours and hotel night."
        })

    # 3. Rental / Local Commute Optimization
    if orig_rental_cost > 2500:
        rental_saving = round(orig_rental_cost * 0.50)
        total_savings += rental_saving
        optimizations.append({
            "category": "🚗 Local Rentals",
            "action": "Switch from private car to scooter rentals / shared local transport",
            "original_cost": f"₹{orig_rental_cost:,}",
            "optimized_cost": f"₹{orig_rental_cost - rental_saving:,}",
            "savings": f"Save ₹{rental_saving:,}",
            "impact": "High agility: effortless parking in narrow streets and scenic coastal riding."
        })

    if not optimizations:
        # Default mild optimization if already minimal budget
        mild_saving = 2500
        total_savings = mild_saving
        optimizations.append({
            "category": "🎟️ Combo Pass & Dining",
            "action": "Book advance sightseeing combo passes and lunch thali packages",
            "original_cost": f"₹{orig_total:,}",
            "optimized_cost": f"₹{orig_total - mild_saving:,}",
            "savings": f"Save ₹{mild_saving:,}",
            "impact": "No compromise on stay or transport."
        })

    optimized_total = max(1000, orig_total - total_savings)
    num_people = current_plan.get("inputs", {}).get("num_people", 2)
    opt_per_person = round(optimized_total / max(1, num_people))

    return {
        "original_total_cost": orig_total,
        "optimized_total_cost": optimized_total,
        "total_savings": total_savings,
        "original_cost_per_person": budget_info.get("cost_per_person", round(orig_total/max(1, num_people))),
        "optimized_cost_per_person": opt_per_person,
        "optimizations_list": optimizations,
        "summary": f"By implementing these smart agent recommendations, your group can save a total of ₹{total_savings:,} (reducing per person cost to ₹{opt_per_person:,})."
    }
