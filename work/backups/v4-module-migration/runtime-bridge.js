/* The original Webflow / GSAP / Lenis runtime owns Reels motion. Only refresh after font loading. */
(() => {
  const refresh=()=>window.ScrollTrigger?.refresh();
  document.fonts.ready.then(refresh);
  addEventListener('load',()=>{
    refresh();
    const id=decodeURIComponent(location.hash.slice(1));
    const target=id&&document.getElementById(id);
    if(target){
      if(window.influxLenis)window.influxLenis.scrollTo(target,{immediate:true,offset:-100});
      else target.scrollIntoView({block:'start'});
    }else if(!location.hash){
      if(window.influxLenis)window.influxLenis.scrollTo(0,{immediate:true});else window.scrollTo(0,0);
    }
  },{once:true});
  if(matchMedia('(prefers-reduced-motion: reduce)').matches){
    document.querySelectorAll('video').forEach(video=>{video.autoplay=false;video.pause();});
  }
  // Align controls with the visible card, which can be shorter than Webflow's mask.
  const slider=document.querySelector('.case-study-slider');
  if(slider){
    const alignControls=()=>{
      const card=slider.querySelector('.w-slide:not([aria-hidden="true"]) .grid-case-card');
      if(!card)return;
      const box=card.getBoundingClientRect(),base=slider.getBoundingClientRect();
      slider.style.setProperty('--capability-control-y',`${box.top-base.top+box.height/2}px`);
    };
    const resize=new ResizeObserver(alignControls);
    resize.observe(slider);
    slider.querySelectorAll('.grid-case-card').forEach(card=>resize.observe(card));
    new MutationObserver(alignControls).observe(slider,{subtree:true,attributes:true,attributeFilter:['aria-hidden']});
    document.fonts.ready.then(alignControls);
    alignControls();
  }
  // Pause hidden-tab playback without replacing Webflow's individual video controls.
  let playing=[];
  document.addEventListener('visibilitychange',()=>{
    if(document.hidden){playing=[...document.querySelectorAll('video')].filter(video=>!video.paused);playing.forEach(video=>video.pause());}
    else{playing.forEach(video=>video.play().catch(()=>{}));playing=[];}
  });
})();
