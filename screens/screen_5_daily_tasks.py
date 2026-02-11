import streamlit as st
import json
from ai.tasks_generator import generate_daily_tasks
from utils.fallbacks import safe_text
from utils.navigation import go_to


def screen_daily_tasks():

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
        "<h2 style='text-align:center'>Suggested Daily Tasks</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;color:#6b7280'>Tasks that suit your child’s nature and energy.</p>",
        unsafe_allow_html=True
    )

    if "daily_tasks" not in st.session_state:
            # Fallback if transition was skipped/lost
            with st.spinner("Finalizing your daily missions..."):
                from ai.tips_generator import generate_parenting_tips
                
                # Ensure we have insights and tips
                traits = st.session_state.get("selected_insights", [])
                tips_raw = st.session_state.get("parenting_tips", "[]")
                from ai.llm_client import clean_json_response
                
                # Just-in-time tips parse for the tasks call
                try:
                    tips = json.loads(clean_json_response(tips_raw))
                except:
                    tips = []

                st.session_state.daily_tasks = generate_daily_tasks(
                    st.session_state.child_data,
                    traits,
                    tips
                )

    # Parse JSON
    tasks_data = []
    from ai.llm_client import clean_json_response
    
    try:
        raw_data = st.session_state.get("daily_tasks", "")
        cleaned_data = clean_json_response(raw_data)
        
        if cleaned_data:
            tasks_data = json.loads(cleaned_data)
        elif isinstance(raw_data, list):
            tasks_data = raw_data
            
    except Exception as e:
        print(f"Tasks Parsing Error: {e}")
        st.session_state.pop("daily_tasks", None)
        st.rerun()

    # 3. Final Check & Rerun if empty
    if not tasks_data:
        st.session_state.pop("daily_tasks", None)
        st.rerun()

    # Render Tasks
    for task in tasks_data:
        title = task.get("title", "Daily Mission")
        desc = task.get("description", "")

        st.markdown(
            f"""
            <div class="task-card">
                <div class="task-title">✨ {title}</div>
                <div class="task-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Smart tip (static, manager-approved)
    st.markdown(
        """
        <div class="insight-card" style="background:#f5f3ff">
            <h4>💡 Activity Tip</h4>
            <p>Young children thrive on repetition. Don't be afraid to repeat these tasks tomorrow!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Start Daily Missions →", key="btn_start_missions"):
        st.session_state.active_missions = tasks_data
        st.success("✅ Daily missions started! You can now follow them every day.")


    if st.button("← Back", key="btn_back_to_tips"):
        go_to("parenting_tips")

    st.markdown("---")

    if st.button("🔁 Start Over", key="btn_start_over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        go_to("intro")