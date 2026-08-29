# ✈️ AI Smart Travel Agent

An intelligent, tool-using autonomous AI Travel Agent built with **Model Context Protocol (MCP)**, **LangChain / Google Gemini**, **Multi-Tiered Data Resilience**, **Budget Optimization**, **Adaptive Itinerary Planning**, and an interactive **Streamlit UI**.

---

## 📌 Problem & Solution

### The Problem
Traditional travel generators rely on static hardcoded templates or simple LLM prompts that invent fake prices, unavailable hotels, or outdated weather. When external APIs fail, standard travel tools break or throw ugly errors.

### The Solution
The **AI Smart Travel Agent** is an autonomous, tool-driven agent that interacts with data sources via **MCP tools**, standardizes results using a data normalization layer, applies multi-tiered data resilience, and dynamically creates realistic, weather-aware travel itineraries for **ANY city in the world**.

---

## 🤖 Why AI Agent & MCP Architecture?

- **Why AI Agent?** Unlike standard calculators, an AI Agent follows a goal-oriented workflow: **UNDERSTAND → PLAN → SELECT TOOLS → CALL TOOLS → COLLECT RESULTS → COMPARE → OPTIMIZE → CREATE PLAN → EXPLAIN**.
- **Why MCP (Model Context Protocol)?** MCP decouples tool execution from model logic. Tools are exposed as clean, standardized endpoints returning structured JSON.

---

## 🏗️ Architecture & Data Sources

```
USER INPUTS (Destination, Dates, Budget, Style, Food, Interests)
      │
      ▼
Streamlit User Interface (app.py)
      │
      ▼
AI Agent Decision Engine (agent.py)
      │
      ▼
MCP Tool Integration Layer (mcp/server.py v2.0.0)
      │
 ┌────┴───────────────────────────────────────────────────────┐
 │                       DATA SOURCES                         │
 ├────────────────────────────────────────────────────────────┤
 │ 1. Live Data (Open-Meteo Weather, OpenStreetMap Overpass)  │
 │ 2. Dynamic City Estimator (Works for ANY city in world)    │
 │ 3. Curated Baseline Dataset (data/curated_destinations.json)│
 └────┬───────────────────────────────────────────────────────┘
      │
      ▼
Data Normalization & Budget Optimizer (services/)
      │
      ▼
Final Trip Plan + AI Planning Score (88/100) + Explainability
```

---

## ⚡ Multi-Tier Data Resilience System

To guarantee the application **NEVER crashes**:
1. **Primary Data Source**: Queries live APIs (Open-Meteo for weather, OpenStreetMap for places, hotels, restaurants, healthcare).
2. **Secondary Source**: Dynamic geolocation & spatial estimation algorithm for any city worldwide.
3. **Curated Fallback**: High-quality static records for top destinations.
4. **Explicit Provenance Labeling**: Every metric displays its origin badge: `LIVE FORECAST`, `ESTIMATED WEATHER`, `LIVE PLACES`, `CURATED FALLBACK`, `DEMO DATA`.

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.12)

### 2. Environment Variables (.env)
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here  # Optional: For live LLM decision engine
GOOGLE_MAPS_API_KEY=                      # Optional
WEATHER_API_KEY=                          # Optional
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. How to Run Application
```bash
streamlit run app.py
```

---

## 🧪 How to Test

Run the automated test suite:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 🎬 Expo Demo Mode

1. Launch `streamlit run app.py`
2. Click **`🎬 LOAD EXPO DEMO TRIP`** on the sidebar.
3. Watch the progress status bar execute tool steps in real-time.
4. Explore all 12 tabs, click **`✨ OPTIMIZE MY TRIP`**, test adaptive edits (`"Change Day 2"`), and ask questions in **`💬 Chat With Your Trip`**.

---

## 📋 Features Checklist (21 Requirements)

- [x] Trip Overview
- [x] Weather Forecast (Daily min/max, rain prob, recommendation)
- [x] Weather-Aware Itinerary
- [x] Tourist Places & Ranking
- [x] Must-Visit Places
- [x] Restaurants & Cuisine Matching
- [x] Hotels & Accommodation Estimates
- [x] Transportation Options (Cheapest, Best Value, Fastest)
- [x] Car Rentals
- [x] Bike Rentals
- [x] Route/Map Waypoints & Text Route Summary
- [x] Itemized Budget Breakdown
- [x] Cost Per Person
- [x] Budget Optimization Engine
- [x] Nearby Hospitals & Healthcare Facilities
- [x] Adaptive Itinerary Modifier
- [x] AI Recommendations
- [x] Explanation of Decisions (Why Hotel / Transport / Day 2)
- [x] Save Trip
- [x] Export Trip Report
- [x] Context-Aware Chatbot
