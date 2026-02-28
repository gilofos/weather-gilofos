import requests
from PIL import Image, ImageDraw, ImageFont
import datetime

# 1. Τα δεδομένα σου (Συντεταγμένες και Υψόμετρα)
locations = {
    "ΜΑΥΡΕΛΙ":    {"lat": 39.838570, "lon": 21.866529, "alt": 1129, "pos": (680, 520)},
    "ΓΗΛΟΦΟΣ":    {"lat": 39.852063, "lon": 21.795340, "alt": 1050, "pos": (450, 480)},
    "ΦΩΤΕΙΝΟ":    {"lat": 39.841578, "lon": 21.791211, "alt": 1011, "pos": (430, 550)},
    "ΔΕΣΚΑΤΗ":    {"lat": 39.926464, "lon": 21.808788, "alt": 876,  "pos": (500, 150)},
    "ΠΑΡΑΣΚΕΥΗ":  {"lat": 39.911870, "lon": 21.769719, "alt": 782,  "pos": (350, 220)},
    "ΔΑΣΟΧΩΡΙ":   {"lat": 39.880756, "lon": 21.817734, "alt": 741,  "pos": (550, 350)},
    "ΚΕΡΑΣΟΥΛΑ":  {"lat": 39.851116, "lon": 21.724994, "alt": 724,  "pos": (180, 480)}
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
        
        # Αλλαγή "ΑΣΤΕΡΟΣ" σε "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ"
        status = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ" if code == 0 else "ΣΥΝΝΕΦΙΑ" 
        return temp, status, w_speed, w_dir, w_deg
    except:
        return "N/A", "N/A", 0, "-", 0

# 2. Επεξεργασία Εικόνας
try:
    map_img = Image.open("map_ghilofos.png").convert("RGBA")
    draw = ImageDraw.Draw(map_img)
    
    # Προσπάθησε να φορτώσεις μια γραμματοσειρά, αλλιώς χρησιμοποίησε την default
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    for name, data in locations.items():
        temp, status, speed, direction, degrees = get_weather(data['lat'], data['lon'])
        
        x, y = data['pos']
        
        # Ειδικά για τον Γήλοφο (Σταθμός) δείχνουμε και άνεμο
        if name == "ΓΗΛΟΦΟΣ":
            info = f"{name}: {temp}°C\n{status}\nΑΝΕΜΟΣ: {speed}km/h {direction} ({degrees}°)"
        else:
            info = f"{name}: {temp}°C"
            
        # Σχεδίαση κειμένου με ένα μικρό "σκούρο" πλαίσιο για να φαίνεται
        draw.text((x, y), info, fill="black", font=font) # Μαύρο για δοκιμή, το αλλάζουμε σε λευκό αν το φόντο είναι σκούρο

    # Αποθήκευση του τελικού χάρτη
    map_img.save("weather_output.png")
    print("Ο χάρτης ενημερώθηκε επιτυχώς!")

except Exception as e:
    print(f"Σφάλμα: {e}")
