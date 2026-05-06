import streamlit as st
import joblib
import re
import os
import gdown

st.set_page_config(page_title="PhishGuard", page_icon="🛡️", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "ensemble_voting_classifier.joblib")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.joblib")

MODEL_URL = "https://drive.google.com/uc?id=1iV1Izr6tJKi_MssvVLgQSRf4jWXK2Xmq"
VECTORIZER_URL = "https://drive.google.com/uc?id=1UggozsGUfIBoVUQjyGMhkWCcpOul58I_"

try:
    if not os.path.exists(MODEL_PATH):
        gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

    if not os.path.exists(VECTORIZER_PATH):
        gdown.download(VECTORIZER_URL, VECTORIZER_PATH, quiet=False)

except Exception as e:
    st.error(f"Download failed: {e}")
    st.stop()

if "email" not in st.session_state:
    st.session_state.email = ""
if "show_about" not in st.session_state:
    st.session_state.show_about = True

if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
    st.error("Model files not found. Check MODEL_PATH and VECTORIZER_PATH.")
    st.stop()

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH), joblib.load(VECTORIZER_PATH)

model, vectorizer = load_model()

SPAM_SIGNALS = [
    "congratulations", "you have won", "free iphone", "claim your reward",
    "limited time offer", "exclusive bonus", "prize", "winner", "selected",
    "act now", "guaranteed", "100% free", "earn money", "make money fast",
    "work from home", "lose weight", "buy now", "order now", "special offer",
]

PHISHING_SIGNALS = [
    "verify your account", "account suspended", "confirm.*identity",
    "update.*payment", "unusual.*activity", "security alert",
    "your.*password", "verify.*immediately", "access.*revoked",
    "secure.*link", r"http://\S+", r"bit\.ly", r"tinyurl",
]

