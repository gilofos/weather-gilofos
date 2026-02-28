import requests
from PIL import Image, ImageDraw, ImageFont

# 1. Δεδομένα Χωριών (Όνομα, Υψόμετρο, Συντεταγμένες στον χάρτη)
stations = {
    "ΓΗΛΟΦΟΣ": {"alt": "910m", "pos": (450, 150)},
    "ΔΕΣΚΑΤΗ": {"alt": "860m", "pos": (600, 50)},
    "ΔΑΣΟΧΩΡΙ": {"alt": "880m", "pos": (650, 750)},
    "ΠΑΡΑΣΚΕΥΗ": {"alt": "920m", "pos": (350, 280)},
    "ΦΩΤΕΙΝΟ": {"alt": "960m", "pos": (250, 780)},
    "ΚΕΡΑΣΟΥΛΑ": {"alt": "1050m", "pos": (240, 920)}
}

def get_weather():
    # Εδώ θα έμπαινε το API call σου. Για τώρα βάζουμε τυχαία για τη δοκιμή
    return {"temp": "5.7", "status": "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ"}

def create_map():
    try:
        img = Image.open("map_ghilofos.png") # Το αρχικό σου αρχείο
        draw = ImageDraw.Draw(img)
        
        # Προσπάθεια για γραμματοσειρά (αν δεν υπάρχει, παίρνει default)
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()

        weather = get_weather()

        for name, info in stations.items():
            x, y = info["pos"]
            text = f"{name} ({info['alt']}): {weather['temp']}°C\n{weather['status']}"
            
            # Σχεδίαση Λευκού Πλαισίου
            padding = 10
            bbox = draw.textbbox((x, y), text, font=font)
            draw.rectangle([bbox[0]-padding, bbox[1]-padding, bbox[2]+padding, bbox[3]+padding], fill="white", outline="black")
            
            # Σχεδίαση Κειμένου
            draw.text((x, y), text, fill="black", font=font)

        img.save("weather_output.png")
        print("Success: Ο χάρτης ετοιμάστηκε!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_map()
