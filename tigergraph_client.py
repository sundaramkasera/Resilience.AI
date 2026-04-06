import pyTigerGraph as tg

def get_tg_connection():
    print("🟢 System: Initializing native pyTigerGraph SDK...")
    host = "https://tg-75e570ca-6b56-4d89-a0d5-00d9c066b0d9.tg-3452941248.i.tgcloud.io"
    graphname = "ResilienceGraph"
    username = "tigergraph"
    password = "Sundaram@123"
    
    # The secret key needed to generate the REST++ token
    secret = "707sk3354kutptl7m0nlmcuas25h78na"
    
    try:
        conn = tg.TigerGraphConnection(
            host=host, 
            graphname=graphname, 
            username=username, 
            password=password
        )
        
        # MONKEY-PATCH: Manually inject the cloud ports to bypass the library bug
        conn.restppPort = 443
        conn.gsPort = 443
        conn.getToken(secret)
        print("🟢 System: pyTigerGraph token successfully generated!")
        return conn
    except Exception as e:
        print(f"🔴 Connection Error: {e}")
        raise e
