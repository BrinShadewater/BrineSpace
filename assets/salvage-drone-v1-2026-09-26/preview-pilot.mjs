const canvas=document.querySelector('#stage'),ctx=canvas.getContext('2d'),readout=document.querySelector('#readout');
const cache=new Map();let data,state='idle',time=0,clock=0,last=0,paused=false,rate=1,cycle=null,water=0,deposit=null;
const image=path=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=()=>reject(Error(path));im.src=path;});
function select(next){state=next;time=0;for(const b of document.querySelectorAll('[data-state]'))b.setAttribute('aria-pressed',String(b.dataset.state===state));}
for(const b of document.querySelectorAll('[data-state]'))b.onclick=()=>{cycle=null;deposit=null;select(b.dataset.state);};
document.querySelector('#cycle').onclick=()=>{cycle=0;deposit=null;water=0;select('retrieve');};
document.querySelector('#replay').onclick=()=>{time=0;deposit=null;water=0;if(cycle!==null){cycle=0;select('retrieve');}};
document.querySelector('#pause').onclick=e=>{paused=!paused;e.target.textContent=paused?'Resume':'Pause';};
document.querySelector('#speed').onchange=e=>rate=+e.target.value;
new ResizeObserver(()=>{const width=Math.round(canvas.clientWidth);if(canvas.width!==width)canvas.width=width;if(canvas.height!==550)canvas.height=550;}).observe(canvas);
function frame(im,entry,n,x,y,scale){const s=data.frameWidth;ctx.drawImage(im,n%6*s,Math.floor(n/6)*s,s,s,x-s*scale/2,y-s*scale/2,s*scale,s*scale);}
function tick(now){requestAnimationFrame(tick);const dt=paused?0:Math.min(.05,(now-(last||now))/1000)*rate;last=now;if(!data)return;time+=dt;clock+=dt;
 if(cycle===0&&time>=4){cycle=1;select('carry');}else if(cycle===1&&time>=3){cycle=2;select('release');}else if(cycle===2&&time>=4){deposit={water};cycle=3;select('idle');}
 if(['swim','carry'].includes(state))water+=dt*24;
 const e=data.states.find(e=>e.state===state),assets=cache.get(state);const n=e.loop?Math.floor(time*30)%e.frameCount:Math.min(e.frameCount-1,Math.floor(time*30));
 ctx.fillStyle='#17272e';ctx.fillRect(0,0,canvas.width,550);ctx.strokeStyle='#21353d';ctx.lineWidth=1;
 for(let y=(water%40)-40;y<550;y+=40){ctx.beginPath();ctx.moveTo(0,y);ctx.bezierCurveTo(canvas.width*.3,y-4,canvas.width*.7,y+4,canvas.width,y);ctx.stroke();}
 ctx.fillStyle='#8faab4';ctx.font='11px system-ui';ctx.fillText('SWIMMING / ENLARGED',14,22);
 const scale=Math.min(1,(canvas.width-40)/512),x=canvas.width/2,y=240+1.5*Math.sin(clock*Math.PI*2/3);
 if(deposit){const release=data.states.find(e=>e.state==='release');frame(cache.get('release').cargo,release,119,x,240+water-deposit.water,scale);}
 function draw(vx,vy,vs){frame(assets.cargo,e,n,vx,vy,vs);frame(assets.body,e,n,vx,vy,vs);const p=data.headings.south.lamp;
 ctx.save();ctx.globalAlpha=.35+.65*(.5+.5*Math.cos(clock/.85*Math.PI*2));ctx.fillStyle=data.lamp.colors[document.querySelector('#light').value];ctx.beginPath();ctx.arc(vx+(p[0]-256)*vs,vy+(p[1]-256)*vs,2.4*vs,0,Math.PI*2);ctx.fill();ctx.restore();}
 draw(x,y,scale);ctx.fillStyle='#17272eee';ctx.fillRect(canvas.width-182,360,182,190);ctx.fillStyle='#8faab4';ctx.fillText('0.34× SCALE',canvas.width-148,380);draw(canvas.width-88,450,.34);
 readout.textContent=`${paused?'Paused':'Playing'} · ${state}-south · ${e.phases[n]} · frame ${n+1}/${e.frameCount}${cycle===3?' · Recovery complete':cycle!==null?' · Recovery cycle':''}`;
}
fetch('manifest.json').then(r=>r.json()).then(async d=>{await Promise.all(d.states.map(async e=>cache.set(e.state,{body:await image(e.atlas.path),cargo:await image(e.cargoAtlas.path)})));data=d;select('idle');requestAnimationFrame(tick);}).catch(e=>readout.textContent='Unable to load '+e.message);
