import streamlit as st
import random

# 1. إعدادات الواجهة وشكل اللعبة
st.set_page_config(page_title="Korra Master Challenge", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .main-title { color: #004a87; text-align: center; font-size: 35px; margin-bottom: 20px; }
    .score-box { background: #ffb800; color: #004a87; padding: 15px; border-radius: 15px; text-align: center; font-size: 24px; font-weight: bold; }
    .game-card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; border: 2px solid #004a87; }
    </style>
""", unsafe_allow_html=True)

# 2. قاعدة بيانات اللعبة
if 'materials' not in st.session_state:
    st.session_state.materials = [
        {"name": "كابلات جهد متوسط", "cat": "⚡ كهرباء", "img": "https://p.globalsources.com/IMAGES/PDT/BIG/311/B1187424311.jpg"},
        {"name": "محابس سكين (Gate Valve)", "cat": "🔧 ميكانيكا", "img": "https://5.imimg.com/data5/SELLER/Default/2022/9/XF/OI/XQ/4491703/cast-iron-gate-valve-500x500.jpg"},
        {"name": "خرسانة جاهزة", "cat": "🏗️ مدني", "img": "https://5.imimg.com/data5/ANDROID/Default/2021/3/ST/YI/TH/25842841/product-500x500.jpg"},
        {"name": "لوحة توزيع كهربائية", "cat": "⚡ كهرباء", "img": "https://5.imimg.com/data5/ANDROID/Default/2022/8/WR/XJ/NP/11186793/product-500x500.jpg"},
        {"name": "طلمبة حريق", "cat": "🔧 ميكانيكا", "img": "https://5.imimg.com/data5/SELLER/Default/2020/12/PL/HS/AL/11059483/fire-fighting-pump-500x500.jpg"}
    ]

# 3. إدارة حالة اللعبة (النقاط والسؤال الحالي)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_item' not in st.session_state:
    st.session_state.current_item = random.choice(st.session_state.materials)
if 'message' not in st.session_state:
    st.session_state.message = ""

# 4. وظيفة التحقق من الإجابة
def check_answer(user_choice):
    if user_choice == st.session_state.current_item['cat']:
        st.session_state.score += 10
        st.session_state.message = "✅ برافو! إجابة هندسية صحيحة (+10 نقاط)"
        st.session_state.current_item = random.choice(st.session_state.materials)
    else:
        st.session_state.message = "❌ خطأ! ركز يا بشمهندس، حاول تاني."

# 5. عرض واجهة اللعبة
st.markdown('<div class="main-title">🏆 تحدي خامات Korra Energi</div>', unsafe_allow_html=True)

col_score, col_empty = st.columns([1, 2])
with col_score:
    st.markdown(f'<div class="score-box">النقاط: {st.session_state.score}</div>', unsafe_allow_html=True)

st.write("---")

with st.container():
    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    st.write(f"### صنف هذه الخامة: **{st.session_state.current_item['name']}**")
    st.image(st.session_state.current_item['img'], width=300)
    
    st.write("اختر القسم الصحيح:")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⚡ كهرباء"): check_answer("⚡ كهرباء")
    with c2:
        if st.button("🔧 ميكانيكا"): check_answer("🔧 ميكانيكا")
    with c3:
        if st.button("🏗️ مدني"): check_answer("🏗️ مدني")
    
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.message:
    if "✅" in st.session_state.message:
        st.success(st.session_state.message)
    else:
        st.error(st.session_state.message)

if st.button("إعادة اللعبة 🔄"):
    st.session_state.score = 0
    st.session_state.message = ""
    st.rerun()
