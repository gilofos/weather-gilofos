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
        # --- ΚΛΗΣΗ API ΜΕ ΤΟ ΜΟΝΤΕΛΟ ΤΟΥ WINDY (ECMWF) ---
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation,wind_speed_10m,wind_direction_10m,wind_gusts_10m,cloud_cover,weather_code&daily=sunrise,sunset,temperature_2m_max,temperature_2m_min&timezone=auto&models=ecmwf_ifs"
        res_json = requests.get(url).json()
        
        data = res_json['current']
        daily = res_json['daily']
        
        T = data['temperature_2m']
        V = data['wind_speed_10m']
        RH = data['relative_humidity_2m']
        RAIN = data['precipitation']
        CLOUDS = data['cloud_cover']
        W_CODE = data['weather_code'] # Ο κωδικός καιρού από το μοντέλο

        # --- 1. ΜΕΤΑΦΡΑΣΗ ΚΑΤΑΣΤΑΣΗΣ (ΚΕΙΜΕΝΟ) ---
        # Χρησιμοποιούμε τους κωδικούς WMO που ακολουθεί και το Windy
        if W_CODE == 0:
            text_status = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ"
        elif W_CODE in [1, 2, 3]:
            text_status = "ΛΙΓΑ ΣΥΝΝΕΦΑ"
        elif W_CODE in [45, 48]:
            text_status = "ΟΜΙΧΛΗ"
        elif W_CODE in [51, 53, 55, 61, 63, 65]:
            text_status = "ΒΡΟΧΗ"
        elif W_CODE >= 80:
            text_status = "ΚΑΤΑΙΓΙΔΑ"
        else:
            text_status = "ΣΥΝΝΕΦΙΑ"

        # Καθορισμός του arrow_status (Πάνω δεξιά ένδειξη)
        # Εμφανίζει ΕΠΙΔΕΙΝΩΣΗ μόνο αν το μοντέλο προβλέπει βροχή ή πολύ βαριά σύννεφα
        if RAIN > 0.1:
            arrow_status = "ΒΡΟΧΗ"
        elif CLOUDS > 75:
            arrow_status = "ΕΠΙΔΕΙΝΩΣΗ"
        else:
            arrow_status = text_status

        # --- 2. ΤΟ ΡΟΜΠΟΤΑΚΙ (model_forecast) ---
        model_final = "" 
        if RAIN > 0.1 or RH > 92:
            model_final = "ΠΡΟΣΟΧΗ: ΦΑΙΝΟΜΕΝΑ ΣΕ ΕΞΕΛΙΞΗ"
        else:
            try:
                # Πρόγνωση 3 ημερών από το Ευρωπαϊκό μοντέλο
                url_f = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&daily=precipitation_sum&timezone=auto&models=ecmwf_ifs"
                res_f = requests.get(url_f).json()
                prec_ecmwf = res_f['daily']['precipitation_sum']
                dates = res_f['daily']['time']
                days_gr = ["ΔΕΥΤΕΡΑ", "ΤΡΙΤΗ", "ΤΕΤΑΡΤΗ", "ΠΕΜΠΤΗ", "ΠΑΡΑΣΚΕΥΗ", "ΣΑΒΒΑΤΟ", "ΚΥΡΙΑΚΗ"]
                
                model_final = text_status
                for i in range(1, 4):
                    if prec_ecmwf[i] > 1.5:
                        dt = datetime.strptime(dates[i], "%Y-%m-%d")
                        model_final = f"ΠΙΘΑΝΗ ΕΠΙΔΕΙΝΩΣΗ ΑΠΟ {days_gr[dt.weekday()]}"
                        break
            except:
                model_final = text_status

        # Υπολογισμός πίεσης στη στάθμη της θάλασσας
        pres_sea = round(data['surface_pressure'] + 103, 1)
        
        # Ώρα ενημέρωσης
        utc_offset = res_json.get('utc_offset_seconds', 7200)
        time_now = (datetime.utcnow() + timedelta(seconds=utc_offset)).strftime("%H:%M:%S")

        # Συγκέντρωση όλων των δεδομένων για το data.json
        weather_data = {
            "temperature": round(T, 1),
            "temp_max": round(daily['temperature_2m_max'][0], 1),
            "temp_min": round(daily['temperature_2m_min'][0], 1),
            "humidity": RH,
            "pressure": pres_sea,
            "dew_point": round(T - ((100 - RH) / 5), 1),
            "wind_speed": V,
            "wind_gust": data.get('wind_gusts_10m', 0),
            "wind_dir": data['wind_direction_10m'],
            "wind_text": f"{data['wind_direction_10m']}° {get_direction(data['wind_direction_10m'])}",
            "rain": RAIN,
            "clouds": CLOUDS,
            "status": arrow_status,
            "moon_icon": get_moon_phase_image(),
            "time": time_now,
            "last_update": time_now,
            "peak_temp": round(T, 1),
            "peak_status": text_status,
            "feels_like": round(T, 1),
            "wind_info": f"{get_direction(data['wind_direction_10m'])} {V} km/h",
            "model_forecast": model_final 
        }
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_weather()
