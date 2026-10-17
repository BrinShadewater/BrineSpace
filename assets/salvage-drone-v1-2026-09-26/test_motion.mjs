import assert from 'node:assert/strict';import {SalvageMotion} from './motion.mjs';
const a=new SalvageMotion(),b=new SalvageMotion();a.command('swim');b.command('swim');let da=a.update(1).distance,db=0;for(let i=0;i<60;i++)db+=b.update(1/60).distance;assert.ok(Math.abs(da-db)<1e-8);assert.ok(Math.abs(a.rotorPhase-b.rotorPhase)<1e-8);
a.command('retrieve','east');a.update(.1);assert.equal(a.sample().state,'swim');assert.equal(a.time,0);a.update(.5);assert.equal(a.velocity,0);assert.equal(a.sample().state,'retrieve');a.command('swim','north');assert.equal(a.heading,'east');a.update(4);assert.equal(a.loaded,true);assert.equal(a.heading,'north');assert.equal(a.state,'swim');
a.command('idle');a.update(1);assert.equal(a.loaded,true);a.command('release','west');a.update(4);assert.equal(a.loaded,false);assert.equal(a.deposited,1);a.update(6);assert.equal(a.deposited,1);
const c=new SalvageMotion();c.command('blocked');c.update(4);assert.equal(c.loaded,false);c.command('power-off');c.update(3);assert.equal(c.rotorSpeed,0);const p=c.rotorPhase;c.update(4);assert.equal(c.rotorPhase,p);c.command('power-on');assert.equal(c.rotorPhase,p);c.update(2);assert.equal(c.rotorSpeed,30);
for(const h of ['north','east','south','west','northeast','northwest','southeast','southwest']){const m=new SalvageMotion();m.command('carry',h);m.update(.3);assert.equal(m.heading,h);assert.equal(m.loaded,true);const phase=m.rotorPhase;m.command('idle');assert.equal(m.rotorPhase,phase);}
for(const state of ['power-on','power-off']){
 const x=new SalvageMotion(),y=new SalvageMotion();x.rotorSpeed=y.rotorSpeed=state==='power-on'?0:120;x.command(state);y.command(state);
 x.update(1.5);for(let i=0;i<90;i++)y.update(1/60);
 assert.ok(Math.abs(x.rotorSpeed-y.rotorSpeed)<1e-8);assert.ok(Math.abs(x.rotorPhase-y.rotorPhase)<1e-8);
 assert.equal(x.rotorSpeed,state==='power-on'?30:0);
}
console.log('PASS: frame-rate independent travel and power ramps, brake-before-work, queued work departure, cargo persistence, once-only deposit, blocked recovery, shutdown/restart phase, eight-way loaded movement.');
