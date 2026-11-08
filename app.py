"""Run: python -m streamlit run app.py"""
import joblib, streamlit as st
from PIL import Image
from knowledge_base import OPTIONS
from engine import infer, advice
from features import extract

st.set_page_config(page_title="Kisan Advisor", page_icon="🌾", layout="wide")

UI = {
 "en": {"sub": "A reasoning assistant for healthier crops", "field": "Your field", "sym": "What do you see on the plant?",
        "photo": "Upload a leaf photo (optional)", "go": "Diagnose my crop", "treat": "Treatment", "prev": "Prevention",
        "why": "Why this result?", "none": "No matching rule. Add more symptoms or ask a local agriculture officer.",
        "note": "Advisory tool only. For serious cases, confirm with a local agriculture officer.",
        "conf": "confidence", "healthy": "The leaf photo looks healthy. If symptoms persist, add them above."},
 "hi": {"sub": "स्वस्थ फसल के लिए एक सहायक सलाहकार", "field": "आपका खेत", "sym": "पौधे पर क्या दिख रहा है?",
        "photo": "पत्ती की फोटो अपलोड करें (वैकल्पिक)", "go": "मेरी फसल की जाँच करें", "treat": "उपचार", "prev": "रोकथाम",
        "why": "यह परिणाम क्यों?", "none": "कोई नियम नहीं मिला। और लक्षण जोड़ें या कृषि अधिकारी से पूछें।",
        "note": "यह केवल सलाह है। गंभीर स्थिति में स्थानीय कृषि अधिकारी से पुष्टि करें।",
        "conf": "विश्वास", "healthy": "पत्ती स्वस्थ दिखती है। लक्षण बने रहें तो ऊपर जोड़ें।"},
}
lang = {"English": "en", "हिन्दी": "hi"}[st.sidebar.radio("Language / भाषा", ["English", "हिन्दी"])]
T = UI[lang]

CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Lato:wght@400;700&display=swap');
html, body, [class*="css"] {font-family:'Lato',sans-serif;}
h1,h2,h3,.serif {font-family:'Playfair Display',serif !important; color:#1f4d2b;}
.stApp {background:#faf6ea;}
.block-container {padding-top:1rem; max-width:1100px;}
.hero {position:relative; height:260px; border-radius:22px; overflow:hidden; background:linear-gradient(#cfe8f3 0%,#f6efd2 70%); box-shadow:0 8px 30px rgba(40,60,30,.18);}
.hero .t {position:absolute; top:28px; left:0; right:0; text-align:center; z-index:5;}
.hero .t h1 {margin:0; font-size:2.6rem; color:#1f4d2b; letter-spacing:.5px;}
.hero .t p {margin:4px 0 0; color:#5a5a3a; font-size:1.05rem; letter-spacing:2px; text-transform:uppercase;}
.sun {position:absolute; top:18px; right:60px; width:70px; height:70px; border-radius:50%; background:radial-gradient(#ffe9a0,#f4c542); box-shadow:0 0 50px 18px rgba(244,197,66,.5); animation:pulse 5s ease-in-out infinite;}
.cloud {position:absolute; font-size:2.6rem; opacity:.85; animation:drift linear infinite;}
.c1 {top:90px; animation-duration:55s;} .c2 {top:30px; animation-duration:80s; animation-delay:-30s; font-size:2rem;}
.ground {position:absolute; bottom:0; left:0; right:0; height:70px; background:linear-gradient(#7fae5a,#4f7f3a);}
.rows {position:absolute; bottom:0; left:0; right:0; height:70px; background:repeating-linear-gradient(100deg,transparent 0 28px,rgba(30,70,30,.25) 28px 32px);}
.flowers {position:absolute; bottom:44px; left:0; right:0; display:flex; justify-content:space-around; font-size:1.7rem; z-index:3;}
.flowers span {display:inline-block; transform-origin:bottom center; animation:sway 3.2s ease-in-out infinite;}
.tractor {position:absolute; bottom:14px; width:130px; z-index:4; animation:drive 16s linear infinite;}
.tractor .w {transform-box:fill-box; transform-origin:center; animation:spin 1.6s linear infinite;}
.card {background:#fffdf5; border:1px solid #e3d9b5; border-radius:18px; padding:20px 22px; margin:14px 0; box-shadow:0 4px 16px rgba(80,70,30,.08); animation:rise .6s ease both;}
.card h3 {margin:0 0 6px;} 
.badge {display:inline-block; padding:2px 12px; border-radius:20px; font-size:.78rem; letter-spacing:1px; text-transform:uppercase; background:#e8f1de; color:#2f6b3a; border:1px solid #b9d3a3; margin-left:8px; font-family:'Lato',sans-serif;}
.bar {height:10px; background:#eee6c9; border-radius:8px; overflow:hidden; margin:8px 0 14px;}
.bar i {display:block; height:100%; background:linear-gradient(90deg,#4f8a3a,#d9a521); border-radius:8px; animation:grow 1.4s ease-out both;}
.two {display:grid; grid-template-columns:1fr 1fr; gap:14px;}
.box {background:#f6f1de; border-left:4px solid #d9a521; border-radius:10px; padding:10px 14px; font-size:.97rem;}
.box b {color:#1f4d2b; display:block; margin-bottom:2px;}
.note {text-align:center; color:#7a7455; font-size:.85rem; margin-top:26px;}
div.stButton > button {background:linear-gradient(#3b7d46,#2a5f34); color:#fff; border:none; border-radius:30px; padding:.65rem 2.2rem; font-size:1.05rem; box-shadow:0 4px 14px rgba(47,107,58,.4); transition:all .25s;}
div.stButton > button:hover {transform:translateY(-2px) scale(1.03); box-shadow:0 8px 20px rgba(47,107,58,.5); color:#fff;}
@keyframes drive {from{left:-160px;} to{left:105%;}}
@keyframes spin {to{transform:rotate(360deg);}}
@keyframes sway {0%,100%{transform:rotate(-7deg);} 50%{transform:rotate(7deg);}}
@keyframes drift {from{left:-10%;} to{left:110%;}}
@keyframes pulse {0%,100%{transform:scale(1);} 50%{transform:scale(1.08);}}
@keyframes rise {from{opacity:0; transform:translateY(18px);} to{opacity:1; transform:none;}}
@keyframes grow {from{width:0;}}
@media (max-width:700px){.two{grid-template-columns:1fr;} .hero .t h1{font-size:1.8rem;}}
</style>"""

TRACTOR = """<svg class="tractor" viewBox="0 0 130 80" xmlns="http://www.w3.org/2000/svg">
<rect x="78" y="10" width="6" height="22" fill="#444"/><rect x="26" y="30" width="62" height="20" rx="5" fill="#c8402a"/>
<rect x="2" y="36" width="34" height="14" rx="4" fill="#c8402a"/><rect x="58" y="12" width="36" height="30" rx="4" fill="#d9a521" opacity=".95"/>
<rect x="64" y="17" width="24" height="16" rx="2" fill="#dff1f7"/>
<g class="w"><circle cx="80" cy="56" r="20" fill="#2b2b2b"/><circle cx="80" cy="56" r="9" fill="#d9a521"/><path d="M80 38v36M62 56h36" stroke="#8a6b12" stroke-width="3"/></g>
<g class="w"><circle cx="22" cy="63" r="11" fill="#2b2b2b"/><circle cx="22" cy="63" r="5" fill="#d9a521"/><path d="M22 54v18M13 63h18" stroke="#8a6b12" stroke-width="2"/></g></svg>"""

HERO = f"""{CSS}<div class="hero"><div class="sun"></div><div class="cloud c1">☁️</div><div class="cloud c2">☁️</div>
<div class="t"><h1>🌾 Kisan Advisor</h1><p>{T['sub']}</p></div>
<div class="ground"></div><div class="rows"></div>
<div class="flowers"><span>🌻</span><span style="animation-delay:.5s">🌷</span><span style="animation-delay:1s">🌾</span><span style="animation-delay:.3s">🌼</span><span style="animation-delay:.8s">🌻</span><span style="animation-delay:1.3s">🌾</span><span style="animation-delay:.2s">🌷</span><span style="animation-delay:.9s">🌼</span><span style="animation-delay:1.1s">🌻</span></div>
{TRACTOR}</div>"""
st.markdown(HERO.replace("\n", ""), unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return joblib.load("models/leaf_rf.joblib")

st.markdown(f"<h2 style='margin-top:22px'>🌱 {T['field']}</h2>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
facts = {}
for col, k, ico in [(c1, "crop", "🌿"), (c2, "stage", "📈"), (c3, "soil", "🟤"), (c1, "weather", "🌦️"), (c2, "irrigation", "💧")]:
    facts[k] = col.selectbox(f"{ico} {k.title()}", OPTIONS[k])
st.markdown(f"<h3 style='margin-top:18px'>🔍 {T['sym']}</h3>", unsafe_allow_html=True)
facts["symptoms"] = st.multiselect("symptoms", OPTIONS["symptoms"], label_visibility="collapsed",
                                   format_func=lambda s: s.replace("_", " ").capitalize())
img = st.file_uploader(f"📷 {T['photo']}", type=["jpg", "jpeg", "png"])

cnn, healthy = None, False
if img:
    im = Image.open(img)
    a, b = st.columns([1, 3])
    a.image(im, width=170)
    bundle = load_model()
    probs = bundle["model"].predict_proba([extract(im)])[0]
    i = int(probs.argmax()); cls, p = bundle["classes"][i], float(probs[i])
    if p >= 0.6:
        b.success(f"🤖 {cls.replace('___', ' - ').replace('_', ' ')} ({p:.0%})")
        if "healthy" in cls: healthy = True
        else: cnn = (cls, p)
    else:
        b.warning(f"🤖 Image model not confident ({p:.0%}); using symptoms only.")

st.write("")
if st.button(f"🚜 {T['go']}"):
    res = infer(facts, cnn)
    if healthy and not res:
        st.balloons(); st.success(T["healthy"])
    elif not res:
        st.error(T["none"])
    else:
        st.toast("Analysis complete 🌾")
    for n, (prob, info) in enumerate(res):
        name, typ, treat, prev = advice(prob, lang)
        pct = int(info["confidence"] * 100)
        st.markdown(f"""<div class="card" style="animation-delay:{n*.15}s"><h3>{name}<span class="badge">{typ}</span></h3>
<small>{T['conf']}: <b>{pct}%</b></small><div class="bar"><i style="width:{pct}%"></i></div>
<div class="two"><div class="box"><b>💊 {T['treat']}</b>{treat}</div><div class="box"><b>🛡️ {T['prev']}</b>{prev}</div></div></div>""".replace("\n", ""), unsafe_allow_html=True)
        with st.expander(f"🔎 {T['why']} ({info['rule']})"):
            for t in info["trace"]:
                st.write("•", t.replace("_", " "))

st.markdown(f"<div class='note'>🌾 {T['note']}</div>", unsafe_allow_html=True)
