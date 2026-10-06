import os
from dotenv import load_dotenv
load_dotenv()
print("📍 TRACE: app.py - Starting imports")
import streamlit as st
import re
import json
import requests
from tigergraph_client import get_tg_connection
print("📍 TRACE: app.py - Importing agent")
from agent import get_resilience_agent
print("📍 TRACE: app.py - Imports complete")
print("📍 TRACE: app.py - Setting page config")
st.set_page_config(layout="wide", page_title="⚡Resilience.AI")

from tigergraph_client import TigerGraphConnectionError

@st.cache_resource
def init_connection():
    print("📍 TRACE: app.py - Inside init_connection, calling get_tg_connection")
    return get_tg_connection()

print("📍 TRACE: app.py - Calling init_connection")
try:
    conn = init_connection()
except TigerGraphConnectionError as e:
    st.toast("Database connection failed. Entering offline mode.", icon="⚠️")
    conn = None
except Exception as e:
    conn = None
print("📍 TRACE: app.py - Connection initialized")

col_controls, col_map = st.columns([1, 3])

with col_map:
    # --- RENDER MAP ---
    map_container = st.empty()
    if conn:
        try:
            from graph_renderer import render_macro_graph 
            map_chart = render_macro_graph(
                affected_nodes=st.session_state.get("offline_nodes", []), 
                spof_node=st.session_state.get("spof_node")
            )
            map_container.pydeck_chart(map_chart, width="stretch")
        except Exception as e:
            st.error(f"Map Rendering Error: {e}")
    else:
        st.warning("Cannot render map. Database connection required.")

with col_controls:
    st.write("# ⚡ Resilience.AI")
    st.markdown("---")

    print("📍 TRACE: app.py - Setting up session state")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "⚡ Commander, Resilience.AI is online. Standing by for macro-city queries."}]

    if "pending_input" not in st.session_state:
        st.session_state.pending_input = ""
        
    if "offline_nodes" not in st.session_state:
        st.session_state.offline_nodes = []
        
    if "spof_node" not in st.session_state:
        st.session_state.spof_node = None

    def handle_submit():
        st.session_state.pending_input = st.session_state.user_input_widget
        st.session_state.user_input_widget = ""

    st.text_input(
        "Query Input", 
        key="user_input_widget",
        label_visibility="collapsed", 
        placeholder="Ask Resilience AI (e.g., 'Target power failures')...",
        on_change=handle_submit
    )

    scan_button = st.button("⚠️ Run Vulnerability Scan", use_container_width=True)
    if scan_button:
        st.session_state.pending_input = "Run a vulnerability scan to find the Single Point of Failure (SPOF)."

    weather_button = st.button("🌩️ Assess Weather Risks", use_container_width=True)
    if weather_button:
        st.session_state.pending_input = "Severe weather detected. Assess infrastructure flood risks for Substations and WaterPumps."

    # --- WAR ROOM CHAT ---
    st.markdown("---")
    st.subheader("🚨 War Room Chat")
    
    chat_container = st.container(height=450, border=True)
    user_input = st.session_state.pending_input

    if user_input and conn:
        run_commander = get_resilience_agent()

        with st.spinner("Analyzing City Grid..."):
            response = run_commander(user_input)

        st.caption(f"Debug - Extracted SPOF: {response.spof_node}")
        
        final_response_text = response.summary
        
        # UI fails silently (no highlight) if spof_node is invalid or empty
        if response.spof_node:
            st.session_state.spof_node = response.spof_node
            st.session_state.offline_nodes = []
        elif response.affected_nodes:
            st.session_state.offline_nodes = response.affected_nodes
            st.session_state.spof_node = None
        else:
            if "simulate" not in user_input.lower() and "scan" not in user_input.lower() and "weather" not in user_input.lower():
                st.session_state.offline_nodes = []
                st.session_state.spof_node = None

        if conn:
            try:
                from graph_renderer import render_macro_graph 
                updated_map = render_macro_graph(
                    affected_nodes=st.session_state.offline_nodes, 
                    spof_node=st.session_state.spof_node
                )
                map_container.pydeck_chart(updated_map, width="stretch")
            except Exception as e:
                pass

        st.session_state.messages.insert(0, {"role": "user", "content": user_input})
        st.session_state.messages.insert(1, {"role": "assistant", "content": final_response_text})
        
        st.session_state.pending_input = ""

    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.chat_message("user").write(message["content"])
            elif message["role"] == "assistant":
                st.chat_message("assistant").write(message["content"])

