import requests
import json
import os
from datetime import datetime

# Ρυθμίσεις για τον Γήλοφο Γρεβενών
LAT = 40.06
LON = 21.80

# ΧΕΙΡΟΚΙΝΗΤΗ ΔΙΟΡΘΩΣΗ (OFFSET): 
# Προσαρμογή ώστε η τελική τιμή να είναι 1009 hPa.
OFFSET = 119 

# URL του Open-Meteo API
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m&timezone=auto"

def update_weather():
    """Λήψη δεδομένων και ενημέρωση του αρχείου data.json"""
    try:
        # Κλήση στο API
        response = requests.get(URL, timeout=10)
        
        if response.status_code == 200:
            data = response.json()["current"]
            
            # 1. Υπολογισμός τελικής πίεσης
            pressure_final = int(data["surface_pressure"] + OFFSET)
            
            # 2. Λογική ALERT
            # Ενεργοποιείται αν η πίεση < 1000 hPa ή ο άνεμος > 35 km/h
            is_alert = False
            if pressure_final < 1000 or data["wind_speed_10m"] > 35:
                is_alert = True

            # 3. Προετοιμασία δεδομένων για το index.html
            weather_info = {
                "temp": round(data["temperature_2m"], 1),
                "hum": data["relative_humidity_2m"],
                "pres": pressure_final,
                "wind": round(data["wind_speed_10m"], 1),
                "alert": is_alert,
                "last_update": datetime.now().strftime("%H:%M:%S")
            }

            # Αποθήκευση στο data.json
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_info, f, indent=4, ensure_ascii=False)
            
            print(f"Ενημέρωση Επιτυχής: {pressure_final} hPa | Alert: {is_alert}")
        else:
            print(f"Σφάλμα API: {response.status_code}")
            
    except Exception as e:
        print(f"Παρουσιάστηκε σφάλμα: {e}")

if __name__ == "__main__":
    update_weather()
