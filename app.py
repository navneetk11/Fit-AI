import streamlit as st

st.set_page_config(
    page_title="FitAI",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

from database import load_all_user_data
from components import home, profile, coach, macros, progress, reminders

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap');

    .stApp {
        background-color: #0a0a0a;
        color: #ffffff;
        font-family: 'Inter', sans-serif !important;
    }

    [data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        background-color: #111111;
        border-right: 1px solid #1f1f1f;
    }

    [data-testid="stSidebar"] .stRadio > div { gap: 2px !important; }

    [data-testid="stSidebar"] .stRadio > div > label {
        background-color: transparent !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 12px 16px !important;
        margin: 1px 0px !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
    }

    [data-testid="stSidebar"] .stRadio > div > label > div:first-child {
        display: none !important;
    }

    [data-testid="stSidebar"] .stRadio > div > label > div:last-child {
        color: #666666 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
    }

    [data-testid="stSidebar"] .stRadio > div > label[data-baseweb="radio"]:has(input:checked) {
        background-color: #FF4500 !important;
        border-radius: 6px !important;
    }

    [data-testid="stSidebar"] .stRadio > div > label[data-baseweb="radio"]:has(input:checked) > div:last-child {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    [data-testid="stSidebar"] .stRadio > div > label:hover > div:last-child {
        color: #ffffff !important;
    }

    .stButton > button[kind="primary"] {
        background: #FF4500 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        width: 100% !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: #cc3700 !important;
    }

    .stButton > button {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 6px !important;
        padding: 10px 16px !important;
        font-weight: 600 !important;
    }

    .stButton > button:hover {
        border-color: #FF4500 !important;
        color: #FF4500 !important;
    }

    [data-testid="metric-container"] {
        background-color: #111111 !important;
        border: 1px solid #1f1f1f !important;
        border-radius: 10px !important;
        padding: 20px !important;
    }

    [data-testid="stMetricLabel"] > div {
        color: #666666 !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        opacity: 1 !important;
    }

    [data-testid="stMetricValue"] > div {
        color: #ffffff !important;
        font-size: 30px !important;
        font-weight: 800 !important;
        opacity: 1 !important;
    }

    [data-testid="stMetricDelta"] { color: #FF4500 !important; }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #111111 !important;
        color: #ffffff !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 6px !important;
        font-size: 14px !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #FF4500 !important;
        box-shadow: 0 0 0 1px #FF4500 !important;
    }

    .stTextArea > div > div > textarea {
        background-color: #111111 !important;
        color: #ffffff !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 6px !important;
    }

    .stTextArea > div > div > textarea:focus {
        border-color: #FF4500 !important;
    }

    .stSelectbox > div > div {
        background-color: #111111 !important;
        color: #ffffff !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 6px !important;
    }

    .stSelectbox > div > div > div { color: #ffffff !important; }

    [data-testid="stInfo"] {
        background-color: #111111 !important;
        border: 1px solid #FF4500 !important;
        border-left: 4px solid #FF4500 !important;
        border-radius: 6px !important;
        color: #cccccc !important;
    }

    [data-testid="stSuccess"] {
        background-color: #0a1a0a !important;
        border: 1px solid #22c55e !important;
        border-left: 4px solid #22c55e !important;
        border-radius: 6px !important;
        color: #cccccc !important;
    }

    [data-testid="stWarning"] {
        background-color: #1a1000 !important;
        border-left: 4px solid #f59e0b !important;
        border-radius: 6px !important;
    }

    [data-testid="stError"] {
        background-color: #1a0000 !important;
        border-left: 4px solid #ef4444 !important;
        border-radius: 6px !important;
    }

    [data-testid="stChatMessage"] {
        background-color: #111111 !important;
        border: 1px solid #1f1f1f !important;
        border-radius: 10px !important;
        margin-bottom: 8px !important;
    }

    [data-testid="stDataFrame"] {
        border-radius: 8px !important;
        overflow: hidden !important;
    }

    hr { border-color: #1f1f1f !important; margin: 28px 0 !important; }

    h1 {
        font-family: 'Barlow Condensed', sans-serif !important;
        color: #ffffff !important;
        font-size: 42px !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
        text-transform: uppercase !important;
    }

    h2 {
        font-family: 'Barlow Condensed', sans-serif !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
    }

    h3 {
        color: #cccccc !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }

    p { color: #999999 !important; }

    .stMultiSelect > div {
        background-color: #111111 !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 6px !important;
    }

    .stMultiSelect span[data-baseweb="tag"] {
        background-color: #FF4500 !important;
        border-radius: 4px !important;
    }

    [data-testid="stExpander"] {
        background-color: #111111 !important;
        border: 1px solid #1f1f1f !important;
        border-radius: 8px !important;
    }

    [data-testid="stExpander"] summary {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #0a0a0a; }
    ::-webkit-scrollbar-thumb { background: #FF4500; border-radius: 2px; }

    label { color: #cccccc !important; }
    .stMarkdown { color: #cccccc !important; }
    .stNumberInput button {
        background: #1a1a1a !important;
        border-color: #2a2a2a !important;
        color: #ffffff !important;
    }
    .stCheckbox label { color: #cccccc !important; }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    .block-container {
        padding-top: 2rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 1400px !important;
    }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE INIT ───────────────────────────────────
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "profile" not in st.session_state:
    st.session_state.profile = {}
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

# ── SIDEBAR ──────────────────────────────────────────────
st.sidebar.markdown("""
<div style='padding: 28px 16px 20px;'>
    <div style='display:flex;align-items:center;gap:10px;margin-bottom:6px'>
        <div style='width:36px;height:36px;background:#FF4500;border-radius:8px;
        display:flex;align-items:center;justify-content:center;
        font-size:18px;font-weight:900;color:white;font-family:Arial Black,sans-serif'>
            F
        </div>
        <div>
            <div style='font-size:20px;font-weight:900;color:#ffffff;letter-spacing:1px;
            font-family:Arial Black,sans-serif;line-height:1'>
                FIT<span style='color:#FF4500'>AI</span>
            </div>
            <div style='font-size:11px;color:#444;font-weight:600;
            letter-spacing:2px;text-transform:uppercase'>
                AI COACH
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(
    "<div style='height:1px;background:#1f1f1f;margin:0 16px 16px'></div>",
    unsafe_allow_html=True
)


# ── NAVIGATION STATE ─────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

# handle programmatic navigation
if st.session_state.get("goto_profile"):
    st.session_state.page = "👤 Profile"
    st.session_state.goto_profile = False

if st.session_state.get("goto_home"):
    st.session_state.page = "🏠 Home"
    st.session_state.goto_home = False

# sidebar navigation — buttons not radio
pages = ["🏠 Home", "👤 Profile", "🤖 AI Coach",
         "📊 Macros", "📈 Progress", "🔔 Reminders"]

for p in pages:
    is_active = st.session_state.page == p
    if is_active:
        st.sidebar.markdown(f"""
        <div style='background:#FF4500;border-radius:6px;
        padding:12px 16px;margin:1px 0;cursor:pointer'>
            <span style='color:#fff;font-size:14px;
            font-weight:700;letter-spacing:0.5px;
            text-transform:uppercase'>{p}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        if st.sidebar.button(p, key=f"nav_{p}"):
            st.session_state.page = p
            st.rerun()

page = st.session_state.page

# profile card in sidebar
if "profile" in st.session_state and st.session_state.profile:
    name_sb = st.session_state.profile.get("name", "")
    goal_sb = st.session_state.profile.get("goal", "")
    initial_sb = name_sb[0].upper() if name_sb else "?"
    st.sidebar.markdown(f"""
    <div style='margin:16px;padding:14px;background:#111111;
    border-radius:8px;border:1px solid #1f1f1f'>
        <div style='display:flex;align-items:center;gap:10px'>
            <div style='width:36px;height:36px;border-radius:50%;
            background:#FF4500;display:flex;align-items:center;
            justify-content:center;font-weight:800;font-size:16px;color:white'>
                {initial_sb}
            </div>
            <div>
                <div style='color:#ffffff;font-size:14px;
                font-weight:700;margin:0'>{name_sb}</div>
                <div style='color:#FF4500;font-size:11px;
                font-weight:600;letter-spacing:0.5px'>{goal_sb}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# logout
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# ── LOGIN SCREEN ─────────────────────────────────────────
if not st.session_state.user_email:

    # ── HERO SECTION ─────────────────────────────────────
    st.markdown("""
    <div style='text-align:center;padding:60px 0 40px'>
        <div style='font-size:56px;margin-bottom:16px'>🔥</div>
        <h1 style='font-size:56px;margin:0 0 16px;letter-spacing:-2px'>
            YOUR AI FITNESS COACH
        </h1>
        <p style='font-size:18px;color:#666;max-width:500px;
        margin:0 auto 40px;line-height:1.6'>
            Personalized workout plans, macro tracking, 
            and AI-powered coaching — all in one place.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── FEATURES ROW ─────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div style='background:#111;border:1px solid #1f1f1f;
        border-radius:12px;padding:24px;text-align:center'>
            <div style='font-size:32px;margin-bottom:12px'>🤖</div>
            <div style='color:#fff;font-weight:700;
            font-size:14px;margin-bottom:6px'>AI COACH</div>
            <div style='color:#666;font-size:13px'>
                Chat with your personal AI fitness coach anytime
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background:#111;border:1px solid #1f1f1f;
        border-radius:12px;padding:24px;text-align:center'>
            <div style='font-size:32px;margin-bottom:12px'>📊</div>
            <div style='color:#fff;font-weight:700;
            font-size:14px;margin-bottom:6px'>MACRO CALCULATOR</div>
            <div style='color:#666;font-size:13px'>
                AI-calculated nutrition targets for your goal
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background:#111;border:1px solid #1f1f1f;
        border-radius:12px;padding:24px;text-align:center'>
            <div style='font-size:32px;margin-bottom:12px'>📈</div>
            <div style='color:#fff;font-weight:700;
            font-size:14px;margin-bottom:6px'>PROGRESS TRACKING</div>
            <div style='color:#666;font-size:13px'>
                Log workouts and visualize your progress over time
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div style='background:#111;border:1px solid #1f1f1f;
        border-radius:12px;padding:24px;text-align:center'>
            <div style='font-size:32px;margin-bottom:12px'>🔔</div>
            <div style='color:#fff;font-weight:700;
            font-size:14px;margin-bottom:6px'>SMART REMINDERS</div>
            <div style='color:#666;font-size:13px'>
                AI-written reminders to keep you consistent
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:40px'></div>", 
        unsafe_allow_html=True)
    st.markdown("---")

    # ── LOGIN SECTION ─────────────────────────────────────
    st.markdown("""
    <div style='text-align:center;padding:20px 0 10px'>
        <p style='color:#666;font-size:15px;margin:0'>
            Enter your email to get started  
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        login_email = st.text_input(
            "Email address",
            placeholder="your@email.com",
            label_visibility="hidden"
        )
        if st.button("GET STARTED →", type="primary"):
            if "@" in login_email:
                with st.spinner("Loading your data..."):
                    profile_data, workouts, notes, \
                        reminder_settings = \
                        load_all_user_data(login_email)

                st.session_state.user_email = login_email

                if profile_data:
                    st.session_state.profile = profile_data

                if workouts:
                    st.session_state.workout_log = workouts

                if notes:
                    st.session_state.notes = notes

                if reminder_settings:
                    st.session_state.reminder_settings = \
                        reminder_settings

                st.rerun()
            else:
                st.error("Please enter a valid email!")

    st.markdown("""
    <div style='text-align:center;margin-top:16px'>
        <p style='color:#444;font-size:13px'>
            New user? Just enter your email and 
            set up your profile to get started.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# ── PAGES ────────────────────────────────────────────────
if page == "🏠 Home":
    home.show()
elif page == "👤 Profile":
    profile.show()
elif page == "🤖 AI Coach":
    coach.show()
elif page == "📊 Macros":
    macros.show()
elif page == "📈 Progress":
    progress.show()
elif page == "🔔 Reminders":
    reminders.show()