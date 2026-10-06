import os
import time
import pyTigerGraph as tg
import traceback

class TigerGraphConnectionError(Exception):
    pass

def get_tg_connection():
    print("🟢 System: Initializing native pyTigerGraph SDK...")
    host = os.getenv("TG_HOST", "")
    graphname = os.getenv("TG_GRAPH", "")
    username = os.getenv("TG_USERNAME", "")
    password = os.getenv("TG_PASSWORD", "")
    secret = os.getenv("TG_SECRET", "")
    
    for attempt in range(3):
        try:
            conn = tg.TigerGraphConnection(
                host=host, 
                graphname=graphname, 
                username=username, 
                password=password,
                tgCloud=True
            )
            
            conn.getToken(secret)
            print("🟢 System: pyTigerGraph token successfully generated!")
            return conn
            
        except Exception as e:
            print(f"⚠️ Connection attempt {attempt + 1} failed.")
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                print("\n🔴 --- FULL SYSTEM TRACEBACK BELOW --- 🔴")
                traceback.print_exc()
                print("🔴 ----------------------------------- 🔴\n")
                raise TigerGraphConnectionError("Failed to connect to TigerGraph after 3 attempts.")

# 👇 THIS TRIGGERS THE FUNCTION WHEN YOU RUN THE FILE DIRECTLY 👇
if __name__ == "__main__":
    print("🚀 Starting direct execution test...")
    get_tg_connection()