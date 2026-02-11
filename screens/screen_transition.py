import streamlit as st
import time
from utils.navigation import go_to

def screen_transition():
    child = st.session_state.get("child_data", {})
    
    if not child.get("dob") or not child.get("country"):
        st.error("Please provide date of birth and country to continue.")
        time.sleep(0.5)
        go_to("child_details")

    job = st.session_state.get("transition_job")

    if not job:
        go_to("child_details")
        st.stop()

    title = job["title"]
    emoji = job.get("emoji", "🤔")
    run = job["run"]
    next_screen = job["next"]

    st.markdown(
        f"""
        <div style="text-align:center;margin-top:4rem">
            <h1>{title}</h1>
            <div style="font-size:3rem;margin:1.5rem 0">{emoji}</div>
            <p style="font-size:1.05rem;color:#4b5563">
                Understanding your child...
            </p>
            <p style="color:#9ca3af">
                This takes just a few seconds
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.spinner("AI is analyzing..."):
        run()

    time.sleep(0.5)
    st.session_state.pop("transition_job")
    go_to(next_screen)