with col_map:
    # --- PHASE 6: AUTO-REFRESHING HORIZONTAL IOT DASHBOARD (MOVED TO TOP) ---
    @st.fragment(run_every="2s")
    def live_telemetry_dashboard():
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📡 Live Substation Telemetry")
            
        try:
            if os.path.exists("telemetry_stream.json"):
                try:
                    with open("telemetry_stream.json", "r") as f:
                        telemetry = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError, PermissionError):
                    telemetry = {}
                    
                subs = ["Sub-1", "Sub-2", "Sub-3", "Sub-4", "Sub-5"]
                cols = st.columns(5)
                critical_alarms = []
                
                for i, sub in enumerate(subs):
                    data = telemetry.get(sub, {"temperature": 0, "load": 0})
                    temp = data["temperature"]
                    load = data["load"]
                    
                    with cols[i]:
                        st.write(f"**{sub}**")
                        if temp > 100:
                            st.markdown(f"<h2 style='color: #ff4b4b; margin-top: -15px;'>{temp}°C</h2>", unsafe_allow_html=True)
                            st.markdown(f"<span style='background-color: #ff4b4b33; color: #ff4b4b; padding: 4px 10px; border-radius: 12px; font-size: 0.85rem;'>↑ {load}% Load</span>", unsafe_allow_html=True)
                            critical_alarms.append((sub, temp, load))
                        else:
                            st.markdown(f"<h2 style='margin-top: -15px;'>{temp}°C</h2>", unsafe_allow_html=True)
                            st.markdown(f"<span style='background-color: #ff4b4b33; color: #ff4b4b; padding: 4px 10px; border-radius: 12px; font-size: 0.85rem;'>↑ {load}% Load</span>", unsafe_allow_html=True)
                            
                if critical_alarms:
                    st.markdown("<br>", unsafe_allow_html=True)
                    for alarm in critical_alarms:
                        st.error(f"⚠️ **CRITICAL ALARM:** {alarm[0]} is Overheating! (Temp: {alarm[1]}°C | Load: {alarm[2]}%)")
                        
            else:
                st.info("Telemetry stream offline. Run telemetry_simulator.py")
        except Exception as e:
            st.caption(f"Telemetry error: {e}")

    live_telemetry_dashboard()
    
    st.markdown("---")

    # --- PHASE 6: AUTO-REFRESHING WEATHER RADAR (MOVED TO BOTTOM) ---
    @st.cache_data(ttl=300, show_spinner=False)
    def fetch_weather_data(api_key):
        url = f"http://api.openweathermap.org/data/2.5/weather?lat=28.6139&lon=77.2090&appid={api_key}&units=metric"
        return requests.get(url).json()

    @st.fragment(run_every=600)
    def live_weather_radar():
        st.subheader("🌩️ Live Weather Radar (Delhi)")
        
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            st.info("⚠️ Add OPENWEATHER_API_KEY to your .env file to enable live weather.")
            return

        try:
            resp = fetch_weather_data(api_key)
            
            if resp.get("cod") == 200:
                weather_desc = resp['weather'][0]['description'].title()
                temp = resp['main']['temp']
                st.write(f"**Current Conditions:** {temp}°C | {weather_desc}")
                
                weather_id = resp['weather'][0]['id']
                if weather_id < 700:
                    st.error("⚠️ **SEVERE WEATHER ALERT:** Storm/Heavy Precipitation detected in grid bounds. Use the 'Assess Weather Risks' button to scan infrastructure.")
                else:
                    st.success("✅ **CLEAR SKIES:** No severe weather threats detected in the grid bounds.")
            else:
                st.caption(f"Weather API Error: {resp.get('message', 'Unknown Error')}")
        except Exception as e:
            st.caption(f"Weather Fetch Error: {e}")

    live_weather_radar()
