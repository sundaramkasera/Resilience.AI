import pandas as pd
import random
import os

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

base_lat = 28.6139
base_lon = 77.2090

def random_offset(base, max_offset=0.06):
    return round(base + random.uniform(-max_offset, max_offset), 4)

print("🏗️ Generating Full Multi-Layered Smart City Data...")

# --- VERTICES ---
substations = [{"substation_id": f"Sub-{i}", "name": f"Substation {i}", "status": "Online", "lat": random_offset(base_lat), "lon": random_offset(base_lon)} for i in range(1, 6)]
hospitals = [{"hospital_id": f"Hospital {i}", "name": f"City Care {i}", "capacity": random.randint(150, 1000), "has_backup_power": random.choice(["True", "False"]), "lat": random_offset(base_lat), "lon": random_offset(base_lon)} for i in range(1, 11)]
towers = [{"id": f"Tower-{i}", "lat": random_offset(base_lat), "lon": random_offset(base_lon)} for i in range(1, 6)]
pumps = [{"id": f"Pump-{i}", "lat": random_offset(base_lat), "lon": random_offset(base_lon)} for i in range(1, 6)]
# Add Roads (15 roads to form a good logistical network)
roads = [{"road_id": f"Road-{i}", "name": f"Route {i}", "risk_level": random.randint(1, 5), "lat": random_offset(base_lat), "lon": random_offset(base_lon)} for i in range(1, 16)]

# --- EDGES ---
# 1. POWERS (Substations -> Hospitals, Towers, Pumps)
powers_edges = [
    {"from_id": "Sub-1", "to_id": "Hospital 1", "max_capacity": 500, "current_load": 300},
    {"from_id": "Sub-1", "to_id": "Hospital 2", "max_capacity": 500, "current_load": 400},
    {"from_id": "Sub-1", "to_id": "Tower-1", "max_capacity": 200, "current_load": 150},
    {"from_id": "Sub-1", "to_id": "Pump-1", "max_capacity": 300, "current_load": 250},
    {"from_id": "Sub-2", "to_id": "Hospital 3", "max_capacity": 600, "current_load": 450},
    {"from_id": "Sub-2", "to_id": "Hospital 4", "max_capacity": 600, "current_load": 300},
    {"from_id": "Sub-2", "to_id": "Tower-4", "max_capacity": 200, "current_load": 180},
    {"from_id": "Sub-2", "to_id": "Pump-2", "max_capacity": 300, "current_load": 280},
    # SPOF
    {"from_id": "Sub-3", "to_id": "Hospital 5", "max_capacity": 1000, "current_load": 950},
    {"from_id": "Sub-3", "to_id": "Hospital 6", "max_capacity": 1000, "current_load": 800},
    {"from_id": "Sub-3", "to_id": "Hospital 7", "max_capacity": 1000, "current_load": 850},
    {"from_id": "Sub-3", "to_id": "Hospital 8", "max_capacity": 1000, "current_load": 900},
    {"from_id": "Sub-3", "to_id": "Tower-2", "max_capacity": 400, "current_load": 350},
    {"from_id": "Sub-3", "to_id": "Tower-3", "max_capacity": 400, "current_load": 380},
    {"from_id": "Sub-3", "to_id": "Tower-5", "max_capacity": 400, "current_load": 390},
    {"from_id": "Sub-3", "to_id": "Pump-4", "max_capacity": 500, "current_load": 480},
    {"from_id": "Sub-3", "to_id": "Pump-5", "max_capacity": 500, "current_load": 490},
    # Redundancies
    {"from_id": "Sub-4", "to_id": "Hospital 9", "max_capacity": 400, "current_load": 200},
    {"from_id": "Sub-4", "to_id": "Hospital 1", "max_capacity": 400, "current_load": 350},
    {"from_id": "Sub-4", "to_id": "Tower-1", "max_capacity": 200, "current_load": 190},
    {"from_id": "Sub-5", "to_id": "Hospital 10", "max_capacity": 700, "current_load": 400},
    {"from_id": "Sub-5", "to_id": "Hospital 3", "max_capacity": 700, "current_load": 600},
    {"from_id": "Sub-5", "to_id": "Pump-3", "max_capacity": 300, "current_load": 210}
]

# 2. PROVIDES_SIGNAL (Tower -> Hospital)
signal_edges = [{"from_id": f"Tower-{random.randint(1, 5)}", "to_id": f"Hospital {i}"} for i in range(1, 11)]

# 3. SUPPLIES_WATER (Pump -> Hospital)
water_edges = [{"from_id": f"Pump-{random.randint(1, 5)}", "to_id": f"Hospital {i}"} for i in range(1, 11)]

# 4. CONNECTS_TO (Road -> Hospital)
connects_edges = [{"from_id": f"Road-{random.randint(1, 15)}", "to_id": f"Hospital {i}"} for i in range(1, 11)]

# 5. INTERSECTS (Road -> Road network)
intersects_edges = [{"from_id": f"Road-{i}", "to_id": f"Road-{random.randint(1, 15)}"} for i in range(1, 16)]

# --- EXPORT ---
pd.DataFrame(substations).to_csv("data/substations.csv", index=False)
pd.DataFrame(hospitals).to_csv("data/hospitals.csv", index=False)
pd.DataFrame(towers).to_csv("data/towers.csv", index=False)
pd.DataFrame(pumps).to_csv("data/pumps.csv", index=False)
pd.DataFrame(roads).to_csv("data/roads.csv", index=False)

pd.DataFrame(powers_edges).to_csv("data/powers_edges.csv", index=False)
pd.DataFrame(signal_edges).to_csv("data/signal_edges.csv", index=False)
pd.DataFrame(water_edges).to_csv("data/water_edges.csv", index=False)
pd.DataFrame(connects_edges).to_csv("data/connects_edges.csv", index=False)
pd.DataFrame(intersects_edges).to_csv("data/intersects_edges.csv", index=False)

print("✅ 10 CSV files generated successfully! The multi-layer matrix is ready.")