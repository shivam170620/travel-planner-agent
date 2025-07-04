# 🧳 Multi-Agent Travel Planner System

## Overview

This project is a **stateful, multi-agent travel planning system** that leverages multiple APIs and custom tools to generate a comprehensive, day-wise travel itinerary and report. The system is orchestrated using a workflow engine (e.g., LangGraph or LangChain), ensuring robust, modular, and reliable execution.

---

## 🏗️ Architecture

```
                      +-----------------+
                      |   User Input    |
                      +--------+--------+
                               |
                      +--------v--------+
                      |   Orchestrator  | (StateGraph Entry)
                      +---+---+----+----+
                          |   |    | 
     +--------------------+   |    +----------------------+
     |                        |                           |
+----v-----+          +-------v-------+           +-------v-------+
| Weather  |          |   Hotel       |           |   Flight      |
| Agent    |          |   Agent       |           |   Agent       |
| (Tool)   |          |   (Tool)      |           |   (Tool)      |
+----------+          +---------------+           +---------------+
     |                       |                           |
     +----------------+------+---------------------------+
                          |
               +----------v------------+
               | Transportation Agent |
               | (e.g. Bus, Metro)    |
               +----------+-----------+
                          |
         +----------------v----------------+
         | Restaurant and Attractions Agent|
         | (Tool for both)                 |
         +----------------+----------------+
                          |
               +----------v-----------+
               | Expense Management   |
               | Agent (Day-wise)    |
               +----------+----------+
                          |
              +-----------v------------+
              |  Final Fusion Agent    |
              | (Generate PDF Report)  |
              +------------------------+
```

---

## 🧩 Components Breakdown

### 1. **Orchestrator Agent**
- **Role:** Receives the user's query (e.g : "user_input_data": {
            "city": "Hyderabad",
            "origin_city": "PAT",
            "destination_city": "HYD",
            "outbound_date": "2025-07-09",
            "return_date": "2025-07-10",
            "num_days": 2
        }, ).

      Next Iteration:- "Plan a 5-day trip to Paris" ()

- **Function:** Delegates tasks to specialized agents(we can say custom function or tool), coordinates data aggregation, and manages the workflow.
- **Implementation:** Built using LangGraph, LangChain, or a custom stateful agent manager.

### 2. **Specialized Agents (Custom Tools)**
Each agent is responsible for a specific domain and interacts with external APIs:

- **Weather Agent:** Fetches weather forecasts (e.g., OpenWeatherMap).
- **Hotel Agent:** Queries hotel booking APIs (e.g., Booking.com, Expedia).
- **Flight Agent:** Queries flight APIs (e.g., Skyscanner, Amadeus, SerpAPI).
- **Transportation Agent:** Finds local transport options (e.g., Google Maps, SerpAPI).
- **Attraction Agent:** Fetches points of interest (POIs) from sources like Geoapify, TripAdvisor.
- **Restaurant Agent:** Finds top restaurants using SerpAPI or Google Maps.
- **Expense Management Agent:** Calculates day-wise expenses, currency exchange, and cost summaries through the LLM.

### 3. **Data Fusion Layer**
- **Role:** Deduplicates, standardizes, and merges responses from different agents.
- **Function:** Combines multi-modal data (e.g., hotels with nearby attractions) for a seamless itinerary.

### 4. **Report Creator (Final Fusion Agent)**
- **Role:** Uses templates and LLMs to generate a natural language itinerary/report.
- **Function:** Adds recommendations, optimal routes, cost summaries, and generates a PDF or shareable report.

---

## 🛠️ Custom Tools Implemented

- **get_weather:** Fetches weather data for a city or coordinates.
- **get_attraction_spots:** Finds top tourist attractions using Geoapify.
- **get_restaurants:** Finds top restaurants using SerpAPI.
- **get_hotels:** Fetches hotel options from booking APIs.
- **get_local_transportation:** Finds local transport options (bus, metro, taxi) using Google Maps/SerpAPI.
- **get_flights:** Finds flights between two cities using SerpAPI.
- **expense_calculation:** Estimates and aggregates daily expenses.
- **report_generation:** Fuses all data and generates a descriptive, day-wise itinerary report.

---

## 🧠 Why a Multi-Agent Workflow?

### **Problems with LLM-Only Approaches**
- **Hallucination:** LLMs can generate plausible but incorrect or non-existent information.
- **Lack of Real-Time Data:** LLMs cannot fetch live prices, availability, or weather.
- **Poor Modularity:** Hard to maintain or extend for new data sources or features.

### **Advantages of Multi-Agent Orchestration**
- **Reliability:** Each agent/tool is responsible for a well-defined, testable task.
- **Real-Time Data:** Agents fetch live data from APIs, ensuring up-to-date results.
- **Modularity:** Easy to add, remove, or update agents for new APIs or features.
- **Stateful Execution:** The orchestrator manages dependencies and state, allowing for complex, multi-step workflows (e.g., "find a hotel near my favorite attraction").
- **Explainability:** Each step and data source is traceable, making the system auditable and debuggable.
- **Fusion & Deduplication:** The data fusion layer ensures that the final report is coherent, non-redundant, and actionable.

---

## 🚀 Example Workflow

1. **User Input:** "Plan a 5-day trip to Paris."
2. **Orchestrator:** Breaks down the request into sub-tasks.
3. **Agents:**  
   - Weather Agent fetches the forecast.
   - Flight Agent finds flights.
   - Hotel Agent finds hotels.
   - Attraction Agent lists POIs.
   - Restaurant Agent finds top restaurants.
   - Transportation Agent finds local transport options.
   - Expense Agent estimates costs.
4. **Data Fusion:** Merges and deduplicates all results.
5. **Report Generation:** Produces a detailed, day-wise itinerary and cost summary.

---

## 📝 How to Use

1. **Set up your `.env` file** with all required API keys (see `.env.example`).
2. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the orchestrator or main entry point:**  
   ```bash
   python main.py
   ```
4. **Interact with the system** via CLI, web UI, or API (depending on your frontend).

---

## 📄 Example Output

- **Day-wise itinerary** with weather, attractions, restaurants, and hotels.
- **Flight and local transport details** with live prices and timings.
- **Expense summary** (day-wise and total).
- **PDF or shareable report** with recommendations and optimal routes.

---

## 🧑‍💻 Extending the System

- Add new agents for more APIs (e.g., events, local guides).
- Swap out or upgrade agents without affecting the overall workflow.
- Integrate with chatbots or voice assistants for conversational planning.

---

## 📚 References

- [SerpAPI Google Maps API](https://serpapi.com/google-maps-api)
- [Geoapify Places API](https://apidocs.geoapify.com/docs/places/#api)
- [LangChain](https://python.langchain.com/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)

---

## 🏆 Why This Approach?

A multi-agent, orchestrated workflow ensures your travel planner is:
- **Accurate** (uses real APIs, not just LLM guesses)
- **Modular** (easy to maintain and extend)
- **Explainable** (each step is traceable)
- **User-centric** (produces actionable, reliable, and beautiful reports)
