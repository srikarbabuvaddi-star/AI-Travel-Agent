import requests
import datetime
import functools
from typing import Dict, Any, List
from services.fallback import geocode_city
from services.data_normalizer import normalize_response
from config import Config

WMO_WEATHER_CODES = {
    0: ("☀️ Clear Sky", "Ideal for all outdoor sightseeing and photography."),
    1: ("🌤️ Mainly Clear", "Great weather for beach visits, walking tours, and outdoor forts."),
    2: ("⛅ Partly Cloudy", "Pleasant climate suitable for outdoor exploring."),
    3: ("☁️ Overcast", "Good for sightseeing; mild temperatures expected."),
    45: ("🌫️ Foggy", "Cool and misty; exercise caution on mountain highways."),
    48: ("🌫️ Frost Fog", "Cold misty weather; warm clothing recommended."),
    51: ("🌦️ Light Drizzle", "Carry an umbrella or raincoat; indoor activities suggested for afternoon."),
    53: ("🌧️ Moderate Rain", "Expect showers; focus on museums, indoor markets, and dining."),
    61: ("🌧️ Slight Rain", "Intermittent rain showers; carry rain gear."),
    63: ("🌧️ Heavy Rain", "High rainfall expected; indoor attractions recommended."),
    80: ("🌦️ Rain Showers", "Passing showers; keep flexible outdoor schedules."),
    95: ("⛈️ Thunderstorm", "Stay indoors during peak thunderstorm hours.")
}

# In-memory LRU Cache for ultra-fast response
_WEATHER_CACHE = {}

def get_weather_forecast(destination: str, start_date_str: str, end_date_str: str) -> Dict[str, Any]:
    """
    Fetches real-time weather forecast from Open-Meteo API with caching and fast fallback.
    """
    cache_key = f"{destination.strip().lower()}_{start_date_str}_{end_date_str}"
    if cache_key in _WEATHER_CACHE:
        return _WEATHER_CACHE[cache_key]

    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except Exception:
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=4)

    num_days = max(1, (end_date - start_date).days + 1)
    coords = geocode_city(destination)
    lat, lon = coords["lat"], coords["lon"]

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode&timezone=auto"
    
    try:
        resp = requests.get(url, timeout=1.5)
        if resp.status_code == 200:
            raw_data = resp.json()
            if "daily" in raw_data:
                daily = raw_data["daily"]
                time_list = daily.get("time", [])
                t_max = daily.get("temperature_2m_max", [])
                t_min = daily.get("temperature_2m_min", [])
                p_prob = daily.get("precipitation_probability_max", [])
                w_codes = daily.get("weathercode", [])

                daily_forecasts = []
                for i in range(min(num_days, len(time_list))):
                    d_str = time_list[i]
                    max_t = round(t_max[i]) if i < len(t_max) and t_max[i] is not None else 30
                    min_t = round(t_min[i]) if i < len(t_min) and t_min[i] is not None else 22
                    rain_p = p_prob[i] if i < len(p_prob) and p_prob[i] is not None else 15
                    code = w_codes[i] if i < len(w_codes) and w_codes[i] is not None else 0

                    cond, rec = WMO_WEATHER_CODES.get(code, ("⛅ Partly Cloudy", "Good weather for general travel."))

                    if rain_p > 50:
                        rec = "Indoor activities recommended due to high rain probability."
                    elif max_t > 34:
                        rec = "Hot temperatures. Plan outdoor sightseeing during early morning or late afternoon."

                    daily_forecasts.append({
                        "day": f"Day {i+1}",
                        "date": d_str,
                        "condition": cond,
                        "min_temp": f"{min_t}°C",
                        "max_temp": f"{max_t}°C",
                        "rain_prob": f"{rain_p}%",
                        "recommendation": rec
                    })

                if daily_forecasts:
                    res = normalize_response(
                        status="success",
                        source="Live forecast",
                        data=daily_forecasts,
                        message=f"Live weather forecast obtained for {destination}"
                    )
                    _WEATHER_CACHE[cache_key] = res
                    return res
    except Exception:
        pass

    # Fallback planning forecast
    fallback_forecasts = []
    curr_date = start_date
    for i in range(num_days):
        day_num = i + 1
        min_t = 22 + (i % 3)
        max_t = 30 + (i % 4)
        rain_p = 10 + ((i * 15) % 40)
        
        cond = "🌤️ Partly Cloudy"
        rec = "Good for outdoor sightseeing and general activities."
        if rain_p > 35:
            cond = "🌧️ Light Showers Likely"
            rec = "Keep an umbrella handy; great for visiting indoor museums and cafes."

        fallback_forecasts.append({
            "day": f"Day {day_num}",
            "date": curr_date.strftime("%Y-%m-%d"),
            "condition": cond,
            "min_temp": f"{min_t}°C",
            "max_temp": f"{max_t}°C",
            "rain_prob": f"{rain_p}%",
            "recommendation": rec
        })
        curr_date += datetime.timedelta(days=1)

    res = normalize_response(
        status="partial",
        source="Forecast unavailable — using planning estimate",
        data=fallback_forecasts,
        message=f"Live weather API unreachable. Using planning weather model for {destination}"
    )
    _WEATHER_CACHE[cache_key] = res
    return res
