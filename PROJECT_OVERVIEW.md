# 📐 PROJECT OVERVIEW - AI Smart Travel Agent

## Conceptual Architecture

```
USER
 ↓ (Inputs: Destination, Dates, People, Budget, Style, Food, Interests)
STREAMLIT UI (app.py)
 ↓
AI AGENT ENGINE (agent.py)
 ↓
MCP TOOL LAYER (mcp/server.py using mcp v2.0.0 MCPServer)
 ↓
DATA SOURCES (Open-Meteo, OpenStreetMap, Nominatim, OSRM)
 ↓
NORMALIZATION LAYER (services/data_normalizer.py)
 ↓
BUDGET OPTIMIZER & ITINERARY BUILDER (services/optimizer.py & itinerary.py)
 ↓
ADAPTIVE PLANNING & EXPLAINABILITY ENGINE
 ↓
FINAL TRIP DASHBOARD & EXPORT
```

## Key Technologies & Concepts Explained

### 1. Model Context Protocol (MCP)
MCP acts as the standardized bridge connecting the AI Agent with external data capabilities. Rather than embedding API calls directly into LLM prompts, MCP tools return clean JSON structures (`status`, `source`, `data`, `message`).

### 2. Multi-Tiered Data Resilience
To prevent single API failures from stopping the application:
- **Tier 1 (Live APIs)**: Queries Open-Meteo & OpenStreetMap Overpass APIs.
- **Tier 2 (Dynamic City Estimator)**: Uses spatial geocoding & geographic distance metrics to dynamically estimate places, hotels, and rentals for **ANY city globally**.
- **Tier 3 (Curated Fallback Dataset)**: High-quality fallback records for popular destinations.

### 3. Weather-Aware Itinerary Generator
Adapts schedule according to daily weather forecasts:
- High Rain (>45%): Prioritizes indoor museums, covered markets, and cultural workshops.
- High Heat (>33°C): Shifts outdoor sightseeing to early mornings and sunset hours.
- Clear Skies: Optimizes for outdoor fort visits, beaches, and nature treks.

### 4. AI Trip Score & Decision Rationale
- **AI Planning Score**: Evaluates budget fit, weather suitability, travel efficiency, preference match, and accommodation style out of 100.
- **Decision Explainability**: Provides clear answers to *"Why this hotel?"*, *"Why this transport?"*, and *"Why was Day 2 planned this way?"*.
