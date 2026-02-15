import requests
import json
from datetime import datetime
import time

# Συντεταγμένες για Γήλοφο
LAT = 39.88
LON = 21.80

def get_direction(degrees):
    directions = ["Β", "ΒΑ", "Α", "ΝΑ", "Ν", "ΝΔ", "Δ", "ΒΔ"]
    idx = int((degrees + 22.5) / 45) % 8
    return directions[idx]

def get_weather():
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation,wind_speed_10m,wind_direction_10m,cloud_cover&timezone=auto"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()['current']
        
        temp = data['temperature_2m']
        precip = data['precipitation']
        hum = data['relative_humidity_2m']
        pres_sea = data['surface_pressure'] + 103 
        wind_spd = data['wind_speed_10m']
        wind_deg = data['wind_direction_10m']
        clouds = data['cloud_cover']
        time_now = datetime.now().strftime("%H:%M:%S")
        
        wind_cardinal = get_direction(wind_deg)
        
        # Υπολογισμός σελήνης - Μόνο αυτό προσθέτουμε
        diff = time.time() - 947116800 
        moon_phase = round((diff % 2551443) / 2551443, 2)

        ora = datetime.now().hour
        is_night = ora >= 18 or ora <= 7
        
        if precip > 0:
            if temp <= 1.5: weather_type = "ΧΙΟΝΟΠΤΩΣΗ ❄️"
            elif temp <= 3.0: weather_type = "ΧΙΟΝΟΝΕΡΟ 🌨️"
            else: weather_type = "ΒΡΟΧΗ 💧"
        else:
            if clouds <= 20:
                weather_type = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ 🌌" if is_night else "ΗΛΙΟΦΑΝΕΙΑ ☀️"
            elif clouds <= 60:
                weather_type = "ΛΙΓΑ ΣΥΝΝΕΦΑ ⛅"
            else:
                weather_type = "ΣΥΝΝΕΦΙΑ ☁️"

        weather_data = {
            "temperature": round(temp, 1),
            "humidity": hum,
            "pressure": round(pres_sea, 1),
            "wind_speed": wind_spd,
            "wind_dir": wind_deg,
            "wind_text": wind_cardinal,
            "rain": precip,
            "clouds": clouds,
            "status": weather_type,
            "phase": moon_phase, # <--- ΑΥΤΗ Η ΓΡΑΜΜΗ ΘΑ ΕΠΑΝΑΦΕΡΕΙ ΤΟΥΣ ΑΡΙΘΜΟΥΣ
            "time": time_now,
            "last_update": time_now
        }
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
        print(f"[{time_now}] Update OK")

    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather()
