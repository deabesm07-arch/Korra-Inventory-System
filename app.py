import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Korra Sniper Challenge", layout="centered")

st.markdown("<h1 style='text-align: center; color: #d32f2f;'>🦅 تحدي القناص: صيد الطيور السريعة</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>تحذير: الطيور سريعة جداً والمهمة صعبة!</p>", unsafe_allow_html=True)

game_html = """
<div style="text-align: center;">
    <canvas id="sniperGame" width="700" height="450" style="border:5px solid #333; border-radius:15px; background: linear-gradient(to bottom, #87CEEB, #E0F7FA); cursor: none;"></canvas>
    <div style="margin-top:10px; font-family:Arial;">
        <h2 style="color:#d32f2f; display:inline;">النقاط: <span id="score">0</span></h2>
        <h3 style="color:#333; margin-left:20px; display:inline;">الطلقات الضائعة: <span id="misses">0</span></h3>
    </div>
    <button onclick="window.location.reload()" style="margin-top:15px; padding:10px 25px; background:#333; color:white; border:none; border-radius:8px; cursor:pointer;">إعادة المحاولة 🔄</button>
</div>

<script>
const canvas = document.getElementById("sniperGame");
const ctx = canvas.getContext("2d");
const scoreEl = document.getElementById("score");
const missEl = document.getElementById("misses");

let score = 0;
let misses = 0;
let mouse = { x: 350, y: 225 };
let birds = [];

// إنشاء طائر جديد بخصائص عشوائية
function createBird() {
    return {
        x: -50,
        y: Math.random() * (canvas.height - 100) + 50,
        speedX: Math.random() * 5 + 4, // سرعة عالية
        speedY: (Math.random() - 0.5) * 4, // حركة متعرجة
        size: Math.random() * 20 + 20,
        color: "#3e2723"
    };
}

// إضافة طيور في البداية
for(let i=0; i<3; i++) birds.push(createBird());

canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
});

canvas.addEventListener('mousedown', () => {
    let hit = false;
    birds.forEach((bird, index) => {
        let dist = Math.hypot(mouse.x - bird.x, mouse.y - bird.y);
        if (dist < bird.size) {
            score += 10;
            birds[index] = createBird(); // استبدال الطائر المقتول
            hit = true;
        }
    });
    if (!hit) {
        misses += 1;
        score = Math.max(0, score - 2); // عقاب على الضرب العشوائي
    }
    scoreEl.innerText = score;
    missEl.innerText = misses;
});

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // رسم السحاب كخلفية
    ctx.fillStyle = "white";
    ctx.beginPath(); ctx.arc(100, 50, 30, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(500, 80, 40, 0, Math.PI*2); ctx.fill();

    // رسم وتحريك الطيور
    birds.forEach((bird, index) => {
        bird.x += bird.speedX;
        bird.y += bird.speedY;

        // لو خرج الطائر من الشاشة يرجع تاني
        if (bird.x > canvas.width + 50) {
            birds[index] = createBird();
        }
        if (bird.y < 0 || bird.y > canvas.height) bird.speedY *= -1;

        // شكل الطائر (بسيط وسريع)
        ctx.fillStyle = bird.color;
        ctx.font = bird.size + "px Arial";
        ctx.fillText("🦅", bird.x - bird.size/2, bird.y + bird.size/2);
    });

    // رسم النيشان (Crosshair)
    ctx.strokeStyle = "red";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(mouse.x, mouse.y, 20, 0, Math.PI * 2);
    ctx.moveTo(mouse.x - 30, mouse.y);
    ctx.lineTo(mouse.x + 30, mouse.y);
    ctx.moveTo(mouse.x, mouse.y - 30);
    ctx.lineTo(mouse.x, mouse.y + 30);
    ctx.stroke();

    requestAnimationFrame(draw);
}

draw();
</script>
"""

components.html(game_html, height=600)
