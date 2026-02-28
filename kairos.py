import subprocess
import sys
import os

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from PIL import Image, ImageDraw, ImageFont
    import requests
except ImportError:
    install('Pillow')
    install('requests')
    from PIL import Image, ImageDraw, ImageFont
    import requests

# 1. Τοποθεσίες με ΑΚΡΙΒΗ υψόμετρα (για να μην σου λέει λάθος θερμοκρασίες)
locations = {
    "ΜΑΥΡΕΛΙ":    {"lat": 39.8386, "lon": 21.8665, "alt": 1130, "pos": (900, 930)},
    "ΓΗΛΟΦΟΣ":    {"lat": 39.8521, "lon": 21.7953, "alt": 1050, "pos": (530, 810)},
    "ΦΩΤΕΙΝΟ":    {"lat": 39.8416, "lon": 21.7912, "alt": 1010, "pos": (490, 890)},
    "ΔΕΣΚΑΤΗ":    {"lat": 39.9265, "lon": 21.8088, "alt": 880,  "pos": (610, 60)},
    "ΠΑΡΑΣΚΕΥΗ":  {"lat": 39.9119, "lon": 21.7697, "alt": 780,  "pos": (380, 220)},
    "ΔΑΣΟΧΩΡΙ":   {"lat": 39.8808, "lon": 21.8177, "alt": 740,  "pos": (650, 520)},
    "ΚΕΡΑΣΟΥΛΑ":  {"lat": 39.8511, "lon": 21.7250, "alt": 720,  "pos": (120, 810)}
}

def get_weather(lat, lon, alt):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&elevation={alt}&current_weather=True"
    try:
        data = requests.get(url).json()['current_weather']
        temp = f"{round(data['temperature'], 1)}°C"
        status = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ" if data['weathercode'] == 0 else "ΚΑΙΡΟΣ"
        w_speed = data['windspeed']
        w_dir = ['Β', 'ΒΑ', 'Α', 'ΝΑ', 'Ν', 'ΝΔ', 'Δ', 'ΒΔ'][round(data['winddirection'] / 45) % 8]
        wind = f"{w_speed}km/h {w_dir} ({data['winddirection']}°)"
        return temp, status, wind
    except:
        return "N/A", "N/A", "N/A"

try:
    # Ανοίγουμε τον χάρτη που ανέβασες
    img = Image.open("map_ghilofos.png").convert("RGBA")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    for name, data in locations.items():
        temp, status, wind = get_weather(data['lat'], data['lon'], data['alt'])
        x, y = data['pos']
        txt = f"{name}\n{temp}\n{status}\n{wind}" if name == "ΓΗΛΟΦΟΣ" else f"{name}\n{temp}"

        # Σχεδίαση με περίγραμμα
        for o in [(-2,-2), (2,-2), (-2,2), (2,2)]:
            draw.text((x+o[0], y+o[1]), txt, fill="white", font=font)
        draw.text((x, y), txt, fill="black", font=font)

    # ΣΩΖΟΥΜΕ ΤΟΝ ΧΑΡΤΗ ΠΑΝΩ ΣΤΟ ΠΑΛΙΟ ΑΡΧΕΙΟ ΓΙΑ ΝΑ ΣΕ ΑΝΑΓΚΑΣΟΥΜΕ ΝΑ ΤΟ ΔΕΙΣ
    img.save("205.jpg", "JPEG") # Το σώζουμε ως 205.jpg για να αντικαταστήσει τον πίνακα!
    
    # Εντολές για να ανέβει στο GitHub
    os.system('git config --global user.name "github-actions"')
    os.system('git config --global user.email "actions@github.com"')
    os.system('git add 205.jpg')
    os.system('git commit -m "Update Map over Table" || exit 0')
    os.system('git push')

except Exception as e:
    print(f"Error: {e}")
