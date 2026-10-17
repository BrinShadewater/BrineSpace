"""Tone Bill's selected east helmet consistently across idle and walk."""

import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.signal import correlate2d


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / "bill-shared-helmet-runtime-v2"
STATES = ("idle-east", "walk-east")
TEMPLATE_BOX = (75, 25, 105, 52)


def locate(image: Image.Image, template: np.ndarray) -> tuple[int, int, float]:
    gray = np.asarray(image.convert("RGB"), dtype=np.float64).mean(axis=2)[12:100, 58:130]
    centered = template - template.mean()
    ones = np.ones_like(template)
    numerator = correlate2d(gray, centered, mode="valid")
    sums = correlate2d(gray, ones, mode="valid")
    squares = correlate2d(gray * gray, ones, mode="valid")
    denominator = np.sqrt(np.maximum((squares - sums * sums / ones.size) * np.sum(centered * centered), 1e-9))
    scores = numerator / denominator
    y, x = np.unravel_index(np.argmax(scores), scores.shape)
    return int(x + 58), int(y + 12), float(scores[y, x])


def darken_shell(image: Image.Image, tx: int, ty: int) -> Image.Image:
    pixels = np.asarray(image, dtype=np.float32).copy()
    yy, xx = np.indices(pixels.shape[:2])
    rgb = pixels[:, :, :3]
    luminance = rgb.mean(axis=2)
    shell = (
        (pixels[:, :, 3] > 15)
        & (xx >= tx - 6) & (xx < tx + 40)
        & (yy >= ty - 7) & (yy < ty + 35)
    )
    # Keep Bill's face, visor interior and white lamp from the accepted source.
    face = (xx >= tx + 19) & (yy >= ty + 4) & (yy < ty + 29)
    lamp = (luminance > 175) & ((rgb.max(axis=2) - rgb.min(axis=2)) < 25)
    shoulder = (yy >= ty + 30) & (xx < tx + 8)
    shell &= ~(face | lamp | shoulder)
    rgb[shell] *= 0.88
    return Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8), "RGBA")


def main() -> None:
    original = json.loads((SOURCE / "manifest.json").read_text(encoding="utf-8"))
    source_states = {s["id"]: s for s in original["states"]}
    reference = Image.open(SOURCE / source_states["idle-east"]["frameFiles"][0]).convert("RGBA")
    x0, y0, x1, y1 = TEMPLATE_BOX
    template = np.asarray(reference.convert("RGB"), dtype=np.float64).mean(axis=2)[y0:y1, x0:x1]
    result = {k: v for k, v in original.items() if k != "states"}
    result.update(name="Bill darker matte east helmet study", status="east_helmet_matte_review", states=[])
    checks = {}
    for key in STATES:
        state = dict(source_states[key])
        state["frameFiles"] = []
        state["provenance"] = "accepted Bill east helmet with graphite shell tone reduced 12 percent"
        folder = HERE / "frames" / key
        folder.mkdir(parents=True, exist_ok=True)
        positions = []
        for i, rel in enumerate(source_states[key]["frameFiles"]):
            image = Image.open(SOURCE / rel).convert("RGBA")
            tx, ty, score = locate(image, template)
            if score < 0.96:
                raise AssertionError(f"Uncertain Bill east helmet anchor {key}/{i}: {score:.3f}")
            adjusted = darken_shell(image, tx, ty)
            dest = folder / f"{i:03d}.png"
            adjusted.save(dest)
            state["frameFiles"].append(str(dest.relative_to(HERE)).replace("\\", "/"))
            positions.append({"frame": i, "template": [tx, ty], "match": round(score, 3)})
        result["states"].append(state)
        checks[key] = positions
    (HERE / "manifest.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (HERE / "checks.json").write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")
    print(f"Bill darker east helmet: {sum(map(len, checks.values()))} idle/walk frames; minimum anchor score {min(p['match'] for v in checks.values() for p in v):.3f}")


if __name__ == "__main__":
    main()
