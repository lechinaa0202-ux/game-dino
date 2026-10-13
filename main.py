import streamlit as st

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="Game Khủng Long Dino Run Đỉnh Cao", page_icon="🦖", layout="centered")

st.title("🦖 Dino Run - Phiên Bản Đỉnh Cao!")
st.write("Game đã có hình ảnh khủng long, xương rồng, chim bay, chế độ ngày/đêm và âm thanh nhé!")

# Đoạn mã game Dino nâng cấp toàn diện
dino_pro_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { text-align: center; font-family: 'Courier New', Courier, monospace; margin: 0; padding: 10px; transition: background-color 0.5s; }
        .day { background-color: #f7f7f7; color: #333; }
        .night { background-color: #222222; color: #fff; }
        canvas { display: block; margin: 10px auto; border: 2px solid #ccc; border-radius: 6px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); background-color: inherit; }
        .score-board { font-size: 24px; font-weight: bold; margin-bottom: 5px; }
        .btn-jump { background: #ff4b4b; color: white; border: none; width: 100%; max-width: 200px; padding: 15px; font-size: 20px; font-weight: bold; border-radius: 10px; cursor: pointer; touch-action: manipulation; margin-top: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
        .btn-jump:active { background: #d43f3f; }
    </style>
</head>
<body class="day" id="gameBody">

    <div class="score-board">HI: <span id="highScoreVal">00000</span> | SCORE: <span id="scoreVal">00000</span></div>
    <canvas id="gameCanvas" width="500" height="180"></canvas>
    
    <button class="btn-jump" onclick="dinoJump()">▲ JUMP ▲</button>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const body = document.getElementById("gameBody");

        // Tạo âm thanh bằng Web Audio API (Không sợ bị lỗi load file mạng)
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playSound(type) {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain); gain.connect(audioCtx.destination);
            if (type === 'score') { // Tiếng bíp khi được điểm giống game thật
                osc.frequency.setValueAtTime(880, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
                osc.start(); osc.stop(audioCtx.currentTime + 0.1);
            } else if (type === 'die') { // Tiếng sập khi thua
                osc.frequency.setValueAtTime(220, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
                osc.start(); osc.stop(audioCtx.currentTime + 0.2);
            }
        }

        let dino, obstacles, clouds, score, highScore = 0, isGameOver, gameInterval, obstacleTimer, cloudTimer;
        let gameSpeed = 6;
        let isNight = false;

        function init() {
            dino = { x: 50, y: 130, w: 30, h: 34, vy: 0, gravity: 1.3, jumpForce: -14, isGrounded: true, frame: 0 };
            obstacles = [];
            clouds = [{x: 200, y: 40}, {x: 400, y: 30}];
            score = 0;
            isGameOver = false;
            gameSpeed = 6;
            isNight = false;
            body.className = "day";
            document.getElementById("scoreVal").innerText = "00000";
            
            clearInterval(gameInterval);
            gameInterval = setInterval(update, 1000 / 60);
            
            clearInterval(obstacleTimer);
            obstacleTimer = setInterval(spawnObstacle, 1400);
        }

        function spawnObstacle() {
            if (isGameOver) return;
            // Ngẫu nhiên tạo Xương rồng (0) hoặc Chim bay trên trời (1)
            let type = Math.random() > 0.6 ? 1 : 0;
            if (type === 0) { // Xương rồng
                let h = Math.floor(Math.random() * 15) + 25;
                obstacles.push({ type: 0, x: canvas.width, y: 164 - h, w: 18, h: h });
            } else { // Chim bay
                let yPos = Math.random() > 0.5 ? 90 : 120; // Độ cao của chim bay
                obstacles.push({ type: 1, x: canvas.width, y: yPos, w: 26, h: 16, frame: 0 });
            }
        }

        function dinoJump() {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            if (isGameOver) { init(); return; }
            if (dino.isGrounded) {
                dino.vy = dino.jumpForce;
                dino.isGrounded = false;
            }
        }

        window.addEventListener("keydown", e => { if (e.key === " " || e.key === "ArrowUp") dinoJump(); });
        canvas.addEventListener("touchstart", (e) => { e.preventDefault(); dinoJump(); });

        // Hàm vẽ Khủng Long pixel bằng Code
        function drawDino(x, y, color) {
            ctx.fillStyle = color;
            // Đầu và mỏ
            ctx.fillRect(x + 14, y, 14, 10);
            ctx.fillRect(x + 14, y + 4, 16, 4);
            // Mắt
            ctx.clearRect(x + 18, y + 2, 2, 2);
            // Cổ và Thân
            ctx.fillRect(x + 10, y + 10, 10, 14);
            ctx.fillRect(x, y + 14, 20, 12);
            ctx.fillRect(x, y + 26, 16, 4);
            // Đuôi
            ctx.fillRect(x, y + 12, 4, 4);
            // Chân chạy nhấp nháy
            if (dino.isGrounded && Math.floor(dino.frame / 6) % 2 === 0) {
                ctx.fillRect(x + 4, y + 30, 4, 4);
                ctx.fillRect(x + 12, y + 30, 4, 2);
            } else {
                ctx.fillRect(x + 4, y + 30, 4, 2);
                ctx.fillRect(x + 12, y + 30, 4, 4);
            }
        }

        // Hàm vẽ Xương rồng pixel
        function drawCactus(x, y, w, h, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x + w/3, y, w/3, h); // Thân chính
            ctx.fillRect(x, y + h/3, w, 5); // Nhánh ngang
            ctx.fillRect(x, y, 4, h/3); // Nhánh trái hướng lên
            ctx.fillRect(x + w - 4, y + h/6, 4, h/3); // Nhánh phải hướng lên
        }

        // Hàm vẽ Chim pixel
        function drawBird(x, y, w, h, frame, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x + 6, y + 4, 16, 6); // Thân chim
            ctx.fillRect(x, y + 6, 6, 3); // Mỏ chim
            // Cánh đập lên xuống
            if (Math.floor(frame / 10) % 2 === 0) {
                ctx.fillRect(x + 10, y, 4, 4); // Cánh hướng lên
            } else {
                ctx.fillRect(x + 10, y + 10, 4, 6); // Cánh hướng xuống
            }
        }

        function update() {
            if (isGameOver) return;
            dino.frame++;

            // Xử lý Ngày và Đêm dựa trên điểm số (Mỗi 15 điểm đổi màu một lần)
            if (score > 0 && score % 15 === 0 && !isNight) { isNight = true; body.className = "night"; }
            if (score > 0 && score % 30 === 0 && isNight) { isNight = false; body.className = "day"; }
            let themeColor = isNight ? "#ffffff" : "#535353";

            // Vật lý khủng long
            dino.vy += dino.gravity; dino.y += dino.vy;
            if (dino.y >= 130) { dino.y = 130; dino.vy = 0; dino.isGrounded = true; }

            // Xử lý Mây trôi nền trời
            clouds.forEach(c => {
                c.x -= 0.5; if (c.x < -40) c.x = canvas.width + 20;
                ctx.fillStyle = isNight ? "#555" : "#d3d3d3";
                ctx.fillRect(c.x, c.y, 30, 8); ctx.fillRect(c.x + 8, c.y - 4, 16, 4);
            });

            // Xử lý các chướng ngại vật (Xương rồng & Chim)
            for (let i = obstacles.length - 1; i >= 0; i--) {
                obstacles[i].x -= gameSpeed;
                if (obstacles[i].type === 1) obstacles[i].frame++;

                // Kiểm tra Đâm vào vật cản (Thua cuộc)
                if (dino.x < obstacles[i].x + obstacles[i].w &&
                    dino.x + dino.w > obstacles[i].x &&
                    dino.y < obstacles[i].y + obstacles[i].h &&
                    dino.y + dino.h > obstacles[i].y) {
                    
                    isGameOver = true;
                    playSound('die');
                    if (score > highScore) highScore = score;
                    document.getElementById("highScoreVal").innerText = String(highScore).padStart(5, '0');
                    alert("💥 GAME OVER! Điểm của bạn: " + score + "\\nBấm OK rồi bấm JUMP để phục thù nhé!");
                    clearInterval(gameInterval); clearInterval(obstacleTimer);
                    return;
                }

                // Tính điểm khi vượt qua thành công
                if (obstacles[i].x + obstacles[i].w < dino.x && !obstacles[i].passed) {
                    obstacles[i].passed = true; score += 1;
                    playSound('score');
                    document.getElementById("scoreVal").innerText = String(score).padStart(5, '0');
                    if (score % 6 === 0) gameSpeed += 0.6; // Game khó dần đều
                }

                if (obstacles[i].x + obstacles[i].w < 0) obstacles.splice(i, 1);
            }

            // VẼ TOÀN BỘ GIAO DIỆN GAME PIXEL
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ đường mặt đất pixel gồ ghề
            ctx.strokeStyle = themeColor; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(0, 164); ctx.lineTo(canvas.width, 164); ctx.stroke();
            for (let i = 0; i < canvas.width; i += 40) { // Thêm vài hạt cát trên đất
                ctx.fillRect(i + (dino.frame % 40), 170, 2, 2);
            }

            // Vẽ nhân vật Khủng long thật
            drawDino(dino.x, dino.y, themeColor);

            // Vẽ các chướng ngại vật thật
            obstacles.forEach(obs => {
                if (obs.type === 0) {
                    drawCactus(obs.x, obs.y, obs.w, obs.h, "#4CAF50"); // Xương rồng xanh lá
                } else {
                    drawBird(obs.x, obs.y, obs.w, obs.h, obs.frame, "#E91E63"); // Chim hồng cánh sen
