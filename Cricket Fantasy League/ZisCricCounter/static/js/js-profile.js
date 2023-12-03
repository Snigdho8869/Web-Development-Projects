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

function getTop5Players() {
    fetch("/get_top_5_players_of_user", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then(response => response.json())
        .then(data => {
            const topPlayersList = document.getElementById("topPlayersList");

            topPlayersList.innerHTML = "";

            data.forEach(player => {
                const listItem = document.createElement("li");
                listItem.innerHTML = `<strong>${player.player_name}</strong> (${player.role}): ${player.player_total_points} points`;
                topPlayersList.appendChild(listItem);
            });
        })
        .catch(error => console.error("Error fetching top players:", error));
}

getTop5Players();

function getBatsmanPlayers() {
    fetch("/get_all_batsman_players_of_user", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then(response => response.json())
        .then(data => {
            const topPlayersList = document.getElementById("batsmanPlayersList");

            topPlayersList.innerHTML = "";

            data.forEach(player => {
                const listItem = document.createElement("li");
                listItem.innerHTML = `<strong>${player.player_name}</strong>: ${player.player_total_points} points`;
                topPlayersList.appendChild(listItem);
            });
        })
        .catch(error => console.error("Error fetching top players:", error));
}

getBatsmanPlayers();

function getBowlerPlayers() {
    fetch("/get_all_bowler_players_of_user", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then(response => response.json())
        .then(data => {
            const topPlayersList = document.getElementById("bowlerPlayersList");

            topPlayersList.innerHTML = "";

            data.forEach(player => {
                const listItem = document.createElement("li");
                listItem.innerHTML = `<strong>${player.player_name}</strong>: ${player.player_total_points} points`;
                topPlayersList.appendChild(listItem);
            });
        })
        .catch(error => console.error("Error fetching top players:", error));
}

getBowlerPlayers();

function getAllrounderPlayers() {
    fetch("/get_all_allrounder_players_of_user", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then(response => response.json())
        .then(data => {
            const topPlayersList = document.getElementById("allrounderPlayersList");

            topPlayersList.innerHTML = "";

            data.forEach(player => {
                const listItem = document.createElement("li");
                listItem.innerHTML = `<strong>${player.player_name}</strong>: ${player.player_total_points} points`;
                topPlayersList.appendChild(listItem);
            });
        })
        .catch(error => console.error("Error fetching top players:", error));
}

getAllrounderPlayers();

function getAllPlayers() {
    fetch("/get_all_players_of_user", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then(response => response.json())
        .then(data => {
            const topPlayersList = document.getElementById("allPlayersList");

            topPlayersList.innerHTML = "";

            data.forEach(player => {
                const listItem = document.createElement("li");
                listItem.innerHTML = `<strong>${player.player_name}</strong> (${player.role}): ${player.player_total_points} points`;
                topPlayersList.appendChild(listItem);
            });
        })
        .catch(error => console.error("Error fetching all players:", error));
}

getAllPlayers();
