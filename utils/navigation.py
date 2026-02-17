import streamlit as st

def go_to(screen_name):
    """Navigate to a screen and push to history."""
    if "navigation_history" not in st.session_state:
        st.session_state.navigation_history = []
    
    # Don't push if we are just refreshing the same page or if it's the same as the last one
    if not st.session_state.navigation_history or st.session_state.navigation_history[-1] != st.session_state.get("current_screen"):
        current = st.session_state.get("current_screen")
        if current:
            st.session_state.navigation_history.append(current)
            
    st.session_state.current_screen = screen_name
    st.rerun()

def go_back():
    """Navigate to the previous screen in history."""
    if "navigation_history" not in st.session_state or not st.session_state.navigation_history:
        st.warning("No previous screen to go back to!")
        return

    previous_screen = st.session_state.navigation_history.pop()
    st.session_state.current_screen = previous_screen
    st.rerun()
