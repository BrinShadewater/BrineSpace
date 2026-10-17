const $=s=>document.querySelector(s),ctx=$('#stage').getContext('2d'),D=148/(384*.17);
const manifest=await(await fetch('manifest.json?rev=occupied-3')).json(),images=new Map(),robots={};
const load=async path=>{if(images.has(path))return images.get(path);const im=new Image();im.src=path+'?rev=occupied-3';await im.decode();images.set(path,im);return im;};
for(const who of ['river','josh']){
 const m=await(await fetch(`../robot-polish-v1/${who}/manifest.json`)).json();robots[who]=Object.fromEntries(m.states.map(s=>[s.id,s]));
 await Promise.all([...manifest.containers[who].opening,...manifest.containers[who].reboot,manifest.containers[who].empty].map(load));
 for(const key of ['walk-south','idle-south'])await Promise.all(robots[who][key].frameFiles.map(p=>load('../robot-polish-v1/'+p)));
}
let t=0,running=true,last=performance.now();
$('#pause').onclick=()=>{running=!running;$('#pause').textContent=running?'Pause':'Play';};
$('#restart').onclick=()=>t=0;
$('#time').oninput=e=>t=Number(e.target.value);
function body(who,key,elapsed){const s=robots[who][key];let ms=(elapsed*1000)%s.frameDurationsMs.reduce((a,b)=>a+b,0),i=0;while(i<s.frameFiles.length-1&&ms>=s.frameDurationsMs[i])ms-=s.frameDurationsMs[i++];return images.get('../robot-polish-v1/'+s.frameFiles[i]);}
function opening(pack,elapsed){let ms=elapsed*1000,i=0;while(i<pack.opening.length-1&&ms>=pack.openingDurationsMs[i])ms-=pack.openingDurationsMs[i++];return pack.opening[i];}
function draw(now){const dt=Math.min(.1,(now-last)/1000);last=now;if(running&&$('#power').checked)t=(t+dt*Number($('#speed').value))%10;$('#time').value=t;
 const c=$('#stage'),w=c.clientWidth,h=c.clientHeight;if(c.width!==w||c.height!==h){c.width=w;c.height=h;}ctx.clearRect(0,0,w,h);ctx.imageSmoothingEnabled=false;
 const boot=Math.max(0,t-1),scale=Number($('#scale').value)/D;
 for(const [i,who] of ['river','josh'].entries()){
  const pack=manifest.containers[who],x=w*(i?.74:.26),y=h*.63;
  let path=pack.opening[0];
  if(t>=9)path=pack.empty;else if(t>=1&&boot<1.2)path=opening(pack,boot);else if(t>=1&&boot<6.4)path=pack.reboot[Math.min(pack.reboot.length-1,Math.floor((boot-1.2)/5.2*pack.reboot.length))];else if(t>=1)path=pack.empty;
  ctx.drawImage(images.get(path),x-160*scale,y-280*scale,320*scale,440*scale);
  if(boot>=6.4){const f=Math.min(1,(boot-6.4)/1.6),start=who==='josh'?-2:-18,offset=start+(40*D-start)*f;const im=body(who,t>=9?'idle-south':'walk-south',boot-6.4);ctx.drawImage(im,x-92*scale,y+(offset-172)*scale,184*scale,184*scale);}
  ctx.fillStyle='#dbe3e4';ctx.font='18px system-ui';ctx.textAlign='center';ctx.fillText(who==='josh'?'Josh':'River',x,34);
 }
 $('#status').textContent=`${t.toFixed(2)} s · ${!$('#power').checked?'Power lost — recovery held':t<1?'Sealed':boot<1.2?'Opening':boot<6.4?'Restarting':t<9?'Rolling out':'Recovered · empty containers'}`;
 requestAnimationFrame(draw);
}requestAnimationFrame(draw);
