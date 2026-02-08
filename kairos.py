import requests
import json
from datetime import datetime, timedelta, timezone

# Συντεταγμένες για Γήλοφο Γρεβενών
LAT = 40.06
LON = 21.80

# URL για Open-Meteo (Προστέθηκε το pressure_msl για σωστή πίεση)
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,wind_direction_10m&timezone=auto"

def get_weather():
    try:
        response = requests.get(URL)
        data = response.json()

        if response.status_code == 200:
            current = data["current"]
            
            # 1. Ώρα 24ωρη με δευτερόλεπτα για την Ελλάδα
            current_time = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%H:%M:%S")

            # 2. Σωστή Πίεση & Alert
            sea_level_pressure = round(current["pressure_msl"], 1)
            
            if sea_level_pressure < 1007:
                alert = "⚠️ Άστατος / Χαμηλή Πίεση"
            elif sea_level_pressure > 1022:
                alert = "☀️ Σταθερός / Υψηλή Πίεση"
            else:
                alert = "✅ Κανονικές Συνθήκες"

            # 3. Δημιουργία του JSON με όλα τα στοιχεία
            weather_data = {
                "temperature": round(current["temperature_2m"], 1),
                "humidity": current["relative_humidity_2m"],
                "pressure": sea_level_pressure,
                "altitude": 1000,
                "wind_speed": round(current["wind_speed_10m"], 1),
                "wind_dir": current["wind_direction_10m"],
                "description": alert,
                "last_update": current_time
            }

            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
            print(f"Ενημερώθηκε στις {current_time} | Πίεση: {sea_level_pressure}")

    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather()
