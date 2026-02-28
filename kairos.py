import requests
import json
from datetime import datetime, timedelta
from PIL import Image, ImageDraw

# Τοποθεσίες με τις συντεταγμένες για τα κουτάκια στον χάρτη
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
        # API Call
        lats = ",".join([str(l["lat"]) for l in locations])
        lons = ",".join([str(l["lon"]) for l in locations])
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lats}&longitude={lons}&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation,cloud_cover,wind_speed_10m,wind_direction_10m&daily=sunrise,sunset&timezone=auto"
        res = requests.get(url, timeout=15).json()

        # Γήλοφος (Index 1)
        gh = res[1]['current']
        gh_daily = res[1]['daily']
        now = datetime.utcnow() + timedelta(hours=2) # Ώρα Ελλάδος
        
        # STATUS
        is_night = now.time() >= datetime.strptime(gh_daily['sunset'][0], "%Y-%m-%dT%H:%M").time() or now.time() <= datetime.strptime(gh_daily['sunrise'][0], "%Y-%m-%dT%H:%M").time()
        status = "ΣΥΝΝΕΦΙΑ ☁️"
        if gh['precipitation'] > 0: status = "ΒΡΟΧΗ 💧"
        elif gh['cloud_cover'] <= 20: status = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ 🌌" if is_night else "ΗΛΙΟΦΑΝΕΙΑ ☀️"

        # Σώζουμε το JSON για τον πίνακα
        data = {
            "temperature": round(gh['temperature_2m'], 1),
            "humidity": gh['relative_humidity_2m'],
            "pressure": round(gh['surface_pressure'] + 103, 1),
            "wind": f"{gh['wind_direction_10m']}° {get_direction(gh['wind_direction_10m'])}",
            "status": status,
            "updated": now.strftime("%H:%M")
        }
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

        # ΖΩΓΡΑΦΙΚΗ ΧΑΡΤΗ
        img = Image.open("map_ghilofos.png").convert("RGB")
        draw = ImageDraw.Draw(img)

        for i, loc in enumerate(locations):
            t = round(res[i]['current']['temperature_2m'], 1)
            label = f"{loc['name']}: {t}C"
            
            # Σχεδιάζουμε το λευκό πλαίσιο για να φαίνονται τα γράμματα
            draw.rectangle([loc["x"]-5, loc["y"]-2, loc["x"]+165, loc["y"]+18], fill="white", outline="black")
            # Γράφουμε το κείμενο
            draw.text((loc["x"], loc["y"]), label, fill="black")

        img.save("weather_output.png")
        print("Success! Ola etoima.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_weather()
