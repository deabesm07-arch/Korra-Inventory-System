import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Korra Pro Snake", layout="centered")

st.markdown("<h1 style='text-align: center; color: #004a87;'>🐍 تحدي الثعبان السريع - Korra</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>الثعبان لن يتوقف! حرك الماوس لتوجيهه فقط.</p>", unsafe_allow_html=True)

# كود اللعبة المطور بمحرك حركة مستمرة
game_html = """
<div style="text-align: center;">
    <canvas id="proSnake" width="700" height="450" style="border:8px solid #004a87; border-radius:20px; background:#050505; cursor:crosshair;"></canvas>
    <div style="margin-top:15px; font-family:Arial; color:#004a87;">
        <h2 style="display:inline;">النقاط: <span id="score">0</span></h2>
        <button onclick="window.location.reload()" style="margin-right:30px; padding:10px 25px; background:#004a87; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold;">إعادة اللعبة 🔄</button>
    </div>
</div>

<script>
const canvas = document.getElementById("proSnake");
const ctx = canvas.getContext("2d");
const scoreElement = document.getElementById("score");

let score = 0;
let speed = 4; // سرعة الثعبان الثابتة
let snake = [];
let snakeLength = 30; // طول الثعبان الابتدائي
let angle = 0; // زاوية الحركة

// بداية الثعبان في المنتصف
for(let i=0; i<snakeLength; i++) {
    snake.push({x: 350, y: 225});
}

let mouse = {x: 350, y: 225};
let food = {x: Math.random() * 660 + 20, y: Math.random() * 410 + 20};

// الماوس هنا للاتجاه فقط
canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
});

function draw() {
    // 1. مسح الشاشة بتأثير خفيف للخلفية (Motion Blur)
    ctx.fillStyle = "rgba(0, 0, 0, 0.2)"; 
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 2. تحديث زاوية الحركة لتتبع الماوس
    let head = {x: snake[0].x, y: snake[0].y};
    let targetAngle = Math.atan2(mouse.y - head.y, mouse.x - head.x);
    
    // جعل الدوران ناعم (Smooth Rotation)
    let diff = targetAngle - angle;
    while (diff < -Math.PI) diff += Math.PI * 2;
    while (diff > Math.PI) diff -= Math.PI * 2;
    angle += diff * 0.1;

    // 3. الحركة المستمرة (حتى لو الماوس وقف)
    head.x += Math.cos(angle) * speed;
    head.y += Math.sin(angle) * speed;

    // 4. عبور الحدود (لو خرج من ناحية يطلع من التانية)
    if (head.x < 0) head.x = canvas.width;
    if (head.x > canvas.width) head.x = 0;
    if (head.y < 0) head.y = canvas.height;
    if (head.y > canvas.height) head.y = 0;

    snake.unshift(head);

    // 5. التحقق من أكل الكورة
    let dist = Math.hypot(head.x - food.x, head.y - food.y);
    if (dist < 20) {
        score += 10;
        scoreElement.innerText = score;
        speed += 0.1; // زيادة السرعة تدريجياً
        food = {x: Math.random() * 640 + 30, y: Math.random() * 390 + 30};
        // نزيد طول الثعبان
        for(let j=0; j<5; j++) snake.push({...snake[snake.length-1]});
    } else {
        snake.pop();
    }

    // 6. رسم الطعام (الكورة) بتوهج
    ctx.fillStyle = "#ffb800";
    ctx.shadowBlur = 20;
    ctx.shadowColor = "#ffb800";
    ctx.beginPath();
    ctx.arc(food.x, food.y, 10, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;

    // 7. رسم جسم الثعبان "الحقيقي" (تدرج لوني وانسيابية)
    snake.forEach((part, i) => {
        // لون الرأس مختلف عن الجسم
        if (i === 0) {
            ctx.fillStyle = "#ffb800"; // لون الرأس ذهبي
        } else {
            let opacity = 1 - (i / snake.length);
            ctx.fillStyle = `rgba(0, 74, 135, ${opacity})`; // لون الجسم أزرق كورا
        }
        
        ctx.beginPath();
        // تصغير حجم الجسم تدريجياً ليعطي شكل ثعبان بجد
        let radius = 12 * (1 - (i / snake.length) * 0.6);
        ctx.arc(part.x, part.y, radius, 0, Math.PI * 2);
        ctx.fill();
    });

    requestAnimationFrame(draw);
}

draw();
</script>
"""

components.html(game_html, height=600)
