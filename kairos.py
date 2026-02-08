import json
import random
import time
import os

def generate_weather_data():
    # Συντεταγμένες Γηλόφου
    lat = 40.06
    lon = 21.80
    
    while True:
        # Προσομοίωση αισθητήρων (Εδώ θα μπουν οι πραγματικές μετρήσεις σου)
        temperature = round(random.uniform(-5.0, 18.0), 1)
        humidity = random.randint(30, 95)
        pressure = random.randint(990, 1030) # Πίεση hPa
        wind_speed = round(random.uniform(0, 60), 1)
        
        # Λογική Alert (Ειδοποίηση)
        # Αν η πίεση πέσει κάτω από 1000 ή ο άνεμος ξεπεράσει τα 45 km/h
        if pressure < 1000 or wind_speed > 45:
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
        
        # Αποθήκευση στο data.json για το index.html
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"Ενημέρωση: {temperature}°C, {pressure} hPa | {status}")
        time.sleep(60)

if __name__ == "__main__":
    generate_weather_data()
