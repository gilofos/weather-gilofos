import requests
import json
import os
from datetime import datetime, timedelta

LAT = 40.58
LON = 21.67

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

def get_pressure_trend(current_pres):
    # Διαβάζουμε την παλιά πίεση από το data.json για να δούμε την τάση
    trend_arrow = "→"
    try:
        if os.path.exists('data.json'):
            with open('data.json', 'r', encoding='utf-8') as f:
                old_data = json.load(f)
                # Παίρνουμε το νούμερο πριν το κενό
                last_pres = float(str(old_data['pressure']).split(' ')[0])
                if current_pres > last_pres + 0.1: trend_arrow = "↑"
                elif current_pres < last_pres - 0.1: trend_arrow = "↓"
    except: pass
    return trend_arrow

def get_weather():
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,surface_pressure,precipitation,wind_speed_10m,wind_direction_10m,cloud_cover&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        res = requests.get(url).json()
        
        cur = res['current']
        pres_sea = round(cur['surface_pressure'] + 103, 1)
        trend = get_pressure_trend(pres_sea)

        weather_data = {
            "temperature": round(cur['temperature_2m'], 1),
            "temp_max": round(res['daily']['temperature_2m_max'][0], 1),
            "temp_min": round(res['daily']['temperature_2m_min'][0], 1),
            "pressure": f"{pres_sea} {trend}", # ΤΩΡΑ ΤΟ ΒΕΛΑΚΙ ΕΙΝΑΙ ΣΩΣΤΟ
            "status": "ΚΑΘΑΡΟΣ", # Βάζουμε μια λέξη που ΔΕΝ έχει βελάκι στο index.html
            "wind_text": f"{cur['wind_direction_10m']}° {get_direction(cur['wind_direction_10m'])} ({get_beaufort(cur['wind_speed_10m'])} Μπφ)",
            "last_update": (datetime.utcnow() + timedelta(hours=2)).strftime("%H:%M:%S")
        }
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    get_weather()
