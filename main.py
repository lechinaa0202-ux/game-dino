import streamlit as st

st.set_page_config(page_title="Dino Color Fix", page_icon="🦖", layout="centered")
st.title("🦖 Dino Run - Phiên Bản Sắc Màu!")
st.write("Khủng long xanh, mặt trời vàng, mây trắng và chim làm cảnh trên trời!")

dino_color_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { text-align: center; font-family: sans-serif; background-color: #f0f2f6; margin: 0; padding: 10px; }
        canvas { display: block; margin: 10px auto; border: 3px solid #4A90E2; border-radius: 8px; box-shadow: 0 6px 12px rgba(0,0,0,0.15); background: #87CEEB; }
        .score { font-size: 22px; font-weight: bold; color: #333; margin-bottom: 5px; font-family: monospace; }
        .btn { background: #4A90E2; color: white; border: none; width: 100%; max-width: 220px; padding: 15px; font-size: 20px; font-weight: bold; border-radius: 12px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
        .btn:active { background: #357ABD; }
    </style>
</head>
<body>
    <div class="score">HI: <span id="h">00000</span> | SCORE: <span id="s">00000</span></div>
    <canvas id="c" width="480" height="160"></canvas>
    <button class="btn" onclick="j()">▲ NHẢY ▲</button>

    <script>
        const canvas = document.getElementById("c"), ctx = canvas.getContext("2d");
        let dino, obstacles, clouds, decorativeBirds, score, highScore = 0, isGameOver, gameInterval, oTimer;
        let speed = 4.5;

        function init() {
            dino = { x: 50, y: 110, w: 30, h: 34, vy: 0, g: 1.0, jF: -12, grounded: true, f: 0 };
            obstacles = []; 
            clouds = [{x: 100, y: 30}, {x: 320, y: 20}];
            decorativeBirds = [{x: 200, y: 25, f: 0}, {x: 450, y: 35, f: 5}];
            score = 0; isGameOver = false; speed = 4.5;
            document.getElementById("s").innerText = "00000";
            clearInterval(gameInterval); clearInterval(oTimer);
            gameInterval = setInterval(update, 1000 / 60); 
            oTimer = setInterval(spawnObstacle, 1600);
        }

        function spawnObstacle() {
            if (isGameOver) return;
            let h = Math.floor(Math.random() * 10) + 25;
            obstacles.push({ x: canvas.width, y: 144 - h, w: 18, h: h });
        }

        function j() {
            if (isGameOver) { init(); return; }
            if (dino.grounded) { dino.vy = dino.jF; dino.grounded = false; }
        }

        window.addEventListener("keydown", e => { if (e.key === " " || e.key === "ArrowUp") j(); });
        canvas.addEventListener("touchstart", (e) => { e.preventDefault(); j(); });

        function drawDino(x, y) {
            ctx.fillStyle = "#2ecc71";
            ctx.fillRect(x + 14, y, 14, 10); ctx.fillRect(x + 14, y + 4, 16, 4); 
            ctx.fillStyle = "#333"; ctx.fillRect(x + 18, y + 2, 2, 2);
            ctx.fillStyle = "#2ecc71";
            ctx.fillRect(x + 10, y + 10, 10, 14); ctx.fillRect(x, y + 14, 20, 12); ctx.fillRect(x, y + 26, 16, 4); ctx.fillRect(x, y + 12, 4, 4);
            if (dino.grounded && Math.floor(dino.f / 6) % 2 === 0) { ctx.fillRect(x + 4, y + 30, 4, 4); ctx.fillRect(x + 12, y + 30, 4, 2); }
            else { ctx.fillRect(x + 4, y + 30, 4, 2); ctx.fillRect(x + 12, y + 30, 4, 4); }
        }

        function drawCactus(x, y, w, h) {
            ctx.fillStyle = "#27ae60";
            ctx.fillRect(x + w/3, y, w/3, h); ctx.fillRect(x, y + h/3, w, 5); ctx.fillRect(x, y, 4, h/3); ctx.fillRect(x + w - 4, y + h/6, 4, h/3);
        }

        function drawBird(x, y, f) {
            ctx.fillStyle = "#e84393"; ctx.fillRect(x + 6, y + 4, 14, 6); ctx.fillRect(x, y + 6, 6, 2);
            if (Math.floor(f / 10) % 2 === 0) { ctx.fillRect(x + 10, y, 4, 4); } else { ctx.fillRect(x + 10, y + 10, 4, 5); }
        }

        function update() {
            if (isGameOver) return; dino.f++;
            dino.vy += dino.g; dino.y += dino.vy; if (dino.y >= 110) { dino.y = 110; dino.vy = 0; dino.grounded = true; }

            clouds.forEach(c => { c.x -= 0.4; if (c.x < -40) c.x = canvas.width + 20; });
            decorativeBirds.forEach(b => { b.x -= 0.8; b.f++; if (b.x < -30) b.x = canvas.width + 30; });

            for (let i = obstacles.length - 1; i >= 0; i--) {
                obstacles[i].x -= speed;
                if (dino.x < obstacles[i].x + obstacles[i].w && dino.x + dino.w > obstacles[i].x && dino.y < obstacles[i].y + obstacles[i].h && dino.y + dino.h > obstacles[i].y) {
                    isGameOver = true;
                    if (score > highScore) highScore = score;
                    document.getElementById("h").innerText = String(highScore).padStart(5, '0');
                    alert("💥 GAME OVER! Điểm của bạn: " + score + "\\nBấm OK rồi bấm NHẢY để chơi lại.");
                    clearInterval(gameInterval); clearInterval(oTimer); return;
                }
                if (obstacles[i].x + obstacles[i].w < dino.x && !obstacles[i].passed) {
                    obstacles[i].passed = true; score += 1;
                    document.getElementById("s").innerText = String(score).padStart(5, '0');
                    if (score % 7 === 0) speed += 0.4;
                }
                if (obstacles[i].x + obstacles[i].w < 0) obstacles.splice(i, 1);
            }

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Mặt trời vàng
            ctx.fillStyle = "#f1c40f"; ctx.beginPath(); ctx.arc(420, 35, 16, 0, 2 * Math.PI); ctx.fill();
            
            // Mây trắng
            ctx.fillStyle = "#ffffff";
            clouds.forEach(c => { ctx.fillRect(c.x, c.y, 30, 8); ctx.fillRect(c.x + 6, c.y - 4, 16, 4); });

            // Chim làm cảnh trên cao
            decorativeBirds.forEach(b => { drawBird(b.x, b.y, b.f); });

            // Mặt đất nâu đất
            ctx.fillStyle = "#d35400"; ctx.fillRect(0, 144, canvas.width, 16);
            ctx.fillStyle = "#ba4a00"; ctx.fillRect(0, 144, canvas.width, 2);

            // Khủng long xanh cute và Xương rồng xanh lá
            drawDino(dino.x, dino.y);
            obstacles.forEach(o => { drawCactus(o.x, o.y, o.w, o.h); });
        }
        init();
    </script>
</body>
</html>
"""

st.components.v1.html(dino_color_html, height=310, scrolling=False)
