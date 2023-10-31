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


const searchBar = document.querySelector('.search-bar');
const videoWrappers = document.querySelectorAll('.video-wrapper');

searchBar.addEventListener('input', () => {
  const searchQuery = searchBar.value.trim().toLowerCase();

  videoWrappers.forEach((videoWrapper) => {
    const title = videoWrapper.querySelector('h4').textContent.toLowerCase();

    if (title.includes(searchQuery)) {
      videoWrapper.style.display = 'block';
    } else {
      videoWrapper.style.display = 'none';
    }
  });
});


