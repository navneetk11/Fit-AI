import streamlit as st
from database import save_workout
from datetime import datetime


def show():
    st.title("🤖 AI Coach")
    st.write("Ask your personal AI fitness coach anything.")
    st.markdown("---")

    if "profile" not in st.session_state or not st.session_state.profile:
        st.warning("Please set up your profile first!")
        st.stop()

    profile = st.session_state.profile
    profile_str = f"""
    Name: {profile.get('name')}
    Age: {profile.get('age')}
    Gender: {profile.get('gender')}
    Weight: {profile.get('weight')}kg
    Height: {profile.get('height')}cm
    Goal: {profile.get('goal')}
    Experience: {profile.get('experience')}
    Equipment: {', '.join(profile.get('equipment', []))}
    """

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            with st.chat_message("user"):
                st.write(chat["message"])
        else:
            with st.chat_message("assistant", avatar="💪"):
                st.write(chat["message"])

    st.markdown("---")
    st.markdown("### ⚡ Quick Questions")
    col1, col2, col3 = st.columns(3)
    quick_question = None

    with col1:
        if st.button("What should I train today?"):
            quick_question = "What should I train today?"
    with col2:
        if st.button("How do I build muscle faster?"):
            quick_question = "How do I build muscle faster?"
    with col3:
        if st.button("What should I eat today?"):
            quick_question = "What should I eat today?"

    user_question = st.chat_input("Ask your AI coach anything...")
    if quick_question:
        user_question = quick_question

    if user_question:
        st.session_state.chat_history.append({
            "role": "user",
            "message": user_question
        })
        with st.chat_message("user"):
            st.write(user_question)

        with st.chat_message("assistant", avatar="💪"):
            with st.spinner("Coach is thinking..."):
                from main import ask_ai
                response = ask_ai(
                    question=user_question,
                    profile=profile_str,
                    notes=st.session_state.get("notes", "No notes")
                )
                st.write(response)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "message": response
                })

    st.markdown("---")
    st.markdown("### 📝 Log Today's Workout")

    col1, col2 = st.columns(2)
    with col1:
        workout_type = st.selectbox("Workout Type",
            ["Push", "Pull", "Legs", "Full Body",
             "Cardio", "Rest Day", "Other"])
    with col2:
        workout_duration = st.number_input(
            "Duration (minutes)", min_value=10, max_value=300, value=45)

    workout_notes = st.text_area(
        "Workout notes",
        placeholder="What did you do? How did it feel?",
        height=80)

    if st.button("✅ Log This Workout", type="primary"):
        if "workout_log" not in st.session_state:
            st.session_state.workout_log = []

        workout_data = {
            "date": datetime.now().strftime("%b %d, %Y"),
            "type": workout_type,
            "duration": workout_duration,
            "notes": workout_notes
        }
        st.session_state.workout_log.append(workout_data)
        save_workout(st.session_state.user_email, workout_data)
        st.toast(f"✅ {workout_type} logged — {workout_duration} mins!", icon="💪")

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()