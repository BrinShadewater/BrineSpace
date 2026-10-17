const $=s=>document.querySelector(s),canvas=$('#stage'),ctx=canvas.getContext('2d');
const [current,baseline]=await Promise.all(['manifest.json','baseline.json'].map(p=>fetch(p).then(r=>r.json())));
const art=new Map();
async function image(path){if(art.has(path))return art.get(path);const im=new Image();im.src=path;await im.decode();art.set(path,im);return im;}
await Promise.all([...new Set([...current.states,...baseline.states].flatMap(s=>s.frameFiles)),'review/bill-scale-reference.png','review/sofa-scale-reference.png'].map(image));
let time=0,paused=false,last=performance.now();
function row(pack,key){return pack.states.find(s=>s.id===key);}
function duration(clip){return clip.frameDurationsMs.reduce((a,b)=>a+b,0);}
function sample(pack,t){
 const action=$('#action').value,d=action==='pet-cycle'?'south':$('#direction').value;let clip,clock;
 if(action.endsWith('-cycle')){
  const name=action.replace('-cycle',''),keys=[`${name}-enter-${d}`,`${name}-${d}`,`${name}-exit-${d}`,`idle-${d}`];
  const lengths=keys.map((k,i)=>i===3?900:duration(row(current,k))*(i===1?2:1));
  let phase=(t*1000)%lengths.reduce((a,b)=>a+b,0),part=0;
  while(part<3&&phase>=lengths[part])phase-=lengths[part++];
  clip=row(pack,keys[part]);clock=part===0||part===2?phase/lengths[part]*duration(clip):phase;
 }else{clip=row(pack,action+'-'+d);clock=t*1000;if(!clip.loop)clock%=duration(clip)+900;}
 const total=clip.frameDurationsMs.reduce((a,b)=>a+b,0);clock=clip.loop?clock%total:Math.min(clock,total-.01);
 let n=0;while(n<clip.frameFiles.length-1&&clock>=clip.frameDurationsMs[n])clock-=clip.frameDurationsMs[n++];
 return {clip,n,im:art.get(clip.frameFiles[n])};
}
function drawSprite(pack,pose,x,y,zoom){
 const k=(pack===current?.441:.882)*zoom;ctx.imageSmoothingEnabled=false;
 const water=pose.clip.id.startsWith('swim-'),surface=y-24*.441*zoom;
 if(water){ctx.fillStyle='#234450';ctx.beginPath();ctx.ellipse(x,surface+7*zoom,34*zoom,13*zoom,0,0,Math.PI*2);ctx.fill();}
 ctx.drawImage(pose.im,x-pack.pivot[0]*k,y-pack.pivot[1]*k,pose.im.width*k,pose.im.height*k);
 if(water){ctx.fillStyle='rgba(55,125,151,.3)';ctx.beginPath();ctx.ellipse(x,surface+10*zoom,32*zoom,10*zoom,0,0,Math.PI*2);ctx.fill();ctx.strokeStyle='rgba(113,176,191,.5)';ctx.beginPath();ctx.ellipse(x,surface+6*zoom,23*zoom+Math.sin(time*4)*zoom,4*zoom,0,0,Math.PI);ctx.stroke();}
}
function text(value,x,y,color='#b7c9ce',size=14){ctx.fillStyle=color;ctx.font=`${size}px system-ui`;ctx.fillText(value,x,y);}
function draw(){
 const w=canvas.clientWidth,h=canvas.clientHeight,dpr=devicePixelRatio;
 if(canvas.width!==Math.round(w*dpr)||canvas.height!==Math.round(h*dpr)){canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);}
 ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,w,h);
 const zoom=Number($('#zoom').value),fresh=sample(current,time),old=sample(baseline,time),middle=w/2;
 ctx.strokeStyle='#34464e';ctx.beginPath();ctx.moveTo(middle,20);ctx.lineTo(middle,310);ctx.stroke();
 text('INSTALLED POLISH',24,30,'#a1d7c7',14);text('PREVIOUS SPRITES',middle+24,30,'#bdc8cc',14);
 const ground=265;ctx.strokeStyle='#465862';ctx.setLineDash([3,5]);ctx.beginPath();ctx.moveTo(20,ground);ctx.lineTo(w-20,ground);ctx.stroke();ctx.setLineDash([]);
 drawSprite(current,fresh,w*.25,ground,zoom);drawSprite(baseline,old,w*.75,ground,zoom);
 text(`${fresh.clip.id} · frame ${fresh.n+1}/${fresh.clip.frameFiles.length}`,24,300);
 text(`${old.clip.id} · frame ${old.n+1}/${old.clip.frameFiles.length}`,middle+24,300);
 ctx.fillStyle='#17252b';ctx.fillRect(0,326,w,h-326);text('STATION SCALE · ILLUSTRATIVE COMPOSITE',24,351,'#a9bdc6',12);
 const z=w<650?1:1.4,base=510;
 ctx.strokeStyle='#2c3b42';for(let y=382;y<550;y+=32){ctx.beginPath();ctx.moveTo(20,y);ctx.lineTo(w-20,y);ctx.stroke();}
 const sofa=art.get('review/sofa-scale-reference.png');ctx.imageSmoothingEnabled=true;ctx.drawImage(sofa,w*.72-sofa.width*.16*z,base-sofa.height*.32*z,sofa.width*.32*z,sofa.height*.32*z);
 const bill=art.get('review/bill-scale-reference.png');ctx.drawImage(bill,w*.16-92*.441*z,base-172*.441*z,bill.width*.441*z,bill.height*.441*z);
 drawSprite(current,fresh,w*.33,base,z);drawSprite(baseline,old,w*.46,base,z);
 text('Bill',w*.16-12,535);text('Polish',w*.33-20,535);text('Current',w*.46-24,535);
 $('#status').textContent=`${paused?'Paused':'Playing'} · ${$('#direction').value} · ${time.toFixed(2)} s · ${fresh.clip.id}`;
 $('#time').value=time%12;
}
$('#pause').onclick=()=>{paused=!paused;$('#pause').textContent=paused?'Resume':'Pause';draw();};
$('#step').onclick=()=>{paused=true;$('#pause').textContent='Resume';time+=.13;draw();};
$('#time').oninput=e=>{time=Number(e.target.value);paused=true;$('#pause').textContent='Resume';draw();};
for(const id of ['direction','action'])$('#'+id).onchange=()=>{time=0;const pet=$('#action').value==='pet-cycle';if(pet)$('#direction').value='south';$('#direction').disabled=pet;draw();};
function tick(now){if(!paused)time+=Math.min((now-last)/1000,.1)*Number($('#speed').value);last=now;draw();requestAnimationFrame(tick);}requestAnimationFrame(tick);
