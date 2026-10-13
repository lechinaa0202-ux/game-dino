import streamlit as st

st.set_page_config(page_title="Dino Pro", page_icon="🦖", layout="centered")
st.title("🦖 Dino Run - Phiên Bản Đỉnh Cao!")
st.write("Game đã có hình ảnh khủng long, xương rồng, chim bay, chế độ ngày/đêm và âm thanh bíp bíp!")

dino_pro_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { text-align: center; font-family: sans-serif; margin: 0; padding: 10px; transition: background 0.5s; }
        .day { background: #f7f7f7; color: #333; }
        .night { background: #222; color: #fff; }
        canvas { display: block; margin: 10px auto; border: 2px solid #ccc; border-radius: 6px; background: inherit; }
        .score { font-size: 22px; font-weight: bold; margin-bottom: 5px; }
        .btn { background: #ff4b4b; color: white; border: none; width: 100%; max-width: 200px; padding: 15px; font-size: 20px; font-weight: bold; border-radius: 10px; cursor: pointer; }
    </style>
</head>
<body class="day" id="b">
    <div class="score">HI: <span id="h">00000</span> | SCORE: <span id="s">00000</span></div>
    <canvas id="c" width="480" height="160"></canvas>
    <button class="btn" onclick="j()">▲ JUMP ▲</button>
    <script>
        const canvas = document.getElementById("c"), ctx = canvas.getContext("2d"), body = document.getElementById("b");
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function pS(t) {
            const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.connect(g); g.connect(audioCtx.destination);
            o.frequency.setValueAtTime(t === 's' ? 880 : 220, audioCtx.currentTime);
            g.gain.setValueAtTime(0.05, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime + 0.1);
        }
        let dino, obstacles, score, highScore = 0, isGameOver, gameInterval, oTimer, speed = 6, isNight = false;
        function init() {
            dino = { x: 40, y: 110, w: 30, h: 34, vy: 0, g: 1.2, jF: -13, grounded: true, f: 0 }; obstacles = [];
            score = 0; isGameOver = false; speed = 6; isNight = false; body.className = "day";
            document.getElementById("s").innerText = "00000"; clearInterval(gameInterval); clearInterval(oTimer);
            gameInterval = setInterval(update, 1000 / 60); oTimer = setInterval(spawn, 1300);
        }
        function spawn() {
            if (isGameOver) return;
            if (Math.random() > 0.6) { obstacles.push({ t: 1, x: canvas.width, y: Math.random() > 0.5 ? 80 : 105, w: 26, h: 16, f: 0 }); }
            else { obstacles.push({ t: 0, x: canvas.width, y: 144 - 30, w: 18, h: 30 }); }
        }
        function j() {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            if (isGameOver) { init(); return; }
            if (dino.grounded) { dino.vy = dino.jF; dino.grounded = false; }
        }
        window.addEventListener("keydown", e => { if (e.key === " " || e.key === "ArrowUp") j(); });
        canvas.addEventListener("touchstart", (e) => { e.preventDefault(); j(); });
        function dD(x, y, c) {
            ctx.fillStyle = c; ctx.fillRect(x + 14, y, 14, 10); ctx.fillRect(x + 14, y + 4, 16, 4); ctx.clearRect(x + 18, y + 2, 2, 2);
            ctx.fillRect(x + 10, y + 10, 10, 14); ctx.fillRect(x, y + 14, 20, 12); ctx.fillRect(x, y + 26, 16, 4); ctx.fillRect(x, y + 12, 4, 4);
            if (dino.grounded && Math.floor(dino.f / 6) % 2 === 0) { ctx.fillRect(x + 4, y + 30, 4, 4); ctx.fillRect(x + 12, y + 30, 4, 2); }
            else { ctx.fillRect(x + 4, y + 30, 4, 2); ctx.fillRect(x + 12, y + 30, 4, 4); }
        }
        function dC(x, y, w, h) {
            ctx.fillStyle = "#4CAF50"; ctx.fillRect(x + w/3, y, w/3, h); ctx.fillRect(x, y + h/3, w, 5); ctx.fillRect(x, y, 4, h/3); ctx.fillRect(x + w - 4, y + h/6, 4, h/3);
        }
        function dB(x, y, w, h, f) {
            ctx.fillStyle = "#E91E63"; ctx.fillRect(x + 6, y + 4, 16, 6); ctx.fillRect(x, y + 6, 6, 3);
            if (Math.floor(f / 10) % 2 === 0) { ctx.fillRect(x + 10, y, 4, 4); } else { ctx.fillRect(x + 10, y + 10, 4, 6); }
        }
        function update() {
            if (isGameOver) return; dino.f++;
            if (score > 0 && score % 15 === 0 && !isNight) { isNight = true; body.className = "night"; }
            if (score > 0 && score % 30 === 0 && isNight) { isNight = false; body.className = "day"; }
            let tc = isNight ? "#fff" : "#333";
            dino.vy += dino.g; dino.y += dino.vy; if (dino.y >= 110) { dino.y = 110; dino.vy = 0; dino.grounded = true; }
            for (let i = obstacles.length - 1; i >= 0; i--) {
                obstacles[i].x -= speed; if (obstacles[i].t === 1) obstacles[i].f++;
                if (dino.x < obstacles[i].x + obstacles[i].w && dino.x + dino.w > obstacles[i].x && dino.y < obstacles[i].y + obstacles[i].h && dino.y + dino.h > obstacles[i].y) {
                    isGameOver = true; pS('d'); if (score > highScore) highScore = score;
                    document.getElementById("h").innerText = String(highScore).padStart(5, '0');
                    alert("💥 GAME OVER! Điểm của bạn: " + score + "\\nBấm OK rồi bấm JUMP để chơi lại.");
                    clearInterval(gameInterval); clearInterval(oTimer); return;
                }
                if (obstacles[i].x + obstacles[i].w < dino.x && !obstacles[i].passed) {
                    obstacles[i].passed = true; score += 1; pS('s');
                    document.getElementById("s").innerText = String(score).padStart(5, '0'); if (score % 6 === 0) speed += 0.5;
                }
                if (obstacles[i].x + obstacles[i].w < 0) obstacles.splice(i, 1);
            }
            ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.fillStyle = tc; ctx.fillRect(0, 144, canvas.width, 2);
            dD(dino.x, dino.y, tc); obstacles.forEach(o => { if (o.t === 0) dC(o.x, o.y, o.w, o.h); else dB(o.x, o.y, o.w, o.h, o.f); });
        }
        init();
    </script>
</body>
</html>
"""

st.components.v1.html(dino_pro_html, height=300, scrolling=False)

