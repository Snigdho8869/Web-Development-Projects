        $(document).ready(function() {
            var canvas = $("#gameCanvas")[0];
            var ctx = canvas.getContext("2d");
            var ballRadius = 12;
            var paddleHeight = 20;
            var paddleWidth = 90;
            var paddleX = (canvas.width - paddleWidth) / 2;
            var brickRowCount = 5;
            var brickColumnCount = 9;
            var brickWidth = 75;
            var brickHeight = 25;
            var brickPadding = 10;
            var brickOffsetTop = 45;
            var brickOffsetLeft = (canvas.width - ((brickWidth + brickPadding) * brickColumnCount - brickPadding)) / 2;
            var bricks = [];
            for (var c = 0; c < brickColumnCount; c++) {
                for (var r = 0; r < brickRowCount; r++) {
                    var brickX = (c * (brickWidth + brickPadding)) + brickOffsetLeft;
                    var brickY = (r * (brickHeight + brickPadding)) + brickOffsetTop;
                    bricks.push({ x: brickX, y: brickY });
                }
            }
            var score = 0;
            var multiplier = 1;
            var gameOver = false;
            var replay = false;
            var rightPressed = false;
            var leftPressed = false;
            var x = canvas.width / 2;
            var y = canvas.height - 50;
            var dx = 3;
            var dy = -3;
            var gameStarted = false;

            function drawBall() {
                ctx.beginPath();
                ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
                ctx.fillStyle = "#0000FF";
                ctx.fill();
                ctx.closePath();
            }

            function drawPaddle() {
                ctx.beginPath();
                ctx.rect(paddleX, canvas.height - paddleHeight, paddleWidth, paddleHeight);
                ctx.fillStyle = "#FF0000";
                ctx.fill();
                ctx.closePath();
            }

            function drawBricks() {
                for (var i = 0; i < bricks.length; i++) {
                    ctx.beginPath();
                    ctx.rect(bricks[i].x, bricks[i].y, brickWidth, brickHeight);
                    ctx.fillStyle = "#FF0000";
                    ctx.fill();
                    ctx.closePath();
                }
            }

            function drawScore() {
                ctx.font = "20px Arial";
                ctx.fillStyle = "#000000";
                ctx.fillText("Score: " + score, 40, 20);
            }

            function collisionDetection() {
                for (var i = 0; i < bricks.length; i++) {
                    var b = bricks[i];
                    if (x > b.x && x < b.x + brickWidth && y > b.y && y < b.y + brickHeight) {
                        dy = -dy;
                        bricks.splice(i, 1);
                        score += multiplier;
                        multiplier++;
                        if (bricks.length === 0) {
                            gameOver = true;
                        }
                    }
                }
            }

            function keyDownHandler(e) {
                if (e.keyCode === 39) {
                    rightPressed = true;
                } else if (e.keyCode === 37) {
                    leftPressed = true;
                }
            }

            function keyUpHandler(e) {
                if (e.keyCode === 39) {
                    rightPressed = false;
                } else if (e.keyCode === 37) {
                    leftPressed = false;
                }
            }

            function resetGame() {
                bricks = [];
                for (var c = 0; c < brickColumnCount; c++) {
                    for (var r = 0; r < brickRowCount; r++) {
                        var brickX = (c * (brickWidth + brickPadding)) + brickOffsetLeft;
                        var brickY = (r * (brickHeight + brickPadding)) + brickOffsetTop;
                        bricks.push({ x: brickX, y: brickY });
                    }
                }
                score = 0;
                multiplier = 1;
                gameOver = false;
                replay = false;
                x = canvas.width / 2;
                y = canvas.height - 50;
                dx = 3;
                dy = -3;
            }

            function startGame() {
                gameStarted = true;
                $("#startText").remove();
                draw();
            }

            function drawStartText() {
                ctx.font = "24px Arial";
                ctx.fillStyle = "#0000FF";
                ctx.textAlign = "center";
                ctx.fillText("Press SPACE or Click to Start", canvas.width / 2, canvas.height / 2);
            }

            function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                drawBricks();
                drawBall();
                drawPaddle();
                drawScore();
                collisionDetection();

                if (gameOver) {
                    ctx.font = "36px Arial";
                    ctx.fillStyle = "#0000FF";
                    ctx.fillText("Game Over!", canvas.width / 2, canvas.height / 2);
                    ctx.font = "20px Arial";
                    ctx.fillText("Press SPACE or CLICK to replay", canvas.width / 2, canvas.height / 2 + 30);
                    if (replay) {
                        resetGame();
                    }
                } else {
                    if (x + dx < ballRadius || x + dx > canvas.width - ballRadius) {
                        dx = -dx;
                    }
                    if (y + dy < ballRadius) {
                        dy = -dy;
                    } else if (y + dy > canvas.height - ballRadius) {
                        if (x > paddleX && x < paddleX + paddleWidth) {
                            dy = -dy;
                            multiplier = 1;
                        } else {
                            gameOver = true;
                        }
                    }

                    if (rightPressed && paddleX < canvas.width - paddleWidth) {
                        paddleX += 7;
                    } else if (leftPressed && paddleX > 0) {
                        paddleX -= 7;
                    }

                    x += dx;
                    y += dy;
                }

                requestAnimationFrame(draw);
            }

            $("#leftButton").on("mousedown touchstart", function() {
                leftPressed = true;
            }).on("mouseup touchend", function() {
                leftPressed = false;
            });

            $("#rightButton").on("mousedown touchstart", function() {
                rightPressed = true;
            }).on("mouseup touchend", function() {
                rightPressed = false;
            });

            $(document).on("keydown click", function(e) {
                if (!gameStarted && (e.keyCode === 32 || e.target === canvas)) {
                    startGame();
                } else if (gameOver && (e.keyCode === 32 || e.target === canvas)) {
                    replay = true;
                }
            });

            $(window).on("load", function() {
                drawStartText();
            });

            document.addEventListener("keydown", keyDownHandler, false);
            document.addEventListener("keyup", keyUpHandler, false);
        });