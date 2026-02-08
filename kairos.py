import requests
import json
from datetime import datetime, timedelta, timezone

# Συντεταγμένες για Γήλοφο
LAT, LON = 40.06, 21.80

# Χρησιμοποιούμε το pressure_msl για πίεση στη θάλασσα
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m&timezone=auto"

def get_weather():
    try:
        response = requests.get(URL, timeout=15)
        if response.status_code == 200:
            data = response.json()["current"]
            
            # Ώρα Ελλάδος (UTC+2) - Το GitHub Actions τρέχει σε UTC
            now_gr = datetime.now(timezone.utc) + timedelta(hours=2)
            current_time = now_gr.strftime("%H:%M:%S")
            
            pressure = round(data["pressure_msl"], 1)

            # Λογική ειδοποίησης
            if pressure < 1007:
                status = "ΕΠΙΔΕΙΝΩΣΗ ΚΑΙΡΟΥ"
            else:
                status = "ΚΑΙΡΟΣ ΣΤΑΘΕΡΟΣ"

            # Δημιουργία των δεδομένων για την HTML
            weather_data = {
                "temperature": round(data["temperature_2m"], 1),
                "humidity": data["relative_humidity_2m"],
                "pressure": pressure,
                "status": status,
                "wind_speed": round(data["wind_speed_10m"], 1),
                "last_update": current_time
            }
            
            # Αποθήκευση στο data.json
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
            print(f"Ενημέρωση GitHub OK: {current_time}")
        else:
            print(f"Σφάλμα API: {response.status_code}")
    except Exception as e:
        print(f"Σφάλμα κατά την εκτέλεση: {e}")

if __name__ == "__main__":
    get_weather()
