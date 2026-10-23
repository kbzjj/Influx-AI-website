const state = { templates: [], filter: '全部模板', search: '' };
const $ = (selector) => document.querySelector(selector);
const icon = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 15 15 5M5 5h10v10"/></svg>';
const escape = (value) => String(value).replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

function reset() {
  state.search = '';
  state.filter = '全部模板';
  $('#search').value = '';
  renderFilters();
  render();
}

function renderFilters() {
  const categories = ['全部模板', ...new Set(state.templates.map((item) => item.category).filter(Boolean))];
  $('#filters').replaceChildren(...categories.map((name) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'filter' + (state.filter === name ? ' active' : '');
    button.setAttribute('aria-pressed', String(state.filter === name));
    const count = name === '全部模板' ? state.templates.length : state.templates.filter((item) => item.category === name).length;
    button.innerHTML = `${escape(name)}<span>${count}</span>`;
    button.addEventListener('click', () => { state.filter = name; renderFilters(); render(); });
    return button;
  }));
}

function render() {
  const query = state.search.trim().toLocaleLowerCase();
  const items = state.templates.filter((item) => (state.filter === '全部模板' || item.category === state.filter)
    && [item.name, item.description, item.stack, item.category, ...(item.tags || [])].join(' ').toLocaleLowerCase().includes(query));
  $('#result-count').textContent = `共 ${items.length} 个模板` + (query ? ` · 搜索“${state.search.trim()}”` : '');
  $('#empty-state').hidden = items.length !== 0;
  $('#template-grid').replaceChildren(...items.map((item, index) => {
    const article = document.createElement('article');
    article.className = 'template-card';
    article.style.animationDelay = `${index * 50}ms`;
    const source = new URL(item.sourceUrl);
    article.innerHTML = `
      <a class="cover-link" href="${escape(item.previewUrl)}" target="_blank" rel="noopener" aria-label="打开 ${escape(item.name)} 本地预览">
        <img src="${escape(item.coverUrl)}" alt="${escape(item.name)} 网站预览封面" loading="eager">
        <span class="stack-badge">${escape(item.stack)}</span><span class="cover-open">${icon}</span>
      </a>
      <div class="card-header"><a class="card-title" href="${escape(item.previewUrl)}" target="_blank" rel="noopener">${escape(item.name)}</a><span class="page-count">${Number(item.pageCount)} 个页面</span></div>
      <p class="card-description">${escape(item.description)}</p>
      <div class="card-tags">${(item.tags || []).map((tag) => `<span class="tag">${escape(tag)}</span>`).join('')}</div>
      <div class="card-bottom"><a class="source-link" href="${escape(source.href)}" target="_blank" rel="noopener" aria-label="打开 ${escape(item.name)} 原站">${escape(source.hostname)} ${icon}</a><a class="learn-link" href="${escape(item.learnUrl)}" target="_blank" rel="noopener">学习指南 ↗</a></div>
      <div class="card-status"><i></i>${escape(item.status || '已收录 · 本地预览')}</div>`;
    return article;
  }));
}

async function load() {
  $('#error-state').hidden = true;
  try {
    const response = await fetch('/api/catalog', { cache: 'no-store' });
    if (!response.ok) throw new Error('无法读取本地模板清单，请确认模板中心服务仍在运行。');
    const data = await response.json();
    state.templates = data.templates;
    $('#total-count').textContent = String(state.templates.length).padStart(2, '0');
    $('#sidebar-count').textContent = state.templates.length;
    renderFilters();
    render();
  } catch (error) {
    $('#error-state').hidden = false;
    $('#error-message').textContent = error.message;
    $('#result-count').textContent = '模板读取失败';
  }
}

$('#search').addEventListener('input', (event) => { state.search = event.target.value; render(); });
$('#all-templates').addEventListener('click', reset);
$('#clear-search').addEventListener('click', reset);
$('#retry').addEventListener('click', load);
document.addEventListener('keydown', (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); $('#search').focus(); }
});
load();
