import requests
import json
from datetime import datetime

# Συντεταγμένες για Γήλοφο
LAT = "40.06"
LON = "21.80"

def get_weather():
    # Παίρνουμε τα δεδομένα από το Open-Meteo
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true&hourly=pressure_msl&timezone=auto"
    response = requests.get(url)
    data = response.json()
    
    current = data['current_weather']
    temp = current['temperature']
    wind = current['windspeed']
    # Παίρνουμε την τρέχουσα πίεση MSL
    pressure = data['hourly']['pressure_msl'][0] 
    
    # Η ΔΙΚΗ ΣΟΥ ΛΟΓΙΚΗ ΓΙΑ ΤΑ ΟΡΙΑ
    if pressure < 1007:
        status = "ΕΠΙΔΕΙΝΩΣΗ"
    elif 1007 <= pressure < 1020:
        status = "ΛΙΑΚΑΔΑ ΜΕ ΣΥΝΝΕΦΑ"
    else:
        status = "ΑΙΘΡΙΟΣ"

    # Αποθήκευση στο data.json
    weather_data = {
        "temperature": temp,
        "humidity": 65,
        "pressure": pressure,
        "wind_speed": wind,
        "status": status,
        "last_update": datetime.now().strftime("%H:%M:%S")
    }
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(weather_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_weather()
