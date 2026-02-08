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

            # Υπολογισμός πίεσης στη θάλασσα (MSL) - Γήλοφος 1050μ
            # Η διόρθωση για 1050μ είναι +124.5 hPa (αναγωγή στο επίπεδο της θάλασσας)
            station_pressure = current["surface_pressure"]
            sea_level_pressure = round(station_pressure + 124.5)

            # Λογική Alert (Επιδείνωση)
            # Αν η πίεση πέσει κάτω από 1000 hPa ή ο άνεμος είναι πάνω από 50 km/h
            alert_status = False
            if sea_level_pressure < 1000 or current["wind_speed_10m"] > 50:
                alert_status = True

            # Προετοιμασία δεδομένων για το αρχείο JSON
            weather_data = {
                "temperature": round(current["temperature_2m"], 1),
                "humidity": current["relative_humidity_2m"],
                "pressure": sea_level_pressure,
                "wind_speed": round(current["wind_speed_10m"], 1),
                "last_update": current_time,
                "alert": alert_status,
                "status": "ΕΠΙΔΕΙΝΩΣΗ" if alert_status else "ΟΜΑΛΟΣ ΚΑΙΡΟΣ"
            }

            # Εγγραφή στο data.json
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
            print(f"Ενημέρωση {current_time}: {weather_data['temperature']}°C, {sea_level_pressure} hPa")

    except Exception as e:
        print(f"Σφάλμα κατά την ανάκτηση δεδομένων: {e}")

if __name__ == "__main__":
    get_weather()
