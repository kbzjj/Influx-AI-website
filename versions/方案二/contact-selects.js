// Presentation enhancement: original selects retain their values, names and change events.
(() => {
  const controls = [];
  document.querySelectorAll('#contact select').forEach(select => {
    const wrapper = document.createElement('div');
    wrapper.className = 'contact-select';
    select.before(wrapper);
    wrapper.append(select);

    const trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.id = `${select.id}-trigger`;
    trigger.className = 'contact-select-trigger';
    trigger.setAttribute('role', 'combobox');
    trigger.setAttribute('aria-haspopup', 'listbox');
    trigger.setAttribute('aria-expanded', 'false');
    trigger.setAttribute('aria-controls', `${select.id}-options`);
    const label = document.querySelector(`label[for="${select.id}"]`);
    if (label) {
      label.id ||= `${select.id}-label`;
      label.htmlFor = trigger.id;
      trigger.setAttribute('aria-labelledby', label.id);
    }
    const value = document.createElement('span');
    value.className = 'contact-select-value';
    trigger.append(value);
    const svgNS = 'http://www.w3.org/2000/svg';
    const chevron = document.createElementNS(svgNS, 'svg');
    chevron.setAttribute('viewBox', '0 0 16 16');
    chevron.setAttribute('aria-hidden', 'true');
    chevron.classList.add('contact-select-chevron');
    const path = document.createElementNS(svgNS, 'path');
    path.setAttribute('d', 'm4 6 4 4 4-4');
    path.setAttribute('fill', 'none');
    path.setAttribute('stroke', 'currentColor');
    path.setAttribute('stroke-width', '1.5');
    path.setAttribute('stroke-linecap', 'round');
    path.setAttribute('stroke-linejoin', 'round');
    chevron.append(path);
    trigger.append(chevron);

    const list = document.createElement('ul');
    list.id = `${select.id}-options`;
    list.className = 'contact-select-menu';
    list.setAttribute('role', 'listbox');
    if (label) list.setAttribute('aria-labelledby', label.id);
    list.hidden = true;
    wrapper.append(trigger, list);

    let active = select.selectedIndex;
    let search = '';
    let searchTimer;
    const isDisabled = option => option.disabled || option.parentElement.disabled;
    const setActive = index => {
      active = index;
      [...list.children].forEach((item, i) => item.classList.toggle('is-active', i === active));
      if (!list.hidden && list.children[active]) trigger.setAttribute('aria-activedescendant', list.children[active].id);
    };
    const close = () => {
      list.hidden = true;
      wrapper.classList.remove('is-open');
      trigger.setAttribute('aria-expanded', 'false');
      trigger.removeAttribute('aria-activedescendant');
      search = '';
      clearTimeout(searchTimer);
    };
    const open = () => {
      if (select.matches(':disabled')) return;
      controls.forEach(control => control.close());
      list.hidden = false;
      wrapper.classList.add('is-open');
      trigger.setAttribute('aria-expanded', 'true');
      setActive(select.selectedIndex);
    };
    const choose = index => {
      if (!select.options[index] || isDisabled(select.options[index])) return;
      const changed = select.selectedIndex !== index;
      select.selectedIndex = index;
      if (changed) {
        select.dispatchEvent(new Event('input', { bubbles: true }));
        select.dispatchEvent(new Event('change', { bubbles: true }));
      }
      sync();
      close();
      trigger.focus({ preventScroll: true });
    };
    const sync = () => {
      value.textContent = select.selectedOptions[0]?.textContent || '';
      trigger.disabled = select.matches(':disabled');
      list.replaceChildren();
      [...select.options].forEach((option, index) => {
        const item = document.createElement('li');
        item.id = `${select.id}-option-${index}`;
        item.className = 'contact-select-option';
        item.setAttribute('role', 'option');
        item.setAttribute('aria-selected', String(option.selected));
        item.setAttribute('aria-disabled', String(isDisabled(option)));
        item.textContent = option.textContent;
        item.addEventListener('pointerdown', event => event.preventDefault());
        item.addEventListener('pointermove', () => { if (!isDisabled(option)) setActive(index); });
        item.addEventListener('click', () => choose(index));
        list.append(item);
      });
      setActive(select.selectedIndex);
    };
    const step = direction => {
      const options = [...select.options];
      for (let count = 0, next = active; count < options.length; count++) {
        next = (next + direction + options.length) % options.length;
        if (!isDisabled(options[next])) { setActive(next); return; }
      }
    };
    trigger.addEventListener('click', () => list.hidden ? open() : close());
    trigger.addEventListener('keydown', event => {
      if (event.key === 'Tab') { close(); return; }
      if (event.key === 'Escape') {
        if (!list.hidden) { event.preventDefault(); event.stopPropagation(); close(); }
        return;
      }
      if (['Enter', ' '].includes(event.key) && !search) {
        event.preventDefault();
        if (list.hidden) open(); else choose(active);
        return;
      }
      if (['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) {
        event.preventDefault();
        const wasClosed = list.hidden;
        if (wasClosed) open();
        if (event.key === 'Home') setActive([...select.options].findIndex(option => !isDisabled(option)));
        else if (event.key === 'End') setActive([...select.options].map((option, i) => isDisabled(option) ? -1 : i).filter(i => i >= 0).pop() ?? 0);
        else if (!wasClosed) step(event.key === 'ArrowDown' ? 1 : -1);
        return;
      }
      if (event.key.length === 1 && !event.ctrlKey && !event.metaKey && !event.altKey) {
        event.preventDefault();
        if (list.hidden) open();
        search += event.key.toLocaleLowerCase();
        clearTimeout(searchTimer);
        searchTimer = setTimeout(() => { search = ''; }, 600);
        const match = [...select.options].findIndex(option => !isDisabled(option) && option.textContent.trim().toLocaleLowerCase().startsWith(search));
        if (match >= 0) setActive(match);
      }
    });
    document.addEventListener('pointerdown', event => { if (!wrapper.contains(event.target)) close(); });
    document.addEventListener('focusin', event => { if (!wrapper.contains(event.target)) close(); });
    select.addEventListener('change', sync);
    const fieldset = select.closest('fieldset');
    if (fieldset) new MutationObserver(sync).observe(fieldset, { attributes: true, attributeFilter: ['disabled', 'hidden'] });
    select.form?.addEventListener('reset', () => { close(); queueMicrotask(sync); });
    new MutationObserver(sync).observe(select, { subtree: true, childList: true, characterData: true, attributes: true });
    // Hide only after the enhancement is ready; FormData still reads the original select.
    sync();
    select.hidden = true;
    controls.push({ close });
  });
})();
