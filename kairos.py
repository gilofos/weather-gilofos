import requests
import json
from datetime import datetime

# Ρυθμίσεις για Γήλοφο
LAT, LON = 40.06, 21.80

# Διόρθωση Πίεσης (Offset) για να δείχνει την επιθυμητή τιμή
OFFSET = 116 

# URL για λήψη τρεχουσών συνθηκών
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m&timezone=auto"

def update_weather():
    try:
        # Λήψη δεδομένων από το Open-Meteo
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            data = response.json()["current"]
            
            # Υπολογισμός τελικής πίεσης με το Offset
            final_pressure = round(data["surface_pressure"] + OFFSET, 1)
            
            # Λογική Κατάστασης (Alert)
            if final_pressure < 1007:
                status_message = "ΕΠΙΔΕΙΝΩΣΗ ΚΑΙΡΟΥ"
            else:
                status_message = "ΚΑΙΡΟΣ ΣΤΑΘΕΡΟΣ"

            # Δομή δεδομένων για το index.html
            weather_results = {
                "temperature": round(data["temperature_2m"], 1),
                "humidity": data["relative_humidity_2m"],
                "pressure": final_pressure,
                "status": status_message,
                "wind_speed": round(data["wind_speed_10m"], 1),
                "last_update": datetime.now().strftime("%H:%M:%S")
            }
            
            # Αποθήκευση στο data.json
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_results, f, ensure_ascii=False, indent=4)
            
            print(f"[{weather_results['last_update']}] Ενημέρωση επιτυχής: {final_pressure} hPa")
        else:
            print(f"Σφάλμα σύνδεσης: {response.status_code}")
            
    except Exception as e:
        print(f"Παρουσιάστηκε σφάλμα: {e}")

if __name__ == "__main__":
    update_weather()
