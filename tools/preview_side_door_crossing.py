"""Package unmodified native screenshot crops into a sampled crossing review."""
from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
source = root / "output/door-redesign/side-v7-final"
output = root / "output/door-redesign/animation-v8/native-crossings.gif"
if output.exists():
    raise SystemExit(f"Refusing overwrite: {output}")
frames = []
for step in [0, 8, 16, 35, 45, 50, 55, 65, 84, 92, 100]:
    canvas = Image.new("RGB", (480, 246), "#202831")
    draw = ImageDraw.Draw(canvas)
    for index, reverse in enumerate(["false", "true"]):
        capture = Image.open(source / f"close-q0-r{reverse}-s{step}.png").convert("RGB")
        canvas.paste(capture, (240 * index, 26))
        draw.text((240 * index + 10, 8), "EASTBOUND" if index == 0 else "WESTBOUND", fill="#e4e5df")
    frames.append(canvas)
palette_source = Image.new("RGB", (480, 246 * len(frames)))
for index, frame in enumerate(frames):
    palette_source.paste(frame, (0, index * 246))
palette = palette_source.quantize(colors=256)
frames = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
frames[0].save(output, save_all=True, append_images=frames[1:], duration=[600]+[180]*4+[700]+[180]*4+[600], loop=0, disposal=2, optimize=False)
print(output)
