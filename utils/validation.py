import datetime
from typing import Tuple, Optional

def validate_trip_inputs(
    destination: str,
    starting_city: str,
    start_date: datetime.date,
    end_date: datetime.date,
    num_people: int,
    budget: float
) -> Tuple[bool, Optional[str]]:
    """
    Validates form inputs for trip planning.
    Returns (is_valid, error_message).
    """
    if not destination or not destination.strip():
        return False, "Please enter a valid Destination city."

    if not starting_city or not starting_city.strip():
        return False, "Please enter a valid Starting City."

    if end_date < start_date:
        return False, "End date cannot be earlier than start date."

    if num_people < 1:
        return False, "Number of travelers must be at least 1."

    if budget <= 0:
        return False, "Total budget must be greater than 0."

    return True, None
