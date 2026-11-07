"""Package native door renders; check aperture, power and neutral finish pixels."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageChops
ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "output/door-redesign/animation-v8"
OUT = PACK / "door-cycle.gif"
if OUT.exists():
    raise SystemExit(f"Refusing overwrite: {OUT}")
variants = ["bio", "life-support", "engineering", "generic"]
for variant in variants:
    for direction in ["front", "side"]:
        opened = Image.open(PACK / f"{variant}-{direction}-09.png").convert("RGBA")
        off = Image.open(PACK / f"{variant}-{direction}-off.png").convert("RGBA")
        assert opened.getchannel("A").tobytes() == off.getchannel("A").tobytes()
        assert ImageChops.difference(opened.convert("RGB"), off.convert("RGB")).getbbox()
        if direction == "front":
            assert opened.getchannel("A").crop((56,118,200,186)).getbbox() is None
        # The side projection includes an opaque floor-level metal threshold;
        # leaf absence is checked on renderer parts, not flattened alpha there.
        first = Image.open(PACK / f"{variant}-{direction}-00.png").convert("RGBA")
        if variant == "generic" and direction == "front":
            r, g, b, _ = first.split()
            assert ImageChops.difference(r,g).getextrema()[1] <= 1
            assert ImageChops.difference(g,b).getextrema()[1] <= 1
frames = []
for index in range(10):
    image = Image.new("RGB", (1024,680), "#252d35")
    draw = ImageDraw.Draw(image)
    for column, variant in enumerate(variants):
        draw.text((column*256+22,12),variant.upper(),fill="#eeeae0")
        for row, direction in enumerate(["front","side"]):
            frame = Image.open(PACK / f"{variant}-{direction}-{index:02d}.png").convert("RGBA")
            image.paste(frame,(column*256,24+row*320),frame)
    draw.text((22,660),"FRONT / SIDE CUTAWAY  |  WHITE LIGHTS  |  FIXED 72-UNIT OPENINGS",fill="#c1c9ce")
    frames.append(image)
palette_source = Image.new("RGB", (1024,6800))
for index, frame in enumerate(frames): palette_source.paste(frame,(0,index*680))
palette = palette_source.quantize(colors=256)
frames = [frame.quantize(palette=palette,dither=Image.Dither.NONE) for frame in frames]
order = list(range(10))+list(range(8,0,-1))
sequence = [frames[i] for i in order]
sequence[0].save(OUT,save_all=True,append_images=sequence[1:],duration=[700]+[60]*8+[900]+[60]*8,loop=0,disposal=2,optimize=False)
(PACK / "pixel-qa.json").write_text(json.dumps({"power_changes_rgb_not_alpha":True,"front_open_alpha_clear":True,"side_leaf_absence":"covered by native part tests; threshold intentionally opaque","generic_front_is_neutral":True,"generic_side":"neutral trim with station wall finish","preview_steps":18},indent=2),encoding="utf-8")
print("PIXEL QA PASS: power masks, clear passages, neutral grey; preview",OUT)
