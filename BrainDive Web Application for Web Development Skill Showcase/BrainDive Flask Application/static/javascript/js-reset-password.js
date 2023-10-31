function validateForm() {
    var password = document.forms[0].new_password.value;
    var confirmPassword = document.forms[0].confirm_password.value;
    var favoriteNumber = document.forms[0].favorite_number.value;

    if (password != confirmPassword) {
        var flash = document.createElement("div");
        flash.className = "flashes";
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

    if (favoriteNumber.length !== 9 || isNaN(parseInt(favoriteNumber))) {
        var flash = document.createElement("div");
        flash.className = "flashes";
        flash.innerText = "Please enter your favorite 9-digit number!";
        flash.style.marginTop = "15px";
        document.body.appendChild(flash);
        setTimeout(function () {
            flash.style.display = "none";
        }, 5000);
        return false;
    }

    return true;
}