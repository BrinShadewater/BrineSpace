// Preview rendering from the preserved hatch masters; no raster files are altered.
(() => {
  const section = document.querySelector('#ocean-hatches');
  const controls = document.createElement('nav');
  controls.innerHTML = '<button id="hatch-cycle">Pause hatches</button><button id="hatch-close">Close hatches</button><button id="hatch-open">Open hatches</button><input id="hatch-progress" aria-label="Hatch opening" type="range" min="0" max="100" value="0"><output id="hatch-state">Sealed</output>';
  section.querySelector('div').before(controls);
  const views = [];
  section.querySelectorAll('article img').forEach((img, i) => {
    const canvas = document.createElement('canvas');
    canvas.width = 360; canvas.height = 360;
    canvas.setAttribute('aria-label', i ? 'Exterior hinged hatch animation' : 'Interior hinged hatch animation');
    img.replaceWith(canvas);
    const source = new Image();
    source.onload = () => { views.push({source, canvas, exterior: !!i}); draw(); };
    source.src = img.getAttribute('src');
  });
  let amount = 0, target = 0, cycling = true, phase = 0, previous = 0;
  const smooth = t => {t = Math.max(0, Math.min(1, t)); return t*t*(3-2*t);};
  const shape = () => {const p = new Path2D(); p.roundRect(330,165,590,925,105); return p;};
  function draw() {
    const swing = smooth((amount - .22)/.78);
    const release = smooth(amount/.22);
    for (const {source,canvas,exterior} of views) {
      const c = canvas.getContext('2d');
      c.clearRect(0,0,360,360); c.save(); c.scale(360/1254,360/1254);
      const leaf = shape();
      // The pressure ring remains stationary around a dark clear aperture.
      c.fillStyle = exterior ? '#0b141a' : '#102b36'; c.fill(leaf);
      c.save();
      const frame = new Path2D(); frame.rect(0,0,1254,1254); frame.addPath(leaf);
      c.clip(frame,'evenodd'); c.drawImage(source,0,0,1254,1254); c.restore();
      // Orthographic projection of a rigid hinged leaf, stopping nearly edge-on.
      const hinge = exterior ? 920 : 330;
      c.save(); c.translate(hinge,0); c.scale(Math.cos(swing*Math.PI*0.49),1); c.translate(-hinge,0);
      c.save(); c.clip(leaf); c.drawImage(source,0,0,1254,1254); c.restore();
      // Turn the existing locking wheel during the seal-release interval.
      c.save(); c.beginPath(); c.arc(623,622,101,0,Math.PI*2); c.clip();
      c.translate(623,622); c.rotate((exterior?-1:1)*release*Math.PI/4);
      c.drawImage(source,-623,-622,1254,1254); c.restore(); c.restore(); c.restore();
    }
    document.querySelector('#hatch-progress').value = Math.round(amount*100);
    document.querySelector('#hatch-state').textContent = amount < .001 ? 'Sealed' : amount > .999 ? 'Open' : amount < .22 ? 'Locking wheel' : 'Hinged travel';
  }
  function choose(next) {cycling=false; target=next; document.querySelector('#hatch-cycle').textContent='Play hatches';}
  document.querySelector('#hatch-open').onclick=()=>choose(1);
  document.querySelector('#hatch-close').onclick=()=>choose(0);
  document.querySelector('#hatch-cycle').onclick=()=>{cycling=!cycling; phase=amount>0.5?2.6:0; document.querySelector('#hatch-cycle').textContent=cycling?'Pause hatches':'Play hatches'; target=amount;};
  document.querySelector('#hatch-progress').oninput=e=>{choose(+e.target.value/100); amount=target; draw();};
  function tick(now) {
    const dt=previous?Math.min(.05,(now-previous)/1000):0; previous=now;
    if(cycling){phase=(phase+dt)%5.2; target=phase<.7?0:phase<3?1:0;}
    const step=dt/1.4;
    amount += Math.sign(target-amount)*Math.min(step,Math.abs(target-amount));
    draw(); requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
})();
