shader_type canvas_item;
render_mode unshaded;
uniform float room_light = 1.0;

// Source-space wear stays attached to each surface through pan and zoom.
// Alpha and silhouettes are untouched; only uncleared room canvases use this.
float hash(vec2 p) {
	return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);
}
float noise(vec2 p) {
	vec2 i=floor(p), f=fract(p);
	f=f*f*(3.0-2.0*f);
	return mix(mix(hash(i),hash(i+vec2(1.0,0.0)),f.x),mix(hash(i+vec2(0.0,1.0)),hash(i+vec2(1.0)),f.x),f.y);
}
void fragment() {
	vec4 source=COLOR;
	vec2 p=floor(UV/max(TEXTURE_PIXEL_SIZE,vec2(0.00001))*.5)*2.0;
	float broad=noise(p*.016);
	float mottling=noise(p*.065+vec2(19.0,47.0));
	float grain=noise(p*.36);
	float value=max(source.r,max(source.g,source.b));
	// Dark glazing/recesses retain their subjects and instruments.
	float surface=smoothstep(.12,.43,value);
	float dirt=smoothstep(.25,.78,broad*.68+mottling*.32);
	float scale=smoothstep(.54,.70,mottling*.62+grain*.38)*smoothstep(.38,.60,broad);
	float pits=smoothstep(.72,.88,grain)*smoothstep(.38,.62,mottling);
	vec3 aged=source.rgb*mix(vec3(.84,.87,.80),vec3(.46,.49,.39),dirt*.85);
	// Flaking enamel exposes warm oxide and dark steel rather than white sparkle.
	vec3 oxide=mix(vec3(.18,.15,.11),vec3(.36,.24,.13),grain)*(.65+value*.45);
	aged=mix(aged,oxide,scale*.76);
	aged*=1.0-pits*.46;
	vec3 finish=mix(source.rgb,aged,surface*.94);
	// Unrepaired hulls have ambient underwater visibility, never electric light.
	finish=mix(finish*.32+vec3(.025,.045,.07)*.68,finish,room_light);
	COLOR=vec4(finish,source.a);
}
