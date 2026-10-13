import streamlit as st

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="Game Khủng Long Dino", page_icon="🦖", layout="centered")

st.title("🦖 Trò chơi Khủng Long Dino Run!")
st.write("Chạm vào màn hình game hoặc bấm nút NHẢY để né xương rồng nhé!")

# Đoạn mã game Dino chạy mượt mà
dino_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { text-align: center; font-family: Arial, sans-serif; background-color: #f0f2f6; margin: 0; padding: 10px; }
        canvas { background: #f7f7f7; display: block; margin: 10px auto; border: 2px solid #ccc; border-radius: 6px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .score { font-size: 22px; font-weight: bold; color: #333; margin-bottom: 5px; }
        .btn-jump { background: #ff4b4b; color: white; border: none; width: 100%; max-width: 200px; padding: 15px; font-size: 20px; font-weight: bold; border-radius: 10px; cursor: pointer; touch-action: manipulation; margin-top: 10px; }
        .btn-jump:active { background: #d43f3f; }
    </style>
</head>
<body>

    <div class="score">Điểm: <span id="scoreVal">0</span></div>
    <canvas id="gameCanvas" width="400" height="150"></canvas>
    
    <button class="btn-jump" onclick="dinoJump()">▲ NHẢY ▲</button>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let dino, obstacles, score, isGameOver, gameInterval, obstacleTimer;
        let gameSpeed = 5;

        function init() {
            dino = { x: 30, y: 120, width: 20, height: 30, vy: 0, gravity: 1.2, jumpForce: -13, isGrounded: true };
            obstacles = [];
            score = 0;
            isGameOver = false;
            gameSpeed = 5;
            document.getElementById("scoreVal").innerText = score;
            
            clearInterval(gameInterval);
            gameInterval = setInterval(update, 1000 / 60); // 60 FPS
            
            // Tự động tạo xương rồng ngẫu nhiên
            clearInterval(obstacleTimer);
            obstacleTimer = setInterval(spawnObstacle, 1500);
        }

        function spawnObstacle() {
            if (isGameOver) return;
            let height = Math.floor(Math.random() * 20) + 20; // Chiều cao xương rồng ngẫu nhiên
            obstacles.push({ x: canvas.width, y: 150 - height, width: 15, height: height });
        }

        function dinoJump() {
            if (isGameOver) {
                init(); // Nếu đang chết thì bấm nút để chơi lại
                return;
            }
            if (dino.isGrounded) {
                dino.vy = dino.jumpForce;
                dino.isGrounded = false;
            }
        }

        // Hỗ trợ phím Cách (Space) nếu chơi trên máy tính
        window.addEventListener("keydown", e => { if (e.key === " " || e.key === "ArrowUp") dinoJump(); });
        canvas.addEventListener("touchstart", () => { dinoJump(); });

        function update() {
            if (isGameOver) return;

            // Xử lý Trọng lực của Khủng long
            dino.vy += dino.gravity;
            dino.y += dino.vy;

            if (dino.y >= 120) { // Chạm đất
                dino.y = 120;
                dino.vy = 0;
                dino.isGrounded = true;
            }

            // Xử lý Xương rồng
            for (let i = obstacles.length - 1; i >= 0; i--) {
                obstacles[i].x -= gameSpeed;

                // Kiểm tra va chạm (Thua cuộc)
                if (dino.x < obstacles[i].x + obstacles[i].width &&
                    dino.x + dino.width > obstacles[i].x &&
                    dino.y < obstacles[i].y + obstacles[i].height &&
                    dino.y + dino.height > obstacles[i].y) {
                    
                    isGameOver = true;
                    alert("Game Over! Điểm của bạn: " + score + ". Bấm OK rồi bấm nút Nhảy để chơi lại.");
                    clearInterval(gameInterval);
                    clearInterval(obstacleTimer);
                    return;
                }

                // Tính điểm khi vượt qua
                if (obstacles[i].x + obstacles[i].width < dino.x && !obstacles[i].passed) {
                    obstacles[i].passed = true;
                    score += 1;
                    document.getElementById("scoreVal").innerText = score;
                    if (score % 5 === 0) gameSpeed += 0.5; // Tăng dần tốc độ
                }

                // Xóa xương rồng chạy khỏi màn hình
                if (obstacles[i].x + obstacles[i].width < 0) {
                    obstacles.splice(i, 1);
                }
            }

            // VẼ GIAO DIỆN
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ mặt đất
            ctx.strokeStyle = "#666";
            ctx.beginPath(); ctx.moveTo(0, 148); ctx.lineTo(canvas.width, 148); ctx.stroke();

            // Vẽ Khủng long (Màu đen/xám tối giản)
            ctx.fillStyle = "#535353";
            ctx.fillRect(dino.x, dino.y, dino.width, dino.height);

            // Vẽ các cây Xương rồng (Màu xanh lá)
            ctx.fillStyle = "#4CAF50";
            obstacles.forEach(obs => {
                ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
            });
        }

        init();
    </script>
</body>
</html>
"""

st.components.v1.html(dino_html, height=280, scrolling=False)
st.info("💡 Mẹo trên điện thoại: Bạn có thể chạm ngón tay thẳng vào vùng màn hình màu xám của game để nhảy cực nhanh!")