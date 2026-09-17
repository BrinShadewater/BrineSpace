shader_type canvas_item;
render_mode unshaded;
uniform sampler2D terrain : filter_nearest, repeat_disable;
uniform vec4 lights[48];
uniform vec4 directions[48];
uniform int light_count = 0;
uniform float cell_size = 384.0;
uniform float clock = 0.0;
uniform vec4 silt = vec4(-100.0,-100.0,0.0,0.0);
// Marine snow (owner playtest: the outside needed movement and sediment): 0 holds it still.
uniform float motion = 1.0;
varying vec2 world;
void vertex(){world=VERTEX/cell_size;}
float grain(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.0-2.0*f);return mix(mix(grain(i),grain(i+vec2(1,0)),f.x),mix(grain(i+vec2(0,1)),grain(i+vec2(1)),f.x),f.y);}
// One layer of sparse sediment flakes: hashed cells, each with one soft flake drifting down
// and swaying on the current.
float snow(vec2 w,float scale,float speed,float t,float seed){
 vec2 p=w*scale+vec2(sin(t*.23+seed)*.35,-t*speed*scale);
 vec2 id=floor(p);vec2 f=fract(p);
 float h=grain(id+seed);
 if(h<.8)return 0.0;
 vec2 center=vec2(grain(id+seed+3.1),grain(id+seed+7.7))*.7+.15;
 float size=mix(.035,.085,grain(id+seed+1.3));
 return(1.0-smoothstep(size*.35,size,length(f-center)))*mix(.45,1.0,grain(id+seed+5.2));
}
void fragment(){
 float illumination=0.0;
 for(int i=0;i<light_count;i++){
  vec2 delta=world-lights[i].xy;float d=length(delta);
  if(d>=lights[i].z)continue;
  float cone=smoothstep(.45,.9,dot(delta/max(d,.001),directions[i].xy));
  float local=1.0-smoothstep(.1,.4,d);
  float value=max(cone,local)*pow(1.0-d/lights[i].z,1.5)*lights[i].w;
  if(value<.001)continue;
  for(int step=1;step<24;step++){
   vec2 point=mix(lights[i].xy,world,float(step)/24.0);
   // Leave the visible rock face lit; the remainder of the mass casts shadow.
   if(texture(terrain,point/40.0).r>.5 && distance(point,world)>.10){value=0.0;break;}
  }
  illumination=max(illumination,value);
 }
 float haze=noise(world*2.4+vec2(clock*.018,-clock*.011));
 float fine=noise(world*29.0+vec2(clock*.035,clock*.02));
 float memory=texture(terrain,world/40.0).g;
 float opacity=mix(.985,.92,memory)-illumination*.83;
 float plume=(1.0-smoothstep(.05,1.15,length(world-silt.xy-vec2(-.15,.04))))*silt.z;
 opacity+=plume*.25;
 vec3 water=mix(vec3(.008,.021,.028),vec3(.026,.077,.081),haze*.4+illumination*.6);
 water+=vec3(.08,.12,.12)*pow(fine,12.0)*illumination;
 water=mix(water,vec3(.105,.135,.12)*(haze*.5+.5),plume*.65);
 // Flakes are finer than a pixel when zoomed far out, so fade them there to avoid shimmer.
 float t=clock*motion;
 float flakes=(snow(world,5.0,.07,t,0.0)*.7+snow(world,9.0,.045,t,11.0)*.5+snow(world,16.0,.028,t,23.0)*.35)*smoothstep(48.0,140.0,cell_size);
 water+=vec3(.30,.40,.40)*flakes*(.22+illumination*1.4);
 // Faint moving caustics where lamps light the water.
 water+=vec3(.02,.045,.045)*pow(abs(sin(noise(world*3.1+vec2(t*.21,t*.13))*6.2832)),6.0)*illumination*motion;
 COLOR=vec4(water,clamp(opacity+haze*.035,.12,.995));
}
