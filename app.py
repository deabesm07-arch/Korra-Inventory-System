import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Korra Interactive Snake", layout="centered")

st.markdown("<h1 style='text-align: center; color: #004a87;'>🐍 صيد خامات كورا بالثعبان</h1>", unsafe_allow_html=True)
st.write("---")

# قاعدة بيانات الأسئلة
questions = [
    {"q": "أين نضع 'كابلات السويدي'؟", "a": "⚡", "hint": "كهرباء"},
    {"q": "أين نضع 'طلمبة الحريق'؟", "a": "🔧", "hint": "ميكانيكا"},
    {"q": "أين نضع 'الخرسانة الجاهزة'؟", "a": "🏗️", "hint": "مدني"}
]

import random
current_q = random.choice(questions)

st.subheader(f"❓ {current_q['q']}")
st.info(f"حرك الثعبان بالماوس ليوجه رأسه نحو أيقونة: {current_q['hint']}")

# كود اللعبة بلغة JavaScript و HTML5 Canvas
game_html = f"""
<div style="text-align: center;">
    <canvas id="snakeGame" width="600" height="400" style="border:5px solid #004a87; border-radius:15px; background:#111; cursor:none;"></canvas>
    <h2 id="scoreDisplay" style="color:#ffb800; font-family:Arial;">النقاط: 0</h2>
</div>

<script>
const canvas = document.getElementById("snakeGame");
const ctx = canvas.getContext("2d");
const scoreDisplay = document.getElementById("scoreDisplay");

let score = 0;
let snake = [{{x: 300, y: 200}}, {{x: 290, y: 200}}, {{x: 280, y: 200}}];
let mouse = {{x: 300, y: 200}};
let targets = [
    {{emoji: "⚡", x: 100, y: 100, val: "⚡"}},
    {{emoji: "🔧", x: 500, y: 100, val: "🔧"}},
    {{emoji: "🏗️", x: 300, y: 350, val: "🏗️"}}
];

canvas.addEventListener('mousemove', (e) => {{
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
}});

function update() {{
    // حركة الرأس تتبع الماوس
    let head = {{x: snake[0].x, y: snake[0].y}};
    let angle = Math.atan2(mouse.y - head.y, mouse.x - head.x);
    head.x += Math.cos(angle) * 4;
    head.y += Math.sin(angle) * 4;

    snake.unshift(head);
    snake.pop();

    // التحقق من الاصطدام بالأهداف
    targets.forEach(t => {{
        let dist = Math.hypot(head.x - t.x, head.y - t.y);
        if (dist < 25) {{
            if (t.val === "{current_q['a']}") {{
                score += 10;
                t.x = Math.random() * 550;
                t.y = Math.random() * 350;
                alert("✅ صح! استعد للسؤال التالي");
                location.reload(); // تحديث للسؤال الجديد
            }} else {{
                score = Math.max(0, score - 5);
                alert("❌ غلط! ابعد عن القسم ده");
                head.x = 300; head.y = 200; // إعادة ضبط
            }}
        }}
    }});
}}

function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // رسم الثعبان
    snake.forEach((part, i) => {{
        ctx.fillStyle = i === 0 ? "#ffb800" : "#004a87";
        ctx.beginPath();
        ctx.arc(part.x, part.y, 10, 0, Math.PI * 2);
        ctx.fill();
    }});

    // رسم الأهداف
    ctx.font = "30px Arial";
    targets.forEach(t => {{
        ctx.fillText(t.emoji, t.x - 15, t.y + 10);
    }});

    scoreDisplay.innerText = "النقاط: " + score;
    update();
    requestAnimationFrame(draw);
}}

draw();
</script>
"""

# تشغيل المكون
components.html(game_html, height=550)
