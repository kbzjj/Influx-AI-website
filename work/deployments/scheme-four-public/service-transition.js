/* Native Framer island: no reference iframe, no second smooth-scroll engine. */
const mount = document.getElementById('service-transition-root');
if (mount) {
  const [React, {default: Transition}] = await Promise.all([
    import('./runtime/service-transition/react.BNsJAPhr.mjs'),
    import('./runtime/service-transition/E7Gy02fTtRRJl6hMB7qcE2rxgwCUbKrxzEbR3iwtkZQ.B9xiGkhW.mjs')
  ]);
  React.n();
  const root = React.r(mount);
  const render = () => root.render(React.c(Transition, {variant: innerWidth < 810 ? 'xYb9_GjwT' : innerWidth < 1200 ? 'rqsJxbMBy' : 'WQLkyLRf1'}));
  render();
  let queued;
  addEventListener('resize', () => { cancelAnimationFrame(queued); queued = requestAnimationFrame(render); }, {passive:true});
  // Native Framer mounts asynchronously; refresh the existing Reels measurements afterwards.
  let aligned = false;
  const align = () => {
    if (window.influxLenis) window.influxLenis.scrollTo(mount.parentElement, {immediate:true, offset:-100});
    else window.scrollTo(0, mount.parentElement.getBoundingClientRect().top + scrollY - 100);
  };
  document.querySelectorAll('a[href="#managed"]').forEach(link => link.addEventListener('click', event => {
    event.preventDefault(); event.stopImmediatePropagation();
    history.replaceState(null, '', '#managed'); align();
  }, true));
  const observer = new ResizeObserver(() => {
    window.ScrollTrigger?.refresh();
    if (!aligned && mount.firstElementChild) {
      aligned = true;
      if (location.hash === '#managed') align();
    }
  });
  observer.observe(mount);
}
