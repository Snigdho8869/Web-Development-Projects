
        $(document).ready(function() {
            $('#decimal-input').hide();
            $('#binary-input').hide();
            $('#octal-input').hide();
            $('#hexadecimal-input').hide();

            $('#choice').change(function() {
                var selectedOption = $(this).val();

                $('#decimal-input').hide();
                $('#binary-input').hide();
                $('#octal-input').hide();
                $('#hexadecimal-input').hide();

                if (selectedOption == '1') {
                    $('#decimal-input').show();
                } else if (selectedOption == '2' || selectedOption == '3') {
                    $('#decimal-input').show();
                } else if (selectedOption == '4' || selectedOption == '5' || selectedOption == '6') {
                    $('#binary-input').show();
                } else if (selectedOption == '7' || selectedOption == '8' || selectedOption == '9') {
                    $('#octal-input').show();
                } else if (selectedOption == '10' || selectedOption == '11' || selectedOption == '12') {
                    $('#hexadecimal-input').show();
                }
            });
        });
    


    document.addEventListener('DOMContentLoaded', function() {
        var textarea = document.getElementById('text');
        var wordCountDisplay = document.getElementById('word-count-display');
        var charCountDisplay = document.getElementById('char-count-display');

        textarea.addEventListener('input', function() {
            var text = this.value;
            var wordCount = countWords(text);
            var charCount = text.length;
            wordCountDisplay.textContent = 'Word Count: ' + wordCount;
            charCountDisplay.textContent = 'Character Count: ' + charCount;
        });

        function countWords(text) {
            var words = text.trim().split(/\s+/); 
            return words.length;
        }
    });






        window.onload = function() {
            const scrollPosition = sessionStorage.getItem('scrollPosition');
            if (scrollPosition) {
                window.scrollTo(0, scrollPosition);
                sessionStorage.removeItem('scrollPosition');
            }
        };
        document.getElementById('password-generator').addEventListener('submit', function() {
            sessionStorage.setItem('scrollPosition', window.pageYOffset);
        });
        document.getElementById('todo-list').addEventListener('submit', function() {
            sessionStorage.setItem('scrollPosition', window.pageYOffset);
        });
        document.getElementById('url-shortner').addEventListener('submit', function() {
            sessionStorage.setItem('scrollPosition', window.pageYOffset);
        });
        document.getElementById('generate-morse-code').addEventListener('submit', function() {
            sessionStorage.setItem('scrollPosition', window.pageYOffset);
        });
        document.getElementById('translate-morse-code').addEventListener('submit', function() {
            sessionStorage.setItem('scrollPosition', window.pageYOffset);
        });
        document.getElementById('qr-code').addEventListener('submit', function() {
            sessionStorage.setItem('scrollPosition', window.pageYOffset);
        });

        document.getElementById('text-to-speech').addEventListener('submit', function() {
            sessionStorage.setItem('scrollPosition', window.pageYOffset);
        });
        document.getElementById('number-conversion').addEventListener('submit', function() {
            sessionStorage.setItem('scrollPosition', window.pageYOffset);
        });