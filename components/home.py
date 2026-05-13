import streamlit as st
from database import save_notes



def show():
    if "profile" not in st.session_state or \
            not st.session_state.profile or \
            not st.session_state.profile.get("name"):
        st.markdown("""
        <div style='text-align:center;padding:60px 0'>
            <div style='font-size:48px;margin-bottom:16px'>👋</div>
            <h2>Welcome to Fit AI!</h2>
            <p style='color:#666;font-size:16px;margin-bottom:32px'>
                Let's set up your profile so we can 
                personalize everything for you.
            </p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("SET UP MY PROFILE →", type="primary"):
                st.session_state.goto_profile = True
                st.rerun()
        st.stop()
    profile = st.session_state.profile
    name = profile.get("name", "Athlete")

    st.markdown(f"### Good morning, {name}! 🌅")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        workouts = len(st.session_state.get("workout_log", []))
        st.metric("Total Workouts", workouts, "this session")
    with col2:
        st.metric("Current Goal", profile.get("goal", "Not set"))
    with col3:
        st.metric("Weight", f"{profile.get('weight', 0)} kg")
    with col4:
        st.metric("Level", profile.get("experience", "Beginner"))

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 Your Goals")
        st.info(f"""
        **Goal:** {profile.get('goal', 'Not set')}  
        **Experience:** {profile.get('experience', 'Not set')}  
        **Equipment:** {', '.join(profile.get('equipment', ['Not set']))}
        """)

        st.markdown("### 📝 Quick Notes")
        notes = st.text_area(
            "Add notes for your AI coach",
            value=st.session_state.get("notes", ""),
            placeholder="e.g. did legs yesterday, feeling tired today...",
            height=100
        )
        if st.button("💾 Save Notes"):
            st.session_state.notes = notes
            save_notes(st.session_state.user_email, notes)
            st.success("Notes saved!")

    with col2:
        st.markdown("### 🤖 Today's AI Suggestion")

        if st.button("✨ Get Today's Suggestion", type="primary"):
            with st.spinner("AI is thinking..."):
                from main import ask_ai
                profile_str = f"""
                Name: {profile.get('name')}
                Age: {profile.get('age')}
                Gender: {profile.get('gender')}
                Weight: {profile.get('weight')}kg
                Goal: {profile.get('goal')}
                Experience: {profile.get('experience')}
                Equipment: {', '.join(profile.get('equipment', []))}
                """
                suggestion = ask_ai(
                    question="What should I focus on today for my fitness?",
                    profile=profile_str,
                    notes=st.session_state.get("notes", "No notes today")
                )
                st.session_state.today_suggestion = suggestion

        if "today_suggestion" in st.session_state:
            st.markdown(st.session_state.today_suggestion)
        else:
            st.markdown("*Click the button above to get your personalized suggestion!*")

    st.markdown("---")
    st.markdown("### 📋 Recent Workouts")
    workout_log = st.session_state.get("workout_log", [])

    if not workout_log:
        st.info("No workouts logged yet. Go to **AI Coach** to get a workout plan!")
    else:
        for workout in reversed(workout_log[-3:]):
            with st.expander(f"💪 {workout['date']} — {workout['type']}"):
                st.write(workout['notes'])