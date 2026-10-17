const load=src=>new Promise((resolve,reject)=>{const i=new Image();i.onload=()=>resolve(i);i.onerror=()=>reject(Error(src));i.src=src;});
const dirs=['north','east','south','west'];
const views=dirs.map((d,q)=>{const a=document.createElement('article');a.innerHTML='<h2>'+d.toUpperCase()+'</h2><canvas width="300" height="300" aria-label="'+d+' passage"></canvas>';document.querySelector('#directions').append(a);return {q,c:a.querySelector('canvas').getContext('2d')};});
let time=0,last=0,paused=false,art,states;
document.querySelector('#pause').onclick=()=>{paused=!paused;document.querySelector('#pause').textContent=paused?'Play':'Pause';};
document.querySelector('#restart').onclick=()=>{time=0;};
const sample=airlockSample;
document.querySelector('#cycle').oninput=e=>{time=+e.target.value;paused=true;document.querySelector('#pause').textContent='Play';if(art)draw();};
function waterLayer(c,q,x,y,scale,s,length){
 if(s.water<=0)return;
 c.save();c.translate(x,y);c.rotate(q*Math.PI/2);c.scale(scale,scale);
 c.beginPath();c.rect(-36,0,72,length);c.clip();
 c.globalAlpha=.52*s.water;c.drawImage(art.sea,-36,0,72,length);
 c.globalAlpha=.28*s.water;c.fillStyle='#27839a';c.fillRect(-36,0,72,length);
 c.globalAlpha=.22*s.water;c.strokeStyle='#b2d8d8';c.lineWidth=.7;
 for(let n=0;n<length;n+=19){const yy=(n+time*5)%length;c.beginPath();c.moveTo(-30,yy);c.lineTo(30,yy+2);c.stroke();}
 c.restore();
}
function base(c,q,x,y,scale,ocean=true){
 c.save();c.translate(x,y);c.rotate(q*Math.PI/2);c.scale(scale,scale);
 if(ocean){c.drawImage(art.sea,-90,-90,180,90);c.fillStyle='rgba(9,38,49,.55)';c.fillRect(-90,-90,180,90);c.fillStyle='#364348';c.fillRect(-90,0,180,90);}
 // Hull and recessed doorway; water remains separate beneath the aperture.
 if(ocean){c.fillStyle='#525f62';c.fillRect(-90,-9,43,18);c.fillRect(47,-9,43,18);}
 c.fillStyle='#121c20';c.fillRect(-43,-10,86,20);
 c.fillStyle='#46575b';c.fillRect(-36,-13,72,26);
 c.strokeStyle='#233439';c.lineWidth=2;
 for(let n=-32;n<36;n+=6){c.beginPath();c.moveTo(n,-12);c.lineTo(n,12);c.stroke();}
 c.fillStyle='#10181c';c.fillRect(-43,-10,7,20);c.fillRect(36,-10,7,20);
 c.restore();
}
function hardware(c,q,x,y,scale,s){
 c.save();c.translate(x,y);c.rotate(q*Math.PI/2);c.scale(scale,scale);
 c.scale(-56/72,56/72);
 c.drawImage(art.hatch,112,334,187,220,-47,-7,11,14);
 c.drawImage(art.hatch,1480,334,182,220,36,-7,11,14);
 c.save();c.translate(-36,0);c.rotate(-s.open*s.open*(3-2*s.open)*Math.PI/2);
 // Compensate for the leaf-width scale so every rotation has the north hatch's steel depth.
 const depth=OUTER_HATCH_DEPTH*72/56;
 c.drawImage(art.rim,147,228,1879,266,0,-depth,72,depth);
 c.fillStyle='rgba(43,133,175,'+(s.water*.10*Math.pow(1-s.open,2))+')';c.fillRect(0,-depth,72,depth);c.restore();
 // Foreground lip avoids covering the center passage or the diver.
 c.fillStyle='#7b8583';c.fillRect(-46,9,10,2);c.fillRect(36,9,10,2);c.restore();
}
function actor(c,q,x,y,scale,s){
 const facing=dirs[(q+s.facing)%4];
 const key=(s.swimming?'swim':s.moving?'walk':'idle')+'-'+facing;
 const clip=states[key], im=clip.images[Math.floor(time*8)%clip.images.length];
 const ax=x+(Math.cos(q*Math.PI/2)*s.x-Math.sin(q*Math.PI/2)*s.y)*scale,ay=y+(Math.sin(q*Math.PI/2)*s.x+Math.cos(q*Math.PI/2)*s.y)*scale;
 // Match nursery_whole_view.gd's crew height, used by the captured room actor.
 const f=65.28/148*scale;
 c.drawImage(im,ax-clip.pivot[0]*f,ay-clip.pivot[1]*f,im.width*f,im.height*f);
}
function northRiserHatch(c,s){
 const sx=56/590,sy=64/925,top=161,bottom=225,left=322;
 c.save();c.translate(700,0);c.scale(-1,1);
 const angle=s.open*s.open*(3-2*s.open)*Math.PI/2;
 const tint=Math.max(0,Math.min(1,s.water))*.10*Math.pow(1-s.open,2);
 // The opening is in the upright north riser; the leaf projects into the ocean.
 // Aperture background is drawn before the swimmer, not over the swimmer.
 c.save();c.translate(left-330*sx,bottom-1090*sy);c.scale(sx,sy);
 const frame=new Path2D();frame.rect(0,0,1254,1254);
 const hole=new Path2D();hole.roundRect(330,165,590,925,105);frame.addPath(hole);
 c.clip(frame,'evenodd');c.drawImage(art.face,0,0,1254,1254);c.restore();
 // Connected textured steel side and top planes share a single solid depth.
 const cosine=Math.cos(angle),sine=Math.sin(angle);
 const steelDepth=OUTER_HATCH_DEPTH;
 if(sine>.001){
  const edgeX=left+56*cosine,edgeY=top-56*sine;
  c.save();c.globalAlpha=Math.min(1,sine*8);
  // Extrude toward the ocean-facing normal, away from the chamber face.
  c.transform(-sine,-cosine,0,1,edgeX,edgeY);
  c.beginPath();c.roundRect(0,0,steelDepth,64,2);c.clip();
  // Reuse the authored rim's steel and gasket strip, not a flat helper fill.
  c.drawImage(art.rim,1630,252,255,210,0,0,steelDepth,64);
  c.fillStyle='rgba(12,20,24,.18)';c.fillRect(0,0,steelDepth,64);
  c.restore();
 }
 // Recess the rim behind the front face; it is concealed when fully seated.
 if(sine>.001){
  c.save();c.globalAlpha=Math.min(1,sine*4);
  c.transform(cosine,-sine,-sine,-cosine,left,top);
  c.drawImage(art.rim,147,228,1879,266,0,0,56,steelDepth);c.restore();
 }
 if(cosine>.04){
 c.save();c.transform(cosine,-sine,0,1,left,top);
 c.beginPath();c.roundRect(0,0,56,64,6);c.clip();
 c.drawImage(art.face,330,165,590,925,0,0,56,64);
 if(tint>0){c.fillStyle='rgba(43,133,175,'+tint+')';c.fillRect(0,0,56,64);}
 c.restore();
 }
 c.restore();
}
function draw(){
 const s=sample(time);document.querySelector('#state').textContent=s.label;document.querySelector('#cycle').value=time%45;
 for(const {q,c} of views){c.clearRect(0,0,300,300);base(c,q,150,150,.55);waterLayer(c,q,150,150,.55,s,219);actor(c,q,150,150,.55,s);hardware(c,q,150,150,.55,s);}
 const c=document.querySelector('#room').getContext('2d');c.clearRect(0,0,700,720);
 const selected=dirs.indexOf(document.querySelector('#view').value);
 if(selected>0){directionalStudy(c,selected,s);return;}
 c.drawImage(art.sea,0,0,700,720);c.fillStyle='rgba(9,38,49,.55)';c.fillRect(0,0,700,720);
 c.drawImage(art.room,375,236,530,620,150,140,400,468);
 // Keep the north riser. Its doorway sits at the far end of the pressure chamber.
 base(c,0,350,225,1,false);waterLayer(c,0,350,225,1,s,219);
 // Continuous opening through the wall cap, riser and hull. Sample the same
 // ocean coordinates as the surrounding background so it reads as a passage.
 c.drawImage(art.sea,322/700*art.sea.width,136/720*art.sea.height,56/700*art.sea.width,89/720*art.sea.height,322,136,56,89);
 c.fillStyle='rgba(9,38,49,.55)';c.fillRect(322,136,56,89);
 innerHatch(c,s);
 // Sill and threshold sit below the swimmer; upper frame sits above them.
 northRiserHatch(c,s);
 actor(c,0,350,225,1,s);
 c.save();c.beginPath();c.rect(295,60,110,153);c.clip();
 northRiserHatch(c,s);
 c.restore();
 // Continuous deep lintel, sampled from the room's existing steel wall cap.
 // It bridges the frame shoulders and occludes the doorway only above its head.
 c.drawImage(art.room,565,236,145,24,311,140,78,18.12);
 cautionLights(c,s);
 // Fixed frame and lintel occlude the swimmer at the aperture edges.
 c.fillStyle='#b5d3d5';c.font='16px system-ui';c.textAlign='center';c.fillText('OCEAN',350,42);
}
document.querySelector('#view').onchange=()=>{if(art)draw();};
function directionalStudy(c,q,s){
 const scale=1.25,angle=q*Math.PI/2;
 const x=350+Math.sin(angle)*62*scale,y=350-Math.cos(angle)*62*scale;
 c.drawImage(art.sea,0,0,700,720);c.fillStyle='rgba(9,38,49,.55)';c.fillRect(0,0,700,720);
 c.save();c.translate(x,y);c.rotate(angle);c.scale(scale,scale);
 // Overhead fitting study: actual chamber grating and cap material, no rotated elevation.
 c.fillStyle='#354044';c.fillRect(-110,0,220,310);
 c.drawImage(art.room,600,400,80,130,-36,0,72,219);
 for(const side of [-45,36])c.drawImage(art.room,559,395,12,130,side,0,9,219);
 c.restore();
 base(c,q,x,y,scale,false);waterLayer(c,q,x,y,scale,s,219);
 c.save();c.translate(x,y);c.rotate(angle);c.scale(scale,scale);c.translate(-350,-225);innerHatch(c,s);c.restore();
 actor(c,q,x,y,scale,s);hardware(c,q,x,y,scale,s);
 c.save();c.translate(x,y);c.rotate(angle);c.scale(scale,scale);c.translate(-350,-225);cautionLights(c,s,true);c.restore();
 c.fillStyle='#d2dfe0';c.font='20px system-ui';c.textAlign='center';
 c.fillText(['North','Right side · East','Bottom · South','Left side · West'][q],350,35);
 c.font='14px system-ui';c.fillText('Overhead chamber fitting · same complete airlock cycle',350,685);
}
function innerHatch(c,s){
 const x=350,y=444,w=36*(1-s.inner);
 // Room-side overhead sliding pressure door: two rigid leaves and fixed jambs.
 c.fillStyle='#202d32';c.fillRect(x-36,y-9,72,18);
 if(w>.01){
  c.drawImage(art.innerDoor,213+865*s.inner,263,865*(1-s.inner),162,x-36,y-9,w,18);
  c.drawImage(art.innerDoor,1091,263,865*(1-s.inner),162,x+36-w,y-9,w,18);
 }
 c.drawImage(art.hatch,112,334,187,220,x-45,y-11,9,22);
 c.drawImage(art.hatch,1480,334,182,220,x+36,y-11,9,22);
}
function cautionLights(c,s,overhead=false){
 // Warn 1.25 seconds before travel and linger 2 seconds after either seal seats.
 const active=airlockWarningActive(time);
 for(const [x,y] of [[302,444],[398,444],[304,overhead?225:152],[396,overhead?225:152]]){
  c.save();c.translate(x,y);
  c.fillStyle='#263036';c.beginPath();c.arc(0,0,5,0,Math.PI*2);c.fill();
  c.fillStyle=active?'#d89532':'#76552e';c.beginPath();c.arc(0,0,3.3,0,Math.PI*2);c.fill();
  if(active){
   c.rotate(time*Math.PI*.8);
   const beam=c.createRadialGradient(0,0,3,0,0,85);beam.addColorStop(0,'rgba(242,164,45,.30)');beam.addColorStop(.55,'rgba(242,164,45,.15)');beam.addColorStop(1,'rgba(242,164,45,0)');
   c.fillStyle=beam;c.beginPath();c.moveTo(0,0);c.arc(0,0,85,-.32,.32);c.closePath();c.fill();
   c.fillStyle='#ffdc8a';c.fillRect(0,-1,3,2);
  }
  c.restore();
 }
}
async function start(){
 states=await fetch('diver-preview.json').then(r=>r.json());
 await Promise.all(Object.values(states).map(async s=>{s.images=await Promise.all(s.frames.map(p=>load('../../'+p)));}));
 const [sea,hatch,room,face,rim,innerDoor]=await Promise.all([load('../../legacy/default/assets/environment/seabed-v1/silt-plain-source-v1.png'),load('ocean-hatch-top.png'),load('diving-room-reference.png'),load('ocean-hatch-interior.png'),load('ocean-hatch-rim.png'),load('airlock-low.png')]);art={sea,hatch,room,face,rim,innerDoor};
 // Actor radius 10: no crossing while moving leaf occupies the center route.
 let checked=0;for(let n=0;n<=4500;n++){const s=sample(n/100);if(Math.abs(s.y)<24&&s.open<.999)throw Error('Hatch clearance failed');checked++;}
 document.querySelector('#state').dataset.clearanceSamples=checked*4;
 function tick(now){if(last&&!paused)time+=Math.min(.05,(now-last)/1000);last=now;draw();requestAnimationFrame(tick);}requestAnimationFrame(tick);
}
start().catch(e=>{document.querySelector('#state').textContent='Preview error: '+e.message;console.error(e);});












