import requests
import json
from datetime import datetime

# Συντεταγμένες για Γήλοφο
LAT = 39.88
LON = 21.80

def get_direction(degrees):
    directions = ["Β", "ΒΑ", "Α", "ΝΑ", "Ν", "ΝΔ", "Δ", "ΒΔ"]
    idx = int((degrees + 22.5) / 45) % 8
    return directions[idx]

def get_beaufort(kmh):
    if kmh < 1: return 0
    elif kmh < 6: return 1
    elif kmh < 12: return 2
    elif kmh < 20: return 3
    elif kmh < 29: return 4
    elif kmh < 39: return 5
    elif kmh < 50: return 6
    elif kmh < 62: return 7
    else: return 8

def get_weather():
    try:
        # 1. Λήψη δεδομένων με Ανατολή/Δύση
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation,wind_speed_10m,wind_direction_10m,cloud_cover&daily=sunrise,sunset&timezone=auto"
        response = requests.get(url)
        response.raise_for_status()
        res_json = response.json()
        
        data = res_json['current']
        daily = res_json['daily']
        
        temp = data['temperature_2m']
        precip = data['precipitation']
        hum = data['relative_humidity_2m']
        pres_sea = data['surface_pressure'] + 103 
        wind_spd = data['wind_speed_10m']
        wind_deg = data['wind_direction_10m']
        clouds = data['cloud_cover']
        time_now_dt = datetime.now()
        time_now_str = time_now_dt.strftime("%H:%M:%S")
        
        # 2. Υπολογισμός Ανέμου (Μόνο Γράμμα και Μποφόρ)
        wind_cardinal = get_direction(wind_deg)
        bft = get_beaufort(wind_spd)
        wind_info = f"{wind_cardinal} ({bft} Μπφ)"
        
        # 3. Δυναμικός έλεγχος Νύχτας
        sunset_time = datetime.strptime(daily['sunset'][0], "%Y-%m-%dT%H:%M").time()
        sunrise_time = datetime.strptime(daily['sunrise'][0], "%Y-%m-%dT%H:%M").time()
        current_time = time_now_dt.time()
        is_night = current_time >= sunset_time or current_time <= sunrise_time
        
        # 4. Λογική Πρόγνωσης
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

        # Αποστολή στο data.json
        weather_data = {
            "temperature": round(temp, 1),
            "humidity": hum,
            "pressure": round(pres_sea, 1),
            "wind_speed": wind_spd,
            "wind_dir": wind_deg,
            "wind_text": wind_info,
            "rain": precip,
            "clouds": clouds,
            "status": weather_type,
            "time": time_now_str,
            "last_update": time_now_str
        }
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
        print(f"[{time_now_str}] {weather_type} | Άνεμος: {wind_deg}° {wind_info}")

    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather()
