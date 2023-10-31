function validateForm() {
    var password = document.forms[0].password.value;
    var confirmPassword = document.forms[0].confirm.value;
    var favoriteNumber = document.forms[0].favorite_number.value;
    var userName = document.forms[0].username.value;
    var eMail = document.forms[0].email.value;
    var phoneNumber = document.forms[0].phone_number.value;
    var bloodGroup = document.getElementById("blood_group").value;
    var gender = document.getElementById("gender").value;
    var emailInput = document.forms[0].email;
    var emailValue = emailInput.value.trim();
    var emailPattern = /^[^@]+@(gmail|outlook|hotmail|yahoo|mail|rediffmail)\.(com)$/;


if (!emailValue.match(emailPattern)) {
    var flash = document.createElement("div");
    flash.className = "flash-error";
    flash.innerText = "Please enter a valid email!";
    flash.style.marginTop = "15px";
    emailInput.parentNode.appendChild(flash);
    setTimeout(function () {
        flash.style.display = "none";
    }, 5000);
    return false;
}

    if (favoriteNumber.length !== 9 || isNaN(parseInt(favoriteNumber))) {
        var flash = document.createElement("div");
        flash.className = "flash-error";
        flash.innerText = "Please enter your favorite 9-digit number!";
        flash.style.marginTop = "15px";
        document.body.appendChild(flash);
        setTimeout(function () {
            flash.style.display = "none";
        }, 5000);
        return false;
    }
    
    if (userName === "") {
        var flash = document.createElement("div");
        flash.className = "flash-error";
        flash.innerText = "Please enter your username!";
        flash.style.marginTop = "15px";
        document.body.appendChild(flash);
        setTimeout(function () {
            flash.style.display = "none";
        }, 5000);
        return false;
    }

    if (eMail === "") {
        var flash = document.createElement("div");
        flash.className = "flash-error";
        flash.innerText = "Please enter your email!";
        flash.style.marginTop = "15px";
        document.body.appendChild(flash);
        setTimeout(function () {
            flash.style.display = "none";
        }, 5000);
        return false;
    }

    if (phoneNumber === "") {
        var flash = document.createElement("div");
        flash.className = "flash-error";
        flash.innerText = "Please enter your phone number!";
        flash.style.marginTop = "15px";
        document.body.appendChild(flash);
        setTimeout(function () {
            flash.style.display = "none";
        }, 5000);
        return false;
    }

    if (bloodGroup === "") {
        var flash = document.createElement("div");
        flash.className = "flash-error";
        flash.innerText = "Please select a blood group!";
        flash.style.marginTop = "15px";
        document.body.appendChild(flash);
        setTimeout(function () {
            flash.style.display = "none";
        }, 5000);
        return false;
    }
    
    if (gender === "") {
        var flash = document.createElement("div");
        flash.className = "flash-error";
        flash.innerText = "Please select a gender!";
        flash.style.marginTop = "15px";
        document.body.appendChild(flash);
        setTimeout(function () {
            flash.style.display = "none";
        }, 5000);
        return false;
    }

    if (password != confirmPassword) {
        var flash = document.createElement("div");
        flash.className = "flash-error";
        flash.innerText = "Passwords must match!";
        flash.style.marginTop = "15px";
        document.body.appendChild(flash);
        setTimeout(function () {
            flash.style.display = "none";
        }, 5000);
        return false;
    } else {
        document.getElementById("password-mismatch").style.display = "none";
    }

    return true;
}



    $(document).ready(function() {
        $('#username-input').on('input', function() {
            var username = $(this).val();
            $.get('/check_username/' + username, function(data) {
                if (data.exists) {
                    $('#username-message').html('Username is not available.').css('color', 'red');
                    $('input[type="submit"]').attr('disabled', true).css('background-color', '#C0C0C0');
                } else {
                    $('#username-message').html('Username is available.').css('color', 'green');
                    $('input[type="submit"]').attr('disabled', false).css('background-color', '#336699');
                }
            });
        });
        
        $('input[type="submit"]:not(:disabled)').hover(
            function() { $(this).css('background-color', '#2e5c8a'); },
            function() { $(this).css('background-color', '#336699'); }
        );
    });
