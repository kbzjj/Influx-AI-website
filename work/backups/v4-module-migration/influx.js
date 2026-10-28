/* Influx content and local-only interactions. Original Reels motion is loaded after this. */
(() => {
  'use strict';
  const dictionary = window.INFLUX_COPY;
  let language = 'en';
  try { language = localStorage.getItem('infux-language') === 'zh' ? 'zh' : 'en'; } catch {}
  const say = key => dictionary[key]?.[language] || dictionary[key]?.en || key;
  document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';
  document.querySelectorAll('[data-copy]').forEach(node => { node.innerHTML = say(node.dataset.copy); });
  document.querySelectorAll('[data-placeholder]').forEach(node => { node.placeholder = say(node.dataset.placeholder); });
  document.querySelectorAll('[data-lang]').forEach(button => { button.setAttribute('aria-pressed', String(button.dataset.lang === language)); });
  const titles = {'index.html':['Influx AI — AI 驱动的达人营销 Agency','Influx AI — AI-powered creator marketing agency'],'pricing.html':['Influx AI — 工具与价格','Influx AI — Tools & pricing'],'free-tools.html':['Influx AI — 互动率计算器','Influx AI — Engagement calculator']};
  document.title = (titles[document.body.dataset.page] || titles['index.html'])[language === 'zh' ? 0 : 1];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const form = document.getElementById('contact-form');
  const draftKey = 'influx-v4-contact-draft';
  const fields = ['name','email','company','message'];
  const saveDraft = () => {
    if (!form) return;
    try { sessionStorage.setItem(draftKey, JSON.stringify(Object.fromEntries(fields.map(key => [key, form.elements[key].value])))); } catch {}
  };
  if (form) {
    try {
      const draft = JSON.parse(sessionStorage.getItem(draftKey) || '{}');
      fields.forEach(key => { if (typeof draft[key] === 'string') form.elements[key].value = draft[key]; });
    } catch {}
    const intent = new URL(location.href).searchParams.get('intent');
    if (['free','plus'].includes(intent)) {
      form.dataset.intent = intent;
      if (!form.elements.message.value.trim()) form.elements.message.value = language === 'zh' ? `我想了解 ${intent === 'free' ? 'Free 体验' : 'Plus 方案'}。` : `I'd like to learn about ${intent === 'free' ? 'the Free experience' : 'the Plus plan'}.`;
      saveDraft();
    }
    form.addEventListener('input', saveDraft);
  }
  // Reload on language changes so the original Webflow/SplitText timelines bind translated nodes once.
  document.querySelectorAll('[data-lang]').forEach(button => button.addEventListener('click', () => {
    if (button.dataset.lang === language) return;
    saveDraft();
    try { localStorage.setItem('infux-language', button.dataset.lang); } catch {}
    location.reload();
  }));
  document.querySelectorAll('a[href^="index.html#"]').forEach(link => {
    if (document.body.dataset.page === 'index.html') link.setAttribute('href', link.getAttribute('href').replace('index.html',''));
  });
  document.querySelectorAll('.desktop-nav a').forEach(link => {
    if (document.body.dataset.page === 'pricing.html' && link.getAttribute('href') === 'pricing.html') link.setAttribute('aria-current','page');
  });
  const header = document.querySelector('.site-header');
  const menu = document.getElementById('mobile-navigation');
  const toggle = document.querySelector('.mobile-menu-toggle');
  const setMenu = (open, restore = false) => {
    menu.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', language === 'zh' ? (open ? '关闭导航' : '打开导航') : (open ? 'Close navigation' : 'Open navigation'));
    header.classList.remove('is-hidden');
    if (open) menu.querySelector('a').focus({preventScroll:true});
    else if (restore) toggle.focus();
  };
  setMenu(false);
  toggle.addEventListener('click', () => setMenu(menu.hidden));
  menu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
  document.addEventListener('click', event => { if (!menu.hidden && !menu.contains(event.target) && !header.contains(event.target)) setMenu(false); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && !menu.hidden) { setMenu(false,true); event.preventDefault(); } });
  let lastScroll = scrollY, scheduled = false;
  addEventListener('scroll', () => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => {
      const current = scrollY;
      header.classList.toggle('is-scrolled',current > 50);
      if (Math.abs(current-lastScroll)>4) {
        header.classList.toggle('is-hidden',current > 140 && current > lastScroll && menu.hidden && !header.contains(document.activeElement));
        lastScroll=current;
      }
      scheduled=false;
    });
  }, {passive:true});
  header.addEventListener('focusin', () => header.classList.remove('is-hidden'));
  document.querySelector('.site-header .brand').addEventListener('click',event=>{
    if(document.body.dataset.page!=='index.html')return;
    event.preventDefault();
    setMenu(false);
    history.replaceState(null,'',location.pathname);
    if(window.influxLenis)window.influxLenis.scrollTo(0);else window.scrollTo({top:0,behavior:reduced.matches?'auto':'smooth'});
  });
  const updateMenu = () => { if (innerWidth>600 && !menu.hidden) setMenu(false); };
  addEventListener('resize',updateMenu,{passive:true});
  // Capture before Webflow's form handler; no form can reach an external business endpoint.
  document.addEventListener('submit', event => {
    if (event.target.id === 'contact-form') {
      event.preventDefault();event.stopImmediatePropagation();
      if (!form.reportValidity()) return;
      const status=form.querySelector('.form-status');
      try {
        const enquiries=JSON.parse(localStorage.getItem('influx-v4-inquiries') || '[]');
        const data=Object.fromEntries(new FormData(form));
        enquiries.push({...data,source:form.dataset.intent || 'contact',savedAt:new Date().toISOString()});
        localStorage.setItem('influx-v4-inquiries',JSON.stringify(enquiries.slice(-20)));
        status.textContent=say('saved');
        saveDraft();
      } catch { status.textContent=say('saveFailed'); }
    }
    if (event.target.id === 'engagement-calculator') {
      event.preventDefault();event.stopImmediatePropagation();
      const calc=event.target;if (!calc.reportValidity()) return;
      const followers=Number(calc.elements.followers.value), likes=Number(calc.elements.likes.value), comments=Number(calc.elements.comments.value);
      if (![followers,likes,comments].every(Number.isFinite) || followers <= 0 || likes < 0 || comments < 0) return;
      const result=document.getElementById('engagement-result');
      result.textContent=((likes+comments)/followers*100).toLocaleString(language==='zh'?'zh-CN':'en-US',{maximumFractionDigits:2})+'%';
      const bounds=result.getBoundingClientRect();
      if(bounds.top<0||bounds.bottom>innerHeight){
        if(window.influxLenis) window.influxLenis.scrollTo(result,{offset:-innerHeight/3});
        else result.scrollIntoView({behavior:reduced.matches?'auto':'smooth',block:'center'});
      }
    }
  },true);
  document.querySelector('.w-slider-arrow-left')?.setAttribute('aria-label',language==='zh'?'上一项能力':'Previous capability');
  document.querySelector('.w-slider-arrow-right')?.setAttribute('aria-label',language==='zh'?'下一项能力':'Next capability');
  const screenDialog=document.getElementById('screen-dialog');
  const expanded=document.getElementById('expanded-screen');
  const openScreen=image=>{
    expanded.src=image.getAttribute('src');expanded.alt=image.alt;
    screenDialog.showModal();window.influxLenis?.stop();
  };
  document.querySelectorAll('[data-product-screen]').forEach(image=>{
    image.setAttribute('aria-label',language==='zh'?'查看完整产品截图':'View full product screenshot');
    image.addEventListener('click',()=>openScreen(image));
    image.addEventListener('keydown',event=>{if (event.key==='Enter'||event.key===' '){event.preventDefault();openScreen(image);}});
  });
  document.querySelectorAll('[data-zoom]').forEach(button=>{
    button.setAttribute('aria-label',say('zoomScreen'));
    const open=()=>openScreen(button.closest('.w-slide').querySelector('[data-product-screen]'));
    button.addEventListener('click',open);
    button.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();open();}});
  });
  const legal=document.getElementById('legal-dialog');
  document.querySelectorAll('[data-legal]').forEach(button=>button.addEventListener('click',()=>{
    legal.querySelector('#legal-title').textContent=say(button.dataset.legal);
    legal.querySelector('#legal-content').textContent=say(button.dataset.legal+'Body');
    legal.showModal();window.influxLenis?.stop();
  }));
  document.querySelectorAll('dialog').forEach(dialog=>{
    dialog.querySelector('[data-close]').addEventListener('click',()=>dialog.close());
    dialog.addEventListener('close',()=>window.influxLenis?.start());
    dialog.addEventListener('click',event=>{
      if(event.target!==dialog)return;
      const rect=dialog.getBoundingClientRect();
      if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)dialog.close();
    });
  });
})();
