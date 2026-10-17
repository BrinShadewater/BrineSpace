"""Fit Veld's selected south helmet to her retained south action motion."""

import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates
from scipy.signal import correlate2d


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
ORIGINAL = ROOT / "dr-veld-v2/packs/helmet-256x256-p128.0-224.0"
BARE_ORIGINAL = ROOT / "dr-veld-v2/packs/bare-256x256-p128.0-224.0"
BARE_IDLE = ROOT / "crew-runtime-matte-v1/veld"
BARE_HERE = ROOT / "veld-action-south-matched-v1"
SHARED = ROOT / "veld-shared-helmet-v1"
SOUTH_HELMET = ROOT / "veld-shared-helmet-south-v1/fitted-helmet.png"
STATES = ("interact-south", "kneel-south", "repair-south", "stand-south")
TEMPLATE_BOX = (110, 79, 146, 99)


def locate(image: Image.Image, template: np.ndarray) -> tuple[int, int, float]:
    gray = np.asarray(image.convert("RGB"), dtype=np.float64).mean(axis=2)[70:155, 95:165]
    centered = template - template.mean()
    ones = np.ones_like(template)
    numerator = correlate2d(gray, centered, mode="valid")
    sums = correlate2d(gray, ones, mode="valid")
    squares = correlate2d(gray * gray, ones, mode="valid")
    denominator = np.sqrt(np.maximum((squares - sums * sums / ones.size) * np.sum(centered * centered), 1e-9))
    scores = numerator / denominator
    y, x = np.unravel_index(np.argmax(scores), scores.shape)
    return int(x + 95), int(y + 70), float(scores[y, x])


def register_to_idle(image: Image.Image) -> Image.Image:
    """Match the old 148 px front action body to the installed 155 px south idle."""
    rgba = np.asarray(image, dtype=np.float32) / 255
    alpha = rgba[:, :, 3]
    premultiplied = np.dstack((rgba[:, :, :3] * alpha[:, :, None], alpha))
    yy, xx = np.mgrid[:184, :184]
    source_x = (xx - 94) / 0.91 + 128
    source_y = (yy - 172) / 1.06 + 224
    warped = np.dstack([
        map_coordinates(premultiplied[:, :, channel], [source_y, source_x], order=1, mode="constant", cval=0)
        for channel in range(4)
    ])
    out_alpha = warped[:, :, 3:4]
    rgb = np.divide(warped[:, :, :3], out_alpha, out=np.zeros_like(warped[:, :, :3]), where=out_alpha > 1e-5)
    return Image.fromarray(np.clip(np.dstack((rgb, out_alpha)) * 255, 0, 255).astype(np.uint8), "RGBA")


def main() -> None:
    old = json.loads((ORIGINAL / "manifest.json").read_text(encoding="utf-8"))
    old_states = {s["id"]: s for s in old["states"]}
    old_bare = json.loads((BARE_ORIGINAL / "manifest.json").read_text(encoding="utf-8"))
    old_bare_states = {s["id"]: s for s in old_bare["states"]}
    shared = json.loads((SHARED / "manifest.json").read_text(encoding="utf-8"))
    idle_state = next(s for s in shared["states"] if s["id"] == "idle-south")
    idle = Image.open(SHARED / idle_state["frameFiles"][0]).convert("RGBA")
    bare_idle_pack = json.loads((BARE_IDLE / "manifest.json").read_text(encoding="utf-8"))
    bare_idle_state = next(s for s in bare_idle_pack["states"] if s["id"] == "idle-south")
    bare_idle = Image.open(BARE_IDLE / bare_idle_state["frameFiles"][0]).convert("RGBA")
    helmet = Image.open(SOUTH_HELMET).convert("RGBA")
    assert helmet.size == (35, 39)
    reference = Image.open(ORIGINAL / old_states["interact-south"]["frameFiles"][0]).convert("RGBA")
    x0, y0, x1, y1 = TEMPLATE_BOX
    template = np.asarray(reference.convert("RGB"), dtype=np.float64).mean(axis=2)[y0:y1, x0:x1]

    result = {k: v for k, v in shared.items() if k != "states"}
    result["name"] = "Veld common-helmet south action study"
    result["status"] = "installed_south_action_helmet"
    result["states"] = []
    bare_result = {k: v for k, v in bare_idle_pack.items() if k != "states"}
    bare_result["name"] = "Veld registered south action body"
    bare_result["status"] = "matched_to_installed_south_idle"
    bare_result["states"] = []
    checks = {}
    for key in STATES:
        source_state = old_states[key]
        dest_state = dict(source_state)
        dest_state["frameFiles"] = []
        dest_state["provenance"] = "retained south action body and selected Veld south helmet"
        bare_source_state = old_bare_states[key]
        if bare_source_state["frameDurationsMs"] != source_state["frameDurationsMs"]:
            raise AssertionError(f"Bare/equipped action timing differs: {key}")
        bare_state = dict(bare_source_state)
        bare_state["frameFiles"] = []
        bare_state["provenance"] = "retained bare south action registered to installed idle"
        folder = HERE / "frames" / key
        folder.mkdir(parents=True, exist_ok=True)
        bare_folder = BARE_HERE / "frames" / key
        bare_folder.mkdir(parents=True, exist_ok=True)
        positions = []
        for i, rel in enumerate(source_state["frameFiles"]):
            source = Image.open(ORIGINAL / rel).convert("RGBA")
            tx, ty, score = locate(source, template)
            if score < 0.70:
                raise AssertionError(f"Uncertain head anchor {key}/{i}: {score:.3f}")
            body = source.copy()
            body.paste((0, 0, 0, 0), (tx - 1, ty - 4, tx + 38, ty + 29))
            composed = register_to_idle(body)
            bare_body = Image.open(BARE_ORIGINAL / bare_source_state["frameFiles"][i]).convert("RGBA")
            bare_composed = register_to_idle(bare_body)
            hx = round((tx - x0) * 0.91 + 76)
            hy = round((ty - y0) * 1.06 + 17)
            composed.alpha_composite(helmet, (hx, hy))
            if (key in ("interact-south", "kneel-south") and i == 0) or (key in ("interact-south", "stand-south") and i == 5):
                composed = idle.copy()
                bare_composed = bare_idle.copy()
            dest = folder / f"{i:03d}.png"
            composed.save(dest)
            dest_state["frameFiles"].append(str(dest.relative_to(HERE)).replace("\\", "/"))
            bare_dest = bare_folder / f"{i:03d}.png"
            bare_composed.save(bare_dest)
            bare_state["frameFiles"].append(str(bare_dest.relative_to(BARE_HERE)).replace("\\", "/"))
            positions.append({"frame": i, "template": [tx, ty], "helmet": [hx, hy], "match": round(score, 3)})
        checks[key] = positions
        result["states"].append(dest_state)
        bare_result["states"].append(bare_state)
    (HERE / "manifest.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (HERE / "checks.json").write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")
    (BARE_HERE / "manifest.json").write_text(json.dumps(bare_result, indent=2) + "\n", encoding="utf-8")
    print(f"Veld south action study: {sum(map(len, checks.values()))} frames; minimum anchor score {min(p['match'] for v in checks.values() for p in v):.3f}")


if __name__ == "__main__":
    main()
