const toggler = document.querySelector(".navbar-toggler");
const collapse = document.getElementById("navbarCollapse");
toggler?.addEventListener("click", () => {
  const open = collapse.classList.toggle("show");
  toggler.setAttribute("aria-expanded", open);
});

window.addEventListener("scroll", () => {
  if (window.scrollY > 100) {
    document.querySelector(".back-to-top").style.display = "block";
  } else {
    document.querySelector(".back-to-top").style.display = "none";
  }
});

const track = document.querySelector(".carousel-track");
if (track) {
  const count = track.children.length;
  track.append(track.firstElementChild.cloneNode(true));
  let index = 0;
  setInterval(() => {
    index++;
    track.style.transition = "transform 0.3s";
    track.style.transform = `translateX(-${index * 100}%)`;
  }, 3000);
  track.addEventListener("transitionend", () => {
    if (index === count) {
      index = 0;
      track.style.transition = "none";
      track.style.transform = "translateX(0)";
    }
  });
}
