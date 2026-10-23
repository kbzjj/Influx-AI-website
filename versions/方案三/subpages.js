/* Scheme three subpages: extra copy, frosted header and pricing tabs. Form logic stays in app.js. */
(() => {
  'use strict';
  Object.assign(zh, {
    sp_pricingkicker: '定价', sp_pricingmeta: '工具产品 / 营销服务',
    sp_pricingtitle: '选择适合你的<br><em>合作方式。</em>',
    sp_pricingintro: '让你的团队用上我们的技术，或让我们的团队投入你的营销项目。',
    sp_tabtool: '工具产品', sp_tabservices: '营销服务',
    sp_freecta: '申请免费体验', sp_pluscta: '申请 Plus 方案',
    sp_quotecta: '获取报价', sp_backmanaged: '了解服务模式', sp_sendquote: '提交报价需求',
    sp_contact: '联系 Influx', sp_help: '还不确定哪种方式适合你？和我们聊聊。',
    sp_freekicker: '免费工具', sp_freemeta: '无需注册',
    sp_freetitle: '让判断更清楚的<br><em>实用工具。</em>',
    sp_calcbutton: '计算互动率', sp_resultkicker: '计算结果',
    sp_explore: '探索产品能力', sp_exploredesc: '达人搜索、数据分析与受众洞察。',
    sp_talk: '与我们的团队聊聊', sp_talkdesc: '由 Influx 团队协助规划与执行。'
  });
  setLanguage(lang);

  const header = document.querySelector('.site-header');
  let previous = scrollY;
  let queued = false;
  const sync = () => {
    const current = scrollY;
    header.classList.toggle('is-scrolled', current > 30);
    if (Math.abs(current - previous) > 4) {
      header.classList.toggle('is-hidden', current > 140 && current > previous && !header.contains(document.activeElement));
      previous = current;
    }
    queued = false;
  };
  addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(sync); } }, { passive: true });
  header.addEventListener('focusin', () => header.classList.remove('is-hidden'));
  sync();

  const tabs = [...document.querySelectorAll('[data-pricing-view]')];
  if (!tabs.length) return;
  const select = (tab, focus) => {
    tabs.forEach(item => {
      const active = item === tab;
      item.setAttribute('aria-selected', String(active));
      item.tabIndex = active ? 0 : -1;
      document.getElementById(item.getAttribute('aria-controls')).hidden = !active;
    });
    if (focus) tab.focus();
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => select(tab, false));
    tab.addEventListener('keydown', event => {
      if (event.key !== 'ArrowRight' && event.key !== 'ArrowLeft') return;
      event.preventDefault();
      const step = event.key === 'ArrowRight' ? 1 : -1;
      select(tabs[(index + step + tabs.length) % tabs.length], true);
    });
  });
  if (location.hash === '#services') select(tabs[1], false);
})();
