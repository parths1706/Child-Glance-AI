import streamlit as st
import time
from utils.navigation import go_to
from utils.loading_states import get_loading_messages, get_fun_fact, get_estimated_time

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
    context = job.get("context", "general")  # insights, tips, tasks, or general

    # Header with pulsing emoji
    st.markdown(
        f"""
        <div style="text-align:center;margin-top:2rem">
            <h1 style="font-size:2rem;color:#1f2937;margin-bottom:1rem">{title}</h1>
            <div class="loading-emoji" style="font-size:4rem;margin:1rem 0;animation:pulse 2s ease-in-out infinite">
                {emoji}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Progress container
    progress_bar = st.progress(0)
    status_text = st.empty()
    fun_fact_text = st.empty()
    
    # Show estimated time
    estimated = get_estimated_time(context)
    st.markdown(
        f"""
        <p style="text-align:center;color:#9ca3af;font-size:0.9rem;margin-top:0.5rem">
            ⏱️ Estimated time: {estimated}
        </p>
        """,
        unsafe_allow_html=True
    )
    
    # Get context-aware messages
    messages = get_loading_messages(context)
    fun_fact = get_fun_fact()
    
    # Show fun fact
    fun_fact_text.markdown(
        f"""
        <div style="text-align:center;margin-top:2rem;padding:1rem;background:#f9fafb;border-radius:12px;border-left:4px solid #7c3aed">
            <p style="color:#4b5563;font-size:0.95rem;margin:0">{fun_fact}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Show initial progress and message
    progress_bar.progress(10)
    status_text.markdown(
        f"""
        <p style="text-align:center;color:#7c3aed;font-weight:600;font-size:1.05rem">
            {messages[0]}
        </p>
        """,
        unsafe_allow_html=True
    )
    
    # Small delay to show initial state
    time.sleep(0.3)
    
    # Update progress to show we're working
    progress_bar.progress(25)
    status_text.markdown(
        f"""
        <p style="text-align:center;color:#7c3aed;font-weight:600;font-size:1.05rem">
            {messages[1] if len(messages) > 1 else messages[0]}
        </p>
        """,
        unsafe_allow_html=True
    )
    
    time.sleep(0.2)
    
    # Run the actual AI task
    try:
        progress_bar.progress(40)
        run()
        
        # Show completion progress
        progress_bar.progress(100)
        status_text.markdown(
            """
            <p style="text-align:center;color:#10b981;font-weight:700;font-size:1.1rem">
                ✅ Complete!
            </p>
            """,
            unsafe_allow_html=True
        )
        
        time.sleep(0.5)
        
    except Exception as e:
        st.error(f"⚠️ Something went wrong: {str(e)}")
        st.stop()
    
    # Clean up and navigate
    st.session_state.pop("transition_job")
    go_to(next_screen)
