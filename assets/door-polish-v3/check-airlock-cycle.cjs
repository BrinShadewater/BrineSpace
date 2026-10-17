const fs=require('fs'),vm=require('vm'),assert=require('assert');
const context={};vm.createContext(context);
vm.runInContext(fs.readFileSync(__dirname+'/airlock-cycle.js','utf8'),context);
const steelDepth=vm.runInContext('OUTER_HATCH_DEPTH',context);
let previous=null;
for(let n=0;n<=3000;n++){
 const s=context.outerAirlockSample(n/100);
 assert(s.open>=0&&s.open<=1&&s.water>=0&&s.water<=1);
 if(Math.abs(s.y)<24)assert(s.open===1,'Crossing before hatch cleared');
 if(s.open>0)assert(s.water===1,'Open hatch without equalized water');
 if(s.water>0||s.y<0)assert(s.swimming,'Diver stood in water');
 const angle=-s.open*s.open*(3-2*s.open)*Math.PI/2;
 const vx=-56*Math.cos(angle),vy=56*Math.sin(angle);
 const u=Math.max(0,Math.min(1,((s.x-28)*vx+s.y*vy)/(56*56)));
 const distance=Math.hypot(s.x-28-u*vx,s.y-u*vy);
 assert(distance>=24,'Swimmer intersects hatch swing envelope');
 // Test the entire outside-facing slab, not only its hinge-to-tip line.
 const opening=-angle,dx=s.x-28;
 const along=-dx*Math.cos(opening)-s.y*Math.sin(opening);
 const outward=dx*Math.sin(opening)-s.y*Math.cos(opening);
 const slabDistance=Math.hypot(Math.max(0,-along,along-56),Math.max(0,-outward,outward-steelDepth));
 assert(slabDistance>=24,'Swimmer intersects thick steel hatch');
 if(previous&&s.water<previous.water)assert(s.open===0,'Draining before seal');
 previous=s;
}
assert(context.outerAirlockSample(11).y<0&&context.outerAirlockSample(11).open<1);
assert(context.outerAirlockSample(21).swimming);
assert(context.outerAirlockSample(22.5).water===1);
assert(context.outerAirlockSample(25).water>0&&context.outerAirlockSample(25).swimming);
assert(!context.outerAirlockSample(28).swimming);
assert(context.outerAirlockSample(5).y===60&&!context.outerAirlockSample(5).moving);
assert(context.outerAirlockSample(11).facing===2&&!context.outerAirlockSample(11).moving);
assert(context.outerAirlockSample(15).facing===2&&!context.outerAirlockSample(15).moving);
assert(context.outerAirlockSample(21).facing===0&&!context.outerAirlockSample(21).moving);
for(let n=0;n<3000;n++){
 const s=context.outerAirlockSample(n/100);
 if(Math.abs(s.x)>18)assert(s.y<=-103,'Swimmer cuts across hull wall');
 assert(s.x===0,'Route must remain centered through the hatch');
 if(s.open>0&&s.open<1)assert(!s.moving,'Swimmer moves during hatch travel');
}
console.log('PASS: clearance, straight centered route, stationary facing waits, seal-before-drain.');
for(let n=0;n<=4500;n++){
 const s=context.airlockSample(n/100);
 assert(!(s.inner>0&&s.open>0),'Both doors open');
 if(s.inner>0)assert(s.water===0,'Inner door open while flooded');
 if(Math.abs(s.y-219)<18)assert(s.inner===1,'Inner threshold crossing before clearance');
 if(s.inner>0&&s.inner<1)assert(!s.moving,'Moving during inner door travel');
 if((s.inner>0&&s.inner<1)||(s.open>0&&s.open<1))assert(context.airlockWarningActive(n/100),'Door moving without caution lights');
}
console.log('PASS: 4501 samples; inner-door interlock, dry opening, entry/exit clearance.');
for(const [start,end] of [[0,2],[5,7],[12,14],[18,20],[22,24],[28,30],[38,40],[43,45]]){
 assert(context.airlockWarningActive(start-1.25),'Missing advance caution');
 assert(context.airlockWarningActive(end+2),'Missing lingering caution');
}
assert(!context.airlockWarningActive(35),'Caution should rest during sealed drain');
console.log('PASS: solid steel clearance; caution covers travel, lead-in, linger and cycle wrap.');


