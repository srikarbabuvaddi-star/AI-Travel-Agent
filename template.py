INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>✈️ AI Smart Travel Agent</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0b0f19;
            color: #f8fafc;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        header {
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding: 1.2rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header-title {
            font-size: 1.8rem;
            font-weight: 800;
            background: linear-gradient(90deg, #38bdf8, #818cf8, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }
        .header-badge {
            background: rgba(56, 189, 248, 0.12);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.3);
            padding: 0.3rem 0.8rem;
            border-radius: 50px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        .app-container {
            display: flex;
            flex: 1;
            gap: 1.5rem;
            padding: 1.5rem;
            max-width: 1600px;
            margin: 0 auto;
            width: 100%;
        }
        .sidebar {
            width: 340px;
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 1.5rem;
            height: fit-content;
        }
        .sidebar h2 { font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; color: #f8fafc; display: flex; align-items: center; gap: 0.5rem; }
        .form-group { margin-bottom: 1rem; }
        .form-group label { display: block; font-size: 0.8rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px; }
        .form-control {
            width: 100%;
            padding: 0.7rem 0.9rem;
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 10px;
            color: #f8fafc;
            font-size: 0.95rem;
            font-family: inherit;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .form-control:focus { outline: none; border-color: #38bdf8; box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15); }
        .city-chips { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-top: 0.4rem; }
        .chip {
            background: rgba(51, 65, 85, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.05);
            color: #cbd5e1;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            font-size: 0.75rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .chip:hover { background: #38bdf8; color: #0f172a; font-weight: 600; }
        .btn-submit {
            width: 100%;
            padding: 0.85rem;
            background: linear-gradient(90deg, #2563eb, #7c3aed);
            border: none;
            border-radius: 12px;
            color: white;
            font-weight: 700;
            font-size: 1rem;
            cursor: pointer;
            margin-top: 0.5rem;
            transition: transform 0.2s, box-shadow 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }
        .btn-submit:hover { transform: translateY(-1px); box-shadow: 0 10px 25px rgba(37, 99, 235, 0.4); }
        .btn-demo {
            width: 100%;
            padding: 0.65rem;
            background: rgba(51, 65, 85, 0.5);
            border: 1px dashed rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            color: #cbd5e1;
            font-weight: 600;
            font-size: 0.85rem;
            cursor: pointer;
            margin-top: 0.8rem;
            transition: all 0.2s;
        }
        .btn-demo:hover { background: #334155; color: white; }

        .main-content { flex: 1; min-width: 0; }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        .metric-card {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 1.2rem;
            text-align: center;
        }
        .metric-title { font-size: 0.75rem; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
        .metric-value { font-size: 1.8rem; font-weight: 800; margin-top: 0.2rem; color: #f8fafc; }

        .tabs-nav {
            display: flex;
            gap: 0.5rem;
            overflow-x: auto;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }
        .tab-btn {
            background: transparent;
            border: none;
            color: #94a3b8;
            padding: 0.6rem 1.1rem;
            font-size: 0.9rem;
            font-weight: 600;
            border-radius: 10px;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }
        .tab-btn:hover { color: #f8fafc; background: rgba(255, 255, 255, 0.05); }
        .tab-btn.active { color: #38bdf8; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.3); }

        .tab-pane { display: none; }
        .tab-pane.active { display: block; animation: fadeIn 0.3s ease; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }

        .card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }
        .info-card {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 1.2rem;
            transition: transform 0.2s, border-color 0.2s;
        }
        .info-card:hover { border-color: rgba(56, 189, 248, 0.4); transform: translateY(-2px); }
        .info-card h4 { color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.4rem; }
        .info-card p { font-size: 0.85rem; color: #94a3b8; line-height: 1.5; }

        .itinerary-day {
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 1.4rem;
            margin-bottom: 1rem;
        }
        .itinerary-header { font-size: 1.2rem; font-weight: 700; color: #38bdf8; margin-bottom: 0.4rem; }
        .itinerary-meta { font-size: 0.85rem; color: #cbd5e1; margin-bottom: 1rem; }
        .activity-block { margin-bottom: 0.75rem; font-size: 0.95rem; line-height: 1.5; }

        .loader {
            display: none;
            text-align: center;
            padding: 3rem;
        }
        .spinner {
            width: 45px;
            height: 45px;
            border: 4px solid rgba(56, 189, 248, 0.2);
            border-top-color: #38bdf8;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem auto;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        .tool-panel {
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 1.5rem;
            margin-top: 2rem;
        }
        .tool-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-top: 1rem; }
        .tool-box { background: #0f172a; border: 1px solid #334155; border-radius: 12px; padding: 1.2rem; }

        table { width: 100%; border-collapse: collapse; margin-top: 1rem; border-radius: 12px; overflow: hidden; }
        th, td { padding: 0.8rem 1rem; text-align: left; }
        th { background: #0f172a; color: #38bdf8; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; }
        td { background: rgba(30, 41, 59, 0.6); border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.9rem; }

        @media (max-width: 900px) {
            .app-container { flex-direction: column; }
            .sidebar { width: 100%; }
        }
    </style>
</head>
<body>
    <header>
        <div class="header-title">✈️ AI Smart Travel Agent</div>
        <div class="header-badge">⚡ Autonomous Multi-Tool Engine</div>
    </header>

    <div class="app-container">
        <!-- SIDEBAR -->
        <div class="sidebar">
            <h2>✈️ Trip Parameters</h2>
            <form id="tripForm">
                <div class="form-group">
                    <label>Destination City</label>
                    <input type="text" id="destination" class="form-control" value="Goa" required />
                    <div class="city-chips">
                        <span class="chip" onclick="setCity('Goa')">Goa</span>
                        <span class="chip" onclick="setCity('Paris')">Paris</span>
                        <span class="chip" onclick="setCity('Kyoto')">Kyoto</span>
                        <span class="chip" onclick="setCity('Tokyo')">Tokyo</span>
                        <span class="chip" onclick="setCity('Jaipur')">Jaipur</span>
                    </div>
                </div>
                <div class="form-group">
                    <label>Starting City</label>
                    <input type="text" id="starting_city" class="form-control" value="Hyderabad" required />
                </div>
                <div class="form-group">
                    <label>Travelers</label>
                    <input type="number" id="num_people" class="form-control" value="4" min="1" max="20" />
                </div>
                <div class="form-group">
                    <label>Total Budget (₹)</label>
                    <input type="number" id="budget" class="form-control" value="40000" step="1000" />
                </div>
                <div class="form-group">
                    <label>Travel Style</label>
                    <select id="travel_style" class="form-control">
                        <option value="Moderate">Moderate</option>
                        <option value="Budget">Budget</option>
                        <option value="Luxury">Luxury</option>
                        <option value="Adventure">Adventure</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Food Preference</label>
                    <select id="food_pref" class="form-control">
                        <option value="Seafood">Seafood</option>
                        <option value="Vegetarian">Vegetarian</option>
                        <option value="Non-Vegetarian">Non-Vegetarian</option>
                        <option value="Any">Any</option>
                    </select>
                </div>
                <button type="submit" class="btn-submit">✨ CREATE MY TRIP</button>
            </form>
            <button class="btn-demo" onclick="loadDemo('Goa')">🎬 LOAD EXPO DEMO TRIP (GOA)</button>
            <button class="btn-demo" onclick="loadDemo('Paris')">🎬 LOAD EXPO DEMO TRIP (PARIS)</button>
        </div>

        <!-- MAIN CONTENT -->
        <div class="main-content">
            <div id="loader" class="loader">
                <div class="spinner"></div>
                <h3 style="color:#38bdf8;">🤖 Agent actively executing MCP tool workflow...</h3>
                <p style="color:#94a3b8; font-size:0.9rem; margin-top:0.5rem;">Fetching parallel Weather, Places, Hotels, Transport & Healthcare APIs</p>
            </div>

            <div id="results" style="display:none;">
                <!-- EXECUTIVE METRICS -->
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-title">⭐ AI Trip Score</div>
                        <div class="metric-value" id="mScore" style="color:#38bdf8;">-</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">💰 Total Cost</div>
                        <div class="metric-value" id="mTotalCost">-</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">👤 Per Person</div>
                        <div class="metric-value" id="mPerPerson">-</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">📊 Budget Status</div>
                        <div class="metric-value" id="mBudgetStatus" style="font-size:1.1rem; margin-top:0.4rem;">-</div>
                    </div>
                </div>

                <!-- NAVIGATION TABS -->
                <div class="tabs-nav">
                    <button class="tab-btn active" onclick="switchTab('tOverview')">📋 Overview</button>
                    <button class="tab-btn" onclick="switchTab('tWeather')">🌦️ Weather</button>
                    <button class="tab-btn" onclick="switchTab('tItinerary')">📅 Itinerary</button>
                    <button class="tab-btn" onclick="switchTab('tPlaces')">📍 Places</button>
                    <button class="tab-btn" onclick="switchTab('tRestaurants')">🍽️ Dining</button>
                    <button class="tab-btn" onclick="switchTab('tHotels')">🏨 Hotels</button>
                    <button class="tab-btn" onclick="switchTab('tTransport')">🚆 Transport</button>
                    <button class="tab-btn" onclick="switchTab('tRentals')">🚗 Rentals</button>
                    <button class="tab-btn" onclick="switchTab('tHealthcare')">🏥 Healthcare</button>
                    <button class="tab-btn" onclick="switchTab('tBudget')">💰 Budget</button>
                </div>

                <!-- TAB PANES -->
                <div id="tOverview" class="tab-pane active"></div>
                <div id="tWeather" class="tab-pane"></div>
                <div id="tItinerary" class="tab-pane"></div>
                <div id="tPlaces" class="tab-pane"></div>
                <div id="tRestaurants" class="tab-pane"></div>
                <div id="tHotels" class="tab-pane"></div>
                <div id="tTransport" class="tab-pane"></div>
                <div id="tRentals" class="tab-pane"></div>
                <div id="tHealthcare" class="tab-pane"></div>
                <div id="tBudget" class="tab-pane"></div>

                <!-- INTERACTIVE CONTROLS -->
                <div class="tool-panel">
                    <h3 style="color:#f8fafc; font-size:1.2rem;">🛠️ Interactive Agent Tools & Controls</h3>
                    <div class="tool-grid">
                        <div class="tool-box">
                            <h4 style="color:#38bdf8; margin-bottom:0.5rem;">✨ Budget Optimizer</h4>
                            <p style="font-size:0.85rem; color:#94a3b8; margin-bottom:0.8rem;">Analyze alternatives to save maximum budget.</p>
                            <button class="btn-submit" style="background:#10b981;" onclick="optimizeBudget()">✨ OPTIMIZE MY TRIP</button>
                            <div id="optResults" style="margin-top:0.8rem; font-size:0.85rem; color:#f8fafc;"></div>
                        </div>

                        <div class="tool-box">
                            <h4 style="color:#38bdf8; margin-bottom:0.5rem;">🔄 Adapt & Modify Plan</h4>
                            <input type="text" id="modPrompt" class="form-control" placeholder="e.g. Change Day 2, Add temples" style="margin-bottom:0.6rem;" />
                            <button class="btn-submit" onclick="adaptPlan()">🔄 UPDATE PLAN</button>
                        </div>

                        <div class="tool-box">
                            <h4 style="color:#38bdf8; margin-bottom:0.5rem;">💬 AI Trip Advisor</h4>
                            <input type="text" id="chatPrompt" class="form-control" placeholder="Ask question about costs or stay..." style="margin-bottom:0.6rem;" />
                            <button class="btn-submit" style="background:#8b5cf6;" onclick="askAdvisor()">💬 SEND QUESTION</button>
                            <div id="chatAnswer" style="margin-top:0.8rem; font-size:0.85rem; color:#cbd5e1;"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentPlan = null;

        function setCity(city) {
            document.getElementById('destination').value = city;
        }

        function loadDemo(city) {
            document.getElementById('destination').value = city;
            document.getElementById('starting_city').value = 'Hyderabad';
            document.getElementById('budget').value = city === 'Paris' ? 120000 : 40000;
            fetchTrip();
        }

        document.getElementById('tripForm').addEventListener('submit', function(e) {
            e.preventDefault();
            fetchTrip();
        });

        async function fetchTrip() {
            const dest = document.getElementById('destination').value;
            const start = document.getElementById('starting_city').value;
            const people = document.getElementById('num_people').value;
            const budget = document.getElementById('budget').value;
            const style = document.getElementById('travel_style').value;
            const food = document.getElementById('food_pref').value;

            document.getElementById('results').style.display = 'none';
            document.getElementById('loader').style.display = 'block';

            try {
                const res = await fetch(`/api/plan?destination=${encodeURIComponent(dest)}&starting_city=${encodeURIComponent(start)}&num_people=${people}&budget=${budget}&travel_style=${style}&food_pref=${food}`);
                const plan = await res.json();
                currentPlan = plan;
                renderPlan(plan);
            } catch (err) {
                alert('Error loading trip plan: ' + err);
            } finally {
                document.getElementById('loader').style.display = 'none';
                document.getElementById('results').style.display = 'block';
            }
        }

        function renderPlan(plan) {
            const budgetData = plan.budget_breakdown.data;
            const totalCost = budgetData.total_group_cost || 0;
            const perPerson = budgetData.cost_per_person || 0;
            const userBudget = budgetData.user_budget || 0;
            const rem = userBudget - totalCost;

            document.getElementById('mScore').innerText = plan.ai_score + ' / 100';
            document.getElementById('mTotalCost').innerText = '₹' + totalCost.toLocaleString();
            document.getElementById('mPerPerson').innerText = '₹' + perPerson.toLocaleString();
            
            const bStatus = document.getElementById('mBudgetStatus');
            if (rem >= 0) {
                bStatus.innerText = 'Under budget (+₹' + rem.toLocaleString() + ')';
                bStatus.style.color = '#10b981';
            } else {
                bStatus.innerText = 'Over budget (-₹' + Math.abs(rem).toLocaleString() + ')';
                bStatus.style.color = '#ef4444';
            }

            // Overview
            let ov = `<h3>✈️ ${plan.destination} Trip Summary</h3>
            <p><b>Route:</b> ${plan.starting_city} ➔ ${plan.destination}</p>
            <p><b>Dates:</b> ${plan.dates}</p>
            <p><b>Travelers:</b> ${plan.num_people} people | <b>Style:</b> ${plan.inputs.travel_style}</p>
            <h4 style="margin-top:1rem; color:#38bdf8;">🌟 Key Highlights</h4>`;
            (plan.ai_recommendations || []).forEach(r => ov += `<p style="margin-top:0.3rem;">${r}</p>`);
            document.getElementById('tOverview').innerHTML = ov;

            // Weather
            let wHtml = `<div class="card-grid">`;
            (plan.weather_forecast.data || []).forEach(w => {
                wHtml += `<div class="info-card">
                    <h4 style="color:#38bdf8;">${w.day} (${w.date})</h4>
                    <div style="font-size:1.6rem; margin:0.3rem 0;">${w.condition}</div>
                    <p><b>Temp:</b> ${w.min_temp} – ${w.max_temp}</p>
                    <p><b>Rain Prob:</b> ${w.rain_prob}</p>
                    <p style="color:#94a3b8; margin-top:0.4rem;">💡 ${w.recommendation}</p>
                </div>`;
            });
            wHtml += `</div>`;
            document.getElementById('tWeather').innerHTML = wHtml;

            // Itinerary
            let itHtml = '';
            (plan.itinerary || []).forEach(day => {
                const tags = (day.places_visited || []).map(p => `<span style="background:#334155; padding:2px 8px; border-radius:4px; font-size:0.8rem; margin-right:4px;">${p}</span>`).join('');
                itHtml += `<div class="itinerary-day">
                    <div class="itinerary-header">📌 ${day.title || day.day}</div>
                    <div class="itinerary-meta">🗓️ Date: ${day.date} | ${day.weather_note}</div>
                    <div class="activity-block">${day.morning}</div>
                    <div class="activity-block">${day.afternoon}</div>
                    <div class="activity-block">${day.evening}</div>
                    <div style="margin-top:0.6rem;">📍 <b>Attractions Visited:</b> ${tags}</div>
                    <div style="margin-top:0.4rem;">🍽️ <b>Dining Highlights:</b> ${day.dining}</div>
                </div>`;
            });
            document.getElementById('tItinerary').innerHTML = itHtml;

            // Places
            let pHtml = `<div class="card-grid">`;
            (plan.places.data || []).forEach(p => {
                pHtml += `<div class="info-card">
                    <h4>📍 ${p.name}</h4>
                    <p><b>Category:</b> ${p.category} | ⭐ <b>Rating:</b> ${p.rating}</p>
                    <p><b>Duration:</b> ${p.duration}</p>
                    <p style="color:#cbd5e1; font-style:italic; margin-top:0.4rem;">${p.reason}</p>
                </div>`;
            });
            pHtml += `</div>`;
            document.getElementById('tPlaces').innerHTML = pHtml;

            // Restaurants
            let rHtml = `<div class="card-grid">`;
            (plan.restaurants.data || []).forEach(r => {
                rHtml += `<div class="info-card">
                    <h4>🍽️ ${r.name}</h4>
                    <p><b>Cuisine:</b> ${r.cuisine} | <b>Price:</b> ${r.price_category}</p>
                    <p style="color:#cbd5e1; font-style:italic; margin-top:0.4rem;">${r.reason}</p>
                </div>`;
            });
            rHtml += `</div>`;
            document.getElementById('tRestaurants').innerHTML = rHtml;

            // Hotels
            let hHtml = `<div class="card-grid">`;
            (plan.hotels.data || []).forEach(h => {
                hHtml += `<div class="info-card">
                    <h4>🏨 ${h.name}</h4>
                    <p>⭐ <b>Rating:</b> ${h.rating} | <span style="color:#10b981; font-weight:700;">${h.estimated_price}</span></p>
                    <p><b>Distance:</b> ${h.distance}</p>
                    <p style="color:#cbd5e1; font-style:italic; margin-top:0.4rem;">${h.reason}</p>
                </div>`;
            });
            hHtml += `</div>`;
            document.getElementById('tHotels').innerHTML = hHtml;

            // Transport
            const tData = plan.transport.data || {};
            const cheap = tData.cheapest_option || {};
            const best = tData.best_value_option || {};
            const fast = tData.fastest_option || {};
            document.getElementById('tTransport').innerHTML = `
            <div class="card-grid">
                <div class="info-card" style="border-color:#10b981;">
                    <div style="color:#10b981; font-weight:700; font-size:0.8rem;">💚 CHEAPEST</div>
                    <h4>${cheap.mode || 'Bus'}</h4>
                    <p><b>Total:</b> ${cheap.total_group_cost}</p>
                    <p><b>Per Person:</b> ${cheap.per_person_cost}</p>
                    <p><b>Duration:</b> ${cheap.duration}</p>
                </div>
                <div class="info-card" style="border-color:#38bdf8;">
                    <div style="color:#38bdf8; font-weight:700; font-size:0.8rem;">⭐ BEST VALUE</div>
                    <h4>${best.mode || 'Train'}</h4>
                    <p><b>Total:</b> ${best.total_group_cost}</p>
                    <p><b>Per Person:</b> ${best.per_person_cost}</p>
                    <p><b>Duration:</b> ${best.duration}</p>
                </div>
                <div class="info-card" style="border-color:#f59e0b;">
                    <div style="color:#f59e0b; font-weight:700; font-size:0.8rem;">⚡ FASTEST</div>
                    <h4>${fast.mode || 'Flight'}</h4>
                    <p><b>Total:</b> ${fast.total_group_cost}</p>
                    <p><b>Per Person:</b> ${fast.per_person_cost}</p>
                    <p><b>Duration:</b> ${fast.duration}</p>
                </div>
            </div>`;

            // Rentals
            let rentHtml = `<div class="card-grid">`;
            (plan.rentals.data.rentals || []).forEach(r => {
                rentHtml += `<div class="info-card">
                    <h4>${r.vehicle_type} (${r.model})</h4>
                    <p><b>Rate:</b> ${r.daily_rate} | <b>Est:</b> <span style="color:#10b981; font-weight:700;">${r.total_estimated}</span></p>
                    <p style="color:#cbd5e1; margin-top:0.3rem;">${r.reason}</p>
                </div>`;
            });
            rentHtml += `</div>`;
            document.getElementById('tRentals').innerHTML = rentHtml;

            // Healthcare
            let healthHtml = `<div class="card-grid">`;
            (plan.healthcare.data || []).forEach(h => {
                healthHtml += `<div class="info-card">
                    <h4>🏥 ${h.name}</h4>
                    <p><b>Address:</b> ${h.address} (${h.distance})</p>
                    <p style="color:#f59e0b; font-weight:700; margin-top:0.3rem;">📞 Phone: ${h.phone}</p>
                </div>`;
            });
            healthHtml += `</div>`;
            document.getElementById('tHealthcare').innerHTML = healthHtml;

            // Budget Table
            let bRows = '';
            for (let [cat, val] of Object.entries(budgetData.categories || {})) {
                bRows += `<tr><td>${cat}</td><td style="text-align:right; font-weight:600;">₹${val.toLocaleString()}</td></tr>`;
            }
            document.getElementById('tBudget').innerHTML = `
            <table>
                <thead><tr><th>Cost Category</th><th style="text-align:right;">Group Estimated Cost</th></tr></thead>
                <tbody>
                    ${bRows}
                    <tr style="background:#0f172a; font-weight:700;">
                        <td>TOTAL ESTIMATED COST</td>
                        <td style="text-align:right; color:#10b981;">₹${totalCost.toLocaleString()}</td>
                    </tr>
                </tbody>
            </table>`;
        }

        function switchTab(tabId) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }

        async function optimizeBudget() {
            if (!currentPlan) return;
            const res = await fetch('/api/optimize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(currentPlan)
            });
            const opt = await res.json();
            document.getElementById('optResults').innerHTML = `
            <div style="background:rgba(16,185,129,0.15); border:1px solid #10b981; padding:0.8rem; border-radius:8px;">
                <b>🎉 Total Savings Found: ₹${opt.total_savings.toLocaleString()}!</b><br>
                <span>Original: ₹${opt.original_total_cost.toLocaleString()} ➔ Optimized: ₹${opt.optimized_total_cost.toLocaleString()}</span>
            </div>`;
        }

        async function adaptPlan() {
            if (!currentPlan) return;
            const prompt = document.getElementById('modPrompt').value;
            if (!prompt) return;
            const res = await fetch('/api/adapt', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ plan: currentPlan, prompt: prompt })
            });
            const updated = await res.json();
            currentPlan = updated;
            renderPlan(updated);
            alert('Plan updated: ' + (updated.adaptation_note || 'Modified schedule'));
        }

        async function askAdvisor() {
            if (!currentPlan) return;
            const q = document.getElementById('chatPrompt').value;
            if (!q) return;
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ plan: currentPlan, question: q })
            });
            const data = await res.json();
            document.getElementById('chatAnswer').innerText = '🤖 AI: ' + data.answer;
        }

        // Auto load initial trip
        fetchTrip();
    </script>
</body>
</html>"""
