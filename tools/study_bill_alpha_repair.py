"""Stage only enclosed lower-body alpha repairs; never edits production files."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy.ndimage import binary_fill_holes, distance_transform_edt, label
from repair_bill_walk import build

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/bill-pixel-layer-2026-09-21/alpha-repair"
SOURCE = ROOT / "output/bill-body-motion-2026-09-20"

def repair(image):
    pixels = np.array(image)
    solid = pixels[:, :, 3] > 0
    holes = binary_fill_holes(solid) & ~solid
    holes[:119] = False
    components, count = label(holes)
    sizes = [int((components == i).sum()) for i in range(1, count + 1)]
    if any(size > 32 for size in sizes):
        raise ValueError("Large enclosed region requires explicit art review")
    _, nearest = distance_transform_edt(~solid, return_indices=True)
    result = pixels.copy()
    result[holes] = pixels[nearest[0][holes], nearest[1][holes]]
    assert np.array_equal(result[solid], pixels[solid])
    assert np.array_equal(result[:119], pixels[:119])
    return Image.fromarray(result), sizes

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = {}
    sheet = Image.new("RGBA", (184 * 3, 184 * 2), "#26383c")
    slot = 0
    for direction in ("east", "west"):
        source = Image.open(SOURCE / f"{direction}-preserved-0.png").convert("RGBA")
        frames, *_ = build(source, direction)
        for index, before in enumerate(frames):
            preserved = OUT / f"bare-{index:03}-before.png"
            if direction == "west" and preserved.exists():
                before = Image.open(preserved).convert("RGBA")
            after, sizes = repair(before)
            after.save(OUT / f"{direction}-{index:02}.png")
            report[f"{direction}-{index}"] = {"filled_pixels": sum(sizes), "hole_sizes": sizes}
            if sizes:
                sheet.alpha_composite(before, (slot * 184, 0))
                sheet.alpha_composite(after, (slot * 184, 184))
                slot += 1
    sheet.resize((1104, 736), Image.Resampling.NEAREST).save(OUT / "comparison.png")
    (OUT / "report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report))

if __name__ == "__main__":
    main()
