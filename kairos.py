import requests
import json
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

# Ρυθμίσεις Γηλόφου
LAT, LON = 39.88, 21.80

# ΤΟΠΟΘΕΣΙΕΣ ΜΕ ΤΑ ΣΗΜΕΡΙΝΑ ΥΨΟΜΕΤΡΑ
locations = [
    {"name": "MAYRELI (1130m)", "lat": 39.84, "lon": 21.84, "x": 580, "y": 720},
    {"name": "GHILOFOS (910m)", "lat": 40.06, "lon": 21.80, "x": 520, "y": 200},
    {"name": "FOTINO (960m)", "lat": 39.91, "lon": 21.74, "x": 380, "y": 550},
    {"name": "DESKATI (860m)", "lat": 39.92, "lon": 21.81, "x": 520, "y": 530},
    {"name": "PARASKEYI (920m)", "lat": 39.90, "lon": 21.78, "x": 460, "y": 580},
    {"name": "DASOCHORI (880m)", "lat": 39.94, "lon": 21.82, "x": 550, "y": 480},
    {"name": "KERASOYLA (1050m)", "lat": 39.87, "lon": 21.73, "x": 350, "y": 650}
]

def get_direction(degrees):
    directions = ["Β", "ΒΑ", "Α", "ΝΑ", "Ν", "ΝΔ", "Δ", "ΒΔ"]
    return directions[int((degrees + 22.5) / 45) % 8]

def get_weather():
    try:
        # API CALL ΓΙΑ ΟΛΑ ΤΑ ΧΩΡΙΑ
        lats = ",".join([str(l["lat"]) for l in locations])
        lons = ",".join([str(l["lon"]) for l in locations])
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lats}&longitude={lons}&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation,wind_speed_10m,wind_direction_10m,cloud_cover&daily=sunrise,sunset&timezone=auto"
        
        res = requests.get(url, timeout=15).json()

        # ΔΕΔΟΜΕΝΑ ΓΙΑ ΤΟ JSON (ΓΗΛΟΦΟΣ - Index 1)
        gh = res[1]['current']
        gh_daily = res[1]['daily']
        temp_gh = gh['temperature_2m']
        
        utc_off = res[1].get('utc_offset_seconds', 7200)
        now = datetime.utcnow() + timedelta(seconds=utc_off)
        is_night = now.time() >= datetime.strptime(gh_daily['sunset'][0], "%Y-%m-%dT%H:%M").time() or now.time() <= datetime.strptime(gh_daily['sunrise'][0], "%Y-%m-%dT%H:%M").time()
        
        # STATUS: ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ (ΟΠΩΣ ΤΟ ΖΗΤΗΣΕΣ)
        status = "ΣΥΝΝΕΦΙΑ ☁️"
        if gh['precipitation'] > 0:
            status = "ΧΙΟΝΙ ❄️" if temp_gh <= 1.5 else "ΒΡΟΧΗ 💧"
        elif gh['cloud_cover'] <= 20:
            status = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ 🌌" if is_night else "ΗΛΙΟΦΑΝΕΙΑ ☀️"

        # ΣΩΖΟΥΜΕ ΤΟ JSON
        data = {
            "temperature": round(temp_gh, 1),
            "humidity": gh['relative_humidity_2m'],
            "pressure": round(gh['surface_pressure'] + 103, 1),
            "wind_text": f"{gh['wind_direction_10m']}° {get_direction(gh['wind_direction_10m'])}",
            "status": status,
            "last_update": now.strftime("%H:%M:%S")
        }
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # ΖΩΓΡΑΦΙΚΗ ΠΑΝΩ ΣΤΟΝ map_ghilofos.png
        img = Image.open("map_ghilofos.png").convert("RGB")
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        for i, loc in enumerate(locations):
            t = round(res[i]['current']['temperature_2m'])
            # Σχεδίαση
            draw.text((loc["x"], loc["y"]), f"{loc['name']}", fill="black", font=font)
            draw.text((loc["x"], loc["y"]+15), f"{t}°C", fill="blue", font=font)

        # ΑΠΟΘΗΚΕΥΣΗ ΤΟΥ ΤΕΛΙΚΟΥ ΧΑΡΤΗ
        img.save("weather_output.png")
        print("Success: Map and Data Updated!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_weather()
