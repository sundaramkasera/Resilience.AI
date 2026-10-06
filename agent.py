print("📍 TRACE: agent.py - Starting imports")
import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from tigergraph_client import get_tg_connection
from pydantic import BaseModel, Field
from typing import List, Optional

load_dotenv()
print("📍 TRACE: agent.py - Imports & load_dotenv complete")

import json

# --- TIGERGRAPH TOOLS ---
@tool
def calculate_blast_radius(failed_node_id: str) -> str:
    """
    Calculates the blast radius (affected nodes) of a cascading failure starting from a given node.
    Returns a JSON string containing the affected nodes.
    """
    try:
        conn = get_tg_connection()
        edges = conn.getEdges("Substation", failed_node_id, "POWERS")
        affected = [edge['to_id'] for edge in edges]
        cascading = []
        for a_id in affected:
            try:
                sig_edges = conn.getEdges("Tower", a_id, "PROVIDES_SIGNAL")
                cascading.extend([e['to_id'] for e in sig_edges])
            except Exception:
                pass
        
        all_affected = list(set(affected + cascading))
        return json.dumps({"affected_nodes": all_affected})
    except Exception as e:
        return json.dumps({"error": f"Database query failed: {str(e)}"})

@tool
def find_single_point_of_failure(region: str = "") -> str:
    """
    Finds the Single Point of Failure (SPOF) - the Substation powering the most downstream nodes.
    Returns a JSON string containing the SPOF node ID.
    """
    try:
        conn = get_tg_connection()
        subs = conn.getVertices("Substation")
        max_edges = -1
        spof = None
        for sub in subs:
            s_id = sub['v_id']
            try:
                edges = conn.getEdges("Substation", s_id, "POWERS")
                if len(edges) > max_edges:
                    max_edges = len(edges)
                    spof = s_id
            except Exception:
                pass
        return json.dumps({"spof_node": spof})
    except Exception as e:
        return json.dumps({"error": f"Database query failed: {str(e)}"})

@tool
def route_emergency_logistics(start_node: str, end_node: str) -> str:
    """
    Formulates a physical route for emergency logistics between two nodes.
    Returns a JSON string with the dispatch plan.
    """
    try:
        conn = get_tg_connection()
        # Mock route since we don't have GSQL shortest path installed
        return json.dumps({
            "logistics_routes": [f"{start_node} -> City Center -> {end_node}"], 
            "status": "Dispatch plan formulated"
        })
    except Exception as e:
        return json.dumps({"error": f"Database query failed: {str(e)}"})

# --- GLOBAL LLM SETUP ---
print("📍 TRACE: agent.py - Initializing Global LLM setup")
llm = ChatGroq(temperature=0, model_name="qwen/qwen3.6-27b").with_fallbacks([ChatGroq(temperature=0, model_name="openai/gpt-oss-20b")])
print("📍 TRACE: agent.py - ChatGroq initialized")
tg_tools = [calculate_blast_radius, find_single_point_of_failure, route_emergency_logistics]

# --- 1. POWER GRID AGENT ---
power_sys_prompt = """You are the Power Grid Agent. 
You exclusively manage electricity, blast radius, SPOF, cascading failures, and flood risks for Substations/Pumps.
You have access to specialized tools: `calculate_blast_radius`, `find_single_point_of_failure`, `route_emergency_logistics`.

When asked about blast radius or cascading failures, use `calculate_blast_radius`.
When asked about vulnerabilities or SPOF, use `find_single_point_of_failure`.
"""
print("📍 TRACE: agent.py - Initializing Power Grid Agent")
power_executor = create_react_agent(llm, tools=tg_tools, state_modifier=power_sys_prompt)
print("📍 TRACE: agent.py - Power Grid Agent initialized")

@tool
def run_power_grid(query: str) -> str:
    """
    Delegate queries about electricity, substations, blast radius, SPOF, telecom power loss, or flooding to this agent.
    Pass a clear instruction as the 'query' string parameter.
    """
    result = power_executor.invoke({"messages": [("user", query)]})
    return result["messages"][-1].content


# --- 2. LOGISTICS AGENT ---
logistics_sys_prompt = """You are the Logistics Agent.
You exclusively handle physical routing, road networks, and supply chains.
You have access to specialized tools: `route_emergency_logistics`.

When queried by the Commander (e.g., to dispatch backup generators to an affected Hospital), formulate a brief dispatch plan using your tools.
"""
print("📍 TRACE: agent.py - Initializing Logistics Agent")
logistics_executor = create_react_agent(llm, tools=tg_tools, state_modifier=logistics_sys_prompt)
print("📍 TRACE: agent.py - Logistics Agent initialized")

@tool
def run_logistics(query: str) -> str:
    """
    Delegate queries about physical routing, dispatching backup generators, road networks, and hospital supply lines to this agent.
    Pass a clear instruction as the 'query' string parameter.
    """
    result = logistics_executor.invoke({"messages": [("user", query)]})
    return result["messages"][-1].content


class SimulationResponse(BaseModel):
    summary: str = Field(description="A clean, professional Commander's Dispatch Brief")
    spof_node: Optional[str] = Field(None, description="The Single Point of Failure node ID, if applicable")
    affected_nodes: Optional[List[str]] = Field(default_factory=list, description="List of affected node IDs")
    logistics_routes: Optional[List[str]] = Field(default_factory=list, description="List of formulated routes")

# --- 3. COMMANDER AGENT (MAIN UI INTERFACE) ---
def get_resilience_agent():
    commander_system_prompt = """You are the Commander Agent of the Resilience.AI War Room.
    You orchestrate the response to city emergencies.
    You have TWO specialized sub-agents: run_power_grid and run_logistics.
    
    YOUR WORKFLOW:
    1. Delegate grid data gathering to run_power_grid (for SPOF, blast radius, or weather/flood scans).
    2. Delegate routing tasks to run_logistics (e.g., dispatching generators to hospitals affected by the blackout).
    3. Synthesize their reports into a clean, professional "Commander's Dispatch Brief".
    """
    
    commander_tools = [run_power_grid, run_logistics]
    executor = create_react_agent(llm, tools=commander_tools, state_modifier=commander_system_prompt)
    
    # We create a chain that takes the executor output and formats it into SimulationResponse
    # This ensures we get a structured object back
    format_prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract the following information from the text and format it into the schema. If no SPOF or affected nodes are mentioned, leave them empty."),
        ("human", "{text}")
    ])
    
    fast_llm = ChatGroq(temperature=0, model_name="llama3-8b-8192")
    structured_llm = fast_llm.with_structured_output(SimulationResponse)
    
    def run_commander(user_input: str) -> SimulationResponse:
        result = executor.invoke({"messages": [("user", user_input)]})
        final_text = result["messages"][-1].content
        return structured_llm.invoke(format_prompt.format(text=final_text))
        
    return run_commander
