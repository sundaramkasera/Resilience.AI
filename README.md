# ⚡ Resilience.AI
**Smart City Command Center & Cascading Failure Simulator**

Resilience.AI is an advanced, AI-driven dashboard built to monitor, simulate, and mitigate infrastructure emergencies in a metropolitan power grid. Moving beyond static dashboards, this project utilizes a **Multi-Agent Large Language Model (LLM)** architecture connected directly to a **Graph Database** to reason through complex, cascading city-wide failures in real-time.

---

## 🚀 Core Features & Capabilities

### 🚨 The War Room (Natural Language Command)
At the heart of the dashboard is the War Room Chat. Instead of clicking through static menus, operators can type natural language commands (e.g., *"Simulate a catastrophic failure at Sub-1"*). The AI parses the intent, queries the graph database, and returns actionable dispatch briefs while automatically triggering UI updates.

### 🕸️ Cascading Failure & Blast Radius Simulation
The system maps dependencies between Substations, Telecom Towers, and Hospitals. If a substation goes down, the AI doesn't just flag the substation—it calculates the **Blast Radius**:
* **Secondary Failures:** Identifies if affected Telecom Towers will cause signal loss to critical hospitals.
* **Load Capacities:** Analyzes if rerouting power will exceed the `max_capacity` of neighboring substations.

### ⚠️ Vulnerability Scanning (SPOF Detection)
Operators can run a one-click Vulnerability Scan. The AI autonomously writes and executes a pyTigerGraph script to traverse the city's grid, identifying the **Single Point of Failure (SPOF)**—the node with the highest outbound dependencies—and instantly flags it on the 3D geospatial map.

### 📡 Live IoT Telemetry & Weather Ingestion
The dashboard maintains situational awareness without interrupting the AI's thought processes using isolated, auto-refreshing UI fragments:
* **Substation Telemetry:** A 15-second auto-refreshing dashboard monitoring live grid temperatures and loads, triggering critical UI alarms if a node overheats.
* **Live Weather Radar:** Integrates the **OpenWeatherMap API** to scan the grid's coordinates every 10 minutes. If severe weather is detected, operators can prompt the AI to cross-reference the storm data with the graph database to flag infrastructure (like WaterPumps) at risk of flooding.

### 🤖 Multi-Agent Orchestration 
To prevent AI hallucinations and handle complex logic, the "Brain" is divided into a robust LangChain Multi-Agent system:
1. **The Commander Agent:** Interfaces with the user, breaks down the emergency, delegates tasks to sub-agents, and formats the final JSON UI payloads.
2. **The Power Grid Agent:** Exclusively handles electricity math, TigerGraph queries for SPOF, and cascading failure logic.
3. **The Logistics Agent:** Exclusively handles physical routing, querying road networks to dispatch backup generators to blackout zones.

---

## 🛠️ Tech Stack Architecture

* **Frontend UI:** Streamlit (Python)
* **Geospatial Rendering:** PyDeck (Deck.GL)
* **Graph Database:** TigerGraph (pyTigerGraph SDK)
* **AI / Orchestration:** LangChain Core & LangChain Agents
* **LLM:** Groq API (Llama-3-70b-versatile)
* **External APIs:** OpenWeatherMap

---

## 🗺️ Known Limitations & Future Scope
* **Logistics Routing:** The Logistics Agent currently utilizes a simplified abstraction for road intersection queries. Future builds will integrate native graph algorithms (like Dijkstra's Shortest Path) directly within TigerGraph for hyper-accurate dispatch routing.
* **Telemetry Data:** Currently utilizing simulated local IoT data streams; future iterations will connect directly to live SCADA systems.

---
*Built for the Devcation Hack 'N' Solve 2026 (IIT Delhi) Hackathon.*
