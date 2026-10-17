import {sample,duration,angles} from './mission.mjs';
const $=id=>document.getElementById(id),canvas=$('stage'),ctx=canvas.getContext('2d');let manifest,art={},time=0,last=0,paused=false,rate=1;
const image=src=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=()=>reject(Error(src));im.src=src});
function resize(){canvas.width=Math.round(canvas.clientWidth);canvas.height=600;}new ResizeObserver(resize).observe(canvas);
function sprite(im,x,y,s){ctx.drawImage(im,x-im.width*s/2,y-im.height*s/2,im.width*s,im.height*s)}
function effect(kind,h,t,x,y,s){const n=Math.floor(t*30)%60,im=art[kind+'-'+h];if(im)ctx.drawImage(im,n%6*512,Math.floor(n/6)*512,512,512,x-256*s,y-256*s,512*s,512*s)}
function topography(h,progress,x,y,s,alpha=1){const n=Math.min(59,Math.max(0,Math.floor(progress*59))),im=art['scan-'+h];ctx.save();ctx.globalAlpha=alpha;ctx.drawImage(im,n%6*512,Math.floor(n/6)*512,512,512,x-256*s,y-256*s,512*s,512*s);ctx.restore();}
function probe(state,h,t,x,y,s){if(['cruise','launch','return','brake'].includes(state))effect('wake',h,t,x,y,s);sprite(art[h],x,y,s);
 const a=angles[h],offset=9,lum=.4+.6*(.5+.5*Math.cos(t*Math.PI*2));ctx.save();ctx.globalAlpha=lum;ctx.fillStyle=state==='recharge'?'#e6bd60':'#6ab8df';ctx.beginPath();ctx.arc(x+Math.cos(a)*offset*s,y+Math.sin(a)*offset*s,2.3*s,0,Math.PI*2);ctx.fill();ctx.restore();}
