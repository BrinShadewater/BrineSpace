import assert from 'node:assert/strict';
import { RoverMotion } from './motion.mjs';
const m = new RoverMotion();
m.update(1,20); assert.equal(m.velocity,20);
const phase = m.wheelFrame;
m.command('steer-left','northwest'); assert.equal(m.wheelFrame,phase);
m.command('reverse'); assert.equal(m.wheelFrame,phase);
m.update(.1,20); assert.equal(m.velocity,15); // Must brake before reversing.
m.update(.7,20); assert.equal(m.velocity,-20);
const forwardPhase = m.wheelFrame, reverseFrame = m.sample().frame;
assert.equal((60-reverseFrame)%60,Math.floor(forwardPhase+1e-8)%60);
m.command('mine','north'); m.update(.1,20);
assert.equal(m.sample().state,'drive'); assert.equal(m.actionTime,null);
m.update(.5,20); assert.equal(m.velocity,0); assert.equal(m.sample().state,'mine');
assert.ok(Math.abs(m.actionTime-.2)<1e-8);
m.update(10,20); assert.equal(m.sample().frame,179);
const a = new RoverMotion(), b = new RoverMotion();
a.update(1,20); for(let i=0;i<60;i++) b.update(1/60,20);
assert.ok(Math.abs(a.distance-b.distance)<1e-8);
assert.ok(Math.abs(a.wheelFrame-b.wheelFrame)<1e-8);
a.command('idle'); a.update(1,20); const stopped = a.wheelFrame;
a.update(5,20); assert.equal(a.wheelFrame,stopped);
a.update(0,20); assert.equal(a.wheelFrame,stopped);
const cancel = new RoverMotion(); cancel.command('mine'); cancel.update(2,20);
cancel.command('drive','east'); assert.equal(cancel.state,'mine'); assert.equal(cancel.actionTime,4.5);
cancel.update(.5,20); assert.equal(cancel.velocity,0); assert.equal(cancel.state,'mine');
cancel.update(.6,20); assert.equal(cancel.state,'drive'); assert.equal(cancel.heading,'east'); assert.equal(cancel.velocity,0);
cancel.update(.1,20); assert.equal(cancel.velocity,5);
const early = new RoverMotion(); early.command('mine'); early.update(.8,20);
const deploymentFrame = early.sample().frame; early.command('idle');
assert.equal(early.sample().frame,179-deploymentFrame);
console.log('PASS: phase continuity, acceleration, braking/reverse, stop hold, mining interlock, retract before departure, partial-deploy cancellation, frame-rate independence.');
const cargo = new RoverMotion();cargo.command('collect');cargo.update(4,20);assert.equal(cargo.cargoLoaded,true);
cargo.command('drive');cargo.update(.2,20);assert.equal(cargo.cargoLoaded,true);
cargo.command('unload');cargo.update(4.3,20);assert.equal(cargo.cargoLoaded,false);assert.equal(cargo.deposited,1);
cargo.update(10,20);assert.equal(cargo.deposited,1);
for(const state of ['blocked','power-on','power-off','charging','disabled']){
  const p=new RoverMotion();p.command(state);p.update(10,20);assert.equal(p.velocity,0);assert.equal(p.sample().state,state);
  const limit=state==='blocked'?120:60;assert.ok(p.sample().frame<limit);
}
console.log('PASS: cargo persists through travel, unload emits once, work/power states hold or loop within their frame counts.');
for(const state of ['mine','collect','unload','blocked','power-on','power-off','charging','disabled']) {
  const joined=new RoverMotion();joined.update(.73,20);joined.command(state);joined.update(1,20);
  const held=joined.wheelSample();joined.update(.8,20);
  assert.equal(joined.wheelSample(),held, state+' must preserve stopped tread phase');
  if(['mine','collect','unload','blocked'].includes(state)) joined.update(8,20);
  joined.command('drive');assert.equal(joined.sample().frame,held,state+' departure must retain phase');
}
console.log('PASS: all work/power wheel layers retain the braking phase through work and departure.');
