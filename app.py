import streamlit as st
from utils.navigation import go_to

from screens.screen_1_intro import screen_intro
from screens.screen_2_child_details import screen_child_details
from screens.screen_3_insights import screen_insights
from screens.screen_4_parenting_tips import screen_parenting_tips
from screens.screen_5_daily_tasks import screen_daily_tasks
from screens.screen_transition import screen_transition

# Load CSS
with open("styles/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "current_screen" not in st.session_state:
    st.session_state.current_screen = "intro"

screen_map = {
    "intro": screen_intro,
    "child_details": screen_child_details,
    "transition": screen_transition,   # ✅ THIS WAS MISSING
    "insights": screen_insights,
    "parenting_tips": screen_parenting_tips,
    "daily_tasks": screen_daily_tasks,
}

screen_map[st.session_state.current_screen]()
