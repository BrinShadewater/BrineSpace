import assert from 'node:assert/strict';import {sample,duration,angles} from './mission.mjs';
const eps=1e-5;let samples=0;
for(const bay of ['north','east','south','west']){
 for(const t of [2,3.6,6,10,12,16,20,24,27,30,32]){
  const a=sample(t-eps,bay),b=sample(t+eps,bay);assert.ok(Math.hypot(a.worldX-b.worldX,a.worldY-b.worldY)<.01,`${bay} discontinuity ${t}`);
 }
 for(let t=.01;t<duration;t+=.025){
  const p=sample(t,bay),next=sample(t+eps,bay);assert.ok(Number.isFinite(p.worldX)&&Number.isFinite(p.worldY));
  const dx=next.worldX-p.worldX,dy=next.worldY-p.worldY,s=Math.hypot(dx,dy);if(s>1e-7){const dot=(dx*Math.cos(angles[p.heading])+dy*Math.sin(angles[p.heading]))/s;assert.ok(p.state==='dock'?dot<-.92:dot>.92,`${bay} sideways motion ${t}`)}
  if(p.state==='scan'){assert.equal(p.x,372);assert.equal(p.y,0);assert.ok(p.scanProgress>=0&&p.scanProgress<=1)}samples++;
 }
 assert.equal(sample(15.9,bay).surveyed,false);assert.equal(sample(16,bay).surveyed,true);assert.equal(sample(31,bay).state,'recharge');assert.equal(sample(31,bay).x,0);assert.equal(sample(31,bay).heading,bay);
 assert.deepEqual(sample(0,bay),sample(32,bay));
}
console.log(`PASS: ${samples} path samples; four bay orientations; continuous positions, nose-first travel, reverse-only docking, stationary scans, stored survey and exact cycle join.`);
