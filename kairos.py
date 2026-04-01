import requests
import json
import os
from datetime import datetime, timedelta

# --- ΣΥΝΤΕΤΑΓΜΕΝΕΣ ΓΗΛΟΦΟΥ ---
LAT = 39.9
LON = 21.8

def get_direction(degrees):
    directions = ["Β", "ΒΑ", "Α", "ΝΑ", "Ν", "ΝΔ", "Δ", "ΒΔ"]
    idx = int((degrees + 22.5) / 45) % 8
    return directions[idx]

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
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation,wind_speed_10m,wind_direction_10m,wind_gusts_10m,cloud_cover&daily=sunrise,sunset,temperature_2m_max,temperature_2m_min&timezone=auto"
        res_json = requests.get(url).json()
        
        data = res_json['current']
        daily = res_json['daily']
        
        T = data['temperature_2m']
        V = data['wind_speed_10m']
        RH = data['relative_humidity_2m']
        RAIN = data['precipitation']
        CLOUDS = data['cloud_cover']

        # --- 1. ΥΠΟΛΟΓΙΣΜΟΣ STATUS (ΧΩΡΙΣ ΠΡΟΕΠΙΛΟΓΕΣ) ---
        text_status = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ"
        if RAIN > 0.1 or RH > 85:
            text_status = "ΟΜΙΧΛΗ / ΒΡΟΧΗ"
        elif CLOUDS > 75:
            text_status = "ΣΥΝΝΕΦΙΑ"

        # --- 2. ΤΟ ΡΟΜΠΟΤΑΚΙ (model_forecast) ---
        # ΞΕΚΙΝΑΕΙ ΑΠΟΛΥΤΑ ΑΔΕΙΟ
        model_
