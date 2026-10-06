import os
import pyTigerGraph as tg
import traceback

def get_tg_connection():
    print("🟢 System: Initializing native pyTigerGraph SDK...")
    host = os.getenv("TG_HOST", "")
    graphname = os.getenv("TG_GRAPH", "")
    username = os.getenv("TG_USERNAME", "")
    password = os.getenv("TG_PASSWORD", "")
    secret = os.getenv("TG_SECRET", "")
    
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
        print("\n🔴 --- FULL SYSTEM TRACEBACK BELOW --- 🔴")
        traceback.print_exc()
        print("🔴 ----------------------------------- 🔴\n")
        # Returning None instead of raising 'e' so it prints cleanly
        return None

# 👇 THIS TRIGGERS THE FUNCTION WHEN YOU RUN THE FILE DIRECTLY 👇
if __name__ == "__main__":
    print("🚀 Starting direct execution test...")
    get_tg_connection()