// Presentation-only behavior. Existing product, language and local form logic is in app.js.
(() => {
  const menu = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('.primary-links');
  const closeMenu = () => {
    menu.setAttribute('aria-expanded', 'false');
    navigation.dataset.open = 'false';
  };
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    navigation.dataset.open = String(open);
  });
  navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
      closeMenu(); menu.focus();
    }
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('header')) closeMenu();
  });
  matchMedia('(min-width: 651px)').addEventListener('change', closeMenu);
  const hero = document.querySelector('.hero');
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => {
      hero.classList.toggle('is-paused', !entry.isIntersecting || document.hidden);
    }, { threshold: 0 }).observe(hero);
  }
  document.addEventListener('visibilitychange', () => {
    hero.classList.toggle('is-paused', document.hidden || hero.getBoundingClientRect().bottom <= 0);
  });
  const localizeControls = () => {
    const chinese = document.documentElement.lang === 'zh-CN';
    menu.setAttribute('aria-label', chinese ? '切换导航菜单' : 'Toggle navigation');
    document.querySelector('.hero-scroll').setAttribute('aria-label', chinese ? '查看创作者资源' : 'Explore creator resources');
  };
  new MutationObserver(localizeControls).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
  localizeControls();
})();
