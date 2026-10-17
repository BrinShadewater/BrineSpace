const $=s=>document.querySelector(s),ctx=$('#stage').getContext('2d');
const data=await fetch('review/view.json').then(r=>r.json()),images=new Map();
let clock=0,last=performance.now(),paused=false,ready=false,token=0;
function selected(){return data[$('#actor').value][$('#state').value];}
function reference(){const d=$('#state').value.split('-').at(-1);return data[$('#actor').value]['idle-'+d]||data[$('#actor').value]['idle-south'];}
async function load(path){if(images.has(path))return;const im=new Image();im.src=path;await im.decode();images.set(path,im);}
async function refresh(){const n=++token;ready=false;$('#status').textContent='Loading...';const s=selected();try{await Promise.all([...s.before,...s.after,reference().after[0]].map(load));if(n===token){clock=0;ready=true;}}catch(e){$('#status').textContent='Unable to load frames: '+e.message;}}
function actorChanged(){const previous=$('#state').value;$('#state').replaceChildren(...Object.keys(data[$('#actor').value]).sort().map(key=>{const o=document.createElement('option');o.value=key;o.textContent=key;return o;}));$('#state').value=data[$('#actor').value][previous]?previous:'walk-south';refresh();}
$('#actor').onchange=actorChanged;$('#state').onchange=refresh;
$('#pause').onclick=()=>{paused=!paused;$('#pause').textContent=paused?'Play':'Pause';};
$('#step').onclick=()=>{paused=true;$('#pause').textContent='Play';const ds=selected().durations,total=ds.reduce((a,b)=>a+b,0);let end=0;for(const d of ds){end+=d;if(end>clock%total+.01)break;}clock=Math.floor(clock/total)*total+end+.02;};
function frame(s){let t=clock%s.durations.reduce((a,b)=>a+b,0),i=0;while(i<s.durations.length-1&&t>=s.durations[i])t-=s.durations[i++];return i;}
function draw(now){if(ready&&!paused)clock+=Math.min(now-last,100)*Number($('#speed').value);last=now;ctx.clearRect(0,0,1200,450);if(ready){const s=selected(),ref=reference(),i=frame(s);[[ref,ref.after[0],'Canonical idle'],[s,s.before[i],'Before'],[s,s.after[i],'Current installed']].forEach(([meta,path,label],col)=>{const im=images.get(path),scale=65.28/meta.height*Number($('#scale').value),x=200+400*col,y=380;ctx.fillStyle='#e0e8e5';ctx.font='18px system-ui';ctx.textAlign='center';ctx.fillText(label,x,38);ctx.strokeStyle='#53696d';ctx.beginPath();ctx.moveTo(x-140,y);ctx.lineTo(x+140,y);ctx.stroke();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,x-meta.pivot[0]*scale,y-meta.pivot[1]*scale,im.width*scale,im.height*scale);});$('#status').textContent=`${$('#actor').value} / ${$('#state').value} / frame ${i+1} of ${s.before.length}`;}requestAnimationFrame(draw);}
actorChanged();requestAnimationFrame(draw);
