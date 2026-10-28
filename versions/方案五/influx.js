/* Business-only behavior. Framer/Motion still owns the reference animations. */
(() => {
  const legal = {
    terms:['服务条款','完整服务条款会在正式上线前公布。当前为页面预览，不构成正式协议。'],
    agreement:['用户协议','用户协议会在开放账号注册前公布。当前预览不会开通账号。'],
    privacy:['隐私政策','完整隐私政策会在上线前公布。当前预览的表单内容只保存在你的浏览器中。']
  };
  const routes={'/projects':'/#services','/about-us':'/#resources','/blog':'/pricing.html','/contact':'/#contact'};
  let scheduled=false;
  function normalize(){
    scheduled=false;
    for(const a of document.querySelectorAll('a[href]')){
      const u=new URL(a.getAttribute('href'),location.href);
      if(u.origin!==location.origin)continue;
      let href=routes[u.pathname.replace(/\/$/,'')]||null;
      if(u.hash.startsWith('#contact?plan='))href='/?'+u.hash.slice(9)+'#contact';
      if(href && a.getAttribute('href')!==href)a.setAttribute('href',href);
      if(u.hash==='#unavailable'){
        a.setAttribute('aria-disabled','true');a.tabIndex=-1;
        a.style.pointerEvents='none';a.style.opacity='.45';
      }
    }
    const ids={services:'[data-framer-name="Services"]',resources:'.framer-r66ymc',process:'[data-framer-name="Our process"]'};
    for(const [id,selector] of Object.entries(ids)){
      const el=document.querySelector(selector);if(el&&!el.id)el.id=id;
    }
    const enquiry=document.getElementById('enquiry-form');
    if(enquiry&&!enquiry.dataset.ready){
      enquiry.dataset.ready='true';
      let draft;try{draft=JSON.parse(sessionStorage.getItem('influx-v5-draft')||'null')}catch{}
      if(draft)for(const [key,value]of Object.entries(draft))if(enquiry.elements[key])enquiry.elements[key].value=value;
      const plan=new URLSearchParams(location.search).get('plan');
      if(plan&&!enquiry.elements.message.value)enquiry.elements.message.value=plan==='Free'?'我想了解 Free 体验。':'我想了解 Plus 方案。';
      enquiry.dataset.source=plan||'website';
    }
    if(!document.body.dataset.anchorDone && document.querySelector('main')){
      document.body.dataset.anchorDone='true';
      if(location.hash){const el=document.getElementById(location.hash.slice(1));if(el)requestAnimationFrame(()=>el.scrollIntoView());}
    }
  }
  function schedule(){if(!scheduled){scheduled=true;requestAnimationFrame(normalize)}}
  function dialog(title,text,src){
    document.querySelector('.influx-dialog')?.remove();
    const d=document.createElement('dialog');d.className='influx-dialog'+(src?' image-dialog':'');
    const close=document.createElement('button');close.className='dialog-close';close.type='button';close.ariaLabel='关闭';close.textContent='×';close.addEventListener('click',()=>d.close());
    d.append(close);
    if(src){const img=document.createElement('img');img.src=src;img.alt=title;d.append(img)}else{const h=document.createElement('h2');h.textContent=title;const p=document.createElement('p');p.textContent=text;d.append(h,p)}
    d.addEventListener('click',e=>{if(e.target===d){const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close()}});
    d.addEventListener('close',()=>d.remove());document.body.append(d);d.showModal();
  }
  document.addEventListener('click',event=>{
    const screenshot=event.target.closest('[data-screenshot]');
    if(screenshot){event.preventDefault();event.stopImmediatePropagation();dialog(screenshot.ariaLabel,'',screenshot.dataset.screenshot);return;}
    const policy=event.target.closest('[data-legal]');
    if(policy){event.preventDefault();dialog(...legal[policy.dataset.legal]);return;}
    const a=event.target.closest('a[href]');
    if(!a||event.button!==0||event.metaKey||event.ctrlKey||event.altKey||event.shiftKey)return;
    let u=new URL(a.getAttribute('href'),location.href);
    if(u.origin!==location.origin)return;
    if(routes[u.pathname.replace(/\/$/,'')])u=new URL(routes[u.pathname.replace(/\/$/,'')],location.origin);
    if(u.hash.startsWith('#contact?plan='))u=new URL('/?'+u.hash.slice(9)+'#contact',location.origin);
    if(u.hash==='#unavailable'){event.preventDefault();event.stopImmediatePropagation();return;}
    event.preventDefault();event.stopImmediatePropagation();
    if((u.pathname==='/'||u.pathname==='/index.html')&&document.body.dataset.page==='home'&&u.hash){
      const target=document.getElementById(u.hash.slice(1));
      if(target){history.replaceState(null,'',u.pathname+u.search+u.hash);target.scrollIntoView({behavior:'smooth'});return;}
    }
    location.assign(u.href);
  },true);
  document.addEventListener('input',event=>{
    if(event.target.closest('#calculator-form')){
      const output=document.getElementById('engagement-result');
      output.replaceChildren(document.createTextNode('—'));
      const unit=document.createElement('small');unit.textContent='%';output.append(unit);
      document.querySelector('#calculator-form .form-status').textContent='';
    }
    const form=event.target.closest('#enquiry-form');if(!form)return;
    try{sessionStorage.setItem('influx-v5-draft',JSON.stringify(Object.fromEntries(new FormData(form))))}catch{}
  });
  document.addEventListener('submit',event=>{
    const form=event.target;if(!(form instanceof HTMLFormElement))return;
    event.preventDefault();event.stopImmediatePropagation();
    if(!form.reportValidity())return;
    const status=form.querySelector('.form-status');status?.removeAttribute('data-error');
    if(form.id==='enquiry-form'){
      try{
        const record={...Object.fromEntries(new FormData(form)),source:form.dataset.source,createdAt:new Date().toISOString()};
        const saved=JSON.parse(localStorage.getItem('influx-v5-enquiries')||'[]');saved.push(record);localStorage.setItem('influx-v5-enquiries',JSON.stringify(saved));
        status.textContent='已保存在这个浏览器中，还没有发送给 Influx。';
      }catch{status.dataset.error='';status.textContent='浏览器暂时无法保存，请先复制你填写的内容，稍后再试。'}
    } else if(form.id==='calculator-form'){
      const f=Number(form.elements.followers.value),l=Number(form.elements.likes.value),c=Number(form.elements.comments.value);
      if(!Number.isSafeInteger(f)||f<=0||![l,c].every(v=>Number.isSafeInteger(v)&&v>=0)){
        status.dataset.error='';status.textContent='粉丝数须为大于 0 的整数，点赞数和评论数须为非负整数。';return;
      }
      const result=(l+c)/f*100;
      const output=document.getElementById('engagement-result');output.replaceChildren(document.createTextNode(result.toFixed(2)));const unit=document.createElement('small');unit.textContent='%';output.append(unit);
      status.textContent='计算完成。';
    }
  },true);
  document.addEventListener('DOMContentLoaded',()=>{
    normalize();new MutationObserver(schedule).observe(document.getElementById('main'),{childList:true,subtree:true});
  });
})();
