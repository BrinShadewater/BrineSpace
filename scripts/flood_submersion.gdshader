shader_type canvas_item;
render_mode unshaded;
uniform float waterline_y = 0.0;
uniform float world_scale = 1.0;
uniform float depth = 0.0;
uniform float clock = 0.0;
varying vec2 world_position;
void vertex() { world_position = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy; }
void fragment() {
	vec4 source = COLOR;
	float scale = max(world_scale, 0.001);
	float wave = sin(world_position.x / scale * 0.13 + clock * 1.3) * scale * 0.8;
	float distance_to_surface = (world_position.y - waterline_y - wave) / scale;
	float wet = smoothstep(-0.4, 1.0, distance_to_surface);
	vec3 submerged = mix(source.rgb * vec3(0.50, 0.73, 0.78), vec3(0.07, 0.29, 0.32), 0.40);
	COLOR.rgb = mix(source.rgb, submerged, wet);
	COLOR.a = source.a * mix(1.0, mix(0.58, 0.28, depth), wet);
	// Preserve dark cast shadows instead of lighting their alpha edges.
	float lit_surface = smoothstep(0.06, 0.24, max(source.r, max(source.g, source.b)));
	float meniscus = (1.0 - smoothstep(0.0, 1.3, abs(distance_to_surface))) * step(0.15, source.a) * lit_surface;
	COLOR.rgb += vec3(0.17, 0.30, 0.29) * meniscus;
}