function mission(){const bay=$('bay').value,p=sample(time,bay),a=angles[bay],u=[Math.cos(a),Math.sin(a)],v=[-u[1],u[0]],vertical=Math.abs(u[1])>.5;
 const [near,far]={east:[70,91],west:[65,85],north:[44,62],south:[35,55]}[bay];
 const fit=Math.min(1.3,(canvas.width-40)/(vertical?320:600),500/(vertical?600:320));
 function P(x,y){return [canvas.width/2+((x-190)*u[0]+(y-50)*v[0])*fit,300+((x-190)*u[1]+(y-50)*v[1])*fit]}
 function poly(points){ctx.beginPath();points.forEach(([x,y],i)=>{const q=P(x,y);i?ctx.lineTo(...q):ctx.moveTo(...q)});ctx.closePath()}
 ctx.fillStyle='#17272e';ctx.fillRect(0,0,canvas.width,600);ctx.strokeStyle='#22373f';
 for(let y=-600;y<900;y+=45){ctx.beginPath();ctx.moveTo(...P(-600,y));ctx.lineTo(...P(900,y));ctx.stroke()}
 poly([[-700,-900],[far,-900],[far,900],[-700,900]]);ctx.fillStyle='#29343a';ctx.fill();poly([[near,-900],[far,-900],[far,900],[near,900]]);ctx.fillStyle='#34464d';ctx.fill();
 if(p.state==='scan'||p.surveyed)topography(p.heading,p.scanProgress,...P(372,0),.58*fit,p.surveyed?.48:1);
 const ore=P(440,0);sprite(art.resource,...ore,.5*fit);if(p.surveyed){ctx.strokeStyle='#739baa';ctx.lineWidth=1;ctx.beginPath();ctx.arc(...ore,36*fit,0,Math.PI*2);ctx.stroke();}
 const dock=P(0,0),m=manifest.launchers[bay],ls=m.libraryScale*.34*fit,launcher=art['bay-'+bay];ctx.drawImage(launcher,dock[0]-m.anchor[0]*ls,dock[1]-m.anchor[1]*ls,launcher.width*ls,launcher.height*ls);
 const pos=P(p.x,p.y);ctx.save();ctx.beginPath();for(const [l,r] of [[-1000,near],[far,1500]]){const ps=[[l,-1000],[r,-1000],[r,1000],[l,1000]].map(q=>P(...q));ctx.moveTo(...ps[0]);for(const q of ps.slice(1))ctx.lineTo(...q);ctx.closePath()}ctx.clip();probe(p.state,p.heading,time,...pos,.34*fit);ctx.restore();
 if(p.beacon){const offsets={east:[79,15],west:[-69,13],north:[35,-54],south:[36,32]},o=offsets[bay];ctx.strokeStyle='#d7af58';ctx.lineWidth=2;ctx.beginPath();ctx.arc(dock[0]+o[0]*fit,dock[1]+o[1]*fit,4*fit,time/.8*Math.PI*2,time/.8*Math.PI*2+1.5);ctx.stroke()}
 ctx.fillStyle='#9db8c0';ctx.font='12px system-ui';ctx.fillText('PROBE BAY',Math.max(10,dock[0]-40),Math.max(20,dock[1]+95*fit));ctx.fillText(p.surveyed?'RESOURCE MAPPED':'UNSURVEYED RESOURCE',Math.min(canvas.width-160,Math.max(10,ore[0]-65)),Math.max(20,ore[1]+55*fit));
 if(p.state==='scan'){ctx.fillStyle='#344d58';ctx.fillRect(20,560,canvas.width-40,5);ctx.fillStyle='#77b2c3';ctx.fillRect(20,560,(canvas.width-40)*p.scanProgress,5)}
 $('phase').textContent=p.state==='scan'?'Mapping local topography · right to left':p.label;$('readout').textContent=`${paused?'Paused':'Playing'} · ${p.t.toFixed(2)} / 32 s · ${p.heading} · ${p.surveyed?'Survey stored':'Survey pending'}`;
}
function clip(){let h=$('heading').value,state=$('clip').value;if(['launch','dock','recharge'].includes(state)&&!['north','east','south','west'].includes(h)){h='east';$('heading').value=h}
 ctx.fillStyle='#17272e';ctx.fillRect(0,0,canvas.width,600);const scale=Math.min(1,(canvas.width-30)/512);if(state==='scan'){topography(h,(time%4)/4,canvas.width/2,240,scale);topography(h,(time%4)/4,canvas.width-105,490,.34)}probe(state,h,time,canvas.width/2,240,scale);probe(state,h,time,canvas.width-105,490,.34);ctx.fillStyle='#9db8c0';ctx.font='12px system-ui';ctx.fillText('NATIVE 0.34 SCALE',canvas.width-170,390);$('phase').textContent=state+' · '+h;$('readout').textContent=`${paused?'Paused':'Playing'} · frame ${Math.floor(time*30)%(state==='scan'?120:60)+1}/${state==='scan'?120:60} · independent effect/status layers`;}
function tick(now){requestAnimationFrame(tick);const dt=Math.min(.05,(now-(last||now))/1000);last=now;if(!manifest)return;if(!paused)time=(time+dt*rate)%duration;if($('view').value==='mission')mission();else clip();$('scrub').value=time;}
$('pause').onclick=()=>{paused=!paused;$('pause').textContent=paused?'Resume':'Pause'};$('restart').onclick=()=>time=0;$('speed').onchange=e=>rate=+e.target.value;$('scrub').oninput=e=>{time=+e.target.value;paused=true;$('pause').textContent='Resume'};
fetch('manifest.json').then(r=>r.json()).then(async d=>{const paths={resource:d.resource};for(const [h,m]of Object.entries(d.headings))paths[h]=m.pose;for(const [h,m]of Object.entries(d.launchers))paths['bay-'+h]=m.image;for(const [id,m]of Object.entries(d.effects))paths[id]=m.atlas;await Promise.all(Object.entries(paths).map(async([id,path])=>art[id]=await image(path)));manifest=d;resize();requestAnimationFrame(tick)}).catch(e=>$('phase').textContent='Unable to load: '+e.message);
