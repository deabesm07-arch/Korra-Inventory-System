import streamlit as st
import time
import random

# 1. إعدادات الصفحة
st.set_page_config(page_title="Korra Snake", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');
    * { font-family: 'Cairo', sans-serif; text-align: center; }
    .game-area { background-color: #0e1117; border: 5px solid #004a87; border-radius: 20px; padding: 20px; }
    .snake-head { font-size: 40px; }
    .food { font-size: 30px; border: 2px solid #ffb800; padding: 10px; border-radius: 10px; cursor: pointer; }
    .score-text { color: #ffb800; font-size: 24px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. بيانات الأسئلة (الثعبان بياكلها)
materials = [
    {"q": "أين نضع 'كابلات السويدي'؟", "a": "⚡ كهرباء", "options": ["⚡ كهرباء", "🔧 ميكانيكا", "🏗️ مدني"]},
    {"q": "أين نضع 'طلمبة التبريد'؟", "a": "🔧 ميكانيكا", "options": ["🏗️ مدني", "🔧 ميكانيكا", "⚡ كهرباء"]},
    {"q": "أين نضع 'حديد التسليح'؟", "a": "🏗️ مدني", "options": ["🏗️ مدني", "⚡ كهرباء", "🔧 ميكانيكا"]}
]

# 3. إدارة حالة اللعبة
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = random.choice(materials)

# 4. واجهة اللعبة
st.markdown('<h1 style="color:#004a87;">🐍 ثعبان المهندس الذكي</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="score-text">مجموع النقاط: {st.session_state.score}</p>', unsafe_allow_html=True)

st.markdown('<div class="game-area">', unsafe_allow_html=True)
st.write(f"### ❓ السؤال: {st.session_state.current_q['q']}")
st.markdown('<div class="snake-head">🐍</div>', unsafe_allow_html=True)
st.write("👇")

# محاكاة حركة الثعبان نحو الإجابات
cols = st.columns(3)
for i, option in enumerate(st.session_state.current_q['options']):
    with cols[i]:
        if st.button(option, key=f"opt_{i}"):
            if option == st.session_state.current_q['a']:
                st.balloons()
                st.session_state.score += 20
                st.success("يممممي! الثعبان أكل الإجابة الصح 😋")
                time.sleep(1)
                st.session_state.current_q = random.choice(materials)
                st.rerun()
            else:
                st.error("أخ! الثعبان أكل إجابة غلط وتعب 🤢")
                st.session_state.score -= 5

st.markdown('</div>', unsafe_allow_html=True)

if st.button("ابدأ من جديد 🔄"):
    st.session_state.score = 0
    st.rerun()
