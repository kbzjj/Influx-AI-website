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

// The new category showcase has its own copy so the original language dictionary stays intact.
(() => {
 const section = document.querySelector('.creator-explorer');
 if (!section) return;
 const copy = {
  en: {eyebrow:'Creator discovery',title:'Different worlds. Your brand.',description:'Start with your brand goals. Explore creator categories and find a clearer direction for your next collaboration.',cta:'Explore our capabilities',beauty:'Beauty & Skincare',fashion:'Fashion',fitness:'Fitness',travel:'Travel',food:'Food & Drink',tech:'Technology',home:'Home & Living',gaming:'Gaming',outdoor:'Outdoors',family:'Family & Parenting',auto:'Automotive',pets:'Pets'},
  zh: {eyebrow:'探索创作者领域',title:'不同领域，同一个品牌目标。',description:'以品牌目标为起点，探索不同领域的创作者，为下一次合作找到更合适的方向。',cta:'探索产品能力',beauty:'美妆护肤',fashion:'时尚穿搭',fitness:'运动健身',travel:'旅行探索',food:'美食生活',tech:'数码科技',home:'家居生活',gaming:'游戏娱乐',outdoor:'户外运动',family:'亲子家庭',auto:'汽车出行',pets:'萌宠日常'}
 };
 const control = section.querySelector('.explorer-motion-control');
 let userPaused = false;
 const localize = () => {
  const chinese = document.documentElement.lang === 'zh-CN';
  const dictionary = copy[chinese ? 'zh' : 'en'];
  section.querySelectorAll('[data-explorer-copy]').forEach(element => element.textContent = dictionary[element.dataset.explorerCopy]);
  section.querySelectorAll('.category-card').forEach(card => {
   const label = dictionary[card.querySelector('[data-explorer-copy]').dataset.explorerCopy];
   card.querySelector('.category-photo').setAttribute('aria-label', chinese ? label + '场景示意' : label + ' editorial illustration');
  });
  section.querySelector('.category-viewport').setAttribute('aria-label', chinese ? '创作者领域场景示意' : 'Illustrative creator categories');
  control.querySelector('[data-motion-label]').textContent = chinese ? (userPaused ? '继续动效' : '暂停动效') : (userPaused ? 'Resume motion' : 'Pause motion');
  control.querySelector('.motion-control-icon').textContent = userPaused ? '▶' : 'Ⅱ';
 };
 control.addEventListener('click', () => {
  userPaused = !userPaused;
  section.classList.toggle('is-user-paused',userPaused);
  control.setAttribute('aria-pressed',String(userPaused));
  localize();
 });
 let inView = true;
 const sync = () => section.classList.toggle('is-paused', !inView || document.hidden);
 if ('IntersectionObserver' in window) new IntersectionObserver(([entry]) => {inView = entry.isIntersecting;sync();},{threshold:0}).observe(section);
 document.addEventListener('visibilitychange',sync);
 new MutationObserver(localize).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
 localize();
})();
