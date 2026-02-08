import json
import random
import time
import os

def generate_weather_data():
    # Ghilofos Coordinates
    lat = 40.06
    lon = 21.80
    
    while True:
        # Simulation of sensors
        temperature = round(random.uniform(-5.0, 15.0), 1)
        humidity = random.randint(30, 95)
        pressure = random.randint(990, 1030) # Pressure included
        wind_speed = round(random.uniform(0, 50), 1)
        
        # Alert Logic (Status)
        if pressure < 1000 or wind_speed > 40:
            status = "ΕΠΙΔΕΙΝΩΣΗ ΚΑΙΡΟΥ"
            alert_active = True
        else:
            status = "ΟΜΑΛΕΣ ΣΥΝΘΗΚΕΣ"
            alert_active = False
            
        data = {
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure,
            "wind_speed": wind_speed,
            "status": status,
            "alert": alert_active,
            "last_update": time.strftime("%H:%M:%S")
        }
        
        # Save to data.json for the HTML to read
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"Data Updated: {temperature}°C, {pressure} hPa - {status}")
        time.sleep(60) # Update every minute

if __name__ == "__main__":
    generate_weather_data()
