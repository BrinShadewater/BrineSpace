"""Package existing Godot-rendered frames as a review loop; invents no sprite art."""
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "output/door-redesign/animation-v1"
OUT = PACK / "door-cycle.gif"
if OUT.exists():
    raise SystemExit(f"Refusing to overwrite {OUT}")
manifest = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
variants = ["bio", "life-support", "engineering"]
images = []
for index in range(10):
    canvas = Image.new("RGB", (768, 228), "#252d35")
    draw = ImageDraw.Draw(canvas)
    for column, variant in enumerate(variants):
        frame = Image.open(PACK / f"{variant}-{index:02d}.png").convert("RGBA")
        canvas.paste(frame, (column * 256, 18), frame)
        draw.text((column * 256 + 20, 12), variant.upper(), fill="#eeeae0")
    draw.text((20, 206), "FRONT-VIEW MOTION STUDY  /  72-UNIT APERTURE  /  WHITE LIGHTS", fill="#c1c9ce")
    images.append(canvas)
# One palette across the whole cycle avoids quantization shimmer.
palette_source = Image.new("RGB", (768, 228 * 10))
for index, image in enumerate(images):
    palette_source.paste(image, (0, index * 228))
palette = palette_source.quantize(colors=256)
images = [image.quantize(palette=palette, dither=Image.Dither.NONE) for image in images]
order = list(range(10)) + list(range(8, 0, -1))
durations = [700] + [60] * 8 + [900] + [60] * 8
frames = [images[index] for index in order]
frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=durations,
               loop=0, disposal=2, optimize=False)
with Image.open(OUT) as check:
    assert check.n_frames == 18
    assert check.size == (768, 228)
print(f"Preview PASS: {OUT}; 18 steps with closed/open holds, shared palette")
