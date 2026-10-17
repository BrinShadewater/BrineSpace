export const duration=32;
export const angles={east:0,southeast:Math.PI/4,south:Math.PI/2,southwest:3*Math.PI/4,west:Math.PI,northwest:5*Math.PI/4,north:3*Math.PI/2,northeast:7*Math.PI/4};
export const order=Object.keys(angles);
const smooth=t=>t*t*(3-2*t),mix=(a,b,t)=>a+(b-a)*t;
function local(t){
 if(t<2)return {state:'recharge',label:'Docked · charging',x:0,y:0,yaw:0};
 if(t<3.6)return {state:'idle',label:'Preparing launch',x:0,y:0,yaw:0,beacon:true};
 if(t<6){let q=(t-3.6)/2.4;return {state:'launch',label:'Launching',x:72*q*q,y:0,yaw:0};}
 if(t<10)return {state:'cruise',label:'Outbound',x:mix(72,312,(t-6)/4),y:0,yaw:0};
 if(t<12){let q=(t-10)/2;return {state:'brake',label:'Braking at resource',x:312+60*(2*q-q*q),y:0,yaw:0};}
 if(t<16)return {state:'scan',label:'Scanning resource',x:372,y:0,yaw:0,scan:(t-12)/4};
 if(t<20){let a=Math.PI*smooth((t-16)/4);return {state:'return',label:'Turning for home',x:372+60*Math.sin(a),y:60-60*Math.cos(a),yaw:a};}
 if(t<24){let q=smooth((t-20)/4);return {state:'return',label:'Returning to bay',x:mix(372,130,q),y:mix(120,90,smooth(q)),yaw:Math.atan2(-30*6*q*(1-q),-242)};}
 if(t<27){let a=Math.PI*smooth((t-24)/3);return {state:'return',label:'Aligning with cradle',x:130-45*Math.sin(a),y:45+45*Math.cos(a),yaw:Math.PI+a};}
 if(t<30)return {state:'dock',label:'Recovering into cradle',x:130*(1-smooth((t-27)/3)),y:0,yaw:0};
 return {state:'recharge',label:'Docked · survey data received',x:0,y:0,yaw:0};
}
export function sample(time,bay='east'){
 const t=((time%duration)+duration)%duration,p=local(t),a=angles[bay],c=Math.cos(a),s=Math.sin(a),yaw=p.yaw+a;
 const heading=order[((Math.round(yaw/(Math.PI/4))%8)+8)%8];
 return {...p,t,heading,worldX:p.x*c-p.y*s,worldY:p.x*s+p.y*c,surveyed:t>=16,scanProgress:t<12?0:t<16?(t-12)/4:1};
}
