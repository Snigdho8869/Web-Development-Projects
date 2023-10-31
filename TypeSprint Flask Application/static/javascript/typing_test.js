var startTime = null;
var timerDuration = parseInt(document.getElementById("timer").textContent);
var timerElement = document.getElementById("timer");
var userInput = document.getElementById("userInput");
var wpmElement = document.getElementById("wpm");
var accuracyElement = document.getElementById("accuracy");
var elapsedElement = document.getElementById("elapsed");
var paragraphElement = document.getElementById("paragraph");
var resultsElement = document.getElementById("results"); 
var realtimeUpdateElement = document.getElementById("realtime_update"); 
var elapsedTime = 0;



    function resetTimer() {
        clearInterval(timerInterval);
        startTime = null;
        elapsedTime = 0;
        elapsedElement.innerText = '0';
        timerElement.innerText = timerDuration;
        userInput.disabled = false;
        $('input[type="submit"]').removeAttr('disabled');
        resultsElement.style.display = 'none'; 
    }

    function updateTimer() {
        if (startTime !== null) {
            var timeRemaining = timerDuration - Math.floor((Date.now() - startTime) / 1000);
            timerElement.innerText = timeRemaining;

            if (timeRemaining <= 0) {
                userInput.disabled = true;
                $('input[type="submit"]').attr('disabled', 'disabled');
                resetTimer();
            }
        }
    }

    function updateResults() {
        if (startTime !== null) {
            $.ajax({
                type: 'POST',
                url: '/result',
                data: $('#typingForm').serialize(),
                success: function(data) {
                    wpmElement.innerText = data.words_per_minute.toFixed(2);
                    accuracyElement.innerText = data.accuracy.toFixed(2);
                    elapsedTime = data.time_elapsed;
                    elapsedElement.innerText = elapsedTime.toFixed(2);

                    resultsElement.innerHTML = `
                        <h4>Words per Minute: ${data.words_per_minute.toFixed(2)}</h4>
                        <h4>Accuracy: ${data.accuracy.toFixed(2)}%</h4>
                        <h4>Time Elapsed: ${elapsedTime.toFixed(2)} seconds</h4>
			<h4>Number of Words: ${data.word_count} words</h4>
                    `;
                },
                dataType: 'json'
            });
        }
    }

    userInput.addEventListener('input', function() {
        if (startTime === null) {
            startTime = Date.now();
            timerInterval = setInterval(function() {
                updateTimer();
                updateResults();
            }, 1000);
            resultsElement.style.display = 'none';
        }
    });

    $('#typingForm').on('submit', function(e) {
        e.preventDefault();
        resetTimer();
        updateTimer();
        updateResults();
        resultsElement.style.display = 'block'; 
        realtimeUpdateElement.style.display = 'none'; 
    });

    $('#changeParagraphButton').click(function() {
        $.ajax({
            type: 'POST',
            url: '/change_paragraph',
            success: function(data) {
                paragraphElement.innerText = data;
                resetTimer();
                updateTimer();
                updateResults();
                resultsElement.style.display = 'none';
                realtimeUpdateElement.style.display = 'block';
                location.reload();
            },
            dataType: 'text'
        });
    });

    $(document).ready(function() {
        resetTimer();
        updateTimer();
        updateResults();
    });