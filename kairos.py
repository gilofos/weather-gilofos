import requests
import json
from datetime import datetime, timedelta, timezone

# Συντεταγμένες για Γήλοφο Γρεβενών
LAT = 40.06
LON = 21.80

# URL για Open-Meteo (Προστέθηκε το pressure_msl για ακρίβεια)
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,apparent_temperature,relative_humidity_2m,pressure_msl,wind_speed_10m,wind_direction_10m,weather_code&hourly=temperature_2m,weather_code&timezone=auto&forecast_days=1"

def get_weather_icon(code):
    mapping = {
        0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️", 
        45: "🌫️", 48: "🌫️", 
        51: "🌦️", 53: "🌦️", 55: "🌦️",
        61: "🌧️", 63: "🌧️", 65: "🌧️",
        71: "❄️", 73: "❄️", 75: "❄️",
        95: "⛈️"
    }
    return mapping.get(code, "🌡️")

def get_weather():
    try:
        response = requests.get(URL)
        data = response.json()

        if response.status_code == 200:
            current = data["current"]
            hourly = data["hourly"]
            
            # Ώρα Ελλάδας
            current_time = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%H:%M:%S")

            # Πίεση στη θάλασσα (MSL) - Πιο ακριβές για το υψόμετρο του Γηλόφου
            sea_level_pressure = round(current["pressure_msl"], 1)

            # --- ΤΟ ALERT ΠΟΥ ΗΘΕΛΕΣ ---
            if sea_level_pressure < 1007:
                alert_text = "⚠️ ΠΡΟΣΟΧΗ: Χαμηλή πίεση - Καιρός άστατος!"
            elif sea_level_pressure > 1025:
                alert_text = "☀️ Υψηλή πίεση - Σταθερός καιρός"
            else:
                alert_text = "✅ Καιρός Σταθερός"

            # Δημιουργία λίστας πρόγνωσης ανά 3 ώρες
            forecast_24h = []
            for i in range(0, 24, 3):
                forecast_24h.append({
                    "time": hourly["time"][i][-5:], 
                    "temp": round(hourly["temperature_2m"][i], 1),
                    "icon": get_weather_icon(hourly["weather_code"][i])
                })

            # ΤΟ JSON ΣΟΥ (Με τα αρχικά ονόματα για να μη χαλάσει η σελίδα)
            weather_info = {
                "temperature": round(current["temperature_2m"], 1),
                "feels_like": round(current["apparent_temperature"], 1),
                "icon": get_weather_icon(current["weather_code"]),
                "humidity": current["relative_humidity_2m"],
                "pressure": sea_level_pressure,
                "wind_speed": round(current["wind_speed_10m"], 1),
                "wind_dir": current["wind_direction_10m"],
                "description": "Live από Γήλοφο",
                "alert": alert_text,  # Προσθήκη alert
                "last_update": current_time,
                "forecast": forecast_24h
            }

            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_info, f, ensure_ascii=False, indent=4)
            
            print(f"Ενημέρωση ολοκληρώθηκε: {current_time} | Πίεση: {sea_level_pressure}")
        else:
            print(f"API Error: {response.status_code}")
    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather()
