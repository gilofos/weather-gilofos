import requests
import json
from datetime import datetime, timedelta, timezone

# Συντεταγμένες για Γήλοφο Γρεβενών
LAT = 40.06
LON = 21.80

# URL για Open-Meteo
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m&timezone=auto"

def get_weather():
    try:
        response = requests.get(URL)
        data = response.json()

        if response.status_code == 200:
            current = data["current"]
            
            # Ώρα Ελλάδας για το GitHub Actions
            current_time = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%H:%M:%S")

            # Υπολογισμός πίεσης στη θάλασσα (MSL) - Γήλοφος ~1000μ
            sea_level_pressure = round(current["surface_pressure"] + 116,1)

            # ΤΟ JSON ΠΟΥ ΘΑ ΔΙΑΒΑΖΕΙ ΤΟ INDEX.HTML
            weather_info = {
                "temperature": round(current["temperature_2m"], 1),
                "humidity": current["relative_humidity_2m"],
                "pressure": sea_level_pressure,
                "wind_speed": round(current["wind_speed_10m"], 1),
                "wind_dir": current["wind_direction_10m"],
                "description": "Live από Γήλοφο",
                "last_update": current_time
            }

            # Αποθήκευση στο data.json
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_info, f, ensure_ascii=False, indent=4)
            
            print(f"Ενημέρωση ολοκληρώθηκε: {current_time}")
            print(f"Θερμοκρασία: {current['temperature_2m']}°C | Πίεση: {sea_level_pressure} hPa")
        else:
            print(f"API Error: {response.status_code}")
    except Exception as e:
        print(f"Σφάλμα κατά την εκτέλεση: {e}")

if __name__ == "__main__":
    get_weather()

