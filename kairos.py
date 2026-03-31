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

def get_model_alert():
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&daily=precipitation_sum&timezone=auto&models=gfs_seamless,ecmwf_ifs"
        res = requests.get(url).json()
        prec_gfs = res['daily']['precipitation_sum_gfs_seamless']
        prec_ecmwf = res['daily']['precipitation_sum_ecmwf_ifs']
        dates = res['daily']['time']
        days_gr = ["ΔΕΥΤΕΡΑ", "ΤΡΙΤΗ", "ΤΕΤΑΡΤΗ", "ΠΕΜΠΤΗ", "ΠΑΡΑΣΚΕΥΗ", "ΣΑΒΒΑΤΟ", "ΚΥΡΙΑΚΗ"]
        for i in range(1, 4):
            if prec_gfs[i] > 1.5 or prec_ecmwf[i] > 1.5:
                dt = datetime.strptime(dates[i], "%Y-%m-%d")
                return f"ΠΙΘΑΝΗ ΕΠΙΔΕΙΝΩΣΗ ΑΠΟ {days_gr[dt.weekday()]}"
        return "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ"
    except:
        return "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ"

def get_weather():
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation,wind_speed_10m,wind_direction_10m,wind_gusts_10m,cloud_cover&daily=sunrise,sunset,temperature_2m_max,temperature_2m_min&timezone=auto"
        res_json = requests.get(url).json()
        
        data = res_json['current']
        daily = res_json['daily']
        
        T = data['temperature_2m']
        V = data['wind_speed_10m']
        RH = data['relative_humidity_2m']

        if T <= 15 and V > 4.8:
            feels_like = 13.12 + 0.6215*T - 11.37*(V**0.16) + 0.3965*T*(V**0.16)
        elif T >= 25:
            feels_like = 0.5 * (T + 61.0 + ((T - 68.0) * 1.2) + (RH * 0.094))
        else:
            feels_like = T
        feels_like = round(feels_like, 1)

        # --- ΚΕΙΜΕΝΟ ΚΑΤΑΣΤΑΣΗΣ (ΒΑΣΙΚΟ) ---
        if data['precipitation'] > 0:
            text_status = "ΒΡΟΧΗ"
        elif data['cloud_cover'] > 70:
            text_status = "ΣΥΝΝΕΦΙΑ"
        elif data['cloud_cover'] > 20:
            text_status = "ΛΙΓΑ ΣΥΝΝΕΦΑ"
        else:
            text_status = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ"

        # --- ΛΟΓΙΚΗ ΤΑΣΗΣ ΚΑΙ ΥΠΕΡΙΣΧΥΣΗΣ (ΔΙΚΑΙΟ ΣΥΣΤΗΜΑ) ---
        last_p_file = "last_pressure.txt"
        pres_sea = round(data['surface_pressure'] + 103, 1)
        arrow_status = text_status 

        if os.path.exists(last_p_file):
            with open(last_p_file, "r") as f:
                try:
                    last_pres = float(f.read().strip())
                    # Αν η πίεση ανεβαίνει, η Βελτίωση κερδίζει τη Βροχή (Δορυφόρος)
                    if pres_sea > (last_pres + 0.01):
                        arrow_status = "ΠΡΟΣΚΑΙΡΗ ΒΕΛΤΙΩΣΗ"
                    # Αν η πίεση πέφτει, πάμε για Επιδείνωση
                    elif pres_sea < (last_pres - 0.01):
                        arrow_status = "ΕΠΙΔΕΙΝΩΣΗ"
                except: pass
        
        with open(last_p_file, "w") as f:
            f.write(str(pres_sea))

        utc_offset = res_json.get('utc_offset_seconds', 7200)
        time_now = (datetime.utcnow() + timedelta(seconds=utc_offset)).strftime("%H:%M:%S")

        weather_data = {
            "model_forecast": get_model_alert(),
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
            "rain": data['precipitation'],
            "clouds": data['cloud_cover'],
            "status": arrow_status,
            "moon_icon": get_moon_phase_image(),
            "time": time_now,
            "last_update": time_now,
            "peak_temp": round(T - 0.5, 1),
            "peak_status": text_status,
            "feels_like": feels_like,
            "wind_info": f"{get_direction(data['wind_direction_10m'])} {V} km/h"
        }
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_weather()
