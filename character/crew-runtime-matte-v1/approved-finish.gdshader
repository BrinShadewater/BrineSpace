shader_type canvas_item;
uniform bool warm_face = false;
uniform vec4 face_rect = vec4(0.0);
void fragment() {
    vec4 tex = texture(TEXTURE, UV);
    vec3 rgb = tex.rgb;
    // Compress bright shading without blurring texture or altering the alpha silhouette.
    rgb = mix(rgb, min(rgb, vec3(0.28)) + max(rgb - vec3(0.28), vec3(0.0)) * 0.72, 0.78);
    rgb *= 0.96;
    // Study only: a conservative face region; no effect on north/back-of-head views.
    bool in_face = UV.x >= face_rect.x && UV.y >= face_rect.y && UV.x <= face_rect.z && UV.y <= face_rect.w;
    if (warm_face && in_face) {
        float bright = smoothstep(0.46, 0.8, max(tex.r,max(tex.g,tex.b)));
        float skin = smoothstep(-0.015,0.08,tex.r-tex.b);
        rgb *= mix(vec3(1.0),vec3(0.96,0.87,0.78),bright*skin*0.75);
    }
    COLOR = vec4(rgb, tex.a);
}
