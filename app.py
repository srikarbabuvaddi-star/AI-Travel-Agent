import streamlit as st
import datetime
import json
import plotly.express as px
import plotly.graph_objects as go
from agent import TravelAgentEngine
from utils.validation import validate_trip_inputs
from utils.formatting import format_currency, get_source_badge_html
from services.optimizer import optimize_trip_budget

def run_streamlit_app():
    # Page configuration
    st.set_page_config(
        page_title="AI Smart Travel Agent",
        page_icon="✈️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for rich aesthetics and dark/glassmorphic theme elements
    st.markdown("""
<style>
    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #3B82F6, #8B5CF6, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #9CA3AF;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: rgba(31, 41, 55, 0.6);
        border: 1px solid rgba(75, 85, 99, 0.4);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    .metric-title {
        font-size: 0.85rem;
        color: #9CA3AF;
        font-weight: 600;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #F3F4F6;
        margin-top: 0.2rem;
    }
    .badge-live {
        background-color: #10B981; color: white; padding: 4px 8px; border-radius: 6px; font-weight: 600; font-size: 0.8rem;
    }
    .badge-est {
        background-color: #F59E0B; color: white; padding: 4px 8px; border-radius: 6px; font-weight: 600; font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

    # Initialize Session State
    if "current_plan" not in st.session_state:
        st.session_state["current_plan"] = None
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "saved_trips" not in st.session_state:
        st.session_state["saved_trips"] = {}
    
    agent = TravelAgentEngine()
    
    # Sidebar Configuration & Form Input
    st.sidebar.markdown("## ✈️ Trip Parameters")
    
    with st.sidebar.form(key="trip_input_form"):
        st.markdown("### 📍 Location")
        destination = st.text_input("Destination City", value="Goa", help="Enter any city in the world (e.g., Goa, Kyoto, Paris, Jaipur)")
        starting_city = st.text_input("Starting City", value="Hyderabad")
    
        st.markdown("### 📅 Dates")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            start_date = st.date_input("Start Date", value=datetime.date.today() + datetime.timedelta(days=10))
        with col_d2:
            end_date = st.date_input("End Date", value=datetime.date.today() + datetime.timedelta(days=14))
    
        st.markdown("### 👥 Travelers & Style")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            num_people = st.number_input("Travelers", min_value=1, max_value=20, value=4)
            trip_type = st.selectbox("Trip Type", ["Friends", "Family", "Couple", "Solo", "Business"])
        with col_t2:
            budget = st.number_input("Total Budget (₹)", min_value=1000, value=40000, step=2000)
            travel_style = st.selectbox("Travel Style", ["Moderate", "Budget", "Luxury", "Adventure", "Relaxed"])
    
        st.markdown("### 🍽️ Preferences")
        food_pref = st.selectbox("Food Preference", ["Any", "Vegetarian", "Non-Vegetarian", "Seafood", "Vegan"])
        interests = st.multiselect(
            "Interests",
            ["Beaches", "Culture", "Nature", "Food", "Shopping", "Photography", "History", "Temples", "Adventure"],
            default=["Beaches", "Culture", "Food"]
        )
    
        submit_btn = st.form_submit_button("✨ CREATE MY TRIP", use_container_width=True)
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🎬 LOAD EXPO DEMO TRIP", use_container_width=True, help="Load ready 5-day demo trip (Hyderabad -> Goa, ₹40k, 4 people)"):
        demo_inputs = {
            "destination": "Goa",
            "starting_city": "Hyderabad",
            "start_date": datetime.date.today() + datetime.timedelta(days=7),
            "end_date": datetime.date.today() + datetime.timedelta(days=11),
            "num_people": 4,
            "budget": 40000,
            "trip_type": "Friends",
            "travel_style": "Moderate",
            "food_pref": "Seafood",
            "interests": ["Beaches", "Culture", "Food", "Photography"]
        }
        with st.status("🎬 Loading Expo Demo Trip...", expanded=True) as status:
            st.session_state["current_plan"] = agent.plan_complete_trip(
                demo_inputs,
                status_callback=lambda msg: status.write(msg)
            )
            status.update(label="✅ Expo Demo Trip Loaded!", state="complete", expanded=False)
        st.rerun()
    
    # Execute Form Submission
    if submit_btn:
        is_valid, err_msg = validate_trip_inputs(destination, starting_city, start_date, end_date, num_people, budget)
        if not is_valid:
            st.error(f"⚠️ Input Error: {err_msg}")
        else:
            inputs = {
                "destination": destination,
                "starting_city": starting_city,
                "start_date": start_date,
                "end_date": end_date,
                "num_people": num_people,
                "budget": budget,
                "trip_type": trip_type,
                "travel_style": travel_style,
                "food_pref": food_pref,
                "interests": interests
            }
    
            with st.status("🤖 Agent actively executing MCP tool workflow...", expanded=True) as status:
                st.session_state["current_plan"] = agent.plan_complete_trip(
                    inputs,
                    status_callback=lambda msg: status.write(msg)
                )
                status.update(label="✅ Final Trip Plan Ready!", state="complete", expanded=False)
    
    # Header Display
    st.markdown('<div class="main-header">✈️ AI Smart Travel Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Tool-Using Autonomous AI Agent powered by MCP Architecture & Multi-Tier Resilience</div>', unsafe_allow_html=True)
    
    plan = st.session_state.get("current_plan")
    
    if not plan:
        st.info("👈 Fill in your travel details on the left sidebar and click **✨ CREATE MY TRIP**, or click **🎬 LOAD EXPO DEMO TRIP** to see the agent in action!")
    else:
        # EXECUTIVE DASHBOARD METRICS
        dest_name = plan["destination"].title()
        ai_score = plan["ai_score"]
        budget_data = plan["budget_breakdown"]["data"]
        total_cost = budget_data.get("total_group_cost", 36500)
        per_person = budget_data.get("cost_per_person", 9125)
        user_budget = budget_data.get("user_budget", 40000)
        rem_balance = user_budget - total_cost
    
        m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
        with m_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">⭐ AI Trip Score</div>
                <div class="metric-value" style="color: #60A5FA;">{ai_score} <span style="font-size: 1rem;">/ 100</span></div>
            </div>
            """, unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">💰 Total Cost</div>
                <div class="metric-value">₹{total_cost:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">👤 Per Person</div>
                <div class="metric-value">₹{per_person:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col4:
            status_color = "#10B981" if rem_balance >= 0 else "#EF4444"
            bal_text = f"Under budget (+₹{rem_balance:,})" if rem_balance >= 0 else f"Over budget (-₹{abs(rem_balance):,})"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">📊 Budget Status</div>
                <div class="metric-value" style="color: {status_color}; font-size: 1.2rem; margin-top: 0.6rem;">{bal_text}</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col5:
            w_source = plan["weather_forecast"].get("source", "Forecast")
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">⚡ Data Provenance</div>
                <div class="metric-value" style="font-size: 0.9rem; margin-top: 0.8rem;">{get_source_badge_html(w_source)}</div>
            </div>
            """, unsafe_allow_html=True)
    
        if "adaptation_note" in plan:
            st.success(f"🔔 **Plan Update:** {plan['adaptation_note']}")
    
        st.markdown("---")
    
        # 12 MAIN TABS
        tabs = st.tabs([
            "📋 Overview",
            "🌦️ Weather",
            "🗺️ Map",
            "📅 Itinerary",
            "📍 Places",
            "🍽️ Restaurants",
            "🏨 Hotels",
            "🚆 Transport",
            "🚗 Rentals",
            "🏥 Healthcare",
            "💰 Budget",
            "🤖 AI Advisor"
        ])
    
        # TAB 1: OVERVIEW
        with tabs[0]:
            col_ov1, col_ov2 = st.columns([2, 1])
            with col_ov1:
                st.markdown(f"### ✈️ {dest_name} Trip Summary")
                st.markdown(f"**Route:** {plan['starting_city'].title()} ➔ {dest_name}")
                st.markdown(f"**Dates:** {plan['dates']}")
                st.markdown(f"**Travelers:** {plan['num_people']} people ({plan['inputs'].get('trip_type', 'Friends')}) | **Style:** {plan['inputs'].get('travel_style', 'Moderate')}")
                st.markdown(f"**Food Preference:** {plan['inputs'].get('food_pref', 'Any')} | **Interests:** {', '.join(plan['inputs'].get('interests', ['Sightseeing']))}")
    
                st.markdown("#### 🌟 Key Highlights")
                for rec in plan.get("ai_recommendations", []):
                    st.markdown(rec)
    
            with col_ov2:
                st.markdown("### ⭐ AI Score Factors")
                st.caption("AI-generated planning score breakdown")
                for factor, val in plan.get("factor_breakdown", {}).items():
                    st.markdown(f"**{factor}:** {val}")
    
        # TAB 2: WEATHER
        with tabs[1]:
            w_res = plan["weather_forecast"]
            st.markdown(f"### 🌦️ Daily Weather Forecast ({dest_name})")
            st.markdown(f"Data Source Tag: {get_source_badge_html(w_res.get('source', 'Estimate'))}", unsafe_allow_html=True)
            st.caption("Weather conditions automatically adapt the daily activity schedule.")
    
            w_cols = st.columns(min(5, len(w_res.get("data", []))))
            for idx, day_w in enumerate(w_res.get("data", [])):
                with w_cols[idx % len(w_cols)]:
                    st.markdown(f"#### {day_w.get('day', f'Day {idx+1}')}")
                    st.markdown(f"📅 **{day_w.get('date', '')}**")
                    st.markdown(f"### {day_w.get('condition', '🌤️')}")
                    st.markdown(f"🌡️ **{day_w.get('min_temp', '22°C')} – {day_w.get('max_temp', '30°C')}**")
                    st.markdown(f"🌧️ Rain Prob: **{day_w.get('rain_prob', '10%')}**")
                    st.info(f"💡 {day_w.get('recommendation', 'Good for outdoor travel.')}")
    
        # TAB 3: MAP
        with tabs[2]:
            st.markdown(f"### 🗺️ Smart Travel Route Map")
            map_data = plan.get("map_route", {}).get("data", {})
            st.markdown(f"**Route Summary:** `{map_data.get('text_route_summary', dest_name)}`")
    
            waypoints = map_data.get("waypoints", [])
            if waypoints:
                try:
                    # Render Pydeck map using Streamlit native map
                    map_points = [{"lat": wp["lat"], "lon": wp["lon"], "name": wp["name"]} for wp in waypoints]
                    st.map(map_points, zoom=10, use_container_width=True)
                except Exception:
                    st.warning("🗺️ Interactive map fallback: See text-based sequence above.")
    
        # TAB 4: ITINERARY
        with tabs[3]:
            st.markdown(f"### 📅 Weather-Aware Day-by-Day Itinerary")
            for day_item in plan.get("itinerary", []):
                day_title = day_item.get("title", f"{day_item.get('day')} ({day_item.get('date')})")
                with st.expander(f"📌 {day_title} — {day_item.get('weather_summary')}", expanded=True):
                    st.caption(f"🗓️ Date: {day_item.get('date')} | {day_item.get('weather_note')}")
                    st.markdown(f"{day_item.get('morning')}")
                    st.markdown(f"{day_item.get('afternoon')}")
                    st.markdown(f"{day_item.get('evening')}")
                    
                    places_tags = ", ".join([f"`{p}`" for p in day_item.get("places_visited", []) if p])
                    if places_tags:
                        st.markdown(f"📍 **Attractions Visited:** {places_tags}")
                    st.markdown(f"🍽️ **Dining Highlights:** {day_item.get('dining')}")
    
        # TAB 5: PLACES
        with tabs[4]:
            st.markdown(f"### 📍 Tourist Attractions & Must-Visit Locations")
            places_data = plan.get("places", {})
            st.markdown(f"Data Source Tag: {get_source_badge_html(places_data.get('source', 'Places'))}", unsafe_allow_html=True)
            
            p_cols = st.columns(2)
            for idx, p in enumerate(places_data.get("data", [])):
                with p_cols[idx % 2]:
                    st.markdown(f"""
                    <div style="border: 1px solid rgba(75, 85, 99, 0.4); border-radius: 10px; padding: 1rem; margin-bottom: 1rem;">
                        <h4>📍 {p.get('name')}</h4>
                        <p><b>Category:</b> {p.get('category')} | <b>Rating:</b> ⭐ {p.get('rating', '4.5')}</p>
                        <p><b>Address:</b> {p.get('address')}</p>
                        <p><b>Suggested Duration:</b> ⏱️ {p.get('duration', '2 hours')}</p>
                        <p style="color: #9CA3AF;"><i>Why visit: {p.get('reason')}</i></p>
                    </div>
                    """, unsafe_allow_html=True)
    
        # TAB 6: RESTAURANTS
        with tabs[5]:
            st.markdown(f"### 🍽️ Curated Dining & Restaurants")
            rests_data = plan.get("restaurants", {})
            st.markdown(f"Data Source Tag: {get_source_badge_html(rests_data.get('source', 'Dining'))}", unsafe_allow_html=True)
    
            r_cols = st.columns(2)
            for idx, r in enumerate(rests_data.get("data", [])):
                with r_cols[idx % 2]:
                    st.markdown(f"""
                    <div style="border: 1px solid rgba(75, 85, 99, 0.4); border-radius: 10px; padding: 1rem; margin-bottom: 1rem;">
                        <h4>🍽️ {r.get('name')}</h4>
                        <p><b>Cuisine:</b> {r.get('cuisine')} | <b>Price:</b> {r.get('price_category')}</p>
                        <p><b>Address:</b> {r.get('address')}</p>
                        <p style="color: #9CA3AF;"><i>Reason: {r.get('reason')}</i></p>
                    </div>
                    """, unsafe_allow_html=True)
    
        # TAB 7: HOTELS
        with tabs[6]:
            st.markdown(f"### 🏨 Accommodation Options")
            hotels_data = plan.get("hotels", {})
            st.markdown(f"Data Source Tag: {get_source_badge_html(hotels_data.get('source', 'Hotels'))}", unsafe_allow_html=True)
    
            for h in hotels_data.get("data", []):
                st.markdown(f"""
                <div style="border: 1px solid rgba(75, 85, 99, 0.4); border-radius: 10px; padding: 1.2rem; margin-bottom: 1rem;">
                    <h3>🏨 {h.get('name')}</h3>
                    <p><b>Rating:</b> ⭐ {h.get('rating')} | <b>Est. Rate:</b> <span style="color: #10B981; font-weight:700;">{h.get('estimated_price')}</span></p>
                    <p><b>Address:</b> {h.get('address')} ({h.get('distance')})</p>
                    <p style="color: #9CA3AF;"><i>Recommendation: {h.get('reason')}</i></p>
                </div>
                """, unsafe_allow_html=True)
    
        # TAB 8: TRANSPORT
        with tabs[7]:
            st.markdown(f"### 🚆 Intercity Transport Comparison")
            trans_data = plan.get("transport", {}).get("data", {})
            st.markdown(f"Data Source Tag: {get_source_badge_html(plan.get('transport', {}).get('source', 'Transport'))}", unsafe_allow_html=True)
            st.info(f"💡 {trans_data.get('recommendation_summary', '')}")
    
            tr_cols = st.columns(3)
            cheap = trans_data.get("cheapest_option", {})
            best = trans_data.get("best_value_option", {})
            fast = trans_data.get("fastest_option", {})
    
            with tr_cols[0]:
                st.markdown("#### 💚 CHEAPEST OPTION")
                st.markdown(f"### {cheap.get('mode', 'Bus/Train')}")
                st.markdown(f"**Total Group Cost:** {cheap.get('total_group_cost')}")
                st.markdown(f"**Per Person:** {cheap.get('per_person_cost')}")
                st.markdown(f"**Duration:** {cheap.get('duration')}")
            with tr_cols[1]:
                st.markdown("#### ⭐ BEST VALUE OPTION")
                st.markdown(f"### {best.get('mode', 'AC Train')}")
                st.markdown(f"**Total Group Cost:** {best.get('total_group_cost')}")
                st.markdown(f"**Per Person:** {best.get('per_person_cost')}")
                st.markdown(f"**Duration:** {best.get('duration')}")
            with tr_cols[2]:
                st.markdown("#### ⚡ FASTEST OPTION")
                st.markdown(f"### {fast.get('mode', 'Flight')}")
                st.markdown(f"**Total Group Cost:** {fast.get('total_group_cost')}")
                st.markdown(f"**Per Person:** {fast.get('per_person_cost')}")
                st.markdown(f"**Duration:** {fast.get('duration')}")
    
        # TAB 9: RENTALS
        with tabs[8]:
            st.markdown(f"### 🚗 Vehicle & Bike Rentals")
            rent_data = plan.get("rentals", {}).get("data", {})
            st.markdown(f"Data Source Tag: {get_source_badge_html(plan.get('rentals', {}).get('source', 'Rentals'))}", unsafe_allow_html=True)
    
            for r in rent_data.get("rentals", []):
                rec_tag = "⭐ RECOMMENDED FOR YOUR GROUP" if r.get("is_recommended") else ""
                st.markdown(f"""
                <div style="border: 1px solid rgba(75, 85, 99, 0.4); border-radius: 10px; padding: 1rem; margin-bottom: 1rem;">
                    <h4>{r.get('vehicle_type')} ({r.get('model')}) <span style="color: #10B981; font-size: 0.85rem;">{rec_tag}</span></h4>
                    <p><b>Daily Rate:</b> {r.get('daily_rate')} | <b>Est. Total:</b> <b>{r.get('total_estimated')}</b></p>
                    <p><b>Suitability:</b> {r.get('suitable_group_size')}</p>
                    <p style="color: #9CA3AF;"><i>{r.get('reason')}</i></p>
                </div>
                """, unsafe_allow_html=True)
    
        # TAB 10: HEALTHCARE
        with tabs[9]:
            st.markdown(f"### 🏥 Emergency Healthcare Facilities")
            health_data = plan.get("healthcare", {})
            st.markdown(f"Data Source Tag: {get_source_badge_html(health_data.get('source', 'Healthcare'))}", unsafe_allow_html=True)
            st.caption("Locate nearby hospitals, urgent care centers, and pharmacies for travel safety.")
    
            for h in health_data.get("data", []):
                st.markdown(f"""
                <div style="border: 1px solid rgba(75, 85, 99, 0.4); border-radius: 10px; padding: 1rem; margin-bottom: 1rem;">
                    <h4>🏥 {h.get('name')}</h4>
                    <p><b>Address:</b> {h.get('address')} ({h.get('distance')})</p>
                    <p>📞 <b>Phone / Emergency:</b> <span style="color: #F59E0B; font-weight:700;">{h.get('phone')}</span></p>
                </div>
                """, unsafe_allow_html=True)
    
        # TAB 11: BUDGET
        with tabs[10]:
            st.markdown(f"### 💰 Itemized Budget Breakdown & Optimization")
            b_info = plan.get("budget_breakdown", {}).get("data", {})
            cats = b_info.get("categories", {})
    
            col_bg1, col_bg2 = st.columns([1, 1])
            with col_bg1:
                st.markdown("#### Cost Categories")
                for cat, val in cats.items():
                    st.markdown(f"• **{cat}:** ₹{val:,}")
                st.markdown("---")
                st.markdown(f"### **Total Cost:** ₹{b_info.get('total_group_cost', 0):,}")
                st.markdown(f"### **Cost Per Person:** ₹{b_info.get('cost_per_person', 0):,}")
    
            with col_bg2:
                st.markdown("#### 📊 Budget Allocation Chart")
                if cats:
                    fig = px.pie(
                        names=list(cats.keys()),
                        values=list(cats.values()),
                        hole=0.4,
                        color_discrete_sequence=px.colors.sequential.RdBu
                    )
                    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig, use_container_width=True)
    
            st.markdown("#### 💡 Savings Suggestions")
            for sugg in b_info.get("savings_suggestions", []):
                st.markdown(sugg)
    
        # TAB 12: AI ADVISOR & DECISION EXPLAINABILITY
        with tabs[11]:
            st.markdown("### 🤖 AI Decision Explainability")
            st.caption("Transparent rationale behind travel agent recommendations.")
    
            expl = plan.get("explanations", {})
            
            st.markdown("#### 🏨 WHY THIS HOTEL?")
            for item in expl.get("why_this_hotel", []):
                st.markdown(f"- {item}")
    
            st.markdown("#### 🚆 WHY THIS TRANSPORT?")
            for item in expl.get("why_this_transport", []):
                st.markdown(f"- {item}")
    
            st.markdown("#### 📅 WHY WAS DAY 2 PLANNED THIS WAY?")
            for item in expl.get("why_day2_changed", []):
                st.markdown(f"- {item}")
    
        st.markdown("---")
    
        # INTERACTIVE ACTION PANEL (OPTIMIZE, ADAPT PLAN, CHAT, SAVE, EXPORT)
        st.markdown("## 🛠️ Interactive Agent Tools & Controls")
        
        act_col1, act_col2, act_col3 = st.columns(3)
    
        # ACTION 1: OPTIMIZE MY TRIP
        with act_col1:
            st.markdown("### ✨ Budget Optimizer")
            if st.button("✨ OPTIMIZE MY TRIP", use_container_width=True):
                opt_res = optimize_trip_budget(plan)
                st.session_state["opt_res"] = opt_res
    
            if "opt_res" in st.session_state:
                opt = st.session_state["opt_res"]
                st.success(f"🎉 **Total Savings Found: ₹{opt['total_savings']:,}!**")
                st.markdown(f"**Original Total:** ₹{opt['original_total_cost']:,} ➔ **Optimized:** ₹{opt['optimized_total_cost']:,}")
                st.markdown(f"**Per Person:** ₹{opt['original_cost_per_person']:,} ➔ **₹{opt['optimized_cost_per_person']:,}**")
                for item in opt["optimizations_list"]:
                    st.markdown(f"• **{item['category']}:** {item['action']} ({item['savings']})")
    
        # ACTION 2: ADAPTIVE ITINERARY MODIFIER
        with act_col2:
            st.markdown("### 🔄 Adapt & Modify Trip")
            mod_prompt = st.text_input("Tell AI to edit plan:", placeholder="e.g. Change Day 2, Reduce budget, Add more temples")
            if st.button("🔄 UPDATE PLAN", use_container_width=True):
                if mod_prompt:
                    st.session_state["current_plan"] = agent.adapt_itinerary(plan, mod_prompt)
                    st.rerun()
    
        # ACTION 3: SAVE & EXPORT
        with act_col3:
            st.markdown("### 💾 Save & Export")
            if st.button("💾 SAVE TRIP", use_container_width=True):
                trip_key = f"{dest_name} ({plan['dates']})"
                st.session_state["saved_trips"][trip_key] = plan
                st.success(f"Saved trip: {trip_key}")
    
            # Download Export Report
            export_text = f"""# ✈️ AI Smart Travel Agent Trip Report - {dest_name}
    Date Generated: {datetime.date.today()}
    Route: {plan['starting_city'].title()} to {dest_name}
    Dates: {plan['dates']}
    Travelers: {plan['num_people']} people | Budget: ₹{user_budget:,}
    AI Score: {ai_score}/100
    
    ## Cost Breakdown
    Total Group Cost: ₹{total_cost:,}
    Cost Per Person: ₹{per_person:,}
    
    ## Daily Itinerary
    """
            for day_item in plan.get("itinerary", []):
                export_text += f"\n### {day_item.get('day')} ({day_item.get('date')})\n"
                export_text += f"- Morning: {day_item.get('morning')}\n"
                export_text += f"- Afternoon: {day_item.get('afternoon')}\n"
                export_text += f"- Evening: {day_item.get('evening')}\n"
    
            st.download_button(
                label="📄 EXPORT TRIP PLAN (.txt / .md)",
                data=export_text,
                file_name=f"{dest_name}_trip_plan.md",
                mime="text/markdown",
                use_container_width=True
            )
    
        # SAVED TRIPS DRAWER
        if st.session_state["saved_trips"]:
            with st.expander("📚 MY SAVED TRIPS", expanded=False):
                for k in st.session_state["saved_trips"].keys():
                    st.markdown(f"• **{k}**")
    
        # ACTION 4: CHAT WITH YOUR TRIP
        st.markdown("---")
        st.markdown("### 💬 Chat With Your Trip")
        st.caption("Ask questions about your trip itinerary, costs, hotels, or alternatives.")
    
        chat_input = st.text_input("Ask AI Travel Advisor:", placeholder="e.g. Which transport is cheapest? Why did you pick this hotel?")
        if st.button("💬 SEND QUESTION"):
            if chat_input:
                ans = agent.chat_with_trip(plan, chat_input)
                st.session_state["chat_history"].append({"q": chat_input, "a": ans})
    
        for chat in reversed(st.session_state["chat_history"]):
            st.markdown(f"**👤 You:** {chat['q']}")
            st.markdown(f"**🤖 AI Agent:** {chat['a']}")
            st.markdown("---")

# ==============================================================================
# WSGI Entrypoint Export for Serverless / Vercel Build Compatibility
# ==============================================================================
def handler(environ, start_response=None):
    """WSGI entrypoint to prevent Vercel Python runtime build errors."""
    if start_response:
        status = '200 OK'
        headers = [('Content-Type', 'text/html; charset=utf-8')]
        start_response(status, headers)
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>AI Smart Travel Agent</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 3rem; text-align: center; }
        .card { background: #1e293b; border-radius: 16px; padding: 2rem; max-width: 600px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        h1 { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        code { background: #334155; padding: 0.2rem 0.5rem; border-radius: 4px; color: #38bdf8; }
        .btn { display: inline-block; background: #3b82f6; color: white; text-decoration: none; padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 600; margin-top: 1rem; }
    </style>
</head>
<body>
    <div class="card">
        <h1>✈️ AI Smart Travel Agent</h1>
        <p>Deployed on <strong>Vercel</strong> Serverless Functions.</p>
        <p>To run interactive Streamlit app locally:</p>
        <p><code>streamlit run app.py</code></p>
    </div>
</body>
</html>"""
    return [html_content.encode('utf-8')]

app = handler
application = handler

if __name__ == "__main__":
    if st.runtime.exists():
        run_streamlit_app()
    else:
        import sys
        from streamlit.web import cli as stcli
        sys.argv = ["streamlit", "run", __file__]
        sys.exit(stcli.main())
else:
    if st.runtime.exists():
        run_streamlit_app()


