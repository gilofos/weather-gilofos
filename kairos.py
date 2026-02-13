import requests
import json
from datetime import datetime

# Συντεταγμένες για Γήλοφο
LAT = "40.06"
LON = "21.80"

def get_wind_dir(degrees):
    # Μετατροπή μοιρών σε γράμματα
    directions = ['Β', 'ΒΑ', 'Α', 'ΝΑ', 'Ν', 'ΝΔ', 'Δ', 'ΒΔ']
    idx = int((degrees + 22.5) / 45) % 8
    return directions[idx]

def get_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true&hourly=pressure_msl&timezone=auto"
    response = requests.get(url)
    data = response.json()
    
    current = data['current_weather']
    temp = current['temperature']
    wind = current['windspeed']
    # Παίρνουμε τις μοίρες του ανέμου
    wind_deg = current['winddirection']
    wind_dir_text = get_wind_dir(wind_deg)
    
    pressure = data['hourly']['pressure_msl'][0] 
    
    if pressure < 1007:
        status = "ΕΠΙΔΕΙΝΩΣΗ"
    elif 1007 <= pressure < 1020:
        status = "ΛΙΑΚΑΔΑ ΜΕ ΣΥΝΝΕΦΑ"
    else:
        status = "ΑΙΘΡΙΟΣ"

    weather_data = {
        "temperature": temp,
        "humidity": 65,
        "pressure": pressure,
        "wind_speed": wind,
        "wind_dir": wind_dir_text, # Τώρα στέλνουμε το Ν, Β, ΝΔ...
        "status": status,
        "last_update": datetime.now().strftime("%H:%M:%S")
    }
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(weather_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_weather()
