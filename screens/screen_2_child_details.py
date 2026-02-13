import streamlit as st
import time
from utils.navigation import go_to
from datetime import date
# from datetime import datetime

def calculate_age(dob):
    today = date.today()
    years = today.year - dob.year
    months = today.month - dob.month

    if today.day < dob.day:
        months -= 1
    if months < 0:
        years -= 1
        months += 12

    return years, months


def screen_child_details():
    st.markdown(
        """
        <div class="app-header">
            <span class="title-emoji floating-emoji">✨</span>
            <span class="app-title-text">Know Your Child</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h2>Tell Us About Your Child</h2>", unsafe_allow_html=True)

    dob = st.date_input(
        "📅 Date of Birth",
        min_value=date(2009, 1, 1),
        max_value=date.today()
    )

    from utils.location_data import get_all_countries, get_states_by_country, get_cities_by_state, get_cities_by_country, get_visitor_country

    # 🌍 Country Selection
    countries = get_all_countries()
    
    if "detected_country" not in st.session_state:
        st.session_state.detected_country = get_visitor_country()

    default_index = 0
    if st.session_state.detected_country and st.session_state.detected_country in countries:
        default_index = countries.index(st.session_state.detected_country)
    else:
        try:
            default_index = countries.index("India")
        except ValueError:
            default_index = 0

    country = st.selectbox(
        "🌍 Birth Country",
        countries,
        index=default_index,
        help="Start typing your country name to search"
    )

    # 🗺️ State Selection
    if "states_cache" not in st.session_state:
        st.session_state.states_cache = {}

    if country not in st.session_state.states_cache:
        with st.spinner(f"Finding states in {country}..."):
            st.session_state.states_cache[country] = sorted(get_states_by_country(country))
    
    states_list = st.session_state.states_cache[country]
    selected_state = None

    if states_list:
        selected_state = st.selectbox(
            "🗺️ State / Province",
            ["Select State..."] + states_list,
            help="Select the state to filter cities"
        )
    
    # 📍 City Selection
    if "cities_cache" not in st.session_state:
        st.session_state.cities_cache = {}
    
    # Key for caching depends on whether state is selected
    cache_key = f"{country}_{selected_state}" if selected_state and selected_state != "Select State..." else country

    if cache_key not in st.session_state.cities_cache:
        with st.spinner(f"Finding cities..."):
            if selected_state and selected_state != "Select State...":
                cities = get_cities_by_state(country, selected_state)
            else:
                cities = get_cities_by_country(country)
            st.session_state.cities_cache[cache_key] = sorted(cities)
    
    city_list = st.session_state.cities_cache[cache_key]

    # Unified "One Box" logic for City
    if "city_mode" not in st.session_state:
        st.session_state.city_mode = "select"

    if st.session_state.city_mode == "select":
        # Filter out empty cities if any
        clean_city_list = [c for c in city_list if c]
        
        city_choice = st.selectbox(
            "📍 Birth City",
            ["Type to search..."] + clean_city_list + ["✍️ My city is not listed (Type manually)"],
            help="Start typing to search your city!"
        )
        
        if city_choice == "✍️ My city is not listed (Type manually)":
            st.session_state.city_mode = "text"
            st.rerun()
        elif city_choice == "Type to search...":
            city = None
        else:
            city = city_choice
    else:
        # Manual Mode
        city = st.text_input(
            "📍 Birth City (Type manually)",
            placeholder="Search your city / write your city name",
            help="Type your city name exactly as it is"
        )
        if st.button("⬅️ Switch to list", key="back_to_select"):
            st.session_state.city_mode = "select"
            st.rerun()

    st.markdown("### ⏰ Birth Time (optional)")

    col1, col2, col3 = st.columns(3)

    with col1:
        hour = st.selectbox("Hour", ["Skip"] + [str(h) for h in range(1, 13)])

    with col2:
        minute = st.selectbox(
            "Minute",
            ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"]
        )

    with col3:
        period = st.selectbox("AM / PM", ["AM", "PM"])

    if hour == "Skip":
        birth_time = None
    else:
        birth_time = f"{hour}:{minute} {period}"

    st.caption("Birth time helps with deeper insights. Approximate is fine — or skip it.")

    if st.button("See Insights 🧬", key="go_insights"):
        if not city:
            st.error("Wait! We need a city to calculate the insights. Please select or type one! 🙏")
            st.stop()
            
        age_years, age_months = calculate_age(dob)

        # Reset location mode for next time
        st.session_state.pop("city_input_mode", None)

        # 🔥 CLEAR OLD DATA TO ENSURE REFRESH (CRITICAL)
        keys_to_clear = [
            "insights", "parenting_tips", "daily_tasks", 
            "selected_insights", "cities_cache", "transition_job"
        ]
        for k in keys_to_clear:
            st.session_state.pop(k, None)

        st.session_state.child_data = {
            "dob": dob,
            "age_years": age_years,
            "age_months": age_months,
            "country": country,
            "city": city,
            "birth_time": birth_time,
        }

        from ai.astrology_generator import generate_comprehensive_report
        
        # Capture strictly needed data for lambda closure
        c_data = st.session_state.child_data

        # Comprehensive generation transition
        st.session_state.transition_job = {
            "title": "Mapping the Stars & Personality",
            "emoji": "✨",
            "run": lambda: st.session_state.update({
                "full_report": generate_comprehensive_report(c_data)
            }),
            "next": "insights",
            "context": "insights",
        }

        go_to("transition")
