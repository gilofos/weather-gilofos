import requests
import json
from datetime import datetime, timedelta, timezone

LAT = 40.06
LON = 21.80
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,apparent_temperature,relative_humidity_2m,pressure_msl,wind_speed_10m,wind_direction_10m,weather_code&hourly=temperature_2m,weather_code&timezone=auto&forecast_days=1"

def get_weather_icon(code):
    mapping = {0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️", 45: "🌫️", 48: "🌫️", 51: "🌦️", 53: "🌦️", 55: "🌦️", 61: "🌧️", 63: "🌧️", 65: "🌧️", 71: "❄️", 73: "❄️", 75: "❄️", 95: "⛈️"}
    return mapping.get(code, "🌡️")

def get_weather():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            current = data["current"]
            current_time = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%H:%M:%S")
            sea_level_pressure = round(current["pressure_msl"], 1)

            # Υπολογισμός Alert / Status
            if sea_level_pressure < 1007:
                st = "⚠️ Χαμηλή πίεση - Άστατος καιρός"
            elif sea_level_pressure > 1025:
                st = "☀️ Υψηλή πίεση - Σταθερότητα"
            else:
                st = "✅ Καιρός Σταθερός"

            weather_info = {
                "temperature": round(current["temperature_2m"], 1),
                "pressure": sea_level_pressure,
                "status": st,  # Εδώ είναι το κλειδί που ζητάει το index.html
                "last_update": current_time
            }

            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_info, f, ensure_ascii=False, indent=4)
            
            print(f"OK: {current_time}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_weather()
