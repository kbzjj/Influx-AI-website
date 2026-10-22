// A light scroll drift recreates the public reference's moving image composition.
(() => {
  const hero = document.querySelector('.hero');
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  let queued = false;
  const paint = () => {
    queued = false;
    const progress = preference.matches ? 0 : Math.max(0, Math.min(1, -hero.getBoundingClientRect().top / innerHeight));
    hero.style.setProperty('--hero-progress', progress.toFixed(3));
  };
  addEventListener('scroll', () => {
    if (!queued && !document.hidden && hero.getBoundingClientRect().bottom > 0) {
      queued = true; requestAnimationFrame(paint);
    }
  }, { passive: true });
  preference.addEventListener('change', paint);
  paint();
})();
