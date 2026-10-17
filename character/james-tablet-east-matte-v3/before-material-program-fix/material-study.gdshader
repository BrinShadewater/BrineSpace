shader_type canvas_item;
render_mode unshaded;

// Staged material program: source silhouettes and clocks remain authoritative.
uniform bool apply_correction = true;
void fragment() {
    vec4 source = texture(TEXTURE, UV);
    vec3 rgb = source.rgb;
    if (apply_correction) {
        if (rgb.g > 1.3 * rgb.r && rgb.g > 1.3 * rgb.b && rgb.g > 70.0 / 255.0) {
            rgb.g = max(rgb.r, rgb.b);
        }
        // Pale violet equipment to the right of the torso. This is a bounded
        // colour/position selection, not semantic tablet segmentation.
        vec2 pixel = UV * vec2(184.0);
        float light = (rgb.r + rgb.g + rgb.b) / 3.0;
        float spread = max(rgb.r, max(rgb.g, rgb.b)) - min(rgb.r, min(rgb.g, rgb.b));
        if (pixel.x >= 98.0 && pixel.y >= 40.0 && pixel.y < 138.0 &&
            light > 85.0 / 255.0 && spread < 35.0 / 255.0 && rgb.b > rgb.g + 3.0 / 255.0) {
            float matte = (70.0 + 0.65 * (light * 255.0 - 85.0)) / 255.0;
            rgb = vec3(matte);
        }
    }
    COLOR = vec4(rgb, source.a) * COLOR;
}
