import requests
import json
from datetime import datetime, timedelta, timezone

# Συντεταγμένες για Γήλοφο
LAT, LON = 40.06, 21.80
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,wind_direction_10m&timezone=auto"

def get_weather():
    try:
        response = requests.get(URL)
        data = response.json()
        if response.status_code == 200:
            current = data["current"]
            # Ώρα Ελλάδος
            current_time = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%H:%M:%S")
            pressure = round(current["pressure_msl"], 1)

            # Λογική Alert: Κάτω από 1007 = ΕΠΙΔΕΙΝΩΣΗ ΚΑΙΡΟΥ
            if pressure < 1007:
                status = "ΕΠΙΔΕΙΝΩΣΗ ΚΑΙΡΟΥ"
            else:
                status = "ΚΑΙΡΟΣ ΣΤΑΘΕΡΟΣ"

            weather_data = {
                "temperature": round(current["temperature_2m"], 1),
                "humidity": current["relative_humidity_2m"],
                "pressure": pressure,
                "status": status,
                "wind_speed": round(current["wind_speed_10m"], 1),
                "last_update": current_time
            }
            
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_data, f, ensure_ascii=False, indent=4)
            print(f"Ενημέρωση: {status} ({pressure} hPa)")
    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather()
