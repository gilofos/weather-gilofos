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
        "last_update": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    # Αποθήκευση σε JSON
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(weather_data, f, ensure_ascii=False)

    # ΦΤΙΑΧΝΟΥΜΕ ΤΟ ΜΕΓΑΛΟ WIDGET
    html_content = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ 
                margin: 0; padding: 10px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                text-align: center; background: #ffffff;
            }}
            .container {{
                border: 3px solid #3498db; border-radius: 20px; padding: 15px; background: #f8f9fa;
            }}
            .city {{ font-size: 22px; font-weight: bold; color: #2c3e50; text-transform: uppercase; }}
            .temp {{ font-size: 80px; font-weight: bold; color: #d9534f; line-height: 1; margin: 10px 0; }}
            .desc {{ font-size: 20px; color: #555; text-transform: capitalize; margin-bottom: 10px; font-weight: bold; }}
            .extra {{ font-size: 24px; color: #3498db; font-weight: bold; }}
            .update {{ font-size: 13px; color: #999; margin-top: 15px; border-top: 1px solid #ddd; padding-top: 5px; }}
            img {{ width: 100px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="city">ΓΗΛΟΦΟΣ</div>
            <img src="https://openweathermap.org/img/wn/{weather_data['icon']}@2x.png">
            <div class="temp">{weather_data['temperature']}°C</div>
            <div class="desc">{weather_data['description']}</div>
            <div class="extra">💧 Υγρασία: {weather_data['humidity']}%</div>
            <div class="update">Τελ. ενημέρωση: {weather_data['last_update']}</div>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Επιτυχής ενημέρωση!")

except Exception as e:
    print(f"Σφάλμα: {e}")
        
