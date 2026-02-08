import requests
import json
import os
from datetime import datetime, timedelta, timezone

# Ρυθμίσεις για τον Γήλοφο Γρεβενών
LAT = 40.06
LON = 21.80

# ΧΕΙΡΟΚΙΝΗΤΗ ΔΙΟΡΘΩΣΗ (OFFSET): 
# Αν η επιφανειακή πίεση από το API είναι ~890, το 119 μας δίνει 1009 hPa.
OFFSET = 119 

# URL του Open-Meteo API
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m&timezone=auto"

def update_weather():
    """Κύρια συνάρτηση λήψης και αποθήκευσης δεδομένων"""
    try:
        # Λήψη δεδομένων με timeout 10 δευτερόλεπτα
        response = requests.get(URL, timeout=10)
        
        if response.status_code == 200:
            data = response.json()["current"]
            
            # 1. Υπολογισμός τελικής πίεσης με το offset
            pressure_final = int(data["surface_pressure"] + OFFSET)
            
            # 2. Λογική ALERT (Ειδοποίησης)
            # Ενεργοποιείται αν η πίεση πέσει κάτω από 1000 hPa (χαμηλό βαρομετρικό)
            # ή αν ο άνεμος ξεπεράσει τα 35 km/h.
            is_alert = False
            if pressure_final < 1000 or data["wind_speed_10m"] > 35:
                is_alert = True

            # 3. Προετοιμασία δεδομένων για το data.json (που διαβάζει το index.html)
            output = {
                "temp": round(data["temperature_2m"], 1),
                "hum": data["relative_humidity_2m"],
                "pres": pressure_final,
                "wind": round(data["wind_speed_10m"], 1),
                "alert": is_alert,
                "last_update": datetime.now().strftime("%H:%M:%S")
            }

            # Αποθήκευση στο αρχείο data.json
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(output, f, indent=4, ensure_ascii=False)
            
            print(f"Ενημέρωση Επιτυχής: {pressure_final} hPa | Alert: {is_alert}")
        else:
            print(f"Σφάλμα API: {response.status_code}")
            
    except Exception as e:
        print(f"Παρουσιάστηκε σφάλμα: {e}")

if __name__ == "__main__":
    # Εκτέλεση της ενημέρωσης
    update_weather()
