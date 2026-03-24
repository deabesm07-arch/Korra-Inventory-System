import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="Korra Infinite Snake", layout="centered")

# --- 1. بنك الأسئلة التفصيلي (تقدر تضيف مئات الأصناف هنا) ---
materials_pool = [
    {"n": "كابلات السويدي 3*240 مم", "cat": "⚡", "hint": "كهرباء"},
    {"n": "قاطع تيار ABB 100A", "cat": "⚡", "hint": "كهرباء"},
    {"n": "محبس سكين 4 بوصة Cast Iron", "cat": "🔧", "hint": "ميكانيكا"},
    {"n": "طلمبة طرد مركزي Grundfos", "cat": "🔧", "hint": "ميكانيكا"},
    {"n": "حديد تسليح عز 16 مم", "cat": "🏗️", "hint": "مدني"},
    {"n": "أسمنت بورتلاندي مقاوم للكبريتات", "cat": "🏗️", "hint": "مدني"},
    {"n": "وصلة مرنة (Flexible Joint) للنظام", "cat": "🔧", "hint": "ميكانيكا"},
    {"n": "لوحة تحكم تحسين معامل القدرة", "cat": "⚡", "hint": "كهرباء"},
    {"n": "رمل سيليكا ناعم للمباني", "cat": "🏗️", "hint": "مدني"},
    {"n": "عداد مياه ديجيتال 2 بوصة", "cat": "🔧", "hint": "ميكانيكا"}
]

# اختيار سؤال عشوائي في كل "ريفرش"
current_q = random.choice(materials_pool)

st.markdown(f"""
    <div style="text-align:center;">
        <h1 style='color:#004a87;'>🐍 تحدي الثعبان الهندسي اللانهائي</h1>
        <div style='background:#f0f2f6; padding:15px; border-radius:10px; border:2px solid #004a87;'>
            <h2 style='color:#333;'>السؤال: {current_q['n']}</h2>
            <p style='color:#666;'>وجه الثعبان نحو أيقونة: <b>{current_q['hint']}</b></p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 2. محرك اللعبة (JavaScript + HTML5 Canvas) ---
game_html = f"""
<div style="text-align: center;">
    <canvas id="snakeGame" width="600" height="400" style="border:5px solid #004a87; border-radius:15px; background:#111; cursor:crosshair;"></canvas>
    <h2 id="scoreDisplay" style="color:#ffb800; font-family:Arial; direction:rtl;">النقاط: 0</h2>
</div>

<script>
const canvas = document.getElementById("snakeGame");
const ctx = canvas.getContext("2d");
const scoreDisplay = document.getElementById("scoreDisplay");

let score = parseInt(localStorage.getItem('korra_score')) || 0;
scoreDisplay.innerText = "النقاط: " + score;

let snake = [];
for(let i=10; i>=0; i--) snake.push({{x: 300 + i*5, y: 200}});
let mouse = {{x: 300, y: 200}};

// توزيع الأهداف في الزوايا بشكل احترافي
let targets = [
    {{emoji: "⚡", x: 80, y: 80, val: "⚡"}},
    {{emoji: "🔧", x: 520, y: 80, val: "🔧"}},
    {{emoji: "🏗️", x: 300, y: 340, val: "🏗️"}}
];

canvas.addEventListener('mousemove', (e) => {{
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
}});

function update() {{
    let head = {{x: snake[0].x, y: snake[0].y}};
    let angle = Math.atan2(mouse.y - head.y, mouse.x - head.x);
    
    // سرعة الثعبان تزيد مع زيادة النقاط!
    let speed = 4 + (score / 100);
    head.x += Math.cos(angle) * speed;
    head.y += Math.sin(angle) * speed;

    snake.unshift(head);
    snake.pop();

    targets.forEach(t => {{
        let dist = Math.hypot(head.x - t.x, head.y - t.y);
        if (dist < 30) {{
            if (t.val === "{current_q['cat']}") {{
                score += 10;
                localStorage.setItem('korra_score', score);
                alert("✅ برافو يا بشمهندس! إجابة صحيحة.");
                window.parent.location.reload(); // طلب سؤال جديد
            }} else {{
                score = Math.max(0, score - 5);
                localStorage.setItem('korra_score', score);
                alert("❌ خطأ! ركز في تصنيف الخامات.");
                head.x = 300; head.y = 200;
            }}
        }}
    }});
}}

function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // رسم شبكة هندسية خلفية (Grid)
    ctx.strokeStyle = "#222";
    for(let i=0; i<canvas.width; i+=40) {{ ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,400); ctx.stroke(); }}
    for(let j=0; j<canvas.height; j+=40) {{ ctx.beginPath(); ctx.moveTo(0,j); ctx.lineTo(600,j); ctx.stroke(); }}

    // رسم الثعبان (تدرج ألوان كورا)
    snake.forEach((part, i) => {{
        ctx.fillStyle = i === 0 ? "#ffb800" : "#004a87";
        ctx.beginPath();
        ctx.arc(part.x, part.y, 10 - (i*0.1), 0, Math.PI * 2);
        ctx.fill();
    }});

    // رسم الأهداف (الأقسام)
    ctx.font = "35px Arial";
    targets.forEach(t => {{
        ctx.shadowBlur = 10;
        ctx.shadowColor = "white";
        ctx.fillText(t.emoji, t.x - 17, t.y + 12);
        ctx.shadowBlur = 0;
    }});

    update();
    requestAnimationFrame(draw);
}}
draw();
</script>
"""

components.html(game_html, height=550)

if st.button("تصفير النقاط والبدء من جديد 🔄"):
    st.components.v1.html("<script>localStorage.setItem('korra_score', 0); window.parent.location.reload();</script>")
