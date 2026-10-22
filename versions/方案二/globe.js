// Rotating dotted globe: land dots, creators that pop in/out with rotation, and meteor arcs between them.
(()=>{
 const world=document.querySelector('.creator-world');
 const canvas=world&&world.querySelector('.globe-canvas');
 const layer=world&&world.querySelector('.globe-avatars');
 const raw=window.GLOBE_LAND_DOTS;
 if(!canvas||!layer||!raw)return;
 const ctx=canvas.getContext('2d');
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const DEG=Math.PI/180;
 const TILT=-28*DEG,SPEED=.065,DOT_RGB='138,157,171',DOT_ALPHA=.62,STRETCH=1.4;
 const LIGHTS=[{el:document.querySelector('.brand-orb-purple'),rgb:'106,55,255'},{el:document.querySelector('.brand-orb-blue'),rgb:'65,114,255'}];

 const dots=new Float32Array(raw.length/2*3);
 for(let i=0,j=0;i<raw.length;i+=2,j+=3){const lat=raw[i]/10*DEG,lon=raw[i+1]/10*DEG;dots[j]=Math.cos(lat)*Math.sin(lon);dots[j+1]=Math.sin(lat);dots[j+2]=Math.cos(lat)*Math.cos(lon);}

 const portraits=['assets/portrait-1.jpg','assets/portrait-2.jpg','assets/portrait-3.jpg','assets/portrait-4.jpg'];
 const cities=[[40.7,-74],[34,-118.2],[43.7,-79.4],[19.4,-99.1],[25.8,-80.2],[47.6,-122.3],[41.9,-87.6],[51.5,-.1],[48.9,2.3],[52.5,13.4],[40.4,-3.7],[41,29],[30,31.2],[25.2,55.3],[19.1,72.9],[28.6,77.2],[13.8,100.5],[31.2,121.5],[35.7,139.7],[37.6,127],[14.6,121],[6.5,3.4],[55.8,37.6],[24.7,46.7],[1.35,103.8],[22.3,114.2],[-1.3,36.8],[59.3,18.1],[45.5,9.2],[39.9,116.4],[49.3,-123.1],[21.3,-157.9],[4.7,-74.1],[29.8,-95.4],[39.7,-105],[45.5,-73.6],[61.2,-149.9],[33.7,-84.4],[37.8,-122.4],[53.3,-6.3],[50.1,14.4],[38,23.7],[32.1,34.8],[41.3,69.2],[23.8,90.4],[21,105.8],[43.1,141.3],[34.7,135.5],[3.1,101.7],[55,82.9],[43.2,76.9],[9,38.7],[14.7,-17.5],[33.6,-7.6],[64.1,-21.9],[47.9,106.9],[13.4,144.8],[25,121.5]];
 const creators=cities.map(([lat,lon],i)=>{
  const el=document.createElement('span');el.className='globe-avatar';
  const face=document.createElement('span');
  const img=document.createElement('img');img.src=portraits[i%portraits.length];img.alt='';img.width=80;img.height=80;img.decoding='async';
  face.appendChild(img);el.appendChild(face);layer.appendChild(el);
  const a=lat*DEG,b=lon*DEG;
  return {el,v:[Math.cos(a)*Math.sin(b),Math.sin(a),Math.cos(a)*Math.cos(b)],size:.82+((i*37)%19)/19*.36,shown:false,x:0,y:0,z:0};
 });

 let W=0,H=0,R=0,cx=0,cy=0,dpr=1,phi=-.35,last=0,frame=0,running=false,inView=true,meteorClock=0;
 const meteors=[];
 const cosT=Math.cos(TILT),sinT=Math.sin(TILT);

 function project(x,y,z,out){
  const c=Math.cos(phi),s=Math.sin(phi);
  const rx=x*c+z*s,rz=-x*s+z*c;
  const ry=y*cosT-rz*sinT,rz2=y*sinT+rz*cosT;
  out.x=cx+rx*R*STRETCH;out.y=cy-ry*R;out.z=rz2;return out;
 }
 function resize(){
  W=world.clientWidth;H=world.clientHeight;dpr=Math.min(devicePixelRatio||1,2);
  canvas.width=Math.round(W*dpr);canvas.height=Math.round(H*dpr);
  R=W*.5;cx=W/2;cy=Math.min(36,H*.08)+R;
  world.style.setProperty('--avatar',Math.max(22,Math.min(40,W/1160*40)).toFixed(1)+'px');
 }
 const smooth=(a,b,v)=>{const t=Math.max(0,Math.min(1,(v-a)/(b-a)));return t*t*(3-2*t);};
 const p={x:0,y:0,z:0};

 function drawDots(){
  const buckets=[[],[],[],[],[]];
  const dotR=Math.max(.9,W/1160*1.4);
  for(let j=0;j<dots.length;j+=3){
   project(dots[j],dots[j+1],dots[j+2],p);
   if(p.z<=.02||p.y>H+4||p.y<-4||p.x<-4||p.x>W+4)continue;
   const edge=smooth(0,W*.16,p.x)*smooth(W,W*.84,p.x);
   const k=Math.floor(smooth(0,.55,p.z)*edge*5);
   if(k<0)continue;
   if(k>4){buckets[4].push(p.x,p.y);continue;}
   buckets[k].push(p.x,p.y);
  }
  buckets.forEach((list,k)=>{
   if(!list.length)return;
   ctx.fillStyle=`rgba(${DOT_RGB},${(DOT_ALPHA*(.22+.78*(k+1)/5)).toFixed(3)})`;
   const r=dotR*(.7+.3*(k+1)/5);
   ctx.beginPath();
   for(let i=0;i<list.length;i+=2){ctx.moveTo(list[i]+r,list[i+1]);ctx.arc(list[i],list[i+1],r,0,Math.PI*2);}
   ctx.fill();
  });
 }
 function tintDots(){
  const box=canvas.getBoundingClientRect();
  ctx.globalCompositeOperation='source-atop';
  LIGHTS.forEach(({el,rgb})=>{
   if(!el)return;
   const alpha=Math.min(1,(parseFloat(el.style.opacity)||0)/.82);
   if(alpha<.01)return;
   const r=el.getBoundingClientRect(),x=r.left+r.width/2-box.left,y=r.top+r.height/2-box.top,rad=el.offsetWidth*.62;
   if(x<-rad||x>W+rad||y<-rad||y>H+rad)return;
   const g=ctx.createRadialGradient(x,y,0,x,y,rad);
   g.addColorStop(0,`rgba(${rgb},${(.85*alpha).toFixed(3)})`);g.addColorStop(.5,`rgba(${rgb},${(.42*alpha).toFixed(3)})`);g.addColorStop(1,`rgba(${rgb},0)`);
   ctx.fillStyle=g;ctx.fillRect(x-rad,y-rad,rad*2,rad*2);
  });
  ctx.globalCompositeOperation='source-over';
 }
 function updateCreators(){
  const scale=parseFloat(getComputedStyle(world).getPropertyValue('--avatar'))||36;
  creators.forEach(c=>{
   project(c.v[0],c.v[1],c.v[2],c);
   const visible=c.z>.2&&c.y>H*.16&&c.y<H*.84&&c.x>W*.12&&c.x<W*.88;
   if(visible!==c.shown){c.shown=visible;c.el.classList.toggle('is-visible',visible);}
   const depth=.72+.28*smooth(.28,.85,c.z);
   c.el.style.transform=`translate3d(${c.x.toFixed(1)}px,${c.y.toFixed(1)}px,0) scale(${(depth*c.size*scale/36).toFixed(3)})`;
   c.el.style.zIndex=Math.round(c.z*100);
  });
 }

 function slerp(a,b,t){
  const d=Math.max(-1,Math.min(1,a[0]*b[0]+a[1]*b[1]+a[2]*b[2])),w=Math.acos(d),s=Math.sin(w)||1;
  const ka=Math.sin((1-t)*w)/s,kb=Math.sin(t*w)/s;
  return [a[0]*ka+b[0]*kb,a[1]*ka+b[1]*kb,a[2]*ka+b[2]*kb,w];
 }
 function spawnMeteor(){
  const live=creators.filter(c=>c.shown);
  if(live.length<2)return;
  for(let tries=0;tries<8;tries++){
   const a=live[Math.random()*live.length|0],b=live[Math.random()*live.length|0];
   const dist=Math.hypot(a.x-b.x,a.y-b.y);
   if(a===b||dist<W*.1||dist>W*.55)continue;
   if(meteors.some(m=>(m.a===a&&m.b===b)||(m.a===b&&m.b===a)))continue;
   meteors.push({a,b,age:0,dur:1.5+dist/W*1.4});return;
  }
 }
 function arcPoints(m,count){
  const pts=[];
  const w=Math.acos(Math.max(-1,Math.min(1,m.a.v[0]*m.b.v[0]+m.a.v[1]*m.b.v[1]+m.a.v[2]*m.b.v[2])));
  for(let i=0;i<=count;i++){
   const t=i/count,v=slerp(m.a.v,m.b.v,t),lift=1+Math.sin(Math.PI*t)*w*.28;
   const q=project(v[0]*lift,v[1]*lift,v[2]*lift,{x:0,y:0,z:0});pts.push(q);
  }
  return pts;
 }
 function drawMeteors(dt){
  for(let i=meteors.length-1;i>=0;i--){
   const m=meteors[i];m.age+=dt;
   const life=m.age/m.dur,fadeOut=1-smooth(1,1.45,life);
   if(life>1.45){meteors.splice(i,1);continue;}
   const N=48,pts=arcPoints(m,N);
   ctx.lineCap='round';
   ctx.beginPath();pts.forEach((q,k)=>k?ctx.lineTo(q.x,q.y):ctx.moveTo(q.x,q.y));
   ctx.strokeStyle=`rgba(142,131,232,${(.22*smooth(0,.25,life)*fadeOut).toFixed(3)})`;ctx.lineWidth=1;ctx.stroke();
   const head=Math.min(1,life),tail=Math.max(0,head-.38);
   if(life<1.15){
    const h=Math.round(head*N),t0=Math.round(tail*N);
    if(h>t0){
     const g=ctx.createLinearGradient(pts[t0].x,pts[t0].y,pts[h].x,pts[h].y);
     g.addColorStop(0,'rgba(106,55,255,0)');g.addColorStop(.7,'rgba(106,55,255,.55)');g.addColorStop(1,'rgba(65,114,255,.95)');
     ctx.beginPath();for(let k=t0;k<=h;k++)k===t0?ctx.moveTo(pts[k].x,pts[k].y):ctx.lineTo(pts[k].x,pts[k].y);
     ctx.strokeStyle=g;ctx.lineWidth=1.8;ctx.globalAlpha=1-smooth(1,1.15,life);ctx.stroke();
     const hp=pts[h],glow=ctx.createRadialGradient(hp.x,hp.y,0,hp.x,hp.y,7);
     glow.addColorStop(0,'rgba(255,255,255,.95)');glow.addColorStop(.35,'rgba(65,114,255,.6)');glow.addColorStop(1,'rgba(65,114,255,0)');
     ctx.fillStyle=glow;ctx.fillRect(hp.x-7,hp.y-7,14,14);ctx.globalAlpha=1;
    }
   }
   if(life>=1){
    const k=smooth(1,1.45,life),end=pts[N];
    ctx.beginPath();ctx.arc(end.x,end.y,6+k*18,0,Math.PI*2);
    ctx.strokeStyle=`rgba(65,114,255,${(.5*(1-k)).toFixed(3)})`;ctx.lineWidth=1.2;ctx.stroke();
   }
  }
 }

 function sphereGradient(stops){
  const g=ctx.createRadialGradient(-R*.18,-R*.32,0,0,0,R);
  stops.forEach(([o,c])=>g.addColorStop(o,c));return g;
 }
 function drawSphere(){
  ctx.save();
  ctx.globalCompositeOperation='destination-over';
  ctx.translate(cx,cy);ctx.scale(STRETCH,1);
  ctx.beginPath();ctx.arc(0,0,R,0,Math.PI*2);
  ctx.lineWidth=1.2/STRETCH;ctx.strokeStyle='rgba(150,166,194,.14)';ctx.stroke();
  ctx.fillStyle=sphereGradient([[0,'rgba(130,150,185,0)'],[.9,'rgba(130,150,185,0)'],[1,'rgba(130,150,185,.035)']]);
  ctx.fill();
  ctx.shadowColor='rgba(91,107,138,.07)';ctx.shadowBlur=Math.max(24,W*.035);ctx.shadowOffsetY=-2;
  ctx.fillStyle=sphereGradient([[0,'#ffffff'],[.7,'#ffffff'],[1,'#fcfdfe']]);
  ctx.fill();
  ctx.restore();
 }
 function fadeEdges(){
  ctx.save();ctx.globalCompositeOperation='destination-in';
  const h=ctx.createLinearGradient(0,0,W,0);
  h.addColorStop(0,'rgba(0,0,0,0)');h.addColorStop(.14,'#000');h.addColorStop(.86,'#000');h.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=h;ctx.fillRect(0,0,W,H);
  const v=ctx.createLinearGradient(0,0,0,H);
  v.addColorStop(0,'#000');v.addColorStop(.72,'#000');v.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=v;ctx.fillRect(0,0,W,H);
  ctx.restore();
 }
 function render(dt){
  ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,W,H);
  drawDots();tintDots();drawSphere();updateCreators();
  if(!reduced.matches){
   meteorClock-=dt;
   if(meteorClock<=0){spawnMeteor();meteorClock=.55+Math.random()*.7;}
   drawMeteors(dt);
  }
  fadeEdges();
 }
 function tick(now){
  frame=0;
  const dt=last?Math.min(.05,(now-last)/1000):0;last=now;
  phi+=dt*SPEED;render(dt);
  if(running)frame=requestAnimationFrame(tick);
 }
 function sync(){
  const should=inView&&!document.hidden&&!reduced.matches;
  if(should&&!running){running=true;last=0;frame=requestAnimationFrame(tick);}
  else if(!should&&running){running=false;cancelAnimationFrame(frame);}
  if(!should)render(0);
 }
 resize();render(0);
 new ResizeObserver(()=>{resize();if(!running)render(0);}).observe(world);
 new IntersectionObserver(e=>{inView=e[0].isIntersecting;sync();}).observe(world);
 document.addEventListener('visibilitychange',sync);
 reduced.addEventListener('change',sync);
 sync();
})();
