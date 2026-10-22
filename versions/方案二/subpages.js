// Shared presentation behavior for the two subpages; product/form logic stays in app.js.
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
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { closeMenu(); menu.focus(); }
  });
  document.addEventListener('click', event => { if (!event.target.closest('header')) closeMenu(); });
  const localize = () => menu.setAttribute('aria-label', document.documentElement.lang === 'zh-CN' ? '切换导航菜单' : 'Toggle navigation');
  new MutationObserver(localize).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
  localize();
})();
