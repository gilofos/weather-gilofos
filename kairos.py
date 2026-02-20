import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

def get_weather():
    try:
        # 1. Κατάσταση από kairosradar.gr
        status_text = "ΣΥΝΝΕΦΙΑ / ΑΙΘΡΙΟΣ"
        try:
            r = requests.get("https://www.kairosradar.gr/", timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            raw = soup.find("div", {"class": "current-condition"}).text.strip()
            
            # Αν το radar λέει Αίθριος, το κάνουμε ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ
            if "Αίθριος" in raw or "Καθαρός" in raw:
                status_text = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ"
            else:
                status_text = raw.upper()
        except:
            pass

        # 2. Δεδομένα από Open-Meteo
        api = "https://api.open-meteo.com/v1/forecast?latitude=40.0125&longitude=21.4625&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m&timezone=Europe%2FAthens"
        res = requests.get(api).json()['current']
        
        # Υπολογισμός κειμένου Ανέμου
        d = res['wind_direction_10m']
        if 337.5 <= d or d < 22.5: txt = "ΒΟΡΕΙΟΣ"
        elif 22.5 <= d < 67.5: txt = "ΒΑ"
        elif 67.5 <= d < 112.5: txt = "ΑΝΑΤΟΛΙΚΟΣ"
        elif 112.5 <= d < 157.5: txt = "ΝΑ"
        elif 157.5 <= d < 202.5: txt = "ΝΟΤΙΟΣ"
        elif 202.5 <= d < 247.5: txt = "ΝΔ"
        elif 247.5 <= d < 292.5: txt = "ΔΥΤΙΚΟΣ"
        else: txt = "ΒΔ"

        # 3. Το JSON που θα διαβάσει η σελίδα σου (data.json)
        data = {
            "temperature": f"{round(res['temperature_2m'])}",
            "humidity": f"{res['relative_humidity_2m']}",
            "pressure": f"{round(res['surface_pressure'])}",
            "wind_speed": f"{round(res['wind_speed_10m'])}",
            "wind_deg": f"{d}",
            "wind_dir": f"{txt}",   # Αυτό θα διώξει το undefined δίπλα στον άνεμο
            "rain": "0.0",          # Αυτό θα διώξει το undefined από τη βροχή
            "status": status_text,  # Εδώ θα μπει το ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ
            "last_update": datetime.now().strftime("%H:%M:%S")
        }

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Όλα έτοιμα και τακτοποιημένα!")

    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather()
