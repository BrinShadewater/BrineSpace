const $=s=>document.querySelector(s),canvas=$('#stage'),ctx=canvas.getContext('2d');
const catalog=await fetch('catalog.json').then(r=>r.json()),packs={},art=new Map();
async function image(path){if(art.has(path))return art.get(path);const im=new Image();im.src=path+'?rev=colour-contact-2';await im.decode();art.set(path,im);return im;}
for(const who of Object.keys(catalog)){packs[who]=await Promise.all([catalog[who].manifest,catalog[who].baseline].map(p=>fetch(p).then(r=>r.json())));}
await Promise.all([...new Set(Object.values(packs).flat(1).flatMap(p=>p.states.flatMap(s=>s.frameFiles))),'review/bill-scale-reference.png','review/margot-scale-reference.png'].map(image));
let time=0,paused=false,last=performance.now();
const actions={josh:['idle','walk','move-start','move-stop','direction-turn','watch-cycle','turn-cycle','torch-cycle','powerdown-cycle','powerdown'],river:['idle','walk','move-start','move-stop','direction-turn','scan-cycle','inspect-cycle','boot-cycle','float','float-idle']};
const row=(p,key)=>p.states.find(s=>s.id===key),duration=c=>c.frameDurationsMs.reduce((a,b)=>a+b,0);
function options(){const value=$('#action').value;$('#action').replaceChildren(...actions[$('#character').value].map(key=>Object.assign(document.createElement('option'),{value:key,textContent:key.replaceAll('-',' ')})));$('#action').value=actions[$('#character').value].includes(value)?value:'walk';time=0;}
options();
function sample(pack,t){
 const action=$('#action').value,d=$('#direction').value,current=packs[$('#character').value][0];let key=action+'-'+d,clock=t*1000;
 if(action==='direction-turn'){let to=$('#target').value;if(to===d)to=['south','west','north','east'][(['south','west','north','east'].indexOf(d)+1)%4];key=`turn-${d}-${to}`;}
 else if(action.endsWith('-cycle')){const name=action.slice(0,-6),keys=name==='boot'?[`boot-${d}`,`boot-exit-${d}`,`idle-${d}`]:[`${name}-enter-${d}`,`${name}-${d}`,`${name}-exit-${d}`,`idle-${d}`];
  const lengths=keys.map((k,i)=>k.startsWith('idle-')?1000:duration(row(current,k))*(i===1&&name!=='boot'?2:1));
  let phase=clock%lengths.reduce((a,b)=>a+b,0),part=0;while(part<keys.length-1&&phase>=lengths[part])phase-=lengths[part++];key=keys[part];clock=phase/lengths[part]*duration(row(pack,key))*(part===1&&name!=='boot'?2:1);
 }
 const clip=row(pack,key);const total=duration(clip);if(!action.endsWith('-cycle'))clock%=total+(clip.loop?0:800);clock=clip.loop?clock%total:Math.min(clock,total-.01);
 let n=0;while(n<clip.frameFiles.length-1&&clock>=clip.frameDurationsMs[n])clock-=clip.frameDurationsMs[n++];return {clip,n,im:art.get(clip.frameFiles[n])};
}
function text(str,x,y,color='#b7c9ce',size=13){ctx.fillStyle=color;ctx.font=`${size}px system-ui`;ctx.fillText(str,x,y);}
function sprite(pack,pose,x,y,zoom){const scale=65.28/pack.standingHeight*zoom;ctx.imageSmoothingEnabled=false;
 const water=pose.clip.id.startsWith('float-');if(water){ctx.fillStyle='#284754';ctx.beginPath();ctx.ellipse(x,y-7*zoom,26*zoom,10*zoom,0,0,Math.PI*2);ctx.fill();}
 ctx.drawImage(pose.im,x-pack.pivot[0]*scale,y-pack.pivot[1]*scale,pose.im.width*scale,pose.im.height*scale);
 if(water){ctx.strokeStyle='#72a4b6';ctx.beginPath();ctx.ellipse(x,y-6*zoom,23*zoom,5*zoom,0,0,Math.PI);ctx.stroke();}
}
function draw(){const w=canvas.clientWidth,h=canvas.clientHeight,dpr=devicePixelRatio;if(canvas.width!==Math.round(w*dpr)||canvas.height!==Math.round(h*dpr)){canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);}ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,w,h);
 const [fresh,old]=packs[$('#character').value],a=sample(fresh,time),b=sample(old,time),z=Number($('#zoom').value),ground=300;
 text('POLISHED ARTWORK',18,24,'#a9d7c3');text('PREVIOUS SPRITES',w/2+18,24);ctx.strokeStyle='#3a505b';ctx.beginPath();ctx.moveTo(w/2,10);ctx.lineTo(w/2,355);ctx.moveTo(18,ground);ctx.lineTo(w-18,ground);ctx.stroke();
 sprite(fresh,a,w*.25,ground,z);sprite(old,b,w*.75,ground,z);text(`${a.clip.id} · frame ${a.n+1}/${a.clip.frameFiles.length}`,18,335);text(`${b.clip.id} · frame ${b.n+1}/${b.clip.frameFiles.length}`,w/2+18,335);
 ctx.fillStyle='#142128';ctx.fillRect(0,360,w,h-360);text('STATION SCALE · ILLUSTRATIVE COMPOSITE',18,389);const rz=1.5,base=515;
 const bill=art.get('review/bill-scale-reference.png'),cat=art.get('review/margot-scale-reference.png');ctx.imageSmoothingEnabled=false;
 for(const [im,x]of [[bill,.13],[cat,.85]])ctx.drawImage(im,w*x-92*.441*rz,base-172*.441*rz,184*.441*rz,184*.441*rz);
 for(const [who,x]of [['josh',.38],['river',.64]]){const pack=packs[who][0];const pose=who===$('#character').value?a:{clip:row(pack,'idle-'+$('#direction').value),im:art.get(row(pack,'idle-'+$('#direction').value).frameFiles[0])};sprite(pack,pose,w*x,base,rz);}
 for(const [s,x]of [['Bill',.13],['Josh',.38],['River',.64],['Margot',.85]])text(s,w*x-15,545);
 $('#status').textContent=`${paused?'Paused':'Playing'} · ${$('#character').value} · ${a.clip.id} · ${time.toFixed(2)} s`;
 $('#time').value=time%12;$('#target').disabled=$('#action').value!=='direction-turn';
}
$('#pause').onclick=()=>{paused=!paused;$('#pause').textContent=paused?'Resume':'Pause';draw();};$('#step').onclick=()=>{paused=true;time+=.16;$('#pause').textContent='Resume';draw();};$('#time').oninput=e=>{paused=true;time=Number(e.target.value);$('#pause').textContent='Resume';draw();};
$('#character').onchange=()=>{options();draw();};for(const id of ['action','direction','target'])$('#'+id).onchange=()=>{time=0;draw();};
function tick(now){if(!paused)time+=Math.min((now-last)/1000,.1)*Number($('#speed').value);last=now;draw();requestAnimationFrame(tick);}requestAnimationFrame(tick);
