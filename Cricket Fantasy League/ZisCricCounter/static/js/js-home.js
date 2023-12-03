var menuToggle = document.getElementById("menu-toggle");
var menu = document.getElementById("menu");
menuToggle.addEventListener("click", function () {
    if (menu.style.height === "0px") {
        menu.style.height = "80px";
        menuToggle.classList.add("active");
    } else {
        menu.style.height = "0px";
        menuToggle.classList.remove("active");
    }
});
