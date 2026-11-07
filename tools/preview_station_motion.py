"""Package native review captures without resizing physical pixels."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/station-motion-review-v1'
frames = [Image.open(OUT / f'normal-motion-{i:02}-v1.png').convert('RGB').crop((10, 115, 1128, 585)) for i in range(18)]
swatches = Image.new('RGB', (frames[0].width, frames[0].height * len(frames)))
for i, frame in enumerate(frames):
    swatches.paste(frame, (0, i * frame.height))
palette = swatches.quantize(colors=256)
indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
indexed[0].save(OUT / 'busy-station-motion-v1.gif', save_all=True, append_images=indexed[1:], duration=180, loop=0, optimize=False)
rotations = Image.new('RGB', (590, 610))
for q in range(4):
    crop = Image.open(OUT / f'battery-q{q}-active-v1.png').convert('RGB').crop((420, 210, 715, 515))
    rotations.paste(crop, ((q % 2) * 295, (q // 2) * 305))
rotations.save(OUT / 'battery-rotations-v1.png')
print('18 native motion frames; four battery rotations; no physical-pixel resizing')
