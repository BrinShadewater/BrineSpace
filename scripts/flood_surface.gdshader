shader_type canvas_item;
render_mode unshaded;
uniform float depth = 0.0;
uniform float clock = 0.0;
varying vec2 floor_position;
void vertex() { floor_position = VERTEX; }
float hash(vec2 p) {
	return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}
float soft_noise(vec2 p) {
	vec2 cell = floor(p);
	vec2 f = fract(p);
	f = f * f * (3.0 - 2.0 * f);
	return mix(mix(hash(cell), hash(cell + vec2(1.0, 0.0)), f.x),
		mix(hash(cell + vec2(0.0, 1.0)), hash(cell + vec2(1.0)), f.x), f.y);
}
void fragment() {
	vec2 p = floor_position;
	float a = sin(p.x * 0.029 + sin(p.y * 0.024) * 1.4);
	float b = sin(p.y * 0.036 + cos(p.x * 0.017) * 1.5);
	float basin = 0.5 + (a + b) * 0.25;
	float threshold = mix(0.88, -0.12, smoothstep(0.0, 0.28, depth));
	float coverage = smoothstep(threshold - 0.055, threshold + 0.055, basin);
	float shore = (1.0 - smoothstep(0.025, 0.09, abs(basin - threshold))) * (1.0 - smoothstep(0.22, 0.32, depth));
	// Broad drifting light patches; no intersecting sine ridges or lattice.
	vec2 drift = vec2(clock * 0.025, -clock * 0.018);
	float broad = soft_noise(p * 0.019 + drift);
	float detail = soft_noise(p * 0.043 - drift * 1.3 + broad * 0.6);
	float light = smoothstep(0.48, 0.88, broad * 0.72 + detail * 0.28);
	vec3 tint = mix(vec3(0.17, 0.43, 0.43), vec3(0.025, 0.18, 0.25), depth);
	tint += vec3(0.12, 0.22, 0.20) * light * mix(0.28, 0.12, depth)
		+ vec3(0.07, 0.14, 0.12) * shore;
	COLOR = vec4(tint, coverage * mix(0.26, 0.68, depth));
}
