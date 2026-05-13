import streamlit as st
from database import save_profile


def show():
    st.title("👤 Your Profile")
    st.write("Tell us about yourself so the AI can personalize everything.")
    st.markdown("---")

    if "profile" not in st.session_state:
        st.session_state.profile = {}

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name",
            value=st.session_state.profile.get("name", ""))
        age = st.number_input("Age", min_value=10, max_value=100,
            value=st.session_state.profile.get("age", 25))
        weight = st.number_input("Weight (kg)", min_value=30, max_value=300,
            value=st.session_state.profile.get("weight", 70))
        height = st.number_input("Height (cm)", min_value=100, max_value=250,
            value=st.session_state.profile.get("height", 170))

    with col2:
        gender = st.selectbox("Gender",
            ["Male", "Female", "Other"],
            index=["Male", "Female", "Other"].index(
                st.session_state.profile.get("gender", "Male")))

        goal = st.selectbox("Fitness Goal",
            ["Build Muscle", "Fat Loss", "Improve Endurance",
             "Stay Active", "Lose Weight"],
            index=["Build Muscle", "Fat Loss", "Improve Endurance",
                   "Stay Active", "Lose Weight"].index(
                st.session_state.profile.get("goal", "Build Muscle")))

        experience = st.selectbox("Experience Level",
            ["Beginner", "Intermediate", "Advanced"],
            index=["Beginner", "Intermediate", "Advanced"].index(
                st.session_state.profile.get("experience", "Beginner")))

        email = st.text_input("Email (for reminders)",
            value=st.session_state.profile.get("email", ""))

    st.markdown("### Equipment Available")
    equipment = st.multiselect("Select all that apply",
        ["Barbell", "Dumbbells", "Cables",
         "Machines", "Resistance Bands", "No Equipment"],
        default=st.session_state.profile.get("equipment", []))

    st.markdown("---")

    if st.button("💾 Save Profile", type="primary"):
        st.session_state.profile = {
            "name": name,
            "age": age,
            "weight": weight,
            "height": height,
            "gender": gender,
            "goal": goal,
            "experience": experience,
            "email": email,
            "equipment": equipment
        }
        save_profile(st.session_state.user_email, st.session_state.profile)
        st.session_state.show_profile_success = True

    if st.session_state.get("show_profile_success"):
        st.markdown(f"""
        <div style='background:#0a1a0a;border-left:4px solid #22c55e;
        border-radius:6px;padding:12px 16px;margin-top:8px'>
            <span style='color:#22c55e;font-weight:700'>
                ✅ Profile saved! Welcome {st.session_state.profile.get("name", "")}!
            </span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.show_profile_success = False