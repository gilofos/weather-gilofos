import requests
import json
import os
from datetime import datetime, timedelta, timezone

# --- ΡΥΘΜΙΣΕΙΣ ΣΤΑΘΜΟΥ ΓΗΛΟΦΟΥ ---
LAT = 40.06
LON = 21.80
ALTITUDE_OFFSET = 116  # Διόρθωση πίεσης για υψόμετρο ~1050m (hPa)

# URL για την άντληση δεδομένων από το Open-Meteo
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m,weathercode&timezone=auto"

def get_weather():
    try:
        # Κλήση στο API
        response = requests.get(URL, timeout=10)
        data = response.json()

        if response.status_code == 200:
            current = data["current"]
            
            # Υπολογισμός Ώρας Ελλάδας (UTC+2 ή UTC+3 ανάλογα την εποχή)
            # Για το GitHub Actions χρησιμοποιούμε σταθερή προσθήκη ή το timezone του API
            now = datetime.now(timezone.utc) + timedelta(hours=2)
            current_time = now.strftime("%H:%M:%S")

            # Υπολογισμός πίεσης στη στάθμη της θάλασσας (MSL)
            sea_level_pressure = round(current["surface_pressure"] + ALTITUDE_OFFSET)

            # --- ΛΟΓΙΚΗ ALERT (ΕΠΙΔΕΙΝΩΣΗ ΚΑΙΡΟΥ) ---
            # Ενεργοποιείται αν: 
            # 1. Η πίεση είναι πολύ χαμηλή (< 1000 hPa)
            # 2. Ο άνεμος είναι ισχυρός (> 30 km/h)
            # 3. Ο κωδικός καιρού δείχνει καταιγίδα (weathercode > 60)
            is_alert = False
            if sea_level_pressure < 1000 or current["wind_speed_10m"] > 30 or current["weathercode"] > 60:
                is_alert = True

            # Δημιουργία του αντικειμένου δεδομένων
            weather_info = {
                "temperature": round(current["temperature_2m"], 1),
                "humidity": current["relative_humidity_2m"],
                "pressure": sea_level_pressure,
                "wind_speed": round(current["wind_speed_10m"], 1),
                "wind_dir": current["wind_direction_10m"],
                "description": "Live από Γήλοφο",
                "last_update": current_time,
                "alert": is_alert,
                "weather_code": current["weathercode"]
            }

            # Αποθήκευση στο αρχείο data.json (αυτό που διαβάζει η ιστοσελίδα)
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_info, f, ensure_ascii=False, indent=4)
            
            print(f"Επιτυχής ενημέρωση: {current_time}")
            print(f"Temp: {weather_info['temperature']}°C | Pres: {sea_level_pressure} hPa | Alert: {is_alert}")
        
        else:
            print(f"Σφάλμα API: {response.status_code}")

    except Exception as e:
        print(f"Σφάλμα κατά την εκτέλεση του script: {e}")

if __name__ == "__main__":
    get_weather()