def preprocess(text):
    t = text.lower()
    t = re.sub(r"http\S+", " urltoken ", t)
    t = re.sub(r"<.*?>", " ", t)
    t = re.sub(r"[^a-zA-Z\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def predict(text):
    tl = text.lower()
    spam_score  = sum(1 for s in SPAM_SIGNALS if s in tl)
    phish_score = sum(1 for p in PHISHING_SIGNALS if re.search(p, tl))

    vec = vectorizer.transform([preprocess(text)])
    ml_pred = int(model.predict(vec)[0])
    proba = model.predict_proba(vec)[0] if hasattr(model, "predict_proba") else None

    if phish_score >= 2:
        return 2
    if spam_score >= 3:
        return 1
    if proba is not None:
        if proba[2] > 0.25:
            return 2
        if proba[1] > 0.30:
            return 1
        if ml_pred == 0 and (spam_score >= 1 or phish_score >= 1):
            return 1 if spam_score >= phish_score else 2
    return ml_pred

LABELS = {
    0: ("HAM",      "#22c55e", "Legitimate Mail"),
    1: ("SPAM",     "#f59e0b", "Unsolicited Mail"),
    2: ("PHISHING", "#ef4444", "Threat Detected"),
}

PHISHING_EX = "URGENT: Your account has been suspended.\n\nClick the secure link below immediately to verify:\nhttp://secure-login-verification.net\n\nFailure to verify within 24 hours will result in permanent suspension."
SPAM_EX = "Congratulations!!! You have won a FREE iPhone 15 Pro Max.\n\nClaim your reward instantly and receive exclusive bonuses.\nLimited time offer!!!"
HAM_EX = "Hi Sarah,\n\nJust following up on our Tuesday meeting. I've attached the revised project timeline and Q2 budget breakdown.\n\nCould you review the milestones section?\n\nBest,\nMarcus"

ABOUT_MD = (
    "PhishGuard is an email security tool that detects and classifies emails "
    "as Ham, Spam, or Phishing in real time. It uses an ensemble machine learning model "
    "combined with rule-based email scanning to improve detection accuracy for suspicious "
    "and malicious emails. Built using Python, scikit-learn, and Streamlit."
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

*, html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; box-sizing: border-box; }
.stApp { background: #0c0c0c; color: #c8c8c8; }
header, [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
.block-container { padding: 18px 44px 10px 44px !important; max-width: 100% !important; }

textarea {
    background: #111 !important; color: #c8c8c8 !important;
    border: 1px solid #1e1e1e !important; border-radius: 3px !important;
    padding: 12px !important; font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important; line-height: 1.65 !important; resize: none !important;
}
textarea:focus { border-color: #2e2e2e !important; box-shadow: none !important; }
textarea::placeholder { color: #333 !important; }

.stButton > button {
    background: #141414 !important; color: #777 !important;
    border: 1px solid #1e1e1e !important; border-radius: 3px !important;
    height: 32px !important; font-size: 12px !important; font-weight: 500 !important;
    letter-spacing: 0.01em !important; transition: all 0.1s ease !important;
}
.stButton > button:hover { background: #1c1c1c !important; color: #bbb !important; border-color: #2a2a2a !important; }

[data-testid="baseButton-primary"] {
    background: #d4d4d4 !important; color: #0c0c0c !important;
    border: none !important; font-weight: 600 !important; height: 32px !important; font-size: 12.5px !important;
}
[data-testid="baseButton-primary"]:hover { background: #bbb !important; }

div.element-container:has(.clear-marker) {
    display: none;
}
div.element-container:has(.clear-marker) + div.element-container button {
    color: #ef4444 !important;
    border: 1px solid #ef4444 !important;
}
div.element-container:has(.clear-marker) + div.element-container button:hover {
    background: #ef4444 !important;
    color: #0c0c0c !important;
}

.divider { border: none; border-top: 1px solid #181818; margin: 14px 0; }
.mono { font-family: 'IBM Plex Mono', monospace; }
.tag { font-size: 10px; letter-spacing: 0.1em; color: #3a3a3a; font-family: 'IBM Plex Mono', monospace; margin-bottom: 6px; }
.brand { font-size: 14px; font-weight: 700; color: #ddd; letter-spacing: -0.01em; }
.badge { background: #0f2318; color: #22c55e; border: 1px solid #1a3a25; padding: 2px 9px; border-radius: 3px; font-size: 10px; font-weight: 600; letter-spacing: 0.08em; font-family: 'IBM Plex Mono', monospace; }

.about-box { background: #0f0f0f; border: 1px solid #1a1a1a; border-radius: 3px; padding: 16px 20px; margin-bottom: 12px; font-size: 12.5px; color: #555; line-height: 1.7; }

.result-box {
    border: 1px solid #181818; border-radius: 3px; background: #0f0f0f;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    text-align: center;
}
.result-label { font-size: 30px; font-weight: 700; letter-spacing: -0.03em; line-height: 1; }
.result-sub { font-size: 10px; color: #444; letter-spacing: 0.1em; font-family: 'IBM Plex Mono', monospace; margin-top: 6px; }

.footer { display: flex; gap: 20px; align-items: center; flex-wrap: wrap; padding-top: 10px; border-top: 1px solid #161616; }
.fi { display: flex; align-items: center; gap: 6px; font-size: 11px; color: #333; }
.dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; display: inline-block; }
</style>
""", unsafe_allow_html=True)

n1, n2 = st.columns([8, 1])
with n1:
    st.markdown('<div style="display:flex;align-items:center;gap:12px;padding:4px 0 14px 0;border-bottom:1px solid #181818;margin-bottom:14px;"><span class="brand">🛡️ PhishGuard</span><span class="badge">ONLINE</span></div>', unsafe_allow_html=True)
with n2:
    if st.button("About", use_container_width=True):
        st.session_state.show_about = not st.session_state.show_about

if st.session_state.show_about:
    st.markdown(f'<div class="about-box">{ABOUT_MD}</div>', unsafe_allow_html=True)

ex1, ex2, ex3, _ = st.columns([1.1, 1, 1, 6])
with ex1:
    if st.button("Phishing example", use_container_width=True):
        st.session_state.email = PHISHING_EX
with ex2:
    if st.button("Spam example", use_container_width=True):
        st.session_state.email = SPAM_EX
with ex3:
    if st.button("Ham example", use_container_width=True):
        st.session_state.email = HAM_EX

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

left, right = st.columns([2, 1])

with left:
    st.markdown('<div class="tag">EMAIL CONTENT</div>', unsafe_allow_html=True)
    email_text = st.text_area("_", value=st.session_state.email, height=260, placeholder="Paste email content here...", label_visibility="collapsed")
    a_col, c_col = st.columns([5, 1])
    with a_col:
        analyze = st.button("Analyze Email", type="primary", use_container_width=True)
    with c_col:
        st.markdown('<span class="clear-marker"></span>', unsafe_allow_html=True)
        if st.button("Clear", use_container_width=True):
            st.session_state.email = ""
            st.rerun()

with right:
    st.markdown('<div class="tag">RESULT</div>', unsafe_allow_html=True)
    h = 298
    if analyze and email_text.strip():
        pred = predict(email_text)
        label, color, desc = LABELS[pred]
        st.markdown(f'<div class="result-box" style="height:{h}px;"><div class="result-label" style="color:{color};">{label}</div><div class="result-sub">{desc.upper()}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="result-box" style="height:{h}px;"><div style="font-size:24px;opacity:0.08;">✉</div><div style="font-size:11.5px;color:#2e2e2e;margin-top:10px;font-family:IBM Plex Mono,monospace;">awaiting input</div></div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <div class="fi"><span class="dot" style="background:#22c55e"></span>HAM — Legitimate</div>
    <div class="fi"><span class="dot" style="background:#f59e0b"></span>SPAM — Unsolicited</div>
    <div class="fi"><span class="dot" style="background:#ef4444"></span>PHISHING — Threat</div>
    <div style="margin-left:auto;font-size:10.5px;color:#252525;font-family:'IBM Plex Mono',monospace;">ML + heuristic · client-side</div>
</div>
""", unsafe_allow_html=True)