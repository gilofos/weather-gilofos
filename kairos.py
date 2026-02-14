import requests
import json
from datetime import datetime

# Συντεταγμένες για Γήλοφο (1050μ υψόμετρο)
LAT = 39.88
LON = 21.80

def get_direction(degrees):
    """Μετατρέπει τις μοίρες σε πλήρη ορίζοντα (16 σημεία)"""
    directions = ["Β", "ΒΒΑ", "ΒΑ", "ΑΒΑ", "Α", "ΑΝΑ", "ΝΑ", "ΝΝΑ", "Ν", "ΝΝΔ", "ΝΔ", "ΔΝΔ", "Δ", "ΔΒΔ", "ΒΔ", "ΒΒΔ"]
    idx = int((degrees + 11.25) / 22.5) % 16
    return directions[idx]

def get_weather():
    try:
        # 1. Λήψη δεδομένων από το API
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation,wind_speed_10m,wind_direction_10m&timezone=auto"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()['current']
        
        temp = data['temperature_2m']
        precip = data['precipitation']
        hum = data['relative_humidity_2m']
        pres_station = data['surface_pressure']
        
        # ΑΝΑΓΩΓΗ ΠΙΕΣΗΣ: Από 918 (σταθμού) σε ~1021 (θάλασσας) για 1050μ υψόμετρο
        pres_sea = pres_station + 103 
        
        wind_spd = data['wind_speed_10m']
        wind_deg = data['wind_direction_10m']
        time_now = datetime.now().strftime("%H:%M:%S")
        
        wind_cardinal = get_direction(wind_deg)
        
        # 2. Έλεγχος Μέρας/Νύχτας
        ora = datetime.now().hour
        is_night = ora >= 18 or ora <= 7
        
        # 3. Λογική Πρόγνωσης (με βάση τη διορθωμένη πίεση)
        if temp <= 1.5 and precip > 0:
            weather_type = "ΧΙΟΝΟΠΤΩΣΗ ❄️"
        elif temp <= 3.0 and precip > 0:
            weather_type = "ΧΙΟΝΟΝΕΡΟ 🌨️"
        elif precip > 0:
            weather_type = "ΒΡΟΧΗ 💧"
        else:
            if pres_sea >= 1022:
                weather_type = "ΞΑΣΤΕΡΙΑ 🌌" if is_night else "ΑΙΘΡΙΟΣ ☀️"
            elif pres_sea >= 1016:
                weather_type = "ΞΑΣΤΕΡΙΑ 🌌" if is_night else "ΔΙΑΣΤΗΜΑΤΑ ΗΛΙΟΦΑΝΕΙΑΣ ⛅"
            elif pres_sea >= 1008:
                weather_type = "ΣΥΝΝΕΦΙΑ ☁️"
            else:
                weather_type = "ΒΑΡΙΑ ΣΥΝΝΕΦΙΑ ☁️☁️"

        # 4. Αποστολή στο data.json
        weather_data = {
            "temperature": temp,
            "humidity": hum,
            "pressure": round(pres_sea, 1), # Στέλνουμε τη σωστή πίεση στο site
            "wind_speed": wind_spd,
            "wind_dir": wind_deg,
            "wind_dir_text": wind_cardinal, # Ελληνικά γράμματα
            "rain": precip,
            "status": weather_type,
            "time": time_now,
            "last_update": time_now
        }
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
        print(f"Ενημερώθηκε! Πίεση: {round(pres_sea, 1)} hPa, Πρόγνωση: {weather_type}")

    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather()
