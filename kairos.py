import requests
import json
from datetime import datetime

# Ρυθμίσεις (Γήλοφος)
API_KEY = "36c53e0281b3749726207f2323f40332" 
LAT = 40.0632
LON = 21.8025
URL = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric&lang=el"

try:
    response = requests.get(URL)
    data = response.json()

    # Φτιάχνουμε το αρχείο δεδομένων που διαβάζει το index.html σου
    weather_data = {
        "temp": round(data["main"]["temp"], 1),
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "description": data["weather"][0]["description"].capitalize(),
        "icon": data["weather"][0]["icon"],
        "last_update": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    # Αποθήκευση στο data.json
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(weather_data, f, ensure_ascii=False, indent=4)

    print(f"Επιτυχής ενημέρωση στις {weather_data['last_update']}!")

except Exception as e:
    print(f"Σφάλμα: {e}")
