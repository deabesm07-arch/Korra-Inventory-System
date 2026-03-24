import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="Korra Technical Challenge", layout="centered")

st.markdown("<h1 style='text-align: center; color: #004a87;'>🏗️ تحدي الخبرة الهندسية - Korra</h1>", unsafe_allow_html=True)

# 1. بنك الأسئلة الفنية العميقة
if 'tech_db' not in st.session_state:
    st.session_state.tech_db = [
        {"q": "كابلات 3*240 مم² النحاسية المعزولة بـ XLPE تستخدم عادة في:", "a": "⚡", "hint": "نقل الجهد المتوسط للمحولات"},
        {"q": "محابس السكين (Gate Valves) ذات القطر الكبير تستخدم أساساً في:", "a": "🔧", "hint": "خطوط طرد طلمبات الحريق"},
        {"q": "مواسير الـ Seamless Carbon Steel الجدول 40 تستخدم في:", "a": "🔧", "hint": "شبكات البخار والضغط العالي"},
        {"q": "خرسانة محتوى 400 كجم/م³ مع إضافات سيكا تستخدم في:", "a": "🏗️", "hint": "صب القواعد المعرضة للمياه الجوفية"},
        {"q": "قواطع الـ ACB (Air Circuit Breakers) تستخدم لحماية:", "a": "⚡", "hint": "لوحات التوزيع الرئيسية LVDP"},
        {"q": "خزانات التمدد (Expansion Tanks) في دوائر الشيلر وظيفتها:", "a": "🔧", "hint": "تعويض فرق الضغط الحراري للمياه"},
        {"q": "حديد التسليح عالي المقاومة (Grade 60) يستخدم في:", "a": "🏗️", "hint": "الأعمدة والكمرات ذات البحور الواسعة"},
        {"q": "وحدات الـ VFD (Variable Frequency Drive) تستخدم لـ:", "a": "⚡", "hint": "التحكم في سرعة مواتير الطلمبات"},
        {"q": "عزل الفوم (Polyurethane) للمواسير يستخدم في:", "a": "🔧", "hint": "منع التكثيف في خطوط مياه التبريد"},
        {"q": "الـ Waterstop البلاستيكي يوضع في الخرسانة عند:", "a": "🏗️", "hint": "فاصل الصب في خزانات المياه"}
    ]

# اختيار سؤال عشوائي
current_q = random.choice(st.session_state.tech_db)

st.markdown(f"""
    <div style="background:#fff3e0; padding:20px; border-radius:15px; border-right:10px solid #ff9800; text-align:right; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h3 style="margin:0; color:#e65100;">⚒️ سؤال المستوى المتقدم:</h3>
        <p style="font-size:22px; font-weight:bold; margin-top:10px;">{current_q['q']}</p>
        <p style="color:#666;">الهدف: وجه الثعبان نحو رمز القطاع المسؤول عن هذا التوصيف.</p>
    </div>
""", unsafe_allow_html=True)

# 2. محرك اللعبة (جافا سكريبت مطور بـ Smooth Animation)
game_html = f"""
<div style="text-align: center;">
    <canvas id="techSnake" width="650" height="400" style="border:6px solid #004a87; border-radius:20px; background:#0a0a0a;"></canvas>
    <div style="display:flex; justify-content:space-around; margin-top:10px;">
        <h2 style="color:#ffb800;">النقاط: <span id="score">0</span></h2>
        <h3 style="color:#4caf50;">الحالة: <span id="status">جاهز</span></h3>
    </div>
</div>

<script>
const canvas = document.getElementById("techSnake");
const ctx = canvas.getContext("2d");
let score = localStorage.getItem('korraScore') || 0;
document.getElementById('score').innerText = score;

let snake = [];
for(let i=0; i<15; i++) snake.push({{x: 325, y: 200}});
let mouse = {{x: 325, y: 200}};

const targets = [
    {{emoji: "⚡", label: "كهرباء", x: 100, y: 100, val: "⚡"}},
    {{emoji: "🔧", label: "ميكانيكا", x: 550, y: 100, val: "🔧"}},
    {{emoji: "🏗️", label: "مدني", x: 325, y: 330, val: "🏗️"}}
];

canvas.addEventListener('mousemove', (e) => {{
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
}});

function update() {{
    let head = {{...snake[0]}};
    let angle = Math.atan2(mouse.y - head.y, mouse.x - head.x);
    head.x += Math.cos(angle) * 6;
    head.y += Math.sin(angle) * 6;

    snake.unshift(head);
    snake.pop();

    targets.forEach(t => {{
        let dist = Math.hypot(head.x - t.x, head.y - t.y);
        if (dist < 35) {{
            if (t.val === "{current_q['a']}") {{
                score = parseInt(score) + 50;
                localStorage.setItem('korraScore', score);
                document.getElementById('status').innerText = "✅ صح!";
                setTimeout(() => window.location.reload(), 500);
            }} else {{
                score = Math.max(0, parseInt(score) - 20);
                localStorage.setItem('korraScore', score);
                document.getElementById('status').innerText = "❌ خطأ!";
                head.x = 325; head.y = 200;
            }}
        }}
    }});
}}

function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // رسم خلفية تقنية
    ctx.strokeStyle = "#1a1a1a";
    for(let i=0; i<canvas.width; i+=50) {{ ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,canvas.height); ctx.stroke(); }}

    // رسم الثعبان (تدرج أزرق كورا)
    snake.forEach((part, i) => {{
        ctx.fillStyle = i === 0 ? "#ffb800" : `rgba(0, 74, 135, ${{1 - i/snake.length}})`;
        ctx.beginPath();
        ctx.arc(part.x, part.y, 14 - (i*0.6), 0, Math.PI * 2);
        ctx.fill();
    }});

    // رسم الأهداف بوضوح عالي
    ctx.font = "40px Arial";
    targets.forEach(t => {{
        ctx.shadowBlur = 20; ctx.shadowColor = "rgba(255,255,255,0.5)";
        ctx.fillText(t.emoji, t.x - 20, t.y + 15);
        ctx.font = "14px Cairo";
        ctx.fillStyle = "white";
        ctx.fillText(t.label, t.x - 25, t.y + 40);
        ctx.font = "40px Arial";
    }});

    update();
    requestAnimationFrame(draw);
}}
draw();
</script>
"""

components.html(game_html, height=550)

if st.button("تصفير التحدي 🔄"):
    st.components.v1.html("<script>localStorage.setItem('korraScore', 0); window.location.reload();</script>")
