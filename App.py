import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime

st.set_page_config(page_title="StressCheck", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Sora', sans-serif; }

.stApp { background: #ffffff !important; }
.main .block-container { background: #ffffff !important; padding-top: 1.5rem; max-width: 880px; }
[data-testid="stAppViewContainer"] { background: #ffffff !important; }
[data-testid="stHeader"] { background: #ffffff !important; }
section[data-testid="stSidebar"] > div { background: #0a1f3c !important; }

[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff !important; border-radius: 16px !important;
    border: 1.5px solid #e2eaf5 !important;
    box-shadow: 0 2px 12px rgba(10,31,60,0.06) !important;
    transition: box-shadow 0.3s, transform 0.3s !important;
}
[data-testid="stVerticalBlockBorderWrapper"] > div { background: #ffffff !important; }
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 8px 28px rgba(10,31,60,0.1) !important;
    transform: translateY(-2px) !important;
}

[data-testid="stSidebar"] * { color: #7aa3cc !important; }
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.08) !important;
    margin-top: 0.3rem !important;
    margin-bottom: 0.5rem !important;
}

/* ── Logo ── */
.sidebar-logo-wrap {
    display: flex; 
    flex-direction: column; 
    align-items: center;
    padding: 2rem 0 1.4rem; 
    padding: 0.8rem 0 0.5rem;
    gap: 4px;
}
.sidebar-logo-icon { font-size: 38px; line-height: 1; }
.sidebar-logo-text {
    font-size: 22px !important; font-weight: 800 !important;
    color: #e8f2ff !important; letter-spacing: 0.01em;
}

/* ── Invisible logo button overlay ── */
section[data-testid="stSidebar"] div[data-testid="stButton"] button {
    position: absolute !important;
    top: 20px !important; left: 0 !important;
    width: 100% !important; height: 110px !important;
    opacity: 0 !important; background: transparent !important;
    border: none !important; box-shadow: none !important;
    cursor: pointer !important; z-index: 10 !important;
    padding: 0 !important; min-height: 0 !important;
}

/* ── Hide radio label completely ── */
[data-testid="stSidebar"] [data-testid="stRadio"] > div:first-child,
[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    display: none !important;
}

/* ── Radio option rows ── */
[data-testid="stSidebar"] .stRadio label {
    display: flex !important; align-items: center !important;
    padding: 8px 12px !important; border-radius: 8px !important;
    font-size: 13px !important; color: #7aa3cc !important;
    cursor: pointer !important; transition: background 0.2s !important;
    margin-bottom: 2px !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.07) !important;
}
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: rgba(255,255,255,0.13) !important;
    color: #e8f2ff !important; font-weight: 600 !important;
}
[data-testid="stSidebar"] .stRadio label:has(input:checked) p {
    color: #e8f2ff !important; font-weight: 600 !important;
}
[data-testid="stSidebar"] .stRadio label > div:first-child { display: none !important; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 2px !important; }

/* ── Sub-items indented ── */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:nth-child(4),
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:nth-child(5),
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:nth-child(6) {
    padding-left: 28px !important;
    font-size: 12px !important;
}

/* ── Animations ── */
@keyframes gradientShift { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
@keyframes fadeUp { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeIn { from{opacity:0} to{opacity:1} }
@keyframes barGrow { from{width:0%} to{width:var(--w)} }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
@keyframes popIn { 0%{opacity:0;transform:scale(0.8)} 60%{transform:scale(1.05)} 100%{opacity:1;transform:scale(1)} }

.hero {
    background: linear-gradient(270deg, #0a1f3c, #1356a0, #0b3d82, #1a5fc7);
    background-size: 400% 400%; animation: gradientShift 9s ease infinite;
    border-radius: 20px; padding: 2.5rem 3rem; margin-bottom: 2rem;
    color: white; position: relative; overflow: hidden;
}
.hero::before { content:''; position:absolute; top:-60px; right:-60px; width:240px; height:240px; border-radius:50%; background:rgba(255,255,255,0.04); }
.hero::after  { content:''; position:absolute; bottom:-80px; right:15%; width:200px; height:200px; border-radius:50%; background:rgba(255,255,255,0.03); }
.hero-eyebrow { font-size:11px; font-weight:600; letter-spacing:0.12em; text-transform:uppercase; opacity:0.6; margin:0 0 8px; animation:fadeUp 0.5s ease forwards; }
.hero-title   { font-size:28px; font-weight:800; margin:0 0 8px; animation:fadeUp 0.5s ease 0.1s both; line-height:1.2; }
.hero-sub     { font-size:14px; opacity:0.7; margin:0; animation:fadeUp 0.5s ease 0.2s both; }

.sec-label { font-size:11px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#1356a0; border-bottom:2px solid #eef3fb; padding-bottom:8px; margin-bottom:1.2rem; }

.stButton > button {
    background: linear-gradient(135deg, #1356a0 0%, #0a1f3c 100%) !important;
    color: white !important; border: none !important; border-radius: 12px !important;
    padding: 13px 36px !important; font-size: 14px !important; font-weight: 700 !important;
    font-family: 'Sora', sans-serif !important; letter-spacing: 0.02em !important;
    box-shadow: 0 6px 20px rgba(19,86,160,0.3) !important; transition: all 0.25s !important;
}
.stButton > button:hover { transform: translateY(-3px) !important; box-shadow: 0 10px 28px rgba(19,86,160,0.4) !important; }

.result-wrap { border-radius:20px; padding:2rem; margin:1.5rem 0; animation:popIn 0.5s ease forwards; }
.result-high   { background:linear-gradient(135deg,#fff0f0,#ffd6d6); border:1.5px solid #f0a0a0; }
.result-medium { background:linear-gradient(135deg,#fffbee,#fff0c0); border:1.5px solid #e8c840; }
.result-low    { background:linear-gradient(135deg,#f0fbee,#d8f5c8); border:1.5px solid #90d060; }
.result-title  { font-size:32px; font-weight:800; margin:0 0 6px; }
.conf-track { background:rgba(0,0,0,0.08); border-radius:99px; height:10px; margin:12px 0 4px; overflow:hidden; }
.conf-fill  { height:100%; border-radius:99px; animation:barGrow 1.2s cubic-bezier(0.34,1.56,0.64,1) forwards 0.3s; width:0%; }
.conf-high   { background:linear-gradient(90deg,#e03030,#ff6060); }
.conf-medium { background:linear-gradient(90deg,#c89010,#f5c030); }
.conf-low    { background:linear-gradient(90deg,#308020,#60c040); }

.tip-row { display:flex; gap:14px; align-items:flex-start; padding:12px 0; border-bottom:1px solid rgba(0,0,0,0.05); animation:fadeUp 0.4s ease forwards; opacity:0; }
.tip-row:last-child { border-bottom:none; }
.tip-icon { width:40px; height:40px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:20px; flex-shrink:0; }
.tip-row:nth-child(1){animation-delay:0.1s} .tip-row:nth-child(2){animation-delay:0.2s}
.tip-row:nth-child(3){animation-delay:0.3s} .tip-row:nth-child(4){animation-delay:0.4s}

.badge-high   { background:#FEECEC; color:#8B1A1A; border:1.5px solid #F5A0A0; border-radius:8px; padding:4px 14px; font-size:12px; font-weight:600; display:inline-block; }
.badge-medium { background:#FFF8E0; color:#7A4800; border:1.5px solid #F5D060; border-radius:8px; padding:4px 14px; font-size:12px; font-weight:600; display:inline-block; }
.badge-low    { background:#EDFBE4; color:#1E5C08; border:1.5px solid #90D060; border-radius:8px; padding:4px 14px; font-size:12px; font-weight:600; display:inline-block; }

.h-entry { display:flex; align-items:center; justify-content:space-between; padding:12px 16px; border-radius:12px; margin-bottom:8px; background:#f8fafd; border:1.5px solid #e8eef6; transition:all 0.2s; animation:fadeUp 0.4s ease forwards; opacity:0; }
.h-entry:hover { background:white; box-shadow:0 4px 16px rgba(10,31,60,0.08); transform:translateX(4px); }
.h-entry:nth-child(1){animation-delay:.05s} .h-entry:nth-child(2){animation-delay:.1s}
.h-entry:nth-child(3){animation-delay:.15s} .h-entry:nth-child(4){animation-delay:.2s}
.h-entry:nth-child(5){animation-delay:.25s}

.stat-box { background:white; border:1.5px solid #e8eef6; border-radius:14px; padding:16px; text-align:center; transition:all 0.2s; animation:fadeIn 0.5s ease forwards; }
.stat-box:hover { transform:translateY(-4px); box-shadow:0 8px 24px rgba(10,31,60,0.1); }

.info-hero-low    { background:linear-gradient(135deg,#1a7a30,#2db84a,#1a9e38); }
.info-hero-medium { background:linear-gradient(135deg,#a06800,#e09010,#c87a00); }
.info-hero-high   { background:linear-gradient(135deg,#8a0f0f,#c83030,#a01818); }
.info-hero { border-radius:20px; padding:2.5rem; margin-bottom:1.5rem; color:white; position:relative; overflow:hidden; }
.info-hero-deco1 { position:absolute; top:-50px; right:-50px; width:200px; height:200px; border-radius:50%; background:rgba(255,255,255,0.08); }
.info-hero-deco2 { position:absolute; bottom:-60px; left:30%; width:160px; height:160px; border-radius:50%; background:rgba(255,255,255,0.05); }
.info-big-emoji  { font-size:56px; animation:float 3s ease-in-out infinite; display:inline-block; }

.sign-pill { display:inline-flex; align-items:center; gap:8px; border-radius:99px; padding:7px 16px; font-size:13px; margin:4px; animation:fadeUp 0.4s ease forwards; opacity:0; }
.sign-pill:nth-child(1){animation-delay:.1s} .sign-pill:nth-child(2){animation-delay:.18s}
.sign-pill:nth-child(3){animation-delay:.26s} .sign-pill:nth-child(4){animation-delay:.34s} .sign-pill:nth-child(5){animation-delay:.42s}

.do-card { background:white; border-radius:14px; padding:1.25rem; margin-bottom:10px; border:1.5px solid #e8eef6; display:flex; gap:14px; align-items:flex-start; animation:fadeUp 0.4s ease forwards; opacity:0; box-shadow:0 2px 8px rgba(10,31,60,0.04); transition:all 0.2s; }
.do-card:hover { transform:translateX(6px); box-shadow:0 6px 20px rgba(10,31,60,0.1); }
.do-card:nth-child(1){animation-delay:.1s} .do-card:nth-child(2){animation-delay:.2s}
.do-card:nth-child(3){animation-delay:.3s} .do-card:nth-child(4){animation-delay:.4s} .do-card:nth-child(5){animation-delay:.5s}
.do-num { width:36px; height:36px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:16px; flex-shrink:0; }

.info-stat { text-align:center; padding:1.5rem 1rem; border-radius:14px; color:white; animation:popIn 0.5s ease forwards; }
.info-stat-num { font-size:36px; font-weight:800; margin:0; }
.info-stat-label { font-size:12px; opacity:0.85; margin:4px 0 0; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ──────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
# active_nav = the true current page (decoupled from widget key)
if "active_nav" not in st.session_state:
    st.session_state.active_nav = "📋  Predict"
# nav_sel = radio widget key (never manually overwritten after render)
if "nav_sel" not in st.session_state:
    st.session_state.nav_sel = "📋  Predict"

@st.cache_resource
def load_model():
    if os.path.exists("model.pkl"):
        return joblib.load("model.pkl")
    return None
model = load_model()

# ── Resolve which options the radio should show ─────────────────────
on_info = st.session_state.active_nav in [
    "📖  Information", "🟢  Low Stress", "🟡  Medium Stress", "🔴  High Stress"
]

if on_info:
    nav_options = [
        "📋  Predict",
        "🕘  History",
        "📖  Information",
        "🟢  Low Stress",
        "🟡  Medium Stress",
        "🔴  High Stress",
    ]
else:
    nav_options = [
        "📋  Predict",
        "🕘  History",
        "📖  Information",
    ]

# ── Sidebar ─────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div class="sidebar-logo-wrap">
        <span class="sidebar-logo-icon">🧠</span>
        <span class="sidebar-logo-text">StressCheck</span>
    </div>""", unsafe_allow_html=True)

    # Invisible overlay button for logo click
    if st.button("logo", key="logo_btn"):
        st.session_state.active_nav = "📋  Predict"
        st.session_state.nav_sel    = "📋  Predict"
        st.rerun()

    st.markdown("---")

    # Unified radio — key is nav_sel, never manually set after this line
    raw_sel = st.radio(
        "",
        nav_options,
        key="nav_sel",
        label_visibility="hidden",
    )

    st.markdown("---")

# ── Handle selection AFTER render (safe — reading, not writing widget key) ──
if raw_sel == "📖  Information":
    # Clicking the parent "Information" item → go to Low Stress sub-page
    # We can't set nav_sel here, but we CAN update active_nav and rerun
    # so next render the radio defaults to showing Low Stress highlighted
    if st.session_state.active_nav != "🟢  Low Stress":
        st.session_state.active_nav = "🟢  Low Stress"
        st.rerun()
else:
    st.session_state.active_nav = raw_sel

# ── Resolve page & info_sub from active_nav ─────────────────────────
active = st.session_state.active_nav
if active in ["🟢  Low Stress", "🟡  Medium Stress", "🔴  High Stress"]:
    page     = "📖  Information"
    info_sub = active
else:
    page     = active
    info_sub = "🟢  Low Stress"

# ══════════════════════════════════════════════
# PREDICT
# ══════════════════════════════════════════════
if page == "📋  Predict":
    st.markdown("""
    <div class="hero">
        <div style="position:relative;z-index:1;">
            <p class="hero-title">🧠 Student Stress Level Predictor</p>
            <p class="hero-sub">Answer 7 quick questions for your personalized stress assessment.</p>
        </div>
    </div>""", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="sec-label">👤 Student Identity</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: student_name = st.text_input("Full Name", placeholder="Enter your name")
        with c2: gender = st.selectbox("Gender", ["Male", "Female"], help="For records only — not used in prediction")

    with st.container(border=True):
        st.markdown('<div class="sec-label">📋 Student Information</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            screen_time     = st.slider("🖥️  Screen Time (hrs/day)", min_value=1, max_value=11, value=5)
            social_media    = st.slider("📱  Social Media Use (hrs/day)", min_value=0, max_value=7, value=3)
            sleep_hours     = st.slider("😴  Sleep Hours (hrs/day)", min_value=4, max_value=9, value=7)
            
            exam_enc        = st.slider("📝  Exam Frequency Pressure", min_value=1, max_value=9, value=5)
        with c2:
            load_enc = st.slider("📚  Assignment Load", min_value=1, max_value=9, value=5)
            support_enc  = st.slider("🏠  Family Support Availability", min_value=1, max_value=9, value=5)
            anxiety_enc   = st.slider("💭  Anxiety Level Intensity", min_value=1, max_value=9, value=5)

    if st.button("🧠  Predict My Stress Level"):
        if not student_name.strip():
            st.warning("Please enter the student's name first.")
        else:
            features = [[screen_time, support_enc, load_enc, exam_enc, anxiety_enc, social_media, sleep_hours]]

            if model:
                prediction = model.predict(features)[0]
                proba      = model.predict_proba(features)[0]
                confidence = round(max(proba) * 100)
            

            tips = {
                "Low":[("🌿","#d8f5c8","Keep your habits","Consistency is key — don't let good routines slip during busy periods."),
                       ("😴","#d8f5c8","Consistent sleep","Keep 7–8 hours to maintain your resilience."),
                       ("📅","#d8f5c8","Plan ahead","Use a planner to stay on top of deadlines before they pile up.")],
                "Medium":[("⏰","#fff0c0","Time-block your study","Break tasks into 25-min Pomodoro sessions."),
                          ("📵","#fff0c0","Reduce screen time","Set a daily limit of under 2 hours on social media."),
                          ("🏃","#fff0c0","Light exercise","Even 30 mins of walking measurably reduces anxiety."),
                          ("💬","#fff0c0","Talk to someone","A friend, family, or campus counselor can help reframe stress.")],
                "High":[("😴","#ffd6d6","Prioritize sleep","7–8 hours is non-negotiable. Sleep deprivation amplifies everything."),
                        ("📵","#ffd6d6","Digital detox","Limit social media to 1 hr/day. Set DND at night."),
                        ("🏃","#ffd6d6","Move your body","20–30 mins of exercise releases endorphins that cut anxiety."),
                        ("🏫","#ffd6d6","Seek professional support","Contact your university's counseling services. It's free & confidential.")]
            }
            descs = {
                "Low":   ("🟢 Low Stress",    "#1E5C08", "result-low",    "conf-low",    "Your lifestyle and psychological indicators are within a healthy range. Keep it up!"),
                "Medium":("🟡 Medium Stress", "#7A4800", "result-medium", "conf-medium", "Some pressure is building. It's manageable now, but worth addressing before it escalates."),
                "High":  ("🔴 High Stress",   "#8B1A1A", "result-high",   "conf-high",   "Your stress is significantly elevated. Please consider the recommendations below — you don't have to handle this alone.")
            }
            label, color, card_cls, bar_cls, desc = descs[prediction]

            st.markdown("---")
            st.markdown(f"### Result for **{student_name}**")
            st.markdown(f"""
            <div class="result-wrap {card_cls}">
                <p style="font-size:12px;text-transform:uppercase;letter-spacing:0.1em;color:{color};opacity:0.7;margin:0 0 6px;font-weight:600;">Predicted stress level</p>
                <p class="result-title" style="color:{color};">{label}</p>
                <p style="font-size:13px;color:#333;margin:8px 0 16px;line-height:1.7;">{desc}</p>
                <p style="font-size:12px;font-weight:600;color:{color};margin:0 0 4px;">Model confidence — {confidence}%</p>
                <div class="conf-track"><div class="conf-fill {bar_cls}" style="width:{confidence}%;"></div></div>
            </div>""", unsafe_allow_html=True)

            st.markdown("**💡 Recommendations**")
            for icon, bg, title, body in tips[prediction]:
                st.markdown(f"""
                <div class="tip-row">
                    <div class="tip-icon" style="background:{bg};">{icon}</div>
                    <div>
                        <strong style="font-size:13px;color:#0a1f3c;">{title}</strong><br>
                        <span style="font-size:12px;color:#556;">{body}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

            st.session_state.history.append({
                "name": student_name, "gender": gender,
                "result": prediction, "confidence": confidence,
                "time": datetime.now().strftime("%d %b %Y, %H:%M")
            })
           

# ══════════════════════════════════════════════
# HISTORY
# ══════════════════════════════════════════════
elif page == "🕘  History":
    st.markdown("""
    <div class="hero">
        <div style="position:relative;z-index:1;">
            <p class="hero-eyebrow">Session Data</p>
            <p class="hero-title">🕘 Prediction History</p>
            <p class="hero-sub">All predictions recorded in this session.</p>
        </div>
    </div>""", unsafe_allow_html=True)

    if not st.session_state.history:
        st.info("No predictions yet. Head to the Predict page to get started.")
    else:
        h = st.session_state.history
        c1, c2, c3, c4 = st.columns(4)
        for col, val, lbl, color in [
            (c1, len(h),                                          "Total",     "#0a1f3c"),
            (c2, sum(1 for x in h if x["result"] == "High"),     "🔴 High",   "#8B1A1A"),
            (c3, sum(1 for x in h if x["result"] == "Medium"),   "🟡 Medium", "#7A4800"),
            (c4, sum(1 for x in h if x["result"] == "Low"),      "🟢 Low",    "#1E5C08"),
        ]:
            col.markdown(f'<div class="stat-box"><p style="font-size:32px;font-weight:800;color:{color};margin:0;">{val}</p><p style="font-size:11px;color:#8aa0bc;text-transform:uppercase;letter-spacing:0.06em;margin:4px 0 0;">{lbl}</p></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        csv = pd.DataFrame(h).to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Export CSV", data=csv, file_name="stresscheck_history.csv", mime="text/csv")


        st.markdown("<br>", unsafe_allow_html=True)
        badge = {
            "Low":    '<span class="badge-low">🟢 Low</span>',
            "Medium": '<span class="badge-medium">🟡 Medium</span>',
            "High":   '<span class="badge-high">🔴 High</span>',
        }
        for e in reversed(h):
            ini = "".join([w[0].upper() for w in e["name"].split()[:2]])
            st.markdown(f"""
            <div class="h-entry">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div style="width:38px;height:38px;border-radius:12px;background:linear-gradient(135deg,#1356a0,#0a1f3c);color:white;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;flex-shrink:0;">{ini}</div>
                    <div>
                        <strong style="font-size:13px;color:#0a1f3c;">{e['name']}</strong>
                        <span style="font-size:11px;color:#9ab0cc;margin-left:6px;">· {e.get('gender','')}</span><br>
                        <span style="font-size:11px;color:#9ab0cc;">{e['time']}</span>
                    </div>
                </div>
                <div style="display:flex;align-items:center;gap:10px;">
                    {badge[e['result']]}
                    <span style="font-size:12px;color:#9ab0cc;font-weight:500;">{e['confidence']}%</span>
                </div>
            </div>""", unsafe_allow_html=True)

        
# ══════════════════════════════════════════════
# INFORMATION
# ══════════════════════════════════════════════
elif page == "📖  Information":

    if info_sub == "🟢  Low Stress":
        st.markdown("""
        <div class="info-hero info-hero-low" style="position:relative;overflow:hidden;">
            <div class="info-hero-deco1"></div><div class="info-hero-deco2"></div>
            <div style="position:relative;z-index:1;">
                <span class="info-big-emoji">😌</span>
                <p style="font-size:13px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;opacity:0.75;margin:12px 0 6px;">Stress Level</p>
                <h1 style="font-size:36px;font-weight:800;margin:0 0 10px;color:white;">Low Stress</h1>
                <p style="font-size:14px;opacity:0.8;margin:0;max-width:540px;">You're managing well. Your daily habits support a balanced and healthy mental state.</p>
            </div>
        </div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        for col, num, lbl in [(c1,"< 6 hrs","Screen time daily"),(c2,"7–8 hrs","Sleep per night"),(c3,"Low","Anxiety level")]:
            col.markdown(f'<div class="info-stat" style="background:linear-gradient(135deg,#1a7a30,#2db84a);"><p class="info-stat-num">{num}</p><p class="info-stat-label">{lbl}</p></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🔍 Signs of Low Stress")
        st.markdown("""
        <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:1.5rem;">
            <span class="sign-pill" style="background:rgba(30,92,8,0.12);color:#1E5C08;border:1px solid rgba(30,92,8,0.2);">✅ Sleeping 7–8 hours consistently</span>
            <span class="sign-pill" style="background:rgba(30,92,8,0.12);color:#1E5C08;border:1px solid rgba(30,92,8,0.2);">✅ Feeling in control of workload</span>
            <span class="sign-pill" style="background:rgba(30,92,8,0.12);color:#1E5C08;border:1px solid rgba(30,92,8,0.2);">✅ Low screen & social media use</span>
            <span class="sign-pill" style="background:rgba(30,92,8,0.12);color:#1E5C08;border:1px solid rgba(30,92,8,0.2);">✅ Good family support</span>
            <span class="sign-pill" style="background:rgba(30,92,8,0.12);color:#1E5C08;border:1px solid rgba(30,92,8,0.2);">✅ Able to focus without feeling overwhelmed</span>
        </div>""", unsafe_allow_html=True)

        st.markdown("### 💚 What To Do")
        for icon, title, body in [
            ("🌿","Maintain your habits","Consistency is everything. Don't let good routines slip during busy academic periods."),
            ("📅","Plan proactively","Use a planner or digital calendar to stay ahead of deadlines before they pile up."),
            ("🏃","Stay active","Even light physical activity maintains your mental resilience and mood."),
            ("🤝","Support others","Share your healthy habits — helping others reduces your own stress too."),
        ]:
            st.markdown(f"""
            <div class="do-card">
                <div class="do-num" style="background:#d8f5c8;color:#1a7a30;">{icon}</div>
                <div><strong style="font-size:14px;color:#0a1f3c;">{title}</strong><br>
                <span style="font-size:13px;color:#556;line-height:1.6;">{body}</span></div>
            </div>""", unsafe_allow_html=True)

    elif info_sub == "🟡  Medium Stress":
        st.markdown("""
        <div class="info-hero info-hero-medium" style="position:relative;overflow:hidden;">
            <div class="info-hero-deco1"></div><div class="info-hero-deco2"></div>
            <div style="position:relative;z-index:1;">
                <span class="info-big-emoji">😓</span>
                <p style="font-size:13px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;opacity:0.75;margin:12px 0 6px;">Stress Level</p>
                <h1 style="font-size:36px;font-weight:800;margin:0 0 10px;color:white;">Medium Stress</h1>
                <p style="font-size:14px;opacity:0.8;margin:0;max-width:540px;">Some pressure is building up. Manageable now — but worth addressing before it escalates.</p>
            </div>
        </div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        for col, num, lbl in [(c1,"6–8 hrs","Screen time daily"),(c2,"5–6 hrs","Sleep per night"),(c3,"Medium","Anxiety level")]:
            col.markdown(f'<div class="info-stat" style="background:linear-gradient(135deg,#a06800,#e09010);"><p class="info-stat-num">{num}</p><p class="info-stat-label">{lbl}</p></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🔍 Signs of Medium Stress")
        st.markdown("""
        <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:1.5rem;">
            <span class="sign-pill" style="background:rgba(122,72,0,0.1);color:#7A4800;border:1px solid rgba(122,72,0,0.2);">⚠️ Tired more often than usual</span>
            <span class="sign-pill" style="background:rgba(122,72,0,0.1);color:#7A4800;border:1px solid rgba(122,72,0,0.2);">⚠️ Difficulty concentrating on tasks</span>
            <span class="sign-pill" style="background:rgba(122,72,0,0.1);color:#7A4800;border:1px solid rgba(122,72,0,0.2);">⚠️ More time on screens to "escape"</span>
            <span class="sign-pill" style="background:rgba(122,72,0,0.1);color:#7A4800;border:1px solid rgba(122,72,0,0.2);">⚠️ Anxious before exams or deadlines</span>
            <span class="sign-pill" style="background:rgba(122,72,0,0.1);color:#7A4800;border:1px solid rgba(122,72,0,0.2);">⚠️ Mood fluctuations — irritable some days</span>
        </div>""", unsafe_allow_html=True)

        st.markdown("### 🟡 What To Do")
        for icon, title, body in [
            ("⏰","Time-block your study","Use the Pomodoro technique — 25 mins focused work, 5 mins break. Prevents burnout."),
            ("📵","Limit social media","Set a hard limit of 2 hours/day. Use your phone's built-in screen time controls."),
            ("😴","Fix sleep first","Aim for a consistent bedtime. Poor sleep makes stress, anxiety, and focus dramatically worse."),
            ("💬","Talk to someone","A friend, family member, or campus counselor can help you reframe stress and feel less alone."),
        ]:
            st.markdown(f"""
            <div class="do-card">
                <div class="do-num" style="background:#fff0c0;color:#a06800;">{icon}</div>
                <div><strong style="font-size:14px;color:#0a1f3c;">{title}</strong><br>
                <span style="font-size:13px;color:#556;line-height:1.6;">{body}</span></div>
            </div>""", unsafe_allow_html=True)

    elif info_sub == "🔴  High Stress":
        st.markdown("""
        <div class="info-hero info-hero-high" style="position:relative;overflow:hidden;">
            <div class="info-hero-deco1"></div><div class="info-hero-deco2"></div>
            <div style="position:relative;z-index:1;">
                <span class="info-big-emoji">😰</span>
                <p style="font-size:13px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;opacity:0.75;margin:12px 0 6px;">Stress Level</p>
                <h1 style="font-size:36px;font-weight:800;margin:0 0 10px;color:white;">High Stress</h1>
                <p style="font-size:14px;opacity:0.8;margin:0;max-width:540px;">Your stress levels are significantly elevated. This needs attention — and you don't have to handle it alone.</p>
            </div>
        </div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        for col, num, lbl in [(c1,"> 8 hrs","Screen time daily"),(c2,"< 5 hrs","Sleep per night"),(c3,"High","Anxiety level")]:
            col.markdown(f'<div class="info-stat" style="background:linear-gradient(135deg,#8a0f0f,#c83030);"><p class="info-stat-num">{num}</p><p class="info-stat-label">{lbl}</p></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🔍 Signs of High Stress")
        st.markdown("""
        <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:1.5rem;">
            <span class="sign-pill" style="background:rgba(139,26,26,0.1);color:#8B1A1A;border:1px solid rgba(139,26,26,0.2);">🔴 Sleeping less than 5 hours regularly</span>
            <span class="sign-pill" style="background:rgba(139,26,26,0.1);color:#8B1A1A;border:1px solid rgba(139,26,26,0.2);">🔴 Feeling overwhelmed or hopeless</span>
            <span class="sign-pill" style="background:rgba(139,26,26,0.1);color:#8B1A1A;border:1px solid rgba(139,26,26,0.2);">🔴 High social media as distraction</span>
            <span class="sign-pill" style="background:rgba(139,26,26,0.1);color:#8B1A1A;border:1px solid rgba(139,26,26,0.2);">🔴 Physical symptoms: headaches, fatigue</span>
            <span class="sign-pill" style="background:rgba(139,26,26,0.1);color:#8B1A1A;border:1px solid rgba(139,26,26,0.2);">🔴 Strong peer pressure, feeling unsupported</span>
        </div>""", unsafe_allow_html=True)

        st.markdown("### 🔴 What To Do")
        for icon, title, body in [
            ("😴","Sleep is non-negotiable","Prioritize 7–8 hours, even during exam season. Your brain literally cannot regulate emotion without it."),
            ("📵","Digital detox","Set your phone to Do Not Disturb at night. Delete social media apps temporarily if needed."),
            ("🏃","Daily movement","Just 20–30 mins of exercise releases endorphins that directly lower cortisol (the stress hormone)."),
            ("🏫","Seek professional help","Contact your university's counseling or mental health services. It's free, confidential, and effective."),
            ("📋","Break tasks down","Overwhelming assignments feel smaller when split into tiny 15-min daily steps. Start with just one thing."),
        ]:
            st.markdown(f"""
            <div class="do-card">
                <div class="do-num" style="background:#ffd6d6;color:#8a0f0f;">{icon}</div>
                <div><strong style="font-size:14px;color:#0a1f3c;">{title}</strong><br>
                <span style="font-size:13px;color:#556;line-height:1.6;">{body}</span></div>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#fff0f0;border:1.5px solid #f5a0a0;border-radius:14px;padding:16px 20px;margin-top:12px;display:flex;gap:12px;align-items:flex-start;">
            <span style="font-size:24px;flex-shrink:0;">🆘</span>
            <div>
                <strong style="color:#8B1A1A;font-size:13px;">If you're feeling overwhelmed right now</strong><br>
                <span style="font-size:12px;color:#a03030;line-height:1.7;">Please reach out to your campus counseling center or a trusted person immediately. You don't have to navigate this alone.</span>
            </div>
        </div>""", unsafe_allow_html=True)