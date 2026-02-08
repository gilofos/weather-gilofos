import requests
import json
import os
from datetime import datetime

# Ρυθμίσεις για τον Γήλοφο Γρεβενών
LAT = 40.06
LON = 21.80

# ΔΙΟΡΘΩΣΗ ΠΙΕΣΗΣ (OFFSET): 
# Προσαρμόζουμε την τιμή ώστε το αποτέλεσμα να είναι 1009 hPa.
# Αν το API δίνει ~890 (επιφανειακή πίεση), το 119 μας δίνει 1009.
OFFSET = 119 

# URL του Open-Meteo API για τις τρέχουσες συνθήκες
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m&timezone=auto"

def update_weather():
    """Λήψη δεδομένων και ενημέρωση του αρχείου data.json"""
    try:
        # Κλήση στο API για λήψη δεδομένων
        response = requests.get(URL, timeout=10)
        
        if response.status_code == 200:
            data = response.json()["current"]
            
            # 1. Υπολογισμός τελικής πίεσης με το offset
            pressure_final = int(data["surface_pressure"] + OFFSET)
            
            # 2. Λογική ALERT (Ενεργοποίηση ειδοποίησης)
            # Αν η πίεση πέσει κάτω από 1000 hPa ή ο άνεμος ξεπεράσει τα 35 km/h
            is_alert = False
            if pressure_final < 1000 or data["wind_speed_10m"] > 35:
                is_alert = True

            # 3. Δημιουργία του αντικειμένου για το data.json
            # Τα ονόματα (keys) είναι ακριβώς αυτά που διαβάζει το index.html (temp, hum, pres, wind, alert)
            weather_info = {
                "temp": round(data["temperature_2m"], 1),
                "hum": data["relative_humidity_2m"],
                "pres": pressure_final,
                "wind": round(data["wind_speed_10m"], 1),
                "alert": is_alert,
                "last_update": datetime.now().strftime("%H:%M:%S")
            }

            # Εγγραφή των δεδομένων στο data.json (στον ίδιο φάκελο)
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_info, f, indent=4, ensure_ascii=False)
            
            print(f"--- ΕΝΗΜΕΡΩΣΗ ΣΤΑΘΜΟΥ ΓΗΛΟΦΟΥ ---")
            print(f"Θερμοκρασία: {weather_info['temp']}°C")
            print(f"Πίεση: {weather_info['pres']} hPa")
            print(f"Κατάσταση Alert: {is_alert}")
            print(f"---------------------------------")
            
        else:
            print(f"Σφάλμα API: {response.status_code}")
            
    except Exception as e:
        print(f"Παρουσιάστηκε σφάλμα: {e}")

if __name__ == "__main__":
    update_weather()
