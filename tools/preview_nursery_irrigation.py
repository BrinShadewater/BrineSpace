"""Package unchanged native room captures as a review loop; no art synthesis."""
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[1]
source = root / "output/nursery-irrigation-v2"
target = source / "irrigation.gif"
if target.exists():
    raise SystemExit("Preserve earlier review output")
frames = [Image.open(source / f"cycle-room-{i:02d}.png").convert("RGB") for i in range(20)]
assert len({frame.size for frame in frames}) == 1
assert len({frame.tobytes() for frame in frames}) > 1
frames[0].save(target, save_all=True, append_images=frames[1:], duration=111, loop=0)
print(f"Native-size review loop: {target}; {frames[0].size}; 20 frames")
