import time
import pydeck as pdk
import pandas as pd
import streamlit as st
from tigergraph_client import get_tg_connection

@st.cache_resource(show_spinner=False)
def get_static_infrastructure_layer(_conn):
    subs = _conn.getVertices("Substation")
    hospitals = _conn.getVertices("Hospital")
    towers = _conn.getVertices("Tower")
    pumps = _conn.getVertices("Pump")
    roads = _conn.getVertices("Road")
    
    nodes_data = []
    def add_nodes(vertices, node_type, color, size):
        for v in vertices:
            attrs = v.get("attributes", {})
            lat, lon = attrs.get("lat"), attrs.get("lon")
            node_id = str(v.get("v_id", ""))
            if not node_id or node_id == "Unknown":
                node_id = str(attrs.get("hospital_id", attrs.get("substation_id", attrs.get("road_id", attrs.get("id", "Unknown")))))
            
            if lat and lon:
                nodes_data.append({
                    "id": node_id, "type": node_type, "lat": float(lat), "lon": float(lon), "default_color": color, "size": size
                })
    
    add_nodes(subs, "Substation", [0, 150, 255, 200], 150)
    add_nodes(hospitals, "Hospital", [255, 140, 0, 200], 100)
    add_nodes(towers, "Telecom Tower", [255, 105, 180, 200], 80)
    add_nodes(pumps, "Water Pump", [0, 255, 255, 200], 80)
    add_nodes(roads, "Road Checkpoint", [200, 200, 200, 200], 60)
    
    coord_map = {n["id"]: (n["lon"], n["lat"]) for n in nodes_data}
    edges_data = []
    
    def add_edges(source_type, edge_type, color):
        sources = _conn.getVertices(source_type)
        for s in sources:
            s_id = str(s.get("v_id", ""))
            if s_id not in coord_map: continue
            s_lon, s_lat = coord_map[s_id]
            try:
                edges = _conn.getEdges(source_type, s_id, edge_type)
            except Exception:
                continue
            for e in edges:
                t_id = str(e.get("to_id", ""))
                if t_id in coord_map:
                    t_lon, t_lat = coord_map[t_id]
                    edges_data.append({
                        "id": f"{s_id} ➡️ {t_id}", "type": edge_type, "source": s_id, "target": t_id,
                        "source_pos": [s_lon, s_lat], "target_pos": [t_lon, t_lat], "default_color": color
                    })

    add_edges("Substation", "POWERS", [0, 250, 154, 150])              
    add_edges("Tower", "PROVIDES_SIGNAL", [255, 105, 180, 100]) 
    add_edges("Pump", "SUPPLIES_WATER", [0, 255, 255, 100])       
    add_edges("Road", "CONNECTS_TO", [150, 150, 150, 100])             
    add_edges("Road", "INTERSECTS", [100, 100, 100, 100])              
    
    return pd.DataFrame(nodes_data), pd.DataFrame(edges_data)

def render_macro_graph(affected_nodes=None, spof_node=None):
    print("🗺️ Generating PyDeck Geospatial Map...")
    affected_nodes = affected_nodes or []
    spof_node = spof_node or ""
    
    try:
        conn = get_tg_connection()
        if not conn:
            return None
            
        df_nodes, df_edges = get_static_infrastructure_layer(conn)
        df_nodes = df_nodes.copy()
        df_edges = df_edges.copy()
        
        df_nodes["color"] = df_nodes.apply(lambda r: [255, 0, 0, 255] if r["id"] == spof_node or r["id"] in affected_nodes else r["default_color"], axis=1)
        df_edges["color"] = df_edges.apply(lambda r: [255, 0, 0, 200] if r["source"] in affected_nodes or r["target"] in affected_nodes else r["default_color"], axis=1)

        static_nodes = df_nodes[~df_nodes["id"].isin(affected_nodes) & (df_nodes["id"] != spof_node)]
        static_edges = df_edges[~df_edges["source"].isin(affected_nodes) & ~df_edges["target"].isin(affected_nodes)]
        
        dynamic_nodes = df_nodes[df_nodes["id"].isin(affected_nodes) | (df_nodes["id"] == spof_node)]
        dynamic_edges = df_edges[df_edges["source"].isin(affected_nodes) | df_edges["target"].isin(affected_nodes)]

        layers = []
        layers.append(pdk.Layer("ScatterplotLayer", static_nodes, get_position="[lon, lat]", get_fill_color="color", get_radius="size", pickable=True, auto_highlight=True))
        layers.append(pdk.Layer("ArcLayer", static_edges, get_source_position="source_pos", get_target_position="target_pos", get_source_color="color", get_target_color="color", get_width=2, pickable=True, auto_highlight=True))
        
        if not dynamic_nodes.empty:
            layers.append(pdk.Layer("ScatterplotLayer", dynamic_nodes, get_position="[lon, lat]", get_fill_color="color", get_radius="size", pickable=True, auto_highlight=True))
        if not dynamic_edges.empty:
            layers.append(pdk.Layer("ArcLayer", dynamic_edges, get_source_position="source_pos", get_target_position="target_pos", get_source_color="color", get_target_color="color", get_width=3, pickable=True, auto_highlight=True))
        
        view_state = pdk.ViewState(latitude=28.6139, longitude=77.2090, zoom=11.5, pitch=45, bearing=0)
        
        r = pdk.Deck(layers=layers, initial_view_state=view_state, map_style=pdk.map_styles.CARTO_DARK, tooltip={"html": "<b>{type}</b>: {id}", "style": {"color": "white", "backgroundColor": "#222222", "fontFamily": "sans-serif"}})
        return r
    except Exception as e:
        print(f"🔴 Map Rendering Error: {e}")
        return None
