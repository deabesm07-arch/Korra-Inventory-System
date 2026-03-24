import streamlit as st
import streamlit.components.v1 as components
import random

# 1. إعدادات الصفحة
st.set_page_config(page_title="Korra Infinite Snake", layout="centered")

st.markdown("<h1 style='text-align: center; color: #004a87;'>🐍 صائد الخامات اللانهائي</h1>", unsafe_allow_html=True)

# 2. بنك الأسئلة التفصيلي الضخم
if 'database' not in st.session_state:
    st.session_state.database = [
        # كهرباء
        {"item": "كابلات السويدي 3*240", "cat": "⚡", "hint": "كهرباء"},
        {"item": "قواطع هوائية (ACB)", "cat": "⚡", "hint": "كهرباء"},
        {"item": "محولات زيتية 2000 KVA", "cat": "⚡", "hint": "كهرباء"},
        {"item": "لوحات تحسين معامل القدرة", "cat": "⚡", "hint": "كهرباء"},
        {"item": "كشافات إنارة شوارع LED", "cat": "⚡", "hint": "كهرباء"},
        # ميكانيكا
        {"item": "طلمبات طرد مركزي (Chilled)", "cat": "🔧", "hint": "ميكانيكا"},
        {"item": "محابس فراشة (Butterfly Valve)", "cat": "🔧", "hint": "ميكانيكا"},
        {"item": "مواسير حديد أسود (Seamless)", "cat": "🔧", "hint": "ميكانيكا"},
        {"item": "وحدات مناولة الهواء (AHU)", "cat": "🔧", "hint": "ميكانيكا"},
        {"item": "رؤوس رشاشات حريق (Sprinklers)", "cat": "🔧", "hint": "ميكانيكا"},
        # مدني
        {"item": "خرسانة جهد 350 نيوتن", "cat": "🏗️", "hint": "مدني"},
        {"item": "حديد تسليح قطر 16 مم", "cat": "🏗️", "hint": "مدني"},
        {"item": "طوب أسمنتي مصمت", "cat": "🏗️", "hint": "مدني"},
        {"item": "مواد عزل مائي (سيكا)", "cat": "🏗️", "hint": "مدني"},
        {"item": "شدات خشبية منزلقة", "cat": "🏗️", "hint": "مدني"}
    ]

# اختيار سؤال عشوائي في كل "ريفرش"
current_q = random.choice(st.session_state.database)

st.markdown(f"""
    <div style="background:#e1f5fe; padding:15px; border-radius:10px; border-right:5px solid #0288d1; text-align:right;">
        <h3 style="margin:0;">🎯 المهمة الحالية:</h3>
        <p style="font-size:20px;">صنف الخامة التفصيلية: <b>{current_q['item']}</b></p>
        <p style="color:#555;">(وجه رأس الثعبان نحو أيقونة: {current_q['hint']})</p>
    </div>
""", unsafe_allow_html=True)

# 3. محرك اللعبة (JavaScript)
game_html = f"""
<div style="text-align: center;">
    <canvas id="snakeGame" width="650" height="400" style="border:5px solid #004a87; border-radius:20px; background:#000; cursor:none;"></canvas>
    <h2 id="scoreDisplay" style="color:#ffb800; font-family:Arial;">النقاط: 0</h2>
</div>

<script>
const canvas = document.getElementById("snakeGame");
const ctx = canvas.getContext("2d");
const scoreDisplay = document.getElementById("scoreDisplay");

let score = localStorage.getItem('snakeScore') || 0;
scoreDisplay.innerText = "النقاط: " + score;

let snake = [];
for(let i=0; i<10; i++) snake.push({{x: 325, y: 200}});
let mouse = {{x: 325, y: 200}};

let targets = [
    {{emoji: "⚡", x: 100, y: 100, val: "⚡"}},
    {{emoji: "🔧", x: 550, y: 100, val: "🔧"}},
    {{emoji: "🏗️", x: 325, y: 350, val: "🏗️"}}
];

canvas.addEventListener('mousemove', (e) => {{
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
}});

function update() {{
    let head = {{x: snake[0].x, y: snake[0].y}};
    let angle = Math.atan2(mouse.y - head.y, mouse.x - head.x);
    
    head.x += Math.cos(angle) * 5;
    head.y += Math.sin(angle) * 5;

    snake.unshift(head);
    snake.pop();

    targets.forEach(t => {{
        let dist = Math.hypot(head.x - t.x, head.y - t.y);
        if (dist < 30) {{
            if (t.val === "{current_q['cat']}") {{
                score = parseInt(score) + 20;
                localStorage.setItem('snakeScore', score);
                alert("✅ هندسة صح! أكلت: {current_q['item']}");
                window.location.reload(); 
            }} else {{
                score = Math.max(0, parseInt(score) - 10);
                localStorage.setItem('snakeScore', score);
                alert("❌ غلط! دي مش {current_q['hint']}");
                head.x = 325; head.y = 200;
            }}
        }}
    }});
}}

function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // رسم شبكة خفيفة (Grid) لشكل احترافي
    ctx.strokeStyle = "#222";
    for(let i=0; i<canvas.width; i+=40) {{ ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,canvas.height); ctx.stroke(); }}
    for(let i=0; i<canvas.height; i+=40) {{ ctx.beginPath(); ctx.moveTo(0,i); ctx.lineTo(canvas.width,i); ctx.stroke(); }}

    // رسم الثعبان بشكل انسيابي
    snake.forEach((part, i) => {{
        ctx.fillStyle = i === 0 ? "#ffb800" : "rgba(0, 74, 135, " + (1 - i/snake.length) + ")";
        ctx.beginPath();
        ctx.arc(part.x, part.y, 12 - (i*0.5), 0, Math.PI * 2);
        ctx.fill();
    }});

    // رسم الأهداف
    ctx.font = "35px Arial";
    targets.forEach(t => {{
        ctx.shadowBlur = 15; ctx.shadowColor = "white";
        ctx.fillText(t.emoji, t.x - 17, t.y + 12);
        ctx.shadowBlur = 0;
    }});

    requestAnimationFrame(() => {{
        update();
        draw();
    }});
}}

draw();
</script>
"""

components.html(game_html, height=550)

if st.button("تصفير النقاط والبدء من جديد ♻️"):
    st.components.v1.html("<script>localStorage.setItem('snakeScore', 0); window.location.reload();</script>")
