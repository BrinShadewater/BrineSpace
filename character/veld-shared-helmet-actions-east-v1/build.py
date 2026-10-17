"""Fit Veld's shared helmet to the retained east action poses."""

import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.signal import correlate2d
from scipy.ndimage import map_coordinates


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
CATALOG = ROOT / "dr-veld-v2"
HELMET = ROOT / "veld-shared-helmet-v1" / "fitted-east.png"
STATES = ("interact-east", "kneel-east", "repair-east", "stand-east")
# Match the helmet neck ring to the shoulder/collar as the body pitches
# forward. The old uncovered head moves farther forward than the suit neck.
# Keep identical offsets where action clips share an exact endpoint pose.
POSE_FIT = {
    "interact-east": [(0, 0), (-1, 1), (-2, 1), (-2, 1), (-1, 1), (0, 0)],
    "kneel-east": [(0, 0), (-1, 0), (-2, 1), (-3, 1), (-3, 1), (-3, 1)],
    "repair-east": [(-3, 1)] * 6,
    "stand-east": [(-3, 1), (-3, 1), (-3, 1), (-2, 1), (-1, 0), (0, 0)],
}


def align_to_installed_idle(image: Image.Image) -> Image.Image:
    """Match the retained 146 px action profile to the 155 px installed idle."""
    pixels = np.asarray(image, dtype=np.float32) / 255.0
    alpha = pixels[:, :, 3]
    premultiplied = np.dstack((pixels[:, :, :3] * alpha[:, :, None], alpha))
    yy, xx = np.mgrid[:184, :184]
    source_y = (yy - 172.0) / 1.06 + 172.0
    source_x = (xx - 104.0) / 1.10 + 92.0
    warped = np.dstack([
        map_coordinates(premultiplied[:, :, channel], [source_y, source_x], order=1, mode="constant", cval=0)
        for channel in range(4)
    ])
    out_alpha = warped[:, :, 3:4]
    rgb = np.divide(warped[:, :, :3], out_alpha, out=np.zeros_like(warped[:, :, :3]), where=out_alpha > 1e-5)
    return Image.fromarray(np.clip(np.dstack((rgb, out_alpha)) * 255, 0, 255).astype(np.uint8), "RGBA")


def seal_rear_neck(image: Image.Image, helmet_x: int, helmet_y: int) -> tuple[Image.Image, int]:
    """Fill only the narrow transparent gap between the neck ring and suit."""
    pixels = np.asarray(image, dtype=np.uint8).copy()
    filled = 0
    x0, x1 = max(0, helmet_x - 10), min(image.width, helmet_x + 13)
    segments = []
    for y in range(max(0, helmet_y + 27), min(image.height, helmet_y + 39)):
        opaque = np.flatnonzero(pixels[y, x0:x1, 3] > 20) + x0
        for left, right in zip(opaque[:-1], opaque[1:]):
            gap = int(right - left - 1)
            if not 1 <= gap <= 7 or left > helmet_x + 1 or right < helmet_x + 3:
                continue
            if not helmet_x - 3 <= (left + right) / 2 <= helmet_x + 7:
                continue
            segments.append((y, int(left), int(right)))
    runs = []
    for segment in segments:
        if not runs or segment[0] > runs[-1][-1][0] + 1:
            runs.append([])
        runs[-1].append(segment)
    for run in runs:
        for row_index, (y, left, right) in enumerate(run):
            # Ease the upper edge into the helmet rather than leaving a flat
            # rectangular lip behind the neck as the character bends.
            opacity = round(235 * (row_index + 1) / len(run))
            for x in range(int(left) + 1, int(right)):
                toward_helmet = (x - left) / (right - left)
                pixels[y, x] = (
                    round(42 + 20 * toward_helmet),
                    round(46 + 19 * toward_helmet),
                    round(49 + 17 * toward_helmet),
                    opacity,
                )
                filled += 1
    return Image.fromarray(pixels, "RGBA"), filled


