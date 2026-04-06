import pydeck as pdk
import pandas as pd
from tigergraph_client import get_tg_connection

def render_macro_graph(affected_nodes=None, spof_node=None):
    print("🗺️ Generating PyDeck Geospatial Map...")
    affected_nodes = affected_nodes or []
    spof_node = spof_node or ""
    
    try:
        conn = get_tg_connection()
        
        subs = conn.getVertices("Substation")
        hospitals = conn.getVertices("Hospital")
        towers = conn.getVertices("TelecomTower")
        pumps = conn.getVertices("WaterPump")
        roads = conn.getVertices("Road")
        
        nodes_data = []
        def add_nodes(vertices, node_type, color, size):
            for v in vertices:
                attrs = v.get("attributes", {})
                lat, lon = attrs.get("lat"), attrs.get("lon")
                node_id = str(v.get("v_id", ""))
                if not node_id or node_id == "Unknown":
                    node_id = str(attrs.get("hospital_id", attrs.get("substation_id", attrs.get("road_id", attrs.get("id", "Unknown")))))
                
                if lat and lon:
                    final_color = color
                    if node_id == spof_node:
                        final_color = [255, 0, 0, 255]  # RED for SPOF
                    elif node_id in affected_nodes:
                        final_color = [255, 0, 0, 255]    # RED for Affected
                        
                    nodes_data.append({
                        "id": node_id, "type": node_type, "lat": float(lat), "lon": float(lon), "color": final_color, "size": size
                    })
        
        add_nodes(subs, "Substation", [0, 150, 255, 200], 150)
        add_nodes(hospitals, "Hospital", [255, 140, 0, 200], 100)
        add_nodes(towers, "Telecom Tower", [255, 105, 180, 200], 80)
        add_nodes(pumps, "Water Pump", [0, 255, 255, 200], 80)
        add_nodes(roads, "Road Checkpoint", [200, 200, 200, 200], 60)
        
        df_nodes = pd.DataFrame(nodes_data)
        coord_map = {n["id"]: (n["lon"], n["lat"]) for n in nodes_data}
        edges_data = []
        
        def add_edges(source_type, edge_type, color):
            sources = conn.getVertices(source_type)
            for s in sources:
                s_id = str(s.get("v_id", ""))
                if s_id not in coord_map: continue
                s_lon, s_lat = coord_map[s_id]
                edges = conn.getEdges(source_type, s_id, edge_type)
                for e in edges:
                    t_id = str(e.get("to_id", ""))
                    if t_id in coord_map:
                        t_lon, t_lat = coord_map[t_id]
                        
                        final_edge_color = color
                        if s_id in affected_nodes or t_id in affected_nodes:
                            final_edge_color = [255, 0, 0, 200] # RED for dead edges
                            
                        edges_data.append({
                            "id": f"{s_id} ➡️ {t_id}", "type": edge_type, "source": s_id, "target": t_id,
                            "source_pos": [s_lon, s_lat], "target_pos": [t_lon, t_lat], "color": final_edge_color
                        })

        add_edges("Substation", "POWERS", [0, 250, 154, 150])              
        add_edges("TelecomTower", "PROVIDES_SIGNAL", [255, 105, 180, 100]) 
        add_edges("WaterPump", "SUPPLIES_WATER", [0, 255, 255, 100])       
        add_edges("Road", "CONNECTS_TO", [150, 150, 150, 100])             
        add_edges("Road", "INTERSECTS", [100, 100, 100, 100])              
        
        df_edges = pd.DataFrame(edges_data)

        scatterplot = pdk.Layer("ScatterplotLayer", df_nodes, get_position="[lon, lat]", get_fill_color="color", get_radius="size", pickable=True, auto_highlight=True)
        arclayer = pdk.Layer("ArcLayer", df_edges, get_source_position="source_pos", get_target_position="target_pos", get_source_color="color", get_target_color="color", get_width=2, pickable=True, auto_highlight=True)
        
        view_state = pdk.ViewState(latitude=28.6139, longitude=77.2090, zoom=11.5, pitch=45, bearing=0)
        
        r = pdk.Deck(layers=[arclayer, scatterplot], initial_view_state=view_state, map_style=pdk.map_styles.CARTO_DARK, tooltip={"html": "<b>{type}</b>: {id}", "style": {"color": "white", "backgroundColor": "#222222", "fontFamily": "sans-serif"}})
        return r
    except Exception as e:
        print(f"🔴 Map Rendering Error: {e}")
        return None
