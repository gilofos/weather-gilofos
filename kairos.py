import requests
import json
import os
from datetime import datetime, timedelta, timezone

# --- ΡΥΘΜΙΣΕΙΣ ΣΤΑΘΜΟΥ ΓΗΛΟΦΟΥ ---
LAT = 40.06
LON = 21.80

# ΧΕΙΡΟΚΙΝΗΤΗ ΔΙΟΡΘΩΣΗ ΠΙΕΣΗΣ (OFFSET)
# Ρύθμισε το CORRECTION έτσι ώστε (surface_pressure + CORRECTION) = 1009 hPa (ή την τιμή που επιθυμείς)
CORRECTION = 119 

# URL για την άντληση δεδομένων από το Open-Meteo
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m&timezone=auto"

def get_weather():
    try:
        # Κλήση στο API με timeout 10 δευτερολέπτων
        response = requests.get(URL, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            current = data["current"]
            
            # Υπολογισμός Ώρας Ελλάδας (UTC+2)
            # Χρησιμοποιούμε την τοπική ώρα του συστήματος για το last_update
            current_time = datetime.now().strftime("%H:%M:%S")

            # Υπολογισμός τελικής πίεσης με τη δική σου διόρθωση
            # Μετατροπή σε integer για καθαρή εμφάνιση στο UI
            final_pressure = int(current["surface_pressure"] + CORRECTION)

            # ΛΟΓΙΚΗ ALERT (ΕΠΙΔΕΙΝΩΣΗ ΚΑΙΡΟΥ)
            # Το index.html περιμένει το πεδίο "alert" (boolean)
            is_alert = False
            if final_pressure < 1000 or current["wind_speed_10m"] > 35:
                is_alert = True

            # Προετοιμασία δεδομένων για το data.json
            weather_info = {
                "temperature": round(current["temperature_2m"], 1),
                "humidity": current["relative_humidity_2m"],
                "pressure": final_pressure,
                "wind_speed": round(current["wind_speed_10m"], 1),
                "last_update": current_time,
                "alert": is_alert
            }

            # Αποθήκευση στο αρχείο data.json
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_info, f, ensure_ascii=False, indent=4)
            
            print(f"Επιτυχής ενημέρωση: {current_time} | Πίεση: {final_pressure} hPa | Alert: {is_alert}")
        
        else:
            print(f"Σφάλμα API: {response.status_code}")

    except Exception as e:
        print(f"Σφάλμα κατά την εκτέλεση: {e}")

if __name__ == "__main__":
    get_weather()
