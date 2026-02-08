import requests
import json
from datetime import datetime, timedelta, timezone

# Συντεταγμένες για Γήλοφο Γρεβενών
LAT = 40.06
LON = 21.80

# URL με όλα τα απαραίτητα δεδομένα (Temp, Humidity, Pressure, Wind)
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,wind_direction_10m,weather_code&timezone=auto"

def get_weather():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            current = data["current"]
            
            # Ώρα Ελλάδας
            current_time = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%H:%M")
            sea_level_pressure = round(current["pressure_msl"], 1)

            # --- ΥΠΟΛΟΓΙΣΜΟΣ STATUS (ALERT) ---
            # Το ονομάζουμε "status" για να το διαβάζει το index.html
            if sea_level_pressure < 1007:
                st = "⚠️ Άστατος Καιρός"
            elif sea_level_pressure > 1025:
                st = "☀️ Σταθερός Καιρός"
            else:
                st = "✅ Καιρός Σταθερός"

            # ΤΟ ΠΛΗΡΕΣ JSON ΠΟΥ ΧΡΕΙΑΖΕΤΑΙ Η ΜΠΛΕ ΣΕΛΙΔΑ
            weather_info = {
                "temperature": round(current["temperature_2m"], 1),
                "humidity": current["relative_humidity_2m"],
                "pressure": sea_level_pressure,
                "wind_speed": round(current["wind_speed_10m"], 1),
                "wind_dir": current["wind_direction_10m"],
                "status": st,
                "last_update": current_time,
                "description": "Μετεωρολογικός Σταθμός Γηλόφου"
            }

            # Εγγραφή στο αρχείο data.json
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_info, f, ensure_ascii=False, indent=4)
            
            print(f"Ενημέρωση Ολοκληρώθηκε: {current_time} | Πίεση: {sea_level_pressure}")
        else:
            print(f"Σφάλμα API: {response.status_code}")
    except Exception as e:
        print(f"Σφάλμα κατά την εκτέλεση: {e}")

if __name__ == "__main__":
    get_weather()
