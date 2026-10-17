(() => {
 const host=document.querySelector('#ocean-hatches');
 const section=document.createElement('section');
 section.id='hatch-topdown';
 section.innerHTML='<h2>Top-down · all four directions</h2><p>72-unit doorway · ocean outside, dry interior inside. The single leaf swings outward by 90°. Shown at 2×; room fitting remains a preview study.</p><nav><button id="top-play">Pause overhead</button><button id="top-open">Open overhead</button><button id="top-close">Close overhead</button><input id="top-position" aria-label="Overhead hatch opening" type="range" min="0" max="100" value="0"><output id="top-status">Closed</output></nav><div id="top-views" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px"></div>';
 host.querySelector('div').before(section);
 const views=['North','East','South','West'].map((name,q)=>{
  const card=document.createElement('article');
  card.innerHTML='<h2>'+name+' ocean exit</h2><canvas width="300" height="300" aria-label="'+name+' overhead hatch"></canvas>';
  section.querySelector('#top-views').append(card);
  return {q,c:card.querySelector('canvas').getContext('2d')};
 });
 const image=new Image();image.src='ocean-hatch-top.png';
 let ready=false,value=0,target=0,playing=true,phase=0,last=0;
 image.onload=()=>{ready=true;draw();};
 const $=id=>document.getElementById(id);
 const ease=t=>t*t*(3-2*t);
 function draw(){
  if(!ready)return;
  for(const {q,c} of views){
   c.clearRect(0,0,300,300);c.save();c.translate(150,150);c.rotate(q*Math.PI/2);c.scale(2,2);
   c.fillStyle='#102b36';c.fillRect(-75,-75,150,75);
   c.fillStyle='#303b3e';c.fillRect(-75,0,150,75);
   c.fillStyle='#677174';c.fillRect(-75,-8,31,16);c.fillRect(44,-8,31,16);
   c.fillStyle='#101b20';c.fillRect(-36,-6,72,12);
   // Registered fixed jambs, kept separate from the hinged rigid leaf.
   c.drawImage(image,112,334,187,220,-47,-7,11,14);
   c.drawImage(image,1480,334,182,220,36,-7,11,14);
   c.save();c.translate(-36,0);c.rotate(-ease(value)*Math.PI/2);
   c.drawImage(image,299,348,1181,211,0,-6,72,13);c.restore();
   c.restore();
   const positions=[[150,24,150,281],[276,150,24,150],[150,281,150,24],[24,150,276,150]][q];
   c.fillStyle='#b3c9cc';c.font='11px system-ui';c.textAlign='center';
   c.fillText('OCEAN',positions[0],positions[1]);c.fillText('ROOM',positions[2],positions[3]);
  }
  $('top-position').value=Math.round(value*100);
  $('top-status').textContent=value===0?'Closed':value===1?'Open':Math.round(value*90)+'°';
 }
 function choose(t){playing=false;target=t;$('top-play').textContent='Play overhead';}
 $('top-open').onclick=()=>choose(1);$('top-close').onclick=()=>choose(0);
 $('top-play').onclick=()=>{playing=!playing;phase=value>.5?2.7:0;target=value;$('top-play').textContent=playing?'Pause overhead':'Play overhead';};
 $('top-position').oninput=e=>{choose(+e.target.value/100);value=target;draw();};
 function tick(now){const dt=last?Math.min(.05,(now-last)/1000):0;last=now;
  if(playing){phase=(phase+dt)%5.2;target=phase<.7?0:phase<3?1:0;}
  value+=Math.sign(target-value)*Math.min(dt/1.4,Math.abs(target-value));draw();requestAnimationFrame(tick);
 }
 requestAnimationFrame(tick);
})();

