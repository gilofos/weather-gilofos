import subprocess
import sys
import os

# 1. Εγκατάσταση απαραίτητων εργαλείων
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

# 2. Δεδομένα Χωριών (Συντεταγμένες και Θέσεις στον Χάρτη)
locations = {
    "ΜΑΥΡΕΛΙ":    {"lat": 39.838570, "lon": 21.866529, "pos": (900, 930)},
    "ΓΗΛΟΦΟΣ":    {"lat": 39.852063, "lon": 21.795340, "pos": (530, 810)},
    "ΦΩΤΕΙΝΟ":    {"lat": 39.841578, "lon": 21.791211, "pos": (490, 890)},
    "ΔΕΣΚΑΤΗ":    {"lat": 39.926464, "lon": 21.808788, "pos": (610, 60)},
    "ΠΑΡΑΣΚΕΥΗ":  {"lat": 39.911870, "lon": 21.769719, "pos": (380, 220)},
    "ΔΑΣΟΧΩΡΙ":   {"lat": 39.880756, "lon": 21.817734, "pos": (650, 520)},
    "ΚΕΡΑΣΟΥΛΑ":  {"lat": 39.851116, "lon": 21.724994, "pos": (120, 810)}
}

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=True"
    try:
        data = requests.get(url).json()['current_weather']
        temp = f"{round(data['temperature'], 1)}°C"
        status = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ" if data['weathercode'] == 0 else "ΣΥΝΝΕΦΙΑ"
        # Ανεμος: Ταχύτητα, Κατεύθυνση και Μοίρες
        w_speed = data['windspeed']
        w_deg = data['winddirection']
        dirs = ['Β', 'ΒΑ', 'Α', 'ΝΑ', 'Ν', 'ΝΔ', 'Δ', 'ΒΔ']
        w_dir = dirs[round(w_deg / 45) % 8]
        wind = f"{w_speed}km/h {w_dir} ({w_deg}°)"
        return temp, status, wind
    except:
        return "N/A", "N/A", "N/A"

# 3. Δημιουργία Εικόνας
try:
    # Ανοίγει τον χάρτη που ανέβασες
    img = Image.open("map_ghilofos.png").convert("RGBA")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    for name, data in locations.items():
        temp, status, wind = get_weather(data['lat'], data['lon'])
        x, y = data['pos']
        
        if name == "ΓΗΛΟΦΟΣ":
            txt = f"{name}: {temp}\n{status}\nΑΝΕΜΟΣ: {wind}"
        else:
            txt = f"{name}: {temp}"

        # Σχεδίαση με λευκό περίγραμμα για να φαίνεται
        for o in [(-1,-1), (1,-1), (-1,1), (1,1)]:
            draw.text((x+o[0], y+o[1]), txt, fill="white", font=font)
        draw.text((x, y), txt, fill="black", font=font)

    # Αποθήκευση της νέας εικόνας
    img.save("weather_output.png")
    
    # ΑΥΤΟΜΑΤΟ PUSH ΣΤΟ GITHUB
    os.system('git config --global user.name "github-actions"')
    os.system('git config --global user.email "actions@github.com"')
    os.system('git add weather_output.png')
    os.system('git commit -m "Update Weather Map" || exit 0')
    os.system('git push')
    
    print("ΤΕΛΟΣ! Ο χάρτης ενημερώθηκε.")

except Exception as e:
    print(f"Σφάλμα: {e}")
