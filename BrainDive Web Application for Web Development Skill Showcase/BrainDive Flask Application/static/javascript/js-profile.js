var uploadIcon = document.querySelector(".upload-icon");
var pictureInput = document.querySelector("#picture");
var previewContainer = document.querySelector(".preview-container");
var previewImage = document.querySelector(".preview-image");
var saveButton = document.querySelector("#save-button");
uploadIcon.addEventListener("click", function () {
    pictureInput.click();
});
pictureInput.addEventListener("change", function () {
    var file = this.files[0];
    if (file) {
        var reader = new FileReader();
        reader.addEventListener("load", function () {
            previewImage.setAttribute("src", reader.result);
            previewContainer.style.display = "block";
            saveButton.style.display = "block";
            uploadIcon.style.display = "none";
        });
        reader.readAsDataURL(file);
    }
});

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

const editButton = document.getElementById("edit-button");
const editOptions = document.getElementById("edit-options");
const profilePic = document.getElementById("profile-pic");
const pictureForm = document.getElementById("upload-icon");
const textContainer = document.getElementById("text-container");

editButton.addEventListener("click", function () {
    editOptions.style.display = "block";
    pictureForm.style.display = "none";
    textContainer.style.display = "none";
});