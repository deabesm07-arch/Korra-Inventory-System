import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Korra Snake Game", layout="centered")

st.markdown("<h1 style='text-align: center; color: #004a87;'>🐍 لعبة الثعبان الكلاسيكية</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>حرك الماوس لتوجيه الثعبان وأكل الكرات المضيئة!</p>", unsafe_allow_html=True)

# كود اللعبة بلغة JavaScript عالية الأداء
game_html = """
<div style="text-align: center;">
    <canvas id="snakeGame" width="600" height="400" style="border:5px solid #004a87; border-radius:15px; background:#000; cursor:crosshair;"></canvas>
    <h2 style="color:#004a87; font-family:Arial; margin-top:10px;">النقاط: <span id="score">0</span></h2>
    <button onclick="window.location.reload()" style="padding:10px 20px; background:#004a87; color:white; border:none; border-radius:5px; cursor:pointer;">إعادة اللعبة 🔄</button>
</div>

<script>
const canvas = document.getElementById("snakeGame");
const ctx = canvas.getContext("2d");
const scoreElement = document.getElementById("score");

let score = 0;
// الثعبان عبارة عن سلسلة من النقاط
let snake = [];
let snakeLength = 20;
for(let i=0; i<snakeLength; i++) {
    snake.push({x: 300, y: 200});
}

let mouse = {x: 300, y: 200};
let food = {x: Math.random() * 580 + 10, y: Math.random() * 380 + 10};

// تتبع حركة الماوس
canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
});

function draw() {
    // مسح الفريم القديم
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // رسم شبكة مربعات خفيفة (Grid)
    ctx.strokeStyle = "#111";
    for(let i=0; i<600; i+=20) { ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,400); ctx.stroke(); }
    for(let i=0; i<400; i+=20) { ctx.beginPath(); ctx.moveTo(0,i); ctx.lineTo(600,i); ctx.stroke(); }

    // تحديث مكان رأس الثعبان ليتبع الماوس
    let head = {x: snake[0].x, y: snake[0].y};
    let angle = Math.atan2(mouse.y - head.y, mouse.x - head.x);
    
    // سرعة الحركة
    head.x += Math.cos(angle) * 5;
    head.y += Math.sin(angle) * 5;

    // إضافة الرأس الجديد
    snake.unshift(head);
    
    // لو أكل الكورة
    let dist = Math.hypot(head.x - food.x, head.y - food.y);
    if (dist < 20) {
        score += 10;
        scoreElement.innerText = score;
        // تكبير الثعبان (عدم حذف الذيل في هذا الفريم)
        food = {x: Math.random() * 560 + 20, y: Math.random() * 360 + 20};
    } else {
        // حذف الذيل للحفاظ على الطول الحالي
        snake.pop();
    }

    // رسم الطعام (الكورة)
    ctx.fillStyle = "#ffb800";
    ctx.shadowBlur = 15;
    ctx.shadowColor = "#ffb800";
    ctx.beginPath();
    ctx.arc(food.x, food.y, 10, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;

    // رسم جسم الثعبان
    snake.forEach((part, i) => {
        ctx.fillStyle = i === 0 ? "#ffb800" : `rgba(0, 74, 135, ${1 - i/snake.length})`;
        ctx.beginPath();
        ctx.arc(part.x, part.y, 12 - (i * 0.2 < 10 ? i * 0.2 : 10), 0, Math.PI * 2);
        ctx.fill();
    });

    requestAnimationFrame(draw);
}

draw();
</script>
"""

# تشغيل اللعبة
components.html(game_html, height=600)
