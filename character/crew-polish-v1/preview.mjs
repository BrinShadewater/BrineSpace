const $=s=>document.querySelector(s),canvas=$('#stage'),ctx=canvas.getContext('2d');
const baseline=await fetch('review/baseline.json').then(r=>r.json());
const motion=Object.fromEntries(await Promise.all(['veld','branforth','marsh'].map(async a=>[a,await fetch(`motion/${a}/manifest.json`).then(r=>r.json())])));
const painted=await fetch('veld-painted-v2/manifest.json').then(r=>r.json());
const helmet=await fetch('veld-painted-v2-helmet/manifest.json').then(r=>r.json());
const art=new Map();let ready=false,time=0,last=performance.now(),paused=false,serial=0;
async function load(path){if(art.has(path))return;const im=new Image();im.src=path;await im.decode();art.set(path,im);}
function clips(){
 const a=$('#actor').value,direction=$('#direction').value,kind=a==='veld'?$('#action').value:'walk';
 const keys=(kind==='chain'?['idle','kneel','repair','repair','stand']: [kind]).map(k=>k+'-'+direction);
 const b=keys.map(k=>baseline[a].bodyStates[k]),m=motion[a],s=m.states.find(s=>s.id===keys[0]);
 const pack=$('#gear').value==='helmet'?helmet:painted,folder=$('#gear').value==='helmet'?'veld-painted-v2-helmet':'veld-painted-v2';
 const p=keys.map(k=>pack.states.find(s=>s.id===k));
 return [
 {label:`Current game - ${b.reduce((n,s)=>n+s.frames.length,0)} poses`,files:b.flatMap(s=>s.frames.map(f=>'../../'+f.path)),dur:b.flatMap(s=>s.durations),pivot:b[0].pivot,height:b[0].standingHeight},
 ...(s&&kind==='walk'?[{label:`Source motion - ${s.frameFiles.length} poses`,files:s.frameFiles.map(f=>`motion/${a}/`+f),dur:s.frameDurationsMs,pivot:m.pivot,height:m.standingHeight}]:[]),
 ...(a==='veld'?[{label:`Painted candidate - ${p.reduce((n,s)=>n+s.frameFiles.length,0)} poses`,files:p.flatMap(s=>s.frameFiles.map(f=>folder+'/'+f)),dur:p.flatMap(s=>s.frameDurationsMs),pivot:pack.pivot,height:pack.standingHeight}]:[])];
}
async function refresh(){const token=++serial;ready=false;$('#status').textContent='Loading selected frames...';try{await Promise.all(clips().flatMap(c=>c.files).map(load));if(token===serial){ready=true;time=0;}}catch(e){$('#status').textContent='Unable to load study: '+e.message;}}
for(const id of ['actor','direction','action','gear'])$('#'+id).addEventListener('change',refresh);
$('#pause').onclick=()=>{paused=!paused;$('#pause').textContent=paused?'Play':'Pause';};
$('#step').onclick=()=>{paused=true;$('#pause').textContent='Play';const c=clips().at(-1),total=c.dur.reduce((a,b)=>a+b,0),clock=time*1000,cycle=Math.floor(clock/total);let end=0;for(const d of c.dur){end+=d;if(end>clock%total+.01)break;}time=(cycle*total+end+.02)/1000;};
function sample(c){let t=(time*1000)%c.dur.reduce((a,b)=>a+b,0),i=0;while(i<c.files.length-1&&t>=c.dur[i])t-=c.dur[i++];return i;}
function draw(now){const dt=Math.min((now-last)/1000,.1);last=now;if(!paused&&ready)time+=dt*Number($('#speed').value);ctx.clearRect(0,0,1200,430);ctx.font='17px system-ui';ctx.textAlign='center';if(ready){const rows=clips(),zoom=Number($('#zoom').value);rows.forEach((c,j)=>{const x=1200*(j+.5)/rows.length,y=365,i=sample(c),im=art.get(c.files[i]),k=65.28/c.height*zoom;ctx.fillStyle='#d7e0df';ctx.fillText(c.label,x,42);ctx.strokeStyle='#526367';ctx.beginPath();ctx.moveTo(x-135,y);ctx.lineTo(x+135,y);ctx.stroke();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,x-c.pivot[0]*k,y-c.pivot[1]*k,im.width*k,im.height*k);ctx.fillStyle='#a7b6b7';ctx.fillText(`Pose ${i+1} / ${c.files.length}`,x,408);});$('#status').textContent=`${$('#actor').value} / ${$('#direction').value} / ${$('#action').value} / clock ${time.toFixed(2)} s / in-place review`;}requestAnimationFrame(draw);}
await refresh();requestAnimationFrame(draw);
