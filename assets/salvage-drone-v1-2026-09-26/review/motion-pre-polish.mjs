const work=new Set(['retrieve','release','blocked']);
const poweredDown=new Set(['power-off','charging','disabled']);
export function integrate(value,target,acceleration,dt){const ramp=Math.min(dt,Math.abs(target-value)/acceleration);const next=value+Math.sign(target-value)*acceleration*ramp;return {value:Math.abs(next-target)<1e-9?target:next,distance:(value+next)*.5*ramp+next*(dt-ramp),ramp};}
export class SalvageMotion {
 constructor(){this.state='idle';this.heading='south';this.time=0;this.velocity=0;this.rotorPhase=0;this.rotorSpeed=30;this.loaded=false;this.completed=false;this.deposited=0;this.pending=null;}
 command(state,heading=this.heading){
  if(work.has(state)&&!['north','east','south','west'].includes(heading))heading='south';
  if(state===this.state&&heading===this.heading)return;
  if(work.has(this.state)&&!this.completed){this.pending={state,heading};return;}
  this.state=state;this.heading=heading;this.time=0;this.completed=false;this.pending=null;
  if(state==='carry')this.loaded=true;
  if(state==='retrieve'||state==='blocked')this.loaded=false;
 }
 replay(){this.time=0;this.velocity=0;this.completed=false;this.pending=null;if(this.state==='retrieve'||this.state==='blocked')this.loaded=false;}
 update(dt){
  const travel=['swim','reverse','carry','start'].includes(this.state);const target=travel?(this.state==='reverse'?-24:24):0;
  const before=this.velocity;const move=integrate(before,target,48,dt);this.velocity=move.value;
  const activeTime=work.has(this.state)?(this.velocity===0?dt-(before===0?0:move.ramp):0):dt;this.time+=Math.max(0,activeTime);
  let rotorTarget=travel?(this.state==='reverse'?-120:120):poweredDown.has(this.state)?0:30;
  if(this.state==='power-on')rotorTarget=30*Math.min(1,this.time/1.5);
  const rotor=integrate(this.rotorSpeed,rotorTarget,120,dt);this.rotorSpeed=rotor.value;this.rotorPhase=((this.rotorPhase+rotor.distance)%60+60)%60;
  if(work.has(this.state)&&this.time>=4&&!this.completed){this.completed=true;if(this.state==='retrieve')this.loaded=true;if(this.state==='release'){this.loaded=false;this.deposited++;}}
  if(this.completed&&this.pending){const next=this.pending;this.pending=null;this.command(next.state,next.heading);}
  return {distance:move.distance,status:before!==0&&target===0&&this.velocity!==0?'Braking':this.velocity===0?'Holding':Math.abs(this.velocity)<24?'Accelerating':'Swimming'};
 }
 sample(){const state=work.has(this.state)&&this.velocity!==0?'swim':this.state;const count=work.has(state)?120:60;const loop=['idle','swim','reverse','carry','charging','disabled'].includes(state);return {state,frame:loop?Math.floor(this.time*30)%count:Math.min(count-1,Math.floor(this.time*30)),rotorFrame:Math.floor(this.rotorPhase)%60};}
}
