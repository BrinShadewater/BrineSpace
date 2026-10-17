import { RoverMotion } from './motion.mjs';
const canvas = document.querySelector('#stage'), ctx = canvas.getContext('2d');
const headingEl = document.querySelector('#heading'), lightEl = document.querySelector('#light');
const readout = document.querySelector('#readout'), manualEl = document.querySelector('#manual');
const motion = new RoverMotion(), cache = new Map(), errors = [], keys = new Set();
const cargoPoses = new Map();
const wheelLayers = new Map();
const cardinalWork = new Set(['mine','collect','unload','blocked']);
let deposits = [], depositSerial = 0, lastUnload = null;
let cycle = null;
const diagonal = Math.SQRT1_2;
const directions = {north:[0,-1],northeast:[diagonal,-diagonal],east:[1,0],southeast:[diagonal,diagonal],south:[0,1],southwest:[-diagonal,diagonal],west:[-1,0],northwest:[-diagonal,-diagonal]};
let data, paused = false, rate = 1, last = 0, clock = 0, manualWasMoving = false;
let ground = {x:0,y:0}, position = {x:0,y:0};
function image(path) {
  return new Promise((resolve,reject) => {
    const im = new Image(); im.onload = () => resolve(im);
    im.onerror = () => reject(Error('Cannot load '+path)); im.src = path;
  });
}
function clip(state) {
  const id = state+'-'+motion.heading;
  if (!cache.has(id)) {
    const entry = data.states.find(e => e.id === id);
    if (!entry) throw Error('Missing '+id);
    const item = {entry,ready:false}; cache.set(id,item);
    Promise.all([image(entry.atlas.path),image(entry.effectAtlas.path),entry.cargoAtlas ? image(entry.cargoAtlas.path) : null])
      .then(([body,effect,cargo]) => Object.assign(item,{body,effect,cargo,ready:true}))
      .catch(e => errors.push(e.message));
  }
  return cache.get(id);
}
function controls() {
  headingEl.value = motion.heading;
  for (const o of headingEl.options) o.disabled = cardinalWork.has(motion.state) && !['north','east','south','west'].includes(o.value);
  for (const b of document.querySelectorAll('[data-state]')) b.setAttribute('aria-pressed',String(b.dataset.state === (motion.pending?.state || motion.state)));
}
function choose(state,heading = motion.heading,fromCycle = false) {
  if (!fromCycle) cycle = null;
  if (cardinalWork.has(state) && !['north','east','south','west'].includes(heading)) heading = 'south';
  if (state === 'collect') deposits = [];
  motion.command(state,heading); controls();
}
for (const b of document.querySelectorAll('[data-state]')) b.onclick = () => choose(b.dataset.state);
headingEl.onchange = () => choose(motion.state,headingEl.value);
document.querySelector('#pause').onclick = e => {paused = !paused; e.target.textContent = paused ? 'Resume' : 'Pause';};
function resetReview() {motion.replay(); position = {x:0,y:0}; ground = {x:0,y:0}; deposits = [];}
function completeCycle() {
  resetReview(); manualEl.checked = false; keys.clear(); motion.cargoLoaded = false;
  cycle = {stage:0,started:clock}; choose('mine',motion.heading,true);
}
document.querySelector('#cycle').onclick = completeCycle;
document.querySelector('#replay').onclick = () => cycle ? completeCycle() : resetReview();
document.querySelector('#speed').onchange = e => rate = +e.target.value;
manualEl.onchange = () => {keys.clear(); manualWasMoving = false; if (manualEl.checked) choose('idle');};
addEventListener('keydown',e => {
  if (e.target.matches('select,input:not([type=checkbox])')) return;
  if (e.code === 'Space') {e.preventDefault(); document.querySelector('#pause').click();}
  if (e.key.startsWith('Arrow') && manualEl.checked) {e.preventDefault(); keys.add(e.key);}
});
addEventListener('keyup',e => keys.delete(e.key));
addEventListener('blur',() => keys.clear());
new ResizeObserver(() => {canvas.width = Math.round(canvas.clientWidth); canvas.height = 520;}).observe(canvas);
function drawFrame(im,entry,n,x,y,scale) {
  const size = data.frameWidth;
  ctx.drawImage(im,n%entry.atlas.columns*size,Math.floor(n/entry.atlas.columns)*size,size,size,x-size*scale/2,y-size*scale/2,size*scale,size*scale);
}
function lamp(x,y,scale,entry,n) {
  const p = data.headings[motion.heading].lamp;
  ctx.save(); ctx.globalAlpha = ['power-on','power-off'].includes(entry.state) ? entry.lampSamples[n] : .35+.65*(.5+.5*Math.cos(clock/data.lamp.periodSeconds*Math.PI*2));
  ctx.fillStyle = data.lamp.colors[lightEl.value === 'automatic' ? entry.lampColor || 'operational' : lightEl.value]; ctx.beginPath();
  ctx.arc(x+(p[0]-data.pivot[0])*scale,y+(p[1]-data.pivot[1])*scale,2.4*scale,0,Math.PI*2); ctx.fill(); ctx.restore();
}
function tick(now) {
  requestAnimationFrame(tick);
  const dt = paused ? 0 : Math.min(.05,(now-(last||now))/1000)*rate; last = now;
  if (!data) return;
  clock += dt;
  if (manualEl.checked && !paused) {
    const dx = Number(keys.has('ArrowRight'))-Number(keys.has('ArrowLeft'));
    const dy = Number(keys.has('ArrowDown'))-Number(keys.has('ArrowUp'));
    if (dx || dy) {
      const heading = dy<0 ? (dx<0?'northwest':dx>0?'northeast':'north') : dy>0 ? (dx<0?'southwest':dx>0?'southeast':'south') : dx<0?'west':'east';
      choose('drive',heading); manualWasMoving = true;
    } else if (manualWasMoving) {choose('idle'); manualWasMoving = false;}
  }
  let active;
  try {active = clip(motion.sample().state);} catch(e) {readout.textContent = e.message; return;}
  if (!active.ready) {readout.textContent = errors.length ? errors.join('; ') : 'Loading '+motion.state+' '+motion.heading+'…'; return;}
  const speed = data.headings[motion.heading].tyreTravelWorldUnitsPerSecond || 22;
  if (active.entry.state === 'unload') lastUnload = {active,x:position.x,y:position.y,gx:ground.x,gy:ground.y};
  const movement = motion.update(dt,speed);
  if (cycle) {
    if (cycle.stage===0 && motion.actionTime>=6) {cycle.stage=1;choose('collect',motion.heading,true);}
    else if (cycle.stage===1 && motion.actionTime>=4) {cycle.stage=2;cycle.started=clock;choose('carry',motion.heading,true);}
    else if (cycle.stage===2 && clock-cycle.started>=3) {cycle.stage=3;choose('unload',motion.heading,true);}
    else if (cycle.stage===3 && motion.actionTime>=4) {cycle.stage=4;choose('idle',motion.heading,true);}
  }
  const sample = motion.sample();
  if (motion.deposited !== depositSerial) {
    depositSerial = motion.deposited;
    if (lastUnload) deposits.push({...lastUnload});
  }
  controls();
  if (active.entry.id !== sample.state+'-'+motion.heading) {
    active = clip(sample.state);
    if (!active.ready) {readout.textContent = 'Loading '+sample.state+'…'; return;}
  }
  const e = active.entry, n = sample.frame, scale = Math.min(1.15,(canvas.width-44)/data.frameWidth);
  const u = directions[motion.heading], pixels = movement.distance/data.worldUnitsPerPixel*scale;
  if (manualEl.checked) {
    const desiredX = position.x+u[0]*pixels, desiredY = position.y+u[1]*pixels;
    position.x = Math.max(-canvas.width*.25,Math.min(canvas.width*.25,desiredX));
    position.y = Math.max(-115,Math.min(90,desiredY));
    ground.x -= desiredX-position.x; ground.y -= desiredY-position.y;
  } else {ground.x -= u[0]*pixels; ground.y -= u[1]*pixels;}
  ctx.clearRect(0,0,canvas.width,520); ctx.fillStyle = '#17272e'; ctx.fillRect(0,0,canvas.width,520);
  ctx.strokeStyle = '#23363e'; ctx.lineWidth = 1;
  for (let x=(ground.x%32)-32;x<canvas.width;x+=32) {ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,520); ctx.stroke();}
  for (let y=(ground.y%32)-32;y<520;y+=32) {ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(canvas.width,y); ctx.stroke();}
  ctx.fillStyle = '#829ba7'; ctx.font = '11px system-ui'; ctx.fillText('SEABED MOTION / ENLARGED',14,22);
  const x = canvas.width/2+position.x, y = 248+position.y;
  for (const drop of deposits) drawFrame(drop.active.cargo,drop.active.entry,119,canvas.width/2+drop.x+ground.x-drop.gx,248+drop.y+ground.y-drop.gy,scale);
  function vehicle(vx,vy,vs) {
    drawFrame(active.body,e,n,vx,vy,vs);
    // Work clips share the stopped rolling texture instead of resetting tyres.
    const wheels = wheelLayers.get(motion.heading);
    if (wheels && !['drive','reverse','steer-left','steer-right','carry','start','stop'].includes(e.state)) {
      drawFrame(wheels,{atlas:data.headings[motion.heading].wheelAtlas},motion.wheelSample(),vx,vy,vs);
    }
    drawFrame(active.effect,e,n,vx,vy,vs);
    if (active.cargo && !(e.state === 'unload' && n===119 && deposits.length)) drawFrame(active.cargo,e,n,vx,vy,vs);
    else if (!active.cargo && motion.cargoLoaded && cargoPoses.has(motion.heading)) {
      ctx.drawImage(cargoPoses.get(motion.heading),vx-224*vs,vy-224*vs,448*vs,448*vs);
    }
    lamp(vx,vy,vs,e,n);
  }
  vehicle(x,y,scale);
  const ix = canvas.width-76, iy = 436;
  ctx.fillStyle = '#17272eee'; ctx.fillRect(canvas.width-152,350,152,169);
  ctx.fillStyle = '#829ba7'; ctx.fillText('0.34× SCALE',canvas.width-130,368);
  vehicle(ix,iy,.34);
  const phase = motion.pending ? 'Finishing '+motion.state+' before '+motion.pending.state : !['drive','reverse','steer-left','steer-right','carry'].includes(sample.state) ? e.phases[n] : movement.status;
  readout.textContent = `${paused?'Paused':'Playing'} · ${motion.state}-${motion.heading} · ${phase} · frame ${n+1}/${e.frameCount} · ${lightEl.value}`;
  if (cycle) readout.textContent += cycle.stage===4 ? ' · Cycle complete' : ' · Complete cycle';
  if (errors.length) readout.textContent = errors.join('; ');
}
fetch('manifest.json').then(r=>r.json()).then(async d=>{
  data=d;
  await Promise.all(Object.entries(data.headings).map(async ([h,entry])=>{
    if(entry.wheelAtlas) wheelLayers.set(h,await image(entry.wheelAtlas.path));
  }));
  for (const [h,entry] of Object.entries(data.headings)) if(entry.cargoPose) image(entry.cargoPose).then(im=>cargoPoses.set(h,im)).catch(e=>errors.push(e.message));
  controls(); requestAnimationFrame(tick);
}).catch(e=>readout.textContent=e.message);
