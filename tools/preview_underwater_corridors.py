"""Package native captures without rescaling them. Never modifies source art."""
from pathlib import Path
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "output/underwater-corridor-v8"
OUT = SOURCE / "review"
OUT.mkdir(exist_ok=False)
frames = []
for index in range(41):
    canvas = Image.new("RGB", (768, 414), "#0d2630")
    draw = ImageDraw.Draw(canvas)
    for q in range(2):
        frame = Image.open(SOURCE / f"cycle-q{q}-rfalse-{index:02}.png").convert("RGB")
        assert frame.size == (384, 384)
        canvas.paste(frame, (384 * q, 30))
        draw.text((384*q+12, 9), "DOWNWARD COLLAR" if q == 0 else "SIDE COLLAR", fill="#dce7de")
    frames.append(canvas)
palette_source = Image.new("RGB", (768, 414*len(frames)))
for index, frame in enumerate(frames): palette_source.paste(frame, (0,index*414))
palette = palette_source.quantize(colors=256)
gif_frames = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
gif_frames[0].save(OUT / "door-crossings.gif", save_all=True, append_images=gif_frames[1:], duration=100, loop=0, disposal=2, optimize=False)
sheet = Image.new("RGB", (768, 828), "#0d2630")
for q in range(4):
    image = Image.open(SOURCE / f"cycle-q{q}-rfalse-20.png").convert("RGB")
    x, y = (q%2)*384, (q//2)*414
    sheet.paste(image,(x,y+30))
    ImageDraw.Draw(sheet).text((x+12,y+9),f"ROTATION {q*90} / PRODUCTION CHARACTER SCALE",fill="#dce7de")
sheet.save(OUT / "four-rotation-midpoints.png")
checks = {"native_size":[384,384],"rescaled":False,"cycle_frames":41,"fps":10,"directions":[],"power_and_sealed":"full-scene native captures; not inferred from this GIF"}
for q in range(4):
    for reverse in ["false","true"]:
        first = Image.open(SOURCE/f"cycle-q{q}-r{reverse}-00.png").tobytes()
        middle = Image.open(SOURCE/f"cycle-q{q}-r{reverse}-20.png").tobytes()
        assert first != middle
        checks["directions"].append({"rotation":q*90,"reverse":reverse=="true","pixels_change":True})
(OUT/"review-qa.json").write_text(json.dumps(checks,indent=2),encoding="utf-8")
print(OUT)
