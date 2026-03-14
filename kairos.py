import requests
import json
from datetime import datetime, timedelta

# Συντεταγμένες για Γήλοφο
LAT = 40.58
LON = 21.67

def get_direction(degrees):
    directions = ["Β", "ΒΑ", "Α", "ΝΑ", "Ν", "ΝΔ", "Δ", "ΒΔ"]
    idx = int((degrees + 22.5) / 45) % 8
    return directions[idx]

def get_beaufort(kmh):
    if kmh < 1: return 0
    elif kmh < 6: return 1
    elif kmh < 12: return 2
    elif kmh < 20: return 3
    elif kmh < 29: return 4
    elif kmh < 39: return 5
    elif kmh < 50: return 6
    elif kmh < 62: return 7
    else: return 8

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
        # Ζητάμε πρόγνωση 3 ημερών από GFS και ECMWF
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&daily=precipitation_sum,precipitation_probability_max&timezone=auto&models=gfs_seamless,ecmwf_ifs"
        res = requests.get(url).json()
        
        precip_gfs = res['daily']['precipitation_sum_gfs_seamless']
        precip_ecmwf = res['daily']['precipitation_sum_ecmwf_ifs']
        prob_gfs = res['daily']['precipitation_probability_max_gfs_seamless']
        dates = res['daily']['time']
        
        days_gr = ["ΔΕΥΤΕΡΑ", "ΤΡΙΤΗ", "ΤΕΤΑΡΤΗ", "ΠΕΜΠΤΗ", "ΠΑΡΑΣΚΕΥΗ", "ΣΑΒΒΑΤΟ", "ΚΥΡΙΑΚΗ"]

        # Ελέγχουμε τις επόμενες 3 ημέρες (ξεκινώντας από αύριο i=1)
        for i in range(1, 4):
            # Αν κάποιο μοντέλο δει πάνω από 1.5mm βροχή ή μεγάλη πιθανότητα
            if precip_gfs[i] > 1.5 or precip_ecmwf[i] > 1.5:
                dt = datetime.strptime(dates[i], "%Y-%m-%d")
                day_name = days_gr[dt.weekday()]
                
                status = "ΒΡΟΧΕΣ"
                if precip_gfs[i] > 5 or precip_ecmwf[i] > 5:
                    status = "ΒΡΟΧΕΣ & ΚΑΤΑΙΓΙΔΕΣ"
                
                return f"ΠΙΘΑΝΗ ΕΠΙΔΕΙΝΩΣΗ ΑΠΟ {day_name} ΜΕ {status}"
        
        return "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ"
    except:
        return "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ"

def get_weather():
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation,wind_speed_10m,wind_direction_10m,wind_gusts_10m,cloud_cover&daily=sunrise,sunset,temperature_2m_max,temperature_2m_min&timezone=auto"
        response = requests.get(url)
        response.raise_for_status()
        res_json = response.json()
        
        data = res_json['current']
        daily = res_json['daily']
        
        utc_offset_sec = res_json.get('utc_offset_seconds', 7200)
        time_now_dt = datetime.utcnow() + timedelta(seconds=utc_offset_sec)
        time_now_str = time_now_dt.strftime("%H:%M:%S")
        
        temp = data['temperature_2m']
        precip = data['precipitation']
        hum = data['relative_humidity_2m']
        pres_sea = data['surface_pressure'] + 103 # Διόρθωση για υψόμετρο Γηλόφου
        wind_spd = data['wind_speed_10m']
        wind_gust = data.get('wind_gusts_10m', 0)
        wind_deg = data['wind_direction_10m']
        clouds = data['cloud_cover']
        
        wind_cardinal = get_direction(wind_deg)
        bft = get_beaufort(wind_spd)
        wind_info = f"{wind_deg}° {wind_cardinal} ({bft} Μπφ)"
        
        sunset_time = datetime.strptime(daily['sunset'][0], "%Y-%m-%dT%H:%M").time()
        sunrise_time = datetime.strptime(daily['sunrise'][0], "%Y-%m-%dT%H:%M").time()
        current_time = time_now_dt.time()
        is_night = current_time >= sunset_time or current_time <= sunrise_time
        
        # Λογική τρέχουσας κατάστασης (κίτρινα γράμματα)
        if precip > 0:
            if temp <= 1.5: weather_type = "ΧΙΟΝΟΠΤΩΣΗ ❄️"
            elif temp <= 3.0: weather_type = "ΧΙΟΝΟΝΕΡΟ 🌨️"
            else: weather_type = "ΒΡΟΧΗ 💧"
        elif clouds <= 20: 
            weather_type = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ 🌌" if is_night else "ΗΛΙΟΦΑΝΕΙΑ ☀️"
        elif pres_sea < 1004:
            weather_type = "ΚΑΚΟΚΑΙΡΙΑ ⚠️"
        elif 1004 <= pres_sea < 1015:
            weather_type = "ΣΥΝΝΕΦΙΑ / ΑΣΤΑΘΕΙΑ ☁️"
        elif clouds <= 60:
            weather_type = "ΛΙΓΑ ΣΥΝΝΕΦΑ ☁️" if is_night else "ΛΙΓΑ ΣΥΝΝΕΦΑ ⛅"
        else:
            weather_type = "ΣΥΝΝΕΦΙΑ ☁️"

        weather_data = {
            "model_forecast": get_model_alert(),
            "temperature": round(temp, 1),
            "temp_max": round(daily['temperature_2m_max'][0], 1),
            "temp_min": round(daily['temperature_2m_min'][0], 1),
            "humidity": hum,
            "pressure": round(pres_sea, 1),
            "wind_speed": wind_spd,
            "wind_gust": wind_gust,
            "wind_dir": wind_deg,
            "wind_text": wind_info,
            "rain": precip,
            "clouds": clouds,
            "status": weather_type,
            "moon_icon": get_moon_phase_image(),
            "time": time_now_str,
            "last_update": time_now_str
        }
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
        print(f"Update Success: {time_now_str} | Status: {weather_type}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_weather()
