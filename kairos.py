import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

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
    if phase < 0.01 or phase > 0.999: return "moon0.png"
    elif phase < 0.19: return "moon7.png"
    elif phase < 0.31: return "moon2.png"
    elif phase < 0.44: return "moon5.png"
    elif phase < 0.56: return "moon4.png"
    elif phase < 0.69: return "moon3.png"
    elif phase < 0.81: return "moon6.png"
    else: return "moon1.png"

def get_weather():
    try:
        # 1. Δεδομένα από Open-Meteo
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation,wind_speed_10m,wind_direction_10m,wind_gusts_10m,cloud_cover&daily=sunrise,sunset,temperature_2m_max,temperature_2m_min&timezone=auto"
        res_json = requests.get(url).json()
        
        data = res_json['current']
        daily = res_json['daily']
        
        now = datetime.now()
        sunrise = datetime.strptime(daily['sunrise'][0], "%Y-%m-%dT%H:%M")
        sunset = datetime.strptime(daily['sunset'][0], "%Y-%m-%dT%H:%M")
        is_night = now >= sunset or now <= sunrise

        # 2. Κατάσταση από Radar (Με την ΞΑΣΤΕΡΙΑ που ζήτησες)
        weather_type = "ΣΥΝΝΕΦΙΑ ☁️"
        try:
            r = requests.get("https://www.kairosradar.gr/", timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            radar_raw = soup.find("div", {"class": "current-condition"}).text.strip()
            
            if "Αίθριος" in radar_raw or "Καθαρός" in radar_raw:
                weather_type = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ 🌌" if is_night else "ΗΛΙΟΦΑΝΕΙΑ ☀️"
            else:
                weather_type = radar_raw.upper()
        except:
            if data['precipitation'] > 0:
                weather_type = "ΒΡΟΧΗ 💧"
            else:
                # Χρήση cloud_cover αν το radar αποτύχει
                if data['cloud_cover'] < 30:
                    weather_type = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ 🌌" if is_night else "ΗΛΙΟΦΑΝΕΙΑ ☀️"
                else:
                    weather_type = "ΣΥΝΝΕΦΙΑ ☁️"

        # 3. Ανεμος (ΟΠΩΣ ΗΤΑΝ - ΔΕΝ ΤΟ ΑΓΓΙΞΑ)
        time_now_str = now.strftime("%H:%M:%S")
        wind_deg = data['wind_direction_10m']
        wind_info = f"{wind_deg}° {get_direction(wind_deg)} ({get_beaufort(data['wind_speed_10m'])} Μπφ)"

        weather_data = {
            "temperature": round(data['temperature_2m'], 1),
            "temp_max": round(daily['temperature_2m_max'][0], 1),
            "temp_min": round(daily['temperature_2m_min'][0], 1),
            "humidity": data['relative_humidity_2m'],
            "pressure": round(data['surface_pressure'] + 103, 1),
            "wind_speed": data['wind_speed_10m'],
            "wind_gust": data.get('wind_gusts_10m', 0),
            "wind_dir": wind_deg,
            "wind_text": wind_info,
            "rain": data['precipitation'],
            "clouds": data['cloud_cover'],
            "status": weather_type,
            "moon_icon": get_moon_phase_image(),
            "time": time_now_str,
            "last_update": time_now_str
        }
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)
        print(f"Ενημέρωση επιτυχής! Κατάσταση: {weather_type}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_weather()
