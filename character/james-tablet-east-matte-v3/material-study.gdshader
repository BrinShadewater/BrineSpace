shader_type canvas_item;
render_mode unshaded;

// Staged material program: source silhouettes and clocks remain authoritative.
uniform bool apply_correction = true;
uniform sampler2D protected_pixels : filter_nearest;
void fragment() {
    vec4 source = texture(TEXTURE, UV);
    vec3 rgb = source.rgb;
    vec3 bytes = round(rgb * 255.0);
    bool spill = 10.0 * bytes.g > 13.0 * bytes.r && 10.0 * bytes.g > 13.0 * bytes.b && bytes.g > 70.0;
    if (apply_correction && (texture(protected_pixels, UV).r < 0.5 || spill)) {
        if (spill) {
            rgb.g = max(rgb.r, rgb.b);
        }
        // Pale violet equipment to the right of the torso. This is a bounded
        // colour/position selection, not semantic tablet segmentation.
        vec2 pixel = UV * vec2(184.0);
        float light = (rgb.r + rgb.g + rgb.b) / 3.0;
        float spread = max(bytes.r, max(bytes.g, bytes.b)) - min(bytes.r, min(bytes.g, bytes.b));
        if (pixel.x >= 98.0 && pixel.y >= 40.0 && pixel.y < 138.0 &&
            bytes.r + bytes.g + bytes.b > 255.0 && spread < 35.0) {
            float matte = (70.0 + 0.65 * (light * 255.0 - 85.0)) / 255.0;
            rgb = vec3(matte);
        }
    }
    COLOR = vec4(rgb, source.a);
}
