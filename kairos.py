import requests
import json
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

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
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation,wind_speed_10m,wind_direction_10m,wind_gusts_10m,cloud_cover&daily=sunrise,sunset,temperature_2m_max,temperature_2m_min&timezone=auto"
        response = requests.get(url)
        response.raise_for_status()
        res_json = response.json()
        
        data = res_json['current']
        daily = res_json['daily']
        
        utc_offset_sec = res_json.get('utc_offset_seconds', 7200)
        time_now_dt = datetime.utcnow() + timedelta(seconds=utc_offset_sec)
        time_now_str = time_now_dt.strftime("%H:%M:%S")
        
        temp = data['temperature_2m']
        precip = data['precipitation']
        hum = data['relative_humidity_2m']
        pres_sea = data['surface_pressure'] + 103 
        wind_spd = data['wind_speed_10m']
        wind_deg = data['wind_direction_10m']
        clouds = data['cloud_cover']
        
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
        elif clouds <= 20:
            weather_type = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ 🌌" if is_night else "ΗΛΙΟΦΑΝΕΙΑ ☀️"
        elif clouds <= 60:
            weather_type = "ΛΙΓΑ ΣΥΝΝΕΦΑ ☁️" if is_night else "ΛΙΓΑ ΣΥΝΝΕΦΑ ⛅"
        else:
            weather_type = "ΣΥΝΝΕΦΙΑ ☁️"

        weather_data = {
            "temperature": round(temp, 1),
            "wind_text": wind_info,
            "status": weather_type,
            "time": time_now_str
        }

        # 1. Αποθήκευση JSON
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)

        # 2. Δημιουργία Χάρτη (Εδώ είναι το κομμάτι που έλειπε)
        create_visual_map(weather_data)
        
        print(f"Update Success: {time_now_str} | Status: {weather_type}")

    except Exception as e:
        print(f"Error: {e}")

def create_visual_map(w):
    try:
        # Άνοιγμα του χάρτη σου
        img = Image.open("map_ghilofos.png")
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 25)
        except:
            font = ImageFont.load_default()

        # Τοποθέτηση πληροφοριών Γήλοφος (Κέντρο χάρτη περίπου)
        text = f"ΓΗΛΟΦΟΣ: {w['temperature']}°C\n{w['status']}\nΑΝΕΜΟΣ: {w['wind_text']}"
        
        # Ζωγραφίζουμε το κείμενο απευθείας (χωρίς κουτάκια που σε εκνεύρισαν)
        draw.text((400, 300), text, fill="black", font=font)
        
        img.save("weather_output.png")
    except:
        pass

if __name__ == "__main__":
    get_weather()
