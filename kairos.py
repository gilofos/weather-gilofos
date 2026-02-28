import subprocess
import sys
import os

# Αυτόματη εγκατάσταση των απαραίτητων βιβλιοθηκών
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

# 1. Τα δεδομένα των χωριών (Συντεταγμένες, Υψόμετρα, Προσεγγιστικά Pixels)
locations = {
    "ΜΑΥΡΕΛΙ":    {"lat": 39.838570, "lon": 21.866529, "alt": 1129, "pos": (650, 500)},
    "ΓΗΛΟΦΟΣ":    {"lat": 39.852063, "lon": 21.795340, "alt": 1050, "pos": (450, 450)},
    "ΦΩΤΕΙΝΟ":    {"lat": 39.841578, "lon": 21.791211, "alt": 1011, "pos": (430, 520)},
    "ΔΕΣΚΑΤΗ":    {"lat": 39.926464, "lon": 21.808788, "alt": 876,  "pos": (480, 150)},
    "ΠΑΡΑΣΚΕΥΗ":  {"lat": 39.911870, "lon": 21.769719, "alt": 782,  "pos": (320, 200)},
    "ΔΑΣΟΧΩΡΙ":   {"lat": 39.880756, "lon": 21.817734, "alt": 741,  "pos": (530, 320)},
    "ΚΕΡΑΣΟΥΛΑ":  {"lat": 39.851116, "lon": 21.724994, "alt": 724,  "pos": (150, 450)}
}

def get_wind_dir(degrees):
    dirs = ['Β', 'ΒΑ', 'Α', 'ΝΑ', 'Ν', 'ΝΔ', 'Δ', 'ΒΔ']
    ix = round(degrees / (360. / len(dirs)))
    return dirs[ix % len(dirs)]

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=True"
    try:
        data = requests.get(url).json()['current_weather']
        temp = round(data['temperature'], 1)
        code = data['weathercode']
        w_speed = data['windspeed']
        w_dir = get_wind_dir(data['winddirection'])
        w_deg = data['winddirection']
        
        status = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ" if code == 0 else "ΣΥΝΝΕΦΙΑ" 
        return temp, status, w_speed, w_dir, w_deg
    except:
        return "N/A", "N/A", 0, "-", 0

# 2. Δημιουργία του Χάρτη
try:
    # Προσπαθούμε να ανοίξουμε τον χάρτη που ανέβασες
    map_img = Image.open("map_ghilofos.png").convert("RGBA")
    draw = ImageDraw.Draw(map_img)
    font = ImageFont.load_default()

    for name, data in locations.items():
        temp, status, speed, direction, degrees = get_weather(data['lat'], data['lon'])
        x, y = data['pos']
        
        # Πληροφορίες ανά χωριό
        if name == "ΓΗΛΟΦΟΣ":
            info = f"{name}: {temp}°C\n{status}\nΑΝΕΜΟΣ: {speed}km/h {direction} ({degrees}°)"
        else:
            info = f"{name}: {temp}°C"
            
        # Σχεδίαση με μαύρα γράμματα (για να φαίνονται στο πράσινο φόντο)
        draw.text((x, y), info, fill="black", font=font)

    # Αποθήκευση του τελικού αρχείου
    map_img.save("weather_output.png")
    print("Επιτυχία! Ο χάρτης weather_output.png δημιουργήθηκε.")

except Exception as e:
    print(f"Πρόβλημα με την εικόνα: {e}")
