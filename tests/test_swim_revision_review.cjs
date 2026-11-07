// Exercise the actual review script, including an early first RAF timestamp.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const base = path.resolve(__dirname, '../character/crew-underwater-v1/revisions');
const source = fs.readFileSync(path.join(base, 'review.html'), 'utf8').match(/<script type="module">([\s\S]*?)<\/script>/)[1];

async function controller(direction='east') {
  const elements = Object.fromEntries(['rows','phase','pause','time','helmet','status'].map(id => [id,{append(){},value:0,checked:false}]));
  const draws = [];
  let callback;
  const context = vm.createContext({
    document: {querySelector: selector => elements[selector.slice(1)], createElement: () => ({append(){},getContext(){const canvas=this;return {clearRect(){},drawImage(image,x,y,w,h){assert.ok(image);assert.ok(x>=0 && y>=0 && x+w<=canvas.width && y+h<=canvas.height,'Full frame must fit review canvas');draws.push(image.src);}}}})},
    fetch: async file => ({ok:true,json:async()=>JSON.parse(fs.readFileSync(path.resolve(base,file),'utf8'))}),
    Image: class {set src(file){this.file=file;const bytes=fs.readFileSync(path.resolve(base,file));this.width=bytes.readUInt32BE(16);this.height=bytes.readUInt32BE(20);assert.ok(fs.existsSync(path.resolve(base,file)));queueMicrotask(()=>this.onload());} get src(){return this.file;}},
    performance:{now:()=>1000}, URLSearchParams, location:{search:'?direction='+direction},
    requestAnimationFrame: fn => {callback=fn;},
  });
  await vm.runInContext(`(async()=>{${source}})()`,context);
  return {elements,draws,tick:time=>callback(time)};
}

test('early first timestamp and backwards clock never select a negative frame', async()=>{
  const c=await controller();
  c.tick(999); // Earlier than performance.now() at initialization.
  assert.match(c.elements.time.textContent,/0 ms · phase 1/);
  c.tick(998);
  assert.match(c.elements.time.textContent,/0 ms · phase 1/);
  for(let time=1098;time<3098;time+=100)c.tick(time);
  assert.equal(c.draws.length,132);
  assert.ok(c.draws.some(file=>file.endsWith('frame_005.png')));
  assert.ok(c.draws.every(file=>/frame_00[0-5]\.png$/.test(file)));
});

test('scrubbing pauses; helmet toggle retains phase across all six comparisons', async()=>{
  const c=await controller();c.tick(0);
  c.elements.phase.value='959';c.elements.phase.oninput();c.tick(100);
  assert.equal(c.elements.pause.textContent,'Play');
  assert.ok(c.draws.slice(-6).every(file=>file.endsWith('frame_005.png')));
  c.elements.helmet.checked=true;c.tick(200);
  assert.ok(c.draws.slice(-6).every(file=>/helmet|equipment/.test(file)));
  assert.ok(c.draws.slice(-6).every(file=>file.endsWith('frame_005.png')));
  c.elements.pause.onclick();c.tick(202);
  assert.ok(c.draws.slice(-6).every(file=>file.endsWith('frame_000.png')));
});

 test('west candidates load both bodies and helmet rows',async()=>{const c=await controller('west');c.tick(0);assert.ok(c.draws.slice(-6).every(file=>file.includes('swim-west')));c.elements.helmet.checked=true;c.tick(100);assert.ok(c.draws.slice(-6).every(file=>/helmet|equipment/.test(file)));});

test('south bodies and helmets fit canvas across every phase',async()=>{const c=await controller('south');for(const helmet of [false,true]){c.elements.helmet.checked=helmet;for(let i=0;i<6;i++){c.elements.phase.value=String(i*160+80);c.elements.phase.oninput();c.tick(i*100);assert.ok(c.draws.slice(-6).every(file=>file.includes('swim-south')));assert.ok(c.draws.slice(-6).every(file=>file.endsWith('frame_00'+i+'.png')));}}});

test('north selects retained Veld cycle and revised Bill/Branforth',async()=>{const c=await controller('north');c.tick(0);assert.ok(c.draws.slice(-6).every(file=>file.includes('swim-north')));assert.match(c.draws[1],/^bill-swim-north-v2/);assert.match(c.draws[3],/pilot\/veld-swim-north/);assert.match(c.draws[5],/^branforth-swim-north-v2/);c.elements.helmet.checked=true;c.tick(100);assert.match(c.draws.at(-3),/equipment\/fitting\/veld-swim-north/);});
