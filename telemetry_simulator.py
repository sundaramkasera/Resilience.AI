import json
import time
import random
import os

def run_telemetry():
    print("🟢 Starting IoT Telemetry Stream (Press CTRL+C to stop)...")
    substations = ["Sub-1", "Sub-2", "Sub-3", "Sub-4", "Sub-5"]
    
    while True:
        telemetry_data = {}
        for sub in substations:
            # Normal temp is 40-70. 15% chance to spike over 100 (Critical).
            if random.random() > 0.85:
                temp = random.randint(101, 115)
            else:
                temp = random.randint(40, 70)
            
            telemetry_data[sub] = {
                "temperature": temp,
                "load": random.randint(40, 99)
            }
        
        with open("telemetry_stream.tmp.json", "w") as f:
            json.dump(telemetry_data, f)
        os.replace("telemetry_stream.tmp.json", "telemetry_stream.json")
        
        print(f"📡 Telemetry Updated: {telemetry_data}")
        time.sleep(15)  # Update every 15 seconds

if __name__ == "__main__":
    run_telemetry()
