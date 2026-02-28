import requests
import json
from datetime import datetime, timedelta
from PIL import Image, ImageDraw

# Τοποθεσίες (X, Y συντεταγμένες για τον χάρτη σου)
locations = [
    {"name": "MAYRELI", "lat": 39.84, "lon": 21.84, "x": 580, "y": 720},
    {"name": "GHILOFOS", "lat": 40.06, "lon": 21.80, "x": 520, "y": 200},
    {"name": "FOTINO", "lat": 39.91, "lon": 21.74, "x": 380, "y": 550},
    {"name": "DESKATI", "lat": 39.92, "lon": 21.81, "x": 520, "y": 530},
    {"name": "PARASKEYI", "lat": 39.90, "lon": 21.78, "x": 460, "y": 580},
    {"name": "DASOCHORI", "lat": 39.94, "lon": 21.82, "x": 550, "y": 480},
    {"name": "KERASOYLA", "lat": 39.87, "lon": 21.73, "x": 350, "y": 650}
]

def get_weather():
    try:
        lats = ",".join([str(l["lat"]) for l in locations])
        lons = ",".join([str(l["lon"]) for l in locations])
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lats}&longitude={lons}&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation,cloud_cover&daily=sunrise,sunset&timezone=auto"
        res = requests.get(url, timeout=15).json()

        # Δεδομένα Γηλόφου
        gh = res[1]['current']
        now = datetime.utcnow() + timedelta(hours=2)
        
        # JSON για τον πίνακα
        data = {"temp": round(gh['temperature_2m'], 1), "updated": now.strftime("%H:%M")}
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

        # --- ΕΔΩ ΕΙΝΑΙ Η ΖΩΓΡΑΦΙΚΗ ΜΕ ΤΑ ΛΕΥΚΑ ΠΛΑΙΣΙΑ ---
        img = Image.open("map_ghilofos.png").convert("RGB")
        draw = ImageDraw.Draw(img)

        for i, loc in enumerate(locations):
            t = round(res[i]['current']['temperature_2m'], 1)
            label = f"{loc['name']}: {t}C"
            
            # 1. Σχεδιάζουμε το λευκό πλαίσιο (Label)
            # [x_start, y_start, x_end, y_end]
            draw.rectangle([loc["x"]-5, loc["y"]-2, loc["x"]+140, loc["y"]+18], fill="white", outline="black")
            
            # 2. Γράφουμε το κείμενο πάνω στο πλαίσιο
            draw.text((loc["x"], loc["y"]), label, fill="black")

        img.save("weather_output.png")
        print("Success: Ο χάρτης με τα πλαίσια ετοιμάστηκε!")

    except Exception as e:
        print(f"Lathos: {e}")

if __name__ == "__main__":
    get_weather()
