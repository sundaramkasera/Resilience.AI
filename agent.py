import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tigergraph_client import get_tg_connection

load_dotenv()

# --- SHARED TIGERGRAPH TOOL ---
@tool
def execute_dynamic_python(python_code: str) -> str:
    """
    Executes dynamic pyTigerGraph Python code.
    Pass the Python script as a string to the 'python_code' argument.
    """
    try:
        conn = get_tg_connection()
        code = python_code.strip()
        
        if code.startswith("```python"): code = code[9:]
        elif code.startswith("```"): code = code[3:]
        if code.endswith("```"): code = code[:-3]
        
        clean_lines = []
        for line in code.split('\n'):
            if "import " in line or "TigerGraphConnection" in line or "conn=" in line or "conn =" in line:
                continue
            clean_lines.append(line)
            
        code = '\n'.join(clean_lines).strip()
        
        print("\n" + "="*50)
        print("🤖 MULTI-AGENT SUB-SYSTEM IS RUNNING THIS SCRIPT:")
        print(code)
        print("="*50 + "\n")
            
        sandbox_env = {"conn": conn, "result": "No result set."}
        exec(code, sandbox_env, sandbox_env)
        
        return str(sandbox_env.get("result"))
    except Exception as e:
        return f"Python Execution Error: {str(e)}"

# --- GLOBAL LLM SETUP ---
llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")
tg_tools = [execute_dynamic_python]

# --- 1. POWER GRID AGENT ---
power_sys_prompt = """You are the Power Grid Agent. 
You exclusively manage electricity, blast radius, SPOF, cascading failures, and flood risks for Substations/WaterPumps.
You have access to TigerGraph via `execute_dynamic_python`. THE `conn` OBJECT IS ALREADY CONNECTED.

GRAPH SCHEMA: Vertices: Substation, Hospital, TelecomTower, WaterPump. Edges: POWERS, PROVIDES_SIGNAL.

PYTIGERGRAPH RULES:
1. `conn.getVertices("VertexType")` -> list of dicts. ID is `vertex['v_id']`.
2. `conn.getEdges("SourceType", "SourceID", "EdgeType")` -> list of dicts. Target ID is `edge['to_id']`.
3. You MUST assign your final answer to the exact variable named `result`.

PHASE 4, 5 & 6 SCENARIOS (CRITICAL LOGIC):
SCENARIO A: Blast Radius & Cascading Failures
1. Find all PRIMARY nodes directly powered by that target.
2. CHECK CASCADING FAILURES: If any affected node is a 'TelecomTower', check if it `PROVIDES_SIGNAL` to other nodes (like Hospitals).
3. Return the exact list of affected node IDs.

SCENARIO B: SPOF / Vulnerability Scan
1. Write a script to find the Substation with the highest count of `POWERS` edges. 
2. Assign this ID to `result`.

SCENARIO C: Weather & Flood Risk
1. Query all 'WaterPump' and 'Substation' vertices.
2. Return these vulnerable IDs to the Commander.
"""
power_prompt = ChatPromptTemplate.from_messages([("system", power_sys_prompt), ("human", "{input}"), ("placeholder", "{agent_scratchpad}")])
power_agent = create_tool_calling_agent(llm, tg_tools, power_prompt)
power_executor = AgentExecutor(agent=power_agent, tools=tg_tools, verbose=True, max_iterations=4, handle_parsing_errors=True)

@tool
def run_power_grid(query: str) -> str:
    """
    Delegate queries about electricity, substations, blast radius, SPOF, telecom power loss, or flooding to this agent.
    Pass a clear instruction as the 'query' string parameter.
    """
    return power_executor.invoke({"input": query})["output"]


# --- 2. LOGISTICS AGENT ---
logistics_sys_prompt = """You are the Logistics Agent.
You exclusively handle physical routing, road networks, and supply chains.
You have access to TigerGraph via `execute_dynamic_python`. THE `conn` OBJECT IS ALREADY CONNECTED.

GRAPH SCHEMA: Vertices: Hospital, Road. Edges: CONNECTS (Road to Road), INTERSECTS (Road to Hospital).

PYTIGERGRAPH RULES:
1. `conn.getVertices("VertexType")` -> list of dicts. ID is `vertex['v_id']`.
2. `conn.getEdges("SourceType", "SourceID", "EdgeType")` -> list of dicts. Target ID is `edge['to_id']`.
3. You MUST assign your final answer to the exact variable named `result`.

When queried by the Commander (e.g., to dispatch backup generators to an affected Hospital), formulate a brief dispatch plan.
"""
logistics_prompt = ChatPromptTemplate.from_messages([("system", logistics_sys_prompt), ("human", "{input}"), ("placeholder", "{agent_scratchpad}")])
logistics_agent = create_tool_calling_agent(llm, tg_tools, logistics_prompt)
logistics_executor = AgentExecutor(agent=logistics_agent, tools=tg_tools, verbose=True, max_iterations=4, handle_parsing_errors=True)

@tool
def run_logistics(query: str) -> str:
    """
    Delegate queries about physical routing, dispatching backup generators, road networks, and hospital supply lines to this agent.
    Pass a clear instruction as the 'query' string parameter.
    """
    return logistics_executor.invoke({"input": query})["output"]


# --- 3. COMMANDER AGENT (MAIN UI INTERFACE) ---
def get_resilience_agent():
    commander_system_prompt = """You are the Commander Agent of the Resilience.AI War Room.
    You orchestrate the response to city emergencies.
    You have TWO specialized sub-agents: run_power_grid and run_logistics.
    
    YOUR WORKFLOW:
    1. Delegate grid data gathering to run_power_grid (for SPOF, blast radius, or weather/flood scans).
    2. Delegate routing tasks to run_logistics (e.g., dispatching generators to hospitals affected by the blackout).
    3. Synthesize their reports into a clean, professional "Commander's Dispatch Brief" for the user.
    
    CRITICAL OUTPUT RULES FOR MAP INTEGRATION (PHASES 4, 5, 6):
    You MUST extract the affected Node IDs or SPOF Node ID from the sub-agents' reports and append a raw JSON block at the VERY END of your response wrapped in exact markdown backticks.

    SCENARIO A: Blast Radius / Simulation
    ```json
    {{"affected_nodes": ["Sub-1", "Tower 1", "Hospital 1"]}}
    ```

    SCENARIO B: SPOF / Vulnerability Scan
    ```json
    {{"spof_node": "Sub-3"}}
    ```

    SCENARIO C: Weather / Flood Assessment
    ```json
    {{"affected_nodes": ["Sub-1", "Pump-1", "Pump-2"]}}
    ```
    """
    
    commander_prompt = ChatPromptTemplate.from_messages([
        ("system", commander_system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    # Use the decorated tools here
    commander_tools = [run_power_grid, run_logistics]
    commander_agent = create_tool_calling_agent(llm, commander_tools, commander_prompt)
    
    return AgentExecutor(
        agent=commander_agent, 
        tools=commander_tools, 
        verbose=True, 
        max_iterations=5, 
        handle_parsing_errors=True
    )
