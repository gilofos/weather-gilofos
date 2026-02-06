import requests
import json
from datetime import datetime

# Ρυθμίσεις
API_KEY = "36c53e0281b3749726207f2323f40332" 
CITY = "Gilofos,GR"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=el"

try:
    response = requests.get(URL)
    data = response.json()

    weather_data = {
        "temperature": round(data["main"]["temp"]),
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
        "last_update": datetime.now().strftime("%H:%M")
    }

    # Αποθήκευση σε JSON
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(weather_data, f, ensure_ascii=False)

    # ΦΤΙΑΧΝΟΥΜΕ ΤΟ WIDGET ΧΩΡΙΣ ΠΟΛΛΑ ΠΛΑΙΣΙΑ
    html_content = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ 
                margin: 0; padding: 0; font-family: 'Arial', sans-serif; 
                text-align: center; background: transparent; color: #333;
            }}
            .temp {{ font-size: 65px; font-weight: bold; color: #d9534f; line-height: 1; }}
            .desc {{ font-size: 18px; color: #555; text-transform: capitalize; margin: 5px 0; }}
            .extra {{ font-size: 20px; color: #2c3e50; }}
            .time {{ font-size: 11px; color: #999; margin-top: 5px; }}
            img {{ width: 70px; margin-bottom: -10px; }}
        </style>
    </head>
    <body>
        <img src="https://openweathermap.org/img/wn/{weather_data['icon']}@2x.png">
        <div class="temp">{weather_data['temperature']}°C</div>
        <div class="desc">{weather_data['description']}</div>
        <div class="extra">Υγρασία: {weather_data['humidity']}%</div>
        <div class="time">Ενημέρωση: {weather_data['last_update']}</div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Επιτυχής ενημέρωση!")

except Exception as e:
    print(f"Σφάλμα: {e}")
           
           

        

