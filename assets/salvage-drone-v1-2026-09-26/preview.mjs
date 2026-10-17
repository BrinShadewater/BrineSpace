import {SalvageMotion} from './motion.mjs';
const canvas=document.querySelector('#stage'),ctx=canvas.getContext('2d'),readout=document.querySelector('#readout'),headingEl=document.querySelector('#heading');
const motion=new SalvageMotion(),cache=new Map(),parts=new Map();let data,clock=0,last=0,paused=false,rate=1,cycle=null,water={x:0,y:0},deposit=null,depositSerial=0,lastRelease=null;
const q=Math.SQRT1_2,dirs={north:[0,-1],northeast:[q,-q],east:[1,0],southeast:[q,q],south:[0,1],southwest:[-q,q],west:[-1,0],northwest:[-q,-q]};
const image=path=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=()=>reject(Error(path));im.src=path;});
function clip(state){const id=state+'-'+motion.heading;if(!cache.has(id)){const e=data.states.find(e=>e.id===id);if(!e)throw Error('Missing '+id);const a={entry:e,ready:false};cache.set(id,a);Promise.all([image(e.atlas.path),image(e.cargoAtlas.path)]).then(([body,cargo])=>Object.assign(a,{body,cargo,ready:true})).catch(error=>a.error=error.message);if(cache.size>6)cache.delete(cache.keys().next().value);}return cache.get(id);}
function controls(){headingEl.value=motion.heading;const work=['retrieve','release','blocked'].includes(motion.state);for(const option of headingEl.options)option.disabled=work&&!['north','east','south','west'].includes(option.value);for(const b of document.querySelectorAll('[data-state]'))b.setAttribute('aria-pressed',String(b.dataset.state===(motion.pending?.state||motion.state)));}
function choose(state,heading=motion.heading,fromCycle=false){if(!fromCycle)cycle=null;if(state==='retrieve')deposit=null;motion.command(state,heading);controls();}
for(const b of document.querySelectorAll('[data-state]'))b.onclick=()=>choose(b.dataset.state);
headingEl.onchange=()=>choose(motion.state,headingEl.value);
function startCycle(){motion.state='idle';motion.replay();motion.loaded=false;cycle={step:0,started:clock};deposit=null;water={x:0,y:0};choose('retrieve',motion.heading,true);}
document.querySelector('#cycle').onclick=startCycle;document.querySelector('#replay').onclick=()=>{if(cycle)startCycle();else{motion.replay();deposit=null;water={x:0,y:0};}};
document.querySelector('#pause').onclick=e=>{paused=!paused;e.target.textContent=paused?'Resume':'Pause';};document.querySelector('#speed').onchange=e=>rate=+e.target.value;
new ResizeObserver(()=>{const width=Math.round(canvas.clientWidth);if(canvas.width!==width)canvas.width=width;if(canvas.height!==550)canvas.height=550;}).observe(canvas);
function frame(im,n,x,y,scale){const s=data.frameWidth;ctx.drawImage(im,n%6*s,Math.floor(n/6)*s,s,s,x-s*scale/2,y-s*scale/2,s*scale,s*scale);}
function tick(now){requestAnimationFrame(tick);const dt=paused?0:Math.min(.05,(now-(last||now))/1000)*rate;last=now;if(!data)return;let active=clip(motion.sample().state);if(!active.ready){readout.textContent=active.error||'Loading '+motion.state+' '+motion.heading;return;}
 clock+=dt;const movement=motion.update(dt);
 if(cycle){if(cycle.step===0&&motion.completed){cycle.step=1;cycle.started=clock;choose('carry',motion.heading,true);}else if(cycle.step===1&&clock-cycle.started>=3){cycle.step=2;choose('release',motion.heading,true);}else if(cycle.step===2&&motion.completed){cycle.step=3;choose('idle',motion.heading,true);}}
 const sample=motion.sample();active=clip(sample.state);if(!active.ready){readout.textContent='Loading '+sample.state;return;}const e=active.entry,n=sample.frame;controls();
 const u=dirs[motion.heading],scale=Math.min(1,(canvas.width-40)/512);water.x-=u[0]*movement.distance/.34*scale;water.y-=u[1]*movement.distance/.34*scale;
 if(e.state==='release')lastRelease={image:active.cargo,water:{...water}};
 if(depositSerial!==motion.deposited){depositSerial=motion.deposited;deposit=lastRelease;}
 ctx.fillStyle='#17272e';ctx.fillRect(0,0,canvas.width,550);ctx.strokeStyle='#21353d';ctx.lineWidth=1;
 for(let y=(water.y%40)-40;y<550;y+=40){ctx.beginPath();ctx.moveTo(0,y);ctx.bezierCurveTo(canvas.width*.3,y-4,canvas.width*.7,y+4,canvas.width,y);ctx.stroke();}
 for(let x=(water.x%100)-100;x<canvas.width;x+=100){ctx.fillStyle='#25404a';ctx.fillRect(x,70,2,2);ctx.fillRect(x+38,315,2,2);}
 ctx.fillStyle='#8faab4';ctx.font='11px system-ui';ctx.fillText('SWIMMING / ENLARGED',14,22);const x=canvas.width/2,y=240+1.5*Math.sin(clock*Math.PI*2/3);
 if(deposit)frame(deposit.image,119,x+water.x-deposit.water.x,240+water.y-deposit.water.y,scale);
 function draw(vx,vy,vs){const p=parts.get(motion.heading);const work=['retrieve','release','blocked'].includes(e.state);if(work&&!(e.state==='release'&&motion.completed))frame(active.cargo,n,vx,vy,vs);else if(motion.loaded)ctx.drawImage(p.cargo,vx-256*vs,vy-256*vs,512*vs,512*vs);
  if(motion.loaded&&!work)ctx.drawImage(p.closed,vx-256*vs,vy-256*vs,512*vs,512*vs);else frame(active.body,n,vx,vy,vs);
  frame(p.rotors,sample.rotorFrame,vx,vy,vs);const lamp=data.headings[motion.heading].lamp,selected=document.querySelector('#light').value;
  ctx.save();ctx.globalAlpha=['power-on','power-off'].includes(e.state)?e.lampSamples[n]:.35+.65*(.5+.5*Math.cos(clock/.85*Math.PI*2));ctx.fillStyle=data.lamp.colors[selected==='automatic'?e.lampColor:selected];ctx.beginPath();ctx.arc(vx+(lamp[0]-256)*vs,vy+(lamp[1]-256)*vs,2.4*vs,0,Math.PI*2);ctx.fill();ctx.restore();}
 draw(x,y,scale);ctx.fillStyle='#17272eee';ctx.fillRect(canvas.width-182,360,182,190);ctx.fillStyle='#8faab4';ctx.fillText('0.34× SCALE',canvas.width-148,380);draw(canvas.width-88,450,.34);
 readout.textContent=`${paused?'Paused':'Playing'} · ${motion.state}-${motion.heading} · ${movement.status} / ${e.phases[n]} · frame ${n+1}/${e.frameCount}${motion.pending?' · Finishing action':''}${cycle?.step===3?' · Recovery complete':cycle?' · Recovery cycle':''}`;
}
fetch('manifest.json').then(r=>r.json()).then(async d=>{await Promise.all(Object.entries(d.headings).map(async ([h,m])=>{const [rotors,closed,cargo]=await Promise.all([image(m.rotorAtlas.path),image(m.closedPose),image(m.cargoPose)]);parts.set(h,{rotors,closed,cargo});}));data=d;controls();requestAnimationFrame(tick);}).catch(e=>readout.textContent='Unable to load '+e.message);
