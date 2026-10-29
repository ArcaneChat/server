import Swiper from "swiper";
import { Autoplay } from "swiper/modules";

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

window.addEventListener("load", () => {
  const swiper = new Swiper(".swiper", {
    modules: [Autoplay],
    slidesPerView: 1,
    centeredSlides: true,
    loop: true,
    autoplay: {
      delay: 3000,
      disableOnInteraction: false,
    },
  });
});
