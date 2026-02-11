import json
import streamlit as st
from utils.navigation import go_to
from utils.fallbacks import safe_text


def screen_parenting_tips():

    # Header
    st.markdown(
        """
        <div class="app-header">
            <span class="title-emoji floating-emoji">✨</span>
            <span class="app-title-text">Know Your Child</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<h2 style='text-align:center'>Parenting Tips That Fit Your Child</h2>",
        unsafe_allow_html=True
    )

    from ai.llm_client import clean_json_response
    from ai.tips_generator import generate_parenting_tips

    # 1. Parse JSON from state
    tips_data = []
    try:
        raw_data = st.session_state.get("parenting_tips", "")
        cleaned_data = clean_json_response(raw_data)
        
        if cleaned_data:
            tips_data = json.loads(cleaned_data)
        elif isinstance(raw_data, list):
            tips_data = raw_data
            
    except Exception as e:
        print(f"Tips Parsing Error: {e}")
        st.session_state.pop("parenting_tips", None)
        st.rerun()

    # 2. Safety Check (if empty, go back to insights to regenerate)
    if not tips_data:
        st.warning("⚠️ Tips couldn't be loaded. Retrying for you...")
        go_to("insights")
        st.stop()

    # Render Tips
    st.markdown('<div class="tips-container">', unsafe_allow_html=True)
    for i, tip in enumerate(tips_data):
        title = tip.get("title", f"Tip {i+1}")
        desc = tip.get("description", "")

        st.markdown(
            f"""
            <div class="tip-card">
                <div class="tip-title">⭐ {title}</div>
                <div class="tip-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Navigation
    cols = st.columns(2)
    col_back = cols[0]
    col_next = cols[1]

    with col_back:
        if st.button("← Back", key="btn_tips_back"):
            go_to("insights")

    with col_next:
        if st.button("Suggested Daily Tasks →", type="primary", key="btn_tips_to_tasks"):
            from ai.tasks_generator import generate_daily_tasks

            st.session_state.transition_job = {
                "title": "Creating Daily Tasks",
                "emoji": "🧩",
                "run": lambda: st.session_state.update({
                    "daily_tasks": generate_daily_tasks(
                        st.session_state.child_data,
                        st.session_state.selected_insights,
                        tips_data
                    )
                }),
                "next": "daily_tasks",
            }
            go_to("transition")