// Smooth scrolling and scroll reveals. Skipped entirely for reduced-motion users.
(() => {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  if (typeof Lenis === 'function') {
    const lenis = new Lenis({
      lerp: 0.1,
      wheelMultiplier: 1,
      anchors: { offset: -45 },
      allowNestedScroll: true,
      prevent: node => !!node.closest('dialog, [data-lenis-prevent]')
    });
    const raf = time => { lenis.raf(time); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);

    const dialogs = document.querySelectorAll('dialog');
    const syncDialogs = () => {
      const open = [...dialogs].some(dialog => dialog.open);
      open ? lenis.stop() : lenis.start();
    };
    dialogs.forEach(dialog => new MutationObserver(syncDialogs).observe(dialog, { attributes: true, attributeFilter: ['open'] }));
  }

  const targets = [
    '.creator-base-layout > *',
    '.tool-intro', '.tool-tab-showcase',
    '#managed .module-heading', '.service-model-intro', '.service-journey',
    '.contact-copy', '.contact-form-wrap',
    '.explorer-copy', '.category-viewport',
    '.footer-inner > *'
  ];
  const elements = [...new Set(targets.flatMap(selector => [...document.querySelectorAll(selector)]))];
  if (!elements.length || !('IntersectionObserver' in window)) return;

  const siblingIndex = new Map();
  elements.forEach(element => {
    const index = siblingIndex.get(element.parentElement) ?? 0;
    siblingIndex.set(element.parentElement, index + 1);
    element.style.setProperty('--reveal-i', Math.min(index, 4));
    element.dataset.reveal = '';
  });

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-revealed');
      observer.unobserve(entry.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  elements.forEach(element => observer.observe(element));
})();
