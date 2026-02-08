import requests
import json
import os
from datetime import datetime, timedelta, timezone

# --- ΡΥΘΜΙΣΕΙΣ ΣΤΑΘΜΟΥ ΓΗΛΟΦΟΥ ---
LAT = 40.06
LON = 21.80

# ΔΙΟΡΘΩΣΗ ΠΙΕΣΗΣ ΓΙΑ ΤΟ ΥΨΟΜΕΤΡΟ (1050m)
# Προσθέτουμε ~125 hPa στην τοπική πίεση (surface pressure) 
# για να έχουμε την πίεση στη στάθμη της θάλασσας (MSL).
PRESSURE_CORRECTION = 125 

# URL για την άντληση δεδομένων από το Open-Meteo
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,weathercode&timezone=auto"

def get_weather():
    try:
        # Κλήση στο API
        response = requests.get(URL, timeout=10)
        data = response.json()

        if response.status_code == 200:
            current = data["current"]
            
            # Υπολογισμός Ώρας Ελλάδας (UTC+2)
            now = datetime.now(timezone.utc) + timedelta(hours=2)
            current_time = now.strftime("%H:%M:%S")

            # Υπολογισμός πίεσης στη στάθμη της θάλασσας (MSL)
            sea_level_pressure = round(current["surface_pressure"] + PRESSURE_CORRECTION)

            # ΛΟΓΙΚΗ ALERT (ΕΠΙΔΕΙΝΩΣΗ ΚΑΙΡΟΥ)
            # Ενεργοποιείται αν η πίεση πέσει κάτω από 1000 hPa ή ο άνεμος > 30 km/h
            is_alert = False
            if sea_level_pressure < 1000 or current["wind_speed_10m"] > 30:
                is_alert = True

            # Δημιουργία του αντικειμένου δεδομένων
            weather_info = {
                "temperature": round(current["temperature_2m"], 1),
                "humidity": current["relative_humidity_2m"],
                "pressure": sea_level_pressure,
                "wind_speed": round(current["wind_speed_10m"], 1),
                "last_update": current_time,
                "alert": is_alert,
                "weather_code": current["weathercode"]
            }

            # Αποθήκευση στο αρχείο data.json
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_info, f, ensure_ascii=False, indent=4)
            
            print(f"Επιτυχής ενημέρωση: {current_time} | Πίεση: {sea_level_pressure} hPa")
        
        else:
            print(f"Σφάλμα API: {response.status_code}")

    except Exception as e:
        print(f"Σφάλμα κατά την εκτέλεση του script: {e}")

if __name__ == "__main__":
    get_weather()
