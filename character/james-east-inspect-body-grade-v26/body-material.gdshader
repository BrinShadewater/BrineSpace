shader_type canvas_item;
render_mode unshaded;
uniform bool apply_correction = true;
uniform sampler2D protected_pixels : filter_nearest;
void fragment() {
    vec4 source = texture(TEXTURE, UV);
    vec3 rgb = source.rgb;
    vec3 bytes = rgb * 255.0;
    vec2 pixel = UV * vec2(184.0);
    if (apply_correction && texture(protected_pixels,UV).r < 0.5 &&
        pixel.x >= 56.0 && pixel.x < 110.0 && pixel.y >= 24.0 && pixel.y < 172.0) {
        float violet = min(bytes.r,bytes.b)-bytes.g;
        float light = (bytes.r+bytes.g+bytes.b)/3.0;
        float weight = smoothstep(2.0,8.0,violet) *
            (1.0-smoothstep(12.0,20.0,abs(bytes.r-bytes.b))) * smoothstep(16.0,30.0,light);
        vec3 neutral = vec3(light+1.0,light,light-1.0)/255.0;
        rgb = mix(rgb,neutral,weight);
    }
    COLOR = vec4(rgb,source.a);
}
