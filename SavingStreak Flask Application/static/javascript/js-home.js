var menuToggle = document.getElementById("menu-toggle");
var menu = document.getElementById("menu");
menuToggle.addEventListener("click", function () {
    if (menu.style.height === "0px") {
        menu.style.height = "160px";
        menuToggle.classList.add("active");
    } else {
        menu.style.height = "0px";
        menuToggle.classList.remove("active");
    }
});





document.getElementById('add-balance-button').addEventListener('click', function() {
  var form = document.getElementById('add-balance-form');
  
  if (form) {
    form.remove();
    return;
  }

  var formHtml = '<form id="add-balance-form">';
  formHtml += '<label for="account-type">Account:</label>';
  formHtml += '<select id="account-type" name="account-type">';
  formHtml += '<option value="cash">Cash</option>';
  formHtml += '<option value="bank">Bank Account</option>';
  formHtml += '<option value="savings">Savings</option>';
  formHtml += '<option value="credit_cards">Credit Cards</option>';

  formHtml += '</select>';
  formHtml += '<br>';
  formHtml += '<label for="balance">Balance:</label>';
  formHtml += '<input type="number" id="balance" name="balance">';
  formHtml += '<br>';
  formHtml += '<input type="submit" id="balance-submit" value="Add">';
  formHtml += '</form>';

document.getElementById('add-balance-form-container').innerHTML = formHtml;

document.getElementById('add-balance-form').style.position = 'absolute';
document.getElementById('add-balance-form').style.top = '235px';
document.getElementById('add-balance-form').style.left = '410px';


  document.getElementById('add-balance-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var accountType = document.getElementById('account-type').value;
    var balance = document.getElementById('balance').value;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/update_account_balance');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
      if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        window.location.href = '/home';
      } else {
        console.log('Error: ' + xhr.status);
      }
    };
    xhr.send(JSON.stringify({
      accountType: accountType,
      balance: balance
    }));
  });
});