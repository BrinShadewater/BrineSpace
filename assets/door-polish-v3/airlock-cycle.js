// Preview-only sequencing. Both seals remain closed during flooding and draining.
const OUTER_HATCH_DEPTH=11;
function airlockWarningActive(seconds){
 const phase=((seconds%45)+45)%45;
 const movements=[[0,2],[5,7],[12,14],[18,20],[22,24],[28,30],[38,40],[43,45]];
 return movements.some(([start,end])=>[-45,0,45].some(offset=>phase+offset>=start-1.25&&phase+offset<=end+2));
}
function airlockSample(seconds){
 const t=((seconds%45)+45)%45;
 if(t>=8&&t<38)return {...outerAirlockSample(t-8),inner:0};
 let inner=0,y=270,moving=false,facing=0,label='';
 if(t<2){inner=t/2;label='Inner door opening · chamber dry';}
 else if(t<5){inner=1;y=270-(t-2)/3*80;moving=true;label='Entering airlock from room';}
 else if(t<7){inner=1-(t-5)/2;y=190;facing=2;label='Waiting inside · inner door closing';}
 else if(t<8){y=190;facing=2;label='Both doors sealed';}
 else if(t<40){inner=(t-38)/2;y=190;facing=2;label='Drained · inner door opening';}
 else if(t<43){inner=1;y=190+(t-40)/3*80;moving=true;facing=2;label='Leaving airlock into room';}
 else{inner=1-(t-43)/2;facing=0;label='Waiting in room · inner door closing';}
 return {open:0,inner,x:0,y,moving,facing,water:0,swimming:false,label};
}
function outerAirlockSample(seconds) {
 const t=((seconds%30)+30)%30;
 let open=0,x=0,y=60,water=1,returning=t>=16,moving=false,facing=0,label='';
 if(t<1){water=0;y=190;label='Dry chamber · inner door sealed';}
 else if(t<4){water=(t-1)/3;y=190-(t-1)/3*130;moving=true;label='Flooding and equalizing · hatch sealed';}
 else if(t<6){open=(t-4)/2;label='Opening outward';}
 else if(t<10){
  open=1;moving=true;const p=(t-6)/4;
  y=60-p*205;facing=0;
  label='Swimming straight through exterior hatch';
 }
 else if(t<12){open=1-(t-10)/2;y=-145;x=0;facing=2;label='Waiting outside facing hatch · closing';}
 else if(t<14){y=-145;x=0;facing=2;label='Waiting outside facing hatch · sealed';}
 else if(t<16){open=(t-14)/2;y=-145;x=0;facing=2;label='Waiting outside facing hatch · opening';}
 else if(t<20){
  open=1;moving=true;const p=(t-16)/4;
  y=-145+p*205;facing=2;
  label='Swimming straight into chamber';
 } else if(t<22){open=1-(t-20)/2;label='Swimming inside · closing hatch';}
 else if(t<23){label='Hatch sealed · verifying seal';}
 else if(t<27){water=1-(t-23)/4;label='Hatch sealed · draining chamber';}
 else{water=0;y=60+Math.min(1,(t-27)/2)*130;moving=t<29;facing=2;label='Drained · returning to inner door';}

 return {open,x,y,facing,water,returning,moving,swimming:y<0||water>0,label};
}







