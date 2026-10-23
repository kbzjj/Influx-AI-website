/* Scheme three: presentation and adapted copy. Inquiry storage stays in app.js. */
(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const english = Object.fromEntries([...document.querySelectorAll('[data-copy]')].map(el => [el.dataset.copy, el.innerHTML]));
  const chinese = {
    menu:'菜单', heroLabel:'AI 驱动 · 达人营销 · 全球连接',
    heroTitle:'让全球布局<br>始于<em>真实连接。</em>',
    heroDescription:'用 AI 理解不同文化，用数据为营销判断提供依据。<br>找到合适的创作者，让有价值的合作从这里发生。',
    stageLabel:'真实的人，更多合作可能。', nativeContent:'融入平台语境的内容', humanStories:'真实的故事。<br>有意义的连接。',
    badgeLabel:'创作者档案，连接全球合作可能。', referenceNote:'参考影像 · 仅作视觉演示', pauseMotion:'暂停动效',
    resourceCardLabel:'覆盖全球的创作者资源库', resourceCardSubtitle:'真实的人，更多合作可能。',
    chipBeauty:'美妆护肤', chipFashion:'时尚穿搭', chipTravel:'旅行探索', chipFood:'美食饮品', chipFitness:'运动健身', chipTech:'数码科技',
    platformHeading:'你的受众遍布世界。<br>从他们所在的平台开始。', manifestoLabel:'不止于粉丝数字',
    manifestoTitle:'好的营销，始于<br><em>找到对的人。</em><br>让理解先于选择。',
    manifestoDescription:'每一个账号背后，都有真实的人、社群，以及人们愿意倾听的理由。我们将这些人与内容的背景连接到数据和 AI，让合作判断更有依据。',
    exploreTools:'探索产品能力', networkLabel:'全球视野，真实连接。', networkTitle:'世界很大。<br><em>合适的人，就在其中。</em>',
    statCreators:'创作者档案', statPlatforms:'主流社交平台', dataSource:'TikTok、YouTube、Instagram 官方 API 数据，支持 X 平台。', creatorRange:'从新兴声音，到成熟的影响力。',
    productTitle:'少一些猜测。<br><em>多一些理解。</em>', capability1:'AI 达人搜索', capability2:'达人资源库', capability3:'营销活动管理', capability4:'品牌洞察',
    discussTools:'聊聊产品需求', viewScreenshot:'查看完整截图 +', productNote:'此处展示整体产品能力，各方案开放范围以定价页为准。',
    serviceVideoLabel:'以数据为据。<br>与真实的人协作。', serviceSticker:'你的品牌。<br>我们的团队。', serviceLabel:'让技术与营销经验，一起投入你的品牌',
    serviceTitle:'你把握方向。<br>我们<em>推进合作。</em>', serviceCta:'聊聊你的营销项目',
    processLabel:'从目标，到一起行动', processTitle:'从一份需求。<br><em>到共同的目标。</em>', processDescription:'四个阶段，清晰分工。<br>同一个目标，一支协作团队。',
    categoriesLabel:'探索创作者领域', categoriesTitle:'不同领域。<br><em>同一个品牌目标。</em>', categoriesDescription:'以品牌目标为起点，探索不同领域。<br>为下一次合作找到合适的方向。',
    categoryBeauty:'美妆与<br>生活方式', categoryFashion:'时尚与<br>潮流文化', categoryFood:'美食与<br>饮品', categoryLiving:'人物与<br>多元视角',
    faqLabel:'关于合作，你可能想了解', faqTitle:'好的问题。<br><em>清晰的答案。</em>', faq1q:'我该选择工具，还是营销服务？',
    faq1a:'如果你希望由自己的团队开展达人营销，可以了解 Influx Tool 的数据与 AI 能力。如果希望由我们的团队支持规划与执行，可以选择 Influx Services。也可以一起沟通两种合作方式。',
    faq2q:'支持哪些社交平台？', faq2a:'当前产品覆盖 TikTok、YouTube、Instagram 和 X。其中 TikTok、YouTube、Instagram 接入官方 API 数据。',
    faq3q:'Plus 包含全部四大产品能力吗？', faq3a:'Plus 专注于达人发现与分析，不包含 Campaign 管理、达人建联、报告、数据与品牌洞察。具体开放能力及方案范围请查看定价页。',
    faq4q:'营销服务的范围如何确定？', faq4a:'我们从品牌目标、目标市场、预算与时间安排开始沟通。具体工作内容、双方职责与报价，围绕项目需求共同约定。',
    contactHeading:'下一次连接，<br>从<em>这里开始。</em>', closingLabel:'真实的人，更多合作可能。',
    closingTitle:'世界充满可能。<br>让每一次<em>连接，</em><br>都更有意义。', closingCta:'一起探索下一次合作'
  };
  let motionContext;
  let userPaused = false;
  let lenis;
  const videos = [...document.querySelectorAll('[data-video]')];
  const pauseButton = document.getElementById('motion-toggle');
  const activeMotion = () => !reduced.matches && !userPaused;
  const zhMode = () => document.documentElement.lang === 'zh-CN';

  function translate() {
    motionContext?.revert();
    document.querySelectorAll('[data-copy]').forEach(el => {
      el.innerHTML = (zhMode() ? chinese : english)[el.dataset.copy] ?? english[el.dataset.copy];
    });
    document.title = zhMode() ? 'Influx AI — 让全球布局，始于真实连接。' : 'Influx AI — Real connections. Worldwide access.';
    document.querySelector('.category-track').setAttribute('aria-label', zhMode() ? '创作者领域示意' : 'Illustrative creator categories');
    document.querySelector('[data-slide="-1"]').setAttribute('aria-label', zhMode() ? '上一组领域' : 'Previous categories');
    document.querySelector('[data-slide="1"]').setAttribute('aria-label', zhMode() ? '下一组领域' : 'Next categories');
    document.querySelector('.network-card').setAttribute('aria-label', zhMode() ? '全球创作者资源库：2.1 亿以上创作者档案' : 'Global creator network: over 210 million profiles');
    document.querySelector('.platform-marquee').setAttribute('aria-label', zhMode() ? '支持的社交平台' : 'Supported social platforms');
    enhanceButtons();
    buildMotion();
    updatePauseLabel();
    syncVideos();
  }

  // Reels-inspired scroll composition; all content remains visible without JS or animation.
  function buildMotion() {
    motionContext?.revert();
    if (!window.gsap || !window.ScrollTrigger || !activeMotion()) return;
    gsap.registerPlugin(ScrollTrigger);
    motionContext = gsap.context(() => {
      gsap.utils.toArray('[data-drift]').forEach(card => {
        gsap.fromTo(card, { y: 0 }, { y: Number(card.dataset.drift), ease: 'none', scrollTrigger: { trigger: '.creator-stage', start: 'top 75%', end: 'bottom top', scrub: 1 } });
      });
      gsap.to('.big-spark', { rotation: 100, ease: 'none', scrollTrigger: { trigger: '.manifesto', start: 'top bottom', end: 'bottom top', scrub: 1 } });
      // Wrap words (or short Chinese phrases) without altering line breaks or emphasis.
      const statement = document.querySelector('.reveal-statement');
      statement.setAttribute('aria-label', statement.innerText.replace(/\n/g, ' '));
      statement.querySelectorAll('.word').forEach(word => word.replaceWith(document.createTextNode(word.textContent)));
      const walker = document.createTreeWalker(statement, NodeFilter.SHOW_TEXT);
      const nodes = [];
      while (walker.nextNode()) nodes.push(walker.currentNode);
      nodes.forEach(node => {
        const parts = zhMode() ? node.textContent.match(/.{1,2}/gu) : node.textContent.split(/(\s+)/);
        const fragment = document.createDocumentFragment();
        (parts || []).forEach(part => {
          if (!part.trim()) fragment.append(document.createTextNode(part));
          else { const word = document.createElement('span'); word.className = 'word'; word.textContent = part; fragment.append(word); }
        });
        node.replaceWith(fragment);
      });
      gsap.fromTo(statement.querySelectorAll('.word'), { opacity: .18 }, { opacity: 1, stagger: .1, ease: 'none', scrollTrigger: { trigger: statement, start: 'top 82%', end: 'bottom 40%', scrub: .5 } });
      if (innerWidth > 800) {
        gsap.utils.toArray('.product-card').slice(0, -1).forEach((card, index) => {
          const retreat = gsap.timeline({ scrollTrigger: {
            trigger: card.nextElementSibling, start: 'top 88%',
            end: () => `top ${100 + (index + 1) * 18}px`, scrub: .55, invalidateOnRefresh: true
          } });
          retreat.to(card, { scale: .9 + index * .012, y: -12, ease: 'none' }, 0);
          retreat.to(card.querySelector('.stack-shade'), { opacity: .08, ease: 'none' }, 0);
        });
      }
      gsap.utils.toArray('.process-card').forEach(card => {
        ScrollTrigger.create({ trigger: card, start: 'top 70%', end: 'bottom 30%', toggleClass: 'is-active' });
      });
    });
    ScrollTrigger.refresh();
  }

  function syncScrolling() {
    if (activeMotion() && window.Lenis && !lenis) {
      lenis = new Lenis({ duration: 1.05, smoothWheel: true, anchors: true, autoRaf: true, prevent: node => node.closest('dialog,.menu-panel,.category-track,.contact-select-menu,textarea,select') });
      if (window.ScrollTrigger) lenis.on('scroll', ScrollTrigger.update);
    } else if (!activeMotion() && lenis) { lenis.destroy(); lenis = undefined; }
  }
  function updateVideoButton(video) {
    const control = video.closest('figure')?.querySelector('.video-toggle');
    if (!control) return;
    const playing = !video.paused;
    control.textContent = playing ? 'Ⅱ' : '▶';
    control.setAttribute('aria-pressed', String(playing));
    control.setAttribute('aria-label', zhMode() ? (playing ? '暂停视频' : '播放视频') : (playing ? 'Pause video' : 'Play video'));
  }
  function syncVideos() {
    videos.forEach(video => {
      if (activeMotion() && !document.hidden && video.dataset.inView === 'true' && video.dataset.userPaused !== 'true') {
        video.play().catch(() => { updateVideoButton(video); });
      } else video.pause();
      updateVideoButton(video);
    });
  }
  const videoObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => { entry.target.dataset.inView = String(entry.isIntersecting); });
    syncVideos();
  }, { threshold: .08 });
  videos.forEach(video => {
    video.muted = true;
    videoObserver.observe(video);
    video.addEventListener('play', () => updateVideoButton(video));
    video.addEventListener('pause', () => updateVideoButton(video));
    const button = video.closest('figure')?.querySelector('.video-toggle');
    button?.addEventListener('click', () => {
      if (video.paused) { video.dataset.userPaused = 'false'; video.play().catch(() => {}); }
      else { video.dataset.userPaused = 'true'; video.pause(); }
    });
  });
  document.addEventListener('visibilitychange', () => {
    document.body.classList.toggle('page-hidden', document.hidden);
    syncVideos();
  });

  function enhanceButtons() {
    document.querySelectorAll('.button').forEach(button => {
      let label = button.querySelector(':scope > [data-i18n], :scope > [data-copy]');
      const previous = button.querySelector('.button-label-first');
      const text = (label?.textContent || previous?.textContent || button.textContent).replace(/[→↗]\s*$/u, '').trim();
      let icon = button.querySelector('.button-icon');
      if (!label) {
        button.replaceChildren();
        label = document.createElement('span');
        button.append(label);
        icon = null;
      }
      if (!icon) {
        icon = document.createElement('span');
        icon.className = 'button-icon';
        icon.setAttribute('aria-hidden', 'true');
        button.prepend(icon);
      }
      icon.innerHTML = '<img src="assets/button-arrow.svg" alt="" width="28" height="20">';
      label.className = 'button-label';
      label.replaceChildren();
      ['button-label-first', 'button-label-next'].forEach((className, index) => {
        const line = document.createElement('span');
        line.className = className;
        line.textContent = text;
        if (index) line.setAttribute('aria-hidden', 'true');
        label.append(line);
      });
    });
    document.querySelectorAll('.text-link > span:last-child, .nav-contact > span:last-child').forEach(icon => {
      if (icon.textContent.trim() === '→') {
        icon.setAttribute('aria-hidden', 'true');
        icon.innerHTML = '<img src="assets/button-arrow.svg" alt="" width="28" height="20">';
      }
    });
  }

  // As in Reels: the hovered card straightens and grows while its neighbors move aside.
  const stageSlots = [...document.querySelectorAll('.stage-slot')];
  function setStageFocus(index) {
    const enabled = innerWidth > 800 && activeMotion() && index >= 0;
    stageSlots.forEach((slot, i) => {
      slot.classList.toggle('is-active', enabled && i === index);
      const distance = enabled && i !== index ? Math.sign(i - index) * Math.min(64, 30 + Math.abs(i - index) * 8) : 0;
      slot.style.setProperty('--nudge', `${distance}px`);
    });
  }
  stageSlots.forEach((slot, index) => {
    slot.addEventListener('pointerenter', event => { if (event.pointerType !== 'touch') setStageFocus(index); });
    slot.addEventListener('pointerleave', () => setStageFocus(-1));
    slot.addEventListener('focusin', () => setStageFocus(index));
    slot.addEventListener('focusout', event => { if (!slot.contains(event.relatedTarget)) setStageFocus(-1); });
  });
  const ambientObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => entry.target.classList.toggle('is-outside', !entry.isIntersecting));
  });
  document.querySelectorAll('.network-card,.platform-bar').forEach(region => ambientObserver.observe(region));

  function updatePauseLabel() {
    const paused = userPaused || reduced.matches;
    document.body.classList.toggle('motion-paused', paused);
    if (paused) setStageFocus(-1);
    pauseButton.setAttribute('aria-pressed', String(paused));
    pauseButton.querySelector('span:first-child').textContent = paused ? '▶' : 'Ⅱ';
    pauseButton.querySelector('[data-copy]').textContent = zhMode() ? (paused ? '继续动效' : '暂停动效') : (paused ? 'Resume motion' : 'Pause motion');
    pauseButton.disabled = reduced.matches;
    pauseButton.title = reduced.matches ? (zhMode() ? '已遵循系统减少动态效果设置' : 'System reduced-motion preference is active') : '';
  }
  pauseButton.addEventListener('click', () => {
    userPaused = !userPaused;
    syncScrolling();
    buildMotion();
    syncVideos();
    updatePauseLabel();
  });
  reduced.addEventListener('change', () => { syncScrolling(); buildMotion(); syncVideos(); updatePauseLabel(); });

  // Disclosure navigation with keyboard focus and Escape handling.
  const menuButton = document.querySelector('.menu-button');
  const header = document.querySelector('.site-header');
  const menu = document.getElementById('menu-panel');
  const scrim = document.querySelector('.menu-scrim');
  function setMenu(open, restoreFocus = true) {
    menuButton.setAttribute('aria-expanded', String(open));
    menu.hidden = !open;
    menu.inert = !open;
    scrim.hidden = !open;
    document.body.classList.toggle('menu-open', open);
    if (open) { lenis?.stop(); menu.querySelector('a').focus(); }
    else { lenis?.start(); if (restoreFocus) menuButton.focus(); }
  }
  const menuClosed = () => !menu || menu.hidden;
  menuButton?.addEventListener('click', () => setMenu(menu.hidden));
  let previousScroll = scrollY;
  let scrollQueued = false;
  addEventListener('scroll', () => {
    if (scrollQueued) return;
    scrollQueued = true;
    requestAnimationFrame(() => {
      const current = scrollY;
      header.classList.toggle('is-scrolled', current > 50);
      if (Math.abs(current - previousScroll) > 4) {
        header.classList.toggle('is-hidden', current > 140 && current > previousScroll && menuClosed() && !header.querySelector(':focus-visible'));
        previousScroll = current;
      }
      scrollQueued = false;
    });
  }, { passive: true });
  header.addEventListener('focusin', () => header.classList.remove('is-hidden'));
  scrim?.addEventListener('click', () => setMenu(false));
  menu?.querySelectorAll('a,button').forEach(link => link.addEventListener('click', () => setMenu(false, false)));
  document.addEventListener('keydown', event => {
    if (menuClosed()) return;
    if (event.key === 'Escape') { event.preventDefault(); setMenu(false); }
    if (event.key === 'Tab') {
      const stops = [menuButton, ...menu.querySelectorAll('a,button')];
      const first = stops[0], last = stops[stops.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
  });
  // Native dialogs own keyboard focus; stop the smooth scroller while one is open.
  document.querySelectorAll('dialog').forEach(dialog => {
    new MutationObserver(() => {
      if ([...document.querySelectorAll('dialog')].some(item => item.open)) lenis?.stop();
      else if (menuClosed()) lenis?.start();
    }).observe(dialog, { attributes: true, attributeFilter: ['open'] });
  });
  const track = document.querySelector('.category-track');
  document.querySelectorAll('[data-zoom]').forEach(button => button.addEventListener('click', () => {
    button.closest('.product-visual').querySelector('[data-product-screen]').click();
  }));
  document.querySelectorAll('[data-slide]').forEach(button => button.addEventListener('click', () => {
    const item = track.querySelector('.category-card');
    track.scrollBy({ left: (item.getBoundingClientRect().width + parseFloat(getComputedStyle(track).gap)) * Number(button.dataset.slide), behavior: reduced.matches ? 'instant' : 'smooth' });
  }));
  track.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      document.querySelector(`[data-slide="${event.key === 'ArrowLeft' ? '-1' : '1'}"]`).click();
    }
  });
  let resizeTimer;
  addEventListener('resize', () => { setStageFocus(-1); clearTimeout(resizeTimer); resizeTimer = setTimeout(buildMotion, 200); }, { passive: true });
  new MutationObserver(translate).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
  syncScrolling();
  translate();
})();
