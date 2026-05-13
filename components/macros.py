import streamlit as st
import json
import re


def show():
    st.title("📊 Macro Calculator")
    st.write("Get your personalized daily nutrition targets powered by AI.")
    st.markdown("---")

    if "profile" not in st.session_state or not st.session_state.profile:
        st.warning("Please set up your profile first!")
        st.stop()

    profile = st.session_state.profile

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 Your Details")
        goal = st.selectbox("Goal",
            ["Fat Loss", "Build Muscle", "Maintain Weight", "Improve Endurance"],
            index=["Fat Loss", "Build Muscle", "Maintain Weight", "Improve Endurance"].index(
                profile.get("goal", "Build Muscle")
                if profile.get("goal") in
                ["Fat Loss", "Build Muscle", "Maintain Weight", "Improve Endurance"]
                else "Build Muscle"))

        activity = st.selectbox("Activity Level",
            ["Sedentary (desk job, no exercise)",
             "Lightly Active (1-3 days/week)",
             "Moderately Active (3-5 days/week)",
             "Very Active (6-7 days/week)",
             "Extremely Active (twice a day)"])

        dietary = st.selectbox("Dietary Preference",
            ["No Preference", "Vegetarian", "Vegan",
             "Keto", "High Protein", "Gluten Free"])

        meals = st.slider("Meals per day", min_value=2, max_value=6, value=3)

    with col2:
        st.markdown("### 📋 Profile Summary")
        st.info(f"""
        **Name:** {profile.get('name')}  
        **Age:** {profile.get('age')} years  
        **Gender:** {profile.get('gender')}  
        **Weight:** {profile.get('weight')} kg  
        **Height:** {profile.get('height')} cm  
        **Experience:** {profile.get('experience')}  
        """)
        st.markdown("### 💡 How it works")
        st.markdown("""
        1. Your profile data is sent to the AI
        2. AI calculates your TDEE (total daily energy)
        3. Macros are split based on your goal
        4. You get protein, carbs, fat targets
        """)

    st.markdown("---")

    if st.button("⚡ Calculate My Macros", type="primary"):
        with st.spinner("AI is calculating your personalized macros..."):
            from main import get_macro
            goals_str = f"""
            Goal: {goal}
            Activity Level: {activity}
            Dietary Preference: {dietary}
            Meals per day: {meals}
            """
            profile_str = f"""
            Name: {profile.get('name')}
            Age: {profile.get('age')}
            Gender: {profile.get('gender')}
            Weight: {profile.get('weight')}kg
            Height: {profile.get('height')}cm
            Experience: {profile.get('experience')}
            """
            result = get_macro(goals_str, profile_str)
            st.session_state.macro_result = result

    if "macro_result" in st.session_state:
        st.markdown("---")
        st.markdown("### 🍽️ Your Personalized Macro Plan")

        raw = st.session_state.macro_result

        try:
            json_match = re.search(r'\{.*?\}', raw, re.DOTALL)
            if json_match:
                macros = json.loads(json_match.group())
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("🔥 Calories", f"{macros.get('calories', 0)} kcal")
                with col2:
                    st.metric("💪 Protein", f"{macros.get('protein', 0)}g")
                with col3:
                    st.metric("🍚 Carbs", f"{macros.get('carbs', 0)}g")
                with col4:
                    st.metric("🥑 Fat", f"{macros.get('fat', 0)}g")

                st.markdown("---")
                st.markdown("### 📊 Macro Breakdown")
                total = (macros.get('protein', 0) +
                         macros.get('carbs', 0) +
                         macros.get('fat', 0))
                if total > 0:
                    protein_pct = round(macros.get('protein', 0) / total * 100)
                    carbs_pct = round(macros.get('carbs', 0) / total * 100)
                    fat_pct = round(macros.get('fat', 0) / total * 100)
                    st.markdown(f"""
                    | Macro | Amount | Percentage |
                    |-------|--------|------------|
                    | 💪 Protein | {macros.get('protein')}g | {protein_pct}% |
                    | 🍚 Carbs | {macros.get('carbs')}g | {carbs_pct}% |
                    | 🥑 Fat | {macros.get('fat')}g | {fat_pct}% |
                    """)

                st.session_state.saved_macros = macros
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col2:
                    if st.button("💾 Save This Plan", type="primary"):
                        st.success("✅ Macro plan saved!")
            else:
                st.markdown(raw)
        except Exception:
            st.markdown(raw)