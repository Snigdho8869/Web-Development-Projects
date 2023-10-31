
    var board = [" ", " ", " ", " ", " ", " ", " ", " ", " "];
    var currentPlayer = "X";
    var gameOver = false;

    function makeMove(index) {
    if (!gameOver) {
        var cell = document.getElementsByClassName("cell")[index];
        if (board[index] === " ") {
            board[index] = currentPlayer;
            cell.innerText = currentPlayer;
            cell.style.color = currentPlayer === "X" ? "red" : "blue";

            if (isWinner(currentPlayer)) {
                document.getElementById("status").innerText = "Congratulations! Player " + currentPlayer + " wins!";
                gameOver = true;
            } else if (isBoardFull()) {
                document.getElementById("status").innerText = "It's a tie!";
                gameOver = true;
            } else {
                currentPlayer = currentPlayer === "X" ? "O" : "X";
                document.getElementById("status").innerText = "Player " + currentPlayer + "'s turn";
            }
        } else {
            document.getElementById("status").innerText = "That position is already occupied. Please try again.";
        }
    } else {
        document.getElementById("status").innerText = "The game is over. Please start a new game.";
    }
}


    function isWinner(player) {
        return (
            (board[0] === player && board[1] === player && board[2] === player) ||
            (board[3] === player && board[4] === player && board[5] === player) ||
            (board[6] === player && board[7] === player && board[8] === player) ||
            (board[0] === player && board[3] === player && board[6] === player) ||
            (board[1] === player && board[4] === player && board[7] === player) ||
            (board[2] === player && board[5] === player && board[8] === player) ||
            (board[0] === player && board[4] === player && board[8] === player) ||
            (board[2] === player && board[4] === player && board[6] === player)
        );
    }

    function isBoardFull() {
        return board.indexOf(" ") === -1;
    }


        document.addEventListener('keydown', function(e) {
            if (e.keyCode === 32 && e.target.nodeName === "BODY") {
                e.preventDefault();
            }
        });




        window.onload = function() {
            const scrollPosition = sessionStorage.getItem('scrollPosition');
            if (scrollPosition) {
                window.scrollTo(0, scrollPosition);
                sessionStorage.removeItem('scrollPosition');
            }
        };

        document.getElementById('guessForm').addEventListener('submit', function() {
            sessionStorage.setItem('scrollPosition', window.pageYOffset);
        });

        document.getElementById('rpsForm').addEventListener('submit', function() {
            sessionStorage.setItem('scrollPosition', window.pageYOffset);
        });
        function startNewGame() {
  sessionStorage.setItem('scrollPosition', window.pageYOffset);
  location.reload();
}


        document.getElementById('palindromeForm').addEventListener('submit', function() {
            sessionStorage.setItem('scrollPosition', window.pageYOffset);
        });

        document.getElementById('fibonacciForm').addEventListener('submit', function() {
            sessionStorage.setItem('scrollPosition', window.pageYOffset);
        });
   
