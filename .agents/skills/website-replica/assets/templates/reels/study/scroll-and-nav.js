// 学习副本：原站内联代码的可读摘录。页面仍使用 HTML 内的原始代码，此文件不会重复执行。

document.addEventListener("DOMContentLoaded", () => {

  // STOP BELOW 768
  const mediaQuery = window.matchMedia("(min-width: 769px)");

  if (!mediaQuery.matches) return;

  let lastScroll = 0;

  // TARGET ITEMS
  const leftItem = document.querySelector(".nav-brand");
  const rightItem = document.querySelector(".right-nav");

  // SAFETY CHECK
  if (!leftItem || !rightItem) return;

  window.addEventListener("scroll", () => {

    const currentScroll = window.pageYOffset;

    // SCROLL DOWN
    if (currentScroll > lastScroll && currentScroll > 100) {

      gsap.to([leftItem, rightItem], {
        y: -80,
        opacity: 0,
        duration: 0.4,
        ease: "power3.out",
        overwrite: true
      });

    } 
    
    // SCROLL UP
    else {

      gsap.to([leftItem, rightItem], {
        y: 0,
        opacity: 1,
        duration: 0.4,
        ease: "power3.out",
        overwrite: true
      });

    }

    lastScroll = currentScroll <= 0 ? 0 : currentScroll;

  });

});

// Lenis Smooth Scroll
const lenis = new Lenis({
  smooth: true,
  lerp: 0.1,
  wheelMultiplier: 1,
  infinite: false,
});

// GSAP + Lenis Connect
lenis.on('scroll', ScrollTrigger.update);

gsap.ticker.add((time) => {
  lenis.raf(time * 1000);
});

gsap.ticker.lagSmoothing(0);
