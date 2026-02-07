import requests
import json
from datetime import datetime, timedelta, timezone

# Συντεταγμένες για Γήλοφο Γρεβενών
LAT = 40.06
LON = 21.80
# Προσθέσαμε wind_speed_10m και wind_direction_10m για να βλέπουμε τον άνεμο
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m&timezone=auto"

def get_weather():
    try:
        response = requests.get(URL)
        data = response.json()

        if response.status_code == 200:
            current = data["current"]
            
            # Αυτόματη Ώρα Ελλάδας (ανιχνεύει μόνη της αν είναι +2 ή +3)
            now = datetime.now()
            # Στο GitHub Actions η ώρα είναι UTC, οπότε προσθέτουμε 2 ώρες για χειμερινή
            current_time = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%H:%M:%S")

            # Υπολογισμός πίεσης στη θάλασσα (MSL)
            # Ο Γήλοφος είναι στα ~1000μ, οπότε η διόρθωση +115 έως +118 hPa είναι σωστή
            sea_level_pressure = round(current["surface_pressure"] + 116)

            weather_info = {
                "temp": round(current["temperature_2m"], 1),
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
            print(f"Θερμοκρασία: {current['temperature_2m']}°C | Άνεμος: {current['wind_speed_10m']} km/h")
        else:
            print(f"API Error: {response.status_code}")
    except Exception as e:
        print(f"Σφάλμα κατά την εκτέλεση: {e}")

if __name__ == "__main__":
    get_weather()
