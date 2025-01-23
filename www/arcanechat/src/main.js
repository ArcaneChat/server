import Swiper from "swiper";
import { Autoplay } from "swiper/modules";
import { Collapse } from "bootstrap";

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
      delay: 2500,
      disableOnInteraction: false,
    },
  });
});