def gray(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB"), dtype=np.float64).mean(axis=2)


def locate(image: np.ndarray, template: np.ndarray) -> tuple[int, int, float]:
    region = image[15:130, 60:125]
    centered = template - template.mean()
    ones = np.ones_like(template)
    numerator = correlate2d(region, centered, mode="valid")
    sums = correlate2d(region, ones, mode="valid")
    squares = correlate2d(region * region, ones, mode="valid")
    denominator = np.sqrt(np.maximum((squares - sums * sums / ones.size) * np.sum(centered * centered), 1e-9))
    scores = numerator / denominator
    y, x = np.unravel_index(np.argmax(scores), scores.shape)
    return int(x + 60), int(y + 15), float(scores[y, x])


def main() -> None:
    catalog = json.loads((CATALOG / "catalog.json").read_text(encoding="utf-8"))
    root = None
    states = {}
    for rel in catalog["equipment"]:
        path = CATALOG / rel
        pack = json.loads(path.read_text(encoding="utf-8"))
        selected = {s["id"]: s for s in pack["states"] if s["id"] in STATES}
        if selected:
            if root is not None:
                raise AssertionError("Action states split across profiles")
            root = path.parent
            profile = pack
            states = selected
    if root is None or set(states) != set(STATES):
        raise AssertionError("Missing Veld east action states")
    reference = gray(root / states["interact-east"]["frameFiles"][0])
    template = reference[28:39, 78:99]
    helmet = Image.open(HELMET).convert("RGBA")
    assert helmet.size == (34, 38)
    result = {k: v for k, v in profile.items() if k != "states"}
    result["name"] = "Veld common-helmet east action study"
    result["status"] = "installed_east_action_helmet"
    result["textureFilter"] = "linear"
    result["states"] = []
    idle_pack = json.loads((ROOT / "veld-shared-helmet-v1" / "manifest.json").read_text(encoding="utf-8"))
    idle_state = next(s for s in idle_pack["states"] if s["id"] == "idle-east")
    idle = Image.open(ROOT / "veld-shared-helmet-v1" / idle_state["frameFiles"][0]).convert("RGBA")
    checks = {}
    for key in STATES:
        original = states[key]
        dest_state = dict(original)
        dest_state["frameFiles"] = []
        dest_state["frameCount"] = len(original["frameFiles"])
        dest_state["provenance"] = "retained action body plus Veld shared east helmet"
        folder = HERE / "frames" / key
        folder.mkdir(parents=True, exist_ok=True)
        positions = []
        for i, rel in enumerate(original["frameFiles"]):
            source = root / rel
            body = Image.open(source).convert("RGBA")
            tx, ty, score = locate(gray(source), template)
            if score < 0.72:
                raise AssertionError(f"Uncertain helmet anchor: {key}/{i} {score:.3f}")
            dx, dy = POSE_FIT[key][i]
            hx, hy = tx - 6 + dx, ty - 2 + dy
            composed = body.copy()
            # Keep the original suit collar beneath the shared helmet's neck
            # ring so the head stays seated throughout the crouch/stand arc.
            clear = (tx - 9, ty - 3, tx + 30, ty + 31)
            composed.paste((0, 0, 0, 0), clear)
            composed.alpha_composite(helmet, (hx, hy))
            # Retained action sources still have tan suit fittings directly below
            # the collar; shift those fittings into Veld's muted silver range.
            pixels = np.asarray(composed, dtype=np.uint8).copy()
            x0, x1 = tx - 10, tx + 27
            y0, y1 = ty + 33, ty + 48
            patch = pixels[y0:y1, x0:x1, :3].astype(np.float32)
            red, green, blue = patch[:, :, 0], patch[:, :, 1], patch[:, :, 2]
            warm = (red > green * 1.17) & (green > blue * 1.06) & (red > 70) & (blue < 120)
            luma = red * 0.25 + green * 0.5 + blue * 0.25
            for channel, factor in enumerate((0.92, 0.93, 0.94)):
                patch[:, :, channel][warm] = luma[warm] * factor
            pixels[y0:y1, x0:x1, :3] = np.clip(patch, 0, 255).astype(np.uint8)
            composed = Image.fromarray(pixels, "RGBA")
            if body.crop((0, 0, 184, max(0, ty - 3))).tobytes() != composed.crop((0, 0, 184, max(0, ty - 3))).tobytes():
                raise AssertionError("Pixels above local helmet changed")
            composed = align_to_installed_idle(composed)
            fitted_x = round((hx - 92) * 1.10 + 104)
            fitted_y = round((hy - 172) * 1.06 + 172)
            composed, seal_pixels = seal_rear_neck(composed, fitted_x, fitted_y)
            if (key in ("interact-east", "kneel-east") and i == 0) or (key in ("interact-east", "stand-east") and i == len(original["frameFiles"]) - 1):
                composed = idle.copy()
            dest = folder / f"{i:03d}.png"
            composed.save(dest)
            dest_state["frameFiles"].append(str(dest.relative_to(HERE)).replace("\\", "/"))
            positions.append({"frame": i, "template": [tx, ty], "helmet": [hx, hy], "neckFit": [dx, dy], "neckSealPixels": seal_pixels, "match": round(score, 3)})
        checks[key] = positions
        result["states"].append(dest_state)
    (HERE / "manifest.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (HERE / "checks.json").write_text(json.dumps(checks, indent=2), encoding="utf-8")
    print(f"Veld east action helmet candidate: {sum(len(v) for v in checks.values())} frames; minimum anchor score {min(p['match'] for v in checks.values() for p in v):.3f}")


if __name__ == "__main__":
    main()
