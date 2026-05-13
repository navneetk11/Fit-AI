import streamlit as st


def show():
    st.title("📈 Progress Tracker")
    st.write("Track your fitness journey over time.")
    st.markdown("---")

    if "profile" not in st.session_state or not st.session_state.profile:
        st.warning("Please set up your profile first!")
        st.stop()

    workout_log = st.session_state.get("workout_log", [])

    if not workout_log:
        st.info("📝 No workouts logged yet! Go to **AI Coach** page and log your first workout.")
        st.stop()

    import pandas as pd
    import plotly.express as px

    df = pd.DataFrame(workout_log)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💪 Total Workouts", len(df))
    with col2:
        st.metric("⏱️ Total Minutes", df['duration'].sum())
    with col3:
        st.metric("📊 Avg Duration", f"{round(df['duration'].mean())} min")
    with col4:
        st.metric("🏆 Fav Workout", df['type'].mode()[0])

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📅 Workouts by Type")
        type_counts = df['type'].value_counts().reset_index()
        type_counts.columns = ['type', 'count']
        fig1 = px.pie(type_counts, values='count', names='type',
            color_discrete_sequence=[
                '#FF4500', '#FF6B35', '#FF8C5A', '#FFAD80', '#FFD0B0'])
        fig1.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("### ⏱️ Duration Per Workout")
        fig2 = px.bar(df, x='date', y='duration', color='type',
            color_discrete_sequence=[
                '#FF4500', '#FF6B35', '#FF8C5A', '#FFAD80', '#FFD0B0'],
            labels={'duration': 'Minutes', 'date': 'Date'})
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🔥 Workout Streak")

    total = len(workout_log)
    rest_days = sum(1 for w in workout_log if w['type'] == 'Rest Day')
    active = total - rest_days

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔥 Active Sessions", active)
    with col2:
        st.metric("😴 Rest Days", rest_days)
    with col3:
        consistency = round(active / total * 100) if total > 0 else 0
        st.metric("📊 Consistency", f"{consistency}%")

    st.markdown("---")
    st.markdown("### 📋 Full Workout History")
    st.dataframe(
        df[['date', 'type', 'duration', 'notes']].sort_index(ascending=False),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("🗑️ Clear Workout Log"):
            st.session_state.workout_log = []
            st.rerun()