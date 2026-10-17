shader_type canvas_item;
render_mode unshaded;
uniform sampler2D admission_pixels : filter_nearest;
void fragment() {
    vec4 source=texture(TEXTURE,UV);
    vec3 rgb=source.rgb;
    if(texture(admission_pixels,UV).r>0.5)rgb.g=min(rgb.g,max(rgb.r,rgb.b));
    COLOR=vec4(rgb,source.a);
}
