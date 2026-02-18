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

def get_moon_phase_image():
    diff = datetime.now() - datetime(2001, 1, 1)
    days = diff.days + diff.seconds / 86400
    lunations = 0.20439731 + (days * 0.03386319269)
    phase = lunations % 1
    # Εδώ είναι η αλλαγή: από 0.06 το κάναμε 0.01
    if phase < 0.01 or phase > 0.99: return "moon0.png"
    elif phase < 0.19: return "moon7.png"
    elif phase < 0.31: return "moon2.png"
    elif phase < 0.44: return "moon5.png"
    elif phase < 0.56: return "moon4.png"
    elif phase < 0.69: return "moon3.png"
    elif phase < 0.81: return "moon6.png"
    else: return "moon1.png"

def get_weather():
    try:
        # Ενημερωμένο URL με Max/Min θερμοκρασίες [cite: 2026-02-14]
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation,wind_speed_10m,wind_direction_10m,wind_gusts_10m,cloud_cover&daily=sunrise,sunset,temperature_2m_max,temperature_2m_min&timezone=auto"
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
        wind_gust = data.get('wind_gusts_10m', 0)
        wind_deg = data['wind_direction_10m']
        clouds = data['cloud_cover']
        time_now_dt = datetime.now()
        time_now_str = time_now_dt.strftime("%H:%M:%S")
        
        wind_cardinal = get_direction(wind_deg)
        bft = get_beaufort(wind_spd)
        wind_info = f"{wind_deg}° {wind_cardinal} ({bft} Μπφ)"
        
        sunset_time = datetime.strptime(daily['sunset'][0], "%Y-%m-%dT%H:%M").time()
        sunrise_time = datetime.strptime(daily['sunrise'][0], "%Y-%m-%dT%H:%M").time()
        current_time = time_now_dt.time()
        is_night = current_time >= sunset_time or current_time <= sunrise_time
        
        if precip > 0:
            if temp <= 1.5: weather_type = "ΧΙΟΝΟΠΤΩΣΗ ❄️"
            elif temp <= 3.0: weather_type = "ΧΙΟΝΟΝΕΡΟ 🌨️"
            else: weather_type = "ΒΡΟΧΗ 💧"
        else:
            if clouds <= 20: 
                weather_type = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ 🌌" if is_night else "ΗΛΙΟΦΑΝΕΙΑ ☀️"
            elif clouds <= 60:
                weather_type = "ΛΙΓΑ ΣΥΝΝΕΦΑ ☁️" if is_night else "ΛΙΓΑ ΣΥΝΝΕΦΑ ⛅"
            else:
                weather_type = "ΣΥΝΝΕΦΙΑ ☁️"

        # Προσθήκη temp_max και temp_min στο data.json [cite: 2026-02-14]
        weather_data = {
            "temperature": round(temp, 1),
            "temp_max": round(daily['temperature_2m_max'][0], 1),
            "temp_min": round(daily['temperature_2m_min'][0], 1),
            "humidity": hum,
            "pressure": round(pres_sea, 1),
            "wind_speed": wind_spd,
            "wind_gust": wind_gust,
            "wind_dir": wind_deg,
            "wind_text": wind_info,
            "rain": precip,
            "clouds": clouds,
            "status": weather_type,
            "moon_icon": get_moon_phase_image(),
            "time": time_now_str,
            "last_update": time_now_str
        }
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
        print(f"Update Success: {time_now_str} | Max: {weather_data['temp_max']} Min: {weather_data['temp_min']}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_weather()


