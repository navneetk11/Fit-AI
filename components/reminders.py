import streamlit as st
from database import save_reminder_settings


def show():
    st.title("🔔 Reminders")
    st.write("Set up automated workout reminders sent to your email.")
    st.markdown("---")

    if "profile" not in st.session_state or not st.session_state.profile:
        st.warning("Please set up your profile first!")
        st.stop()

    profile = st.session_state.profile
    name = profile.get("name", "Athlete")
    goal = profile.get("goal", "fitness")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ⚙️ Reminder Settings")
        email = st.text_input(
            "Email address",
            value=profile.get("email", ""),
            placeholder="your@email.com"
        )
        st.markdown("**Remind me on:**")
        days = {
            "Monday": st.checkbox("Monday", value=True),
            "Tuesday": st.checkbox("Tuesday", value=False),
            "Wednesday": st.checkbox("Wednesday", value=True),
            "Thursday": st.checkbox("Thursday", value=False),
            "Friday": st.checkbox("Friday", value=True),
            "Saturday": st.checkbox("Saturday", value=False),
            "Sunday": st.checkbox("Sunday", value=False),
        }
        selected_days = [day for day, checked in days.items() if checked]
        reminder_time = st.time_input("Send reminder at", value=None)

    with col2:
        st.markdown("### 📧 Email Preview")
        st.info(f"""
        **To:** {email or "your@email.com"}  
        **Subject:** 💪 Time to work out, {name}!  

        *Hey {name}!*  
        *Your AI coach here — it's time to get moving!*  
        *Based on your goal to **{goal}**, today is a great day to train.*  
        *Open FitAI to get today's personalized workout plan.*  
        *Stay consistent — you've got this! 💪*  
        *— FitAI, Your AI Fitness Coach*
        """)

        st.markdown("### 📊 Reminder Stats")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("📧 Emails Sent",
                st.session_state.get("emails_sent", 0))
        with col_b:
            st.metric("📅 Active Days", len(selected_days))

    st.markdown("---")

    if st.button("💾 Save Reminder Settings", type="primary"):
        if not email:
            st.error("Please enter your email address!")
        elif not selected_days:
            st.error("Please select at least one day!")
        else:
            settings = {
                "email": email,
                "days": selected_days,
                "time": str(reminder_time)
            }
            st.session_state.reminder_settings = settings
            save_reminder_settings(st.session_state.user_email, settings)
            st.success(f"✅ Reminders saved! Days: {', '.join(selected_days)}")

    st.markdown("---")
    st.markdown("### 🧪 Send Test Email")
    st.write("Send yourself a test email to make sure it works.")

    if st.button("📧 Send Test Email Now"):
        if not email:
            st.error("Please enter your email first!")
        else:
            with st.spinner("Sending test email..."):
                try:
                    import smtplib
                    from email.mime.text import MIMEText
                    from email.mime.multipart import MIMEMultipart
                    import os
                    from dotenv import load_dotenv
                    load_dotenv()
                    from main import ask_ai

                    ai_message = ask_ai(
                        question="Write a short motivational workout reminder",
                        profile=f"Name: {name}, Goal: {goal}",
                        notes=st.session_state.get("notes", "")
                    )

                    msg = MIMEMultipart()
                    msg['Subject'] = f"💪 Time to work out, {name}!"
                    msg['From'] = os.getenv("EMAIL")
                    msg['To'] = email
                    msg.attach(MIMEText(
                        f"Hey {name}!\n\n{ai_message}\n\n"
                        f"Stay consistent!\n\n— FitAI Coach",
                        'plain'
                    ))

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                        server.login(
                            os.getenv("EMAIL"),
                            os.getenv("APP_PASSWORD")
                        )
                        server.send_message(msg)

                    st.session_state.emails_sent = (
                        st.session_state.get("emails_sent", 0) + 1)
                    st.success(f"✅ Test email sent to {email}!")
                    st.balloons()

                except Exception as e:
                    st.error(f"Email failed: {str(e)}")
                    st.info(
                        "Check EMAIL and APP_PASSWORD in your .env file")

    if "reminder_settings" in st.session_state:
        settings = st.session_state.reminder_settings
        st.markdown("---")
        st.markdown("### ✅ Current Settings")
        st.success(f"""
        **Email:** {settings.get('email')}  
        **Days:** {', '.join(settings.get('days', []))}  
        **Time:** {settings.get('time')}
        """)