"""Fit Bill's approved east helmet to his retained east action poses."""

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter
from scipy.ndimage import map_coordinates
from scipy.signal import correlate2d


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / "major-bill-v3"
EQUIPPED = SOURCE / "packs/helmet-184x184-p92-172"
BARE = SOURCE / "packs/bare-184x184-p92-172"
APPROVED = ROOT / "bill-shared-helmet-east-matte-v1"
BARE_IDLE = ROOT / "crew-runtime-matte-v1/bill"
BARE_OUT = ROOT / "bill-action-east-matched-v1"
STATES = ("interact-east", "kneel-east", "repair-east", "stand-east")
TEMPLATE_BOX = (75, 25, 105, 52)
SCALE_Y = 1.026
INTERACT_ARM_POLYGONS = {
    1: [(88, 72), (102, 70), (117, 76), (128, 84), (131, 98), (116, 106), (98, 106), (86, 96)],
    2: [(84, 71), (103, 71), (132, 76), (141, 83), (141, 101), (111, 105), (85, 98)],
    3: [(84, 71), (103, 71), (135, 76), (142, 82), (142, 101), (111, 105), (85, 98)],
    4: [(87, 74), (104, 76), (125, 86), (135, 96), (134, 112), (116, 121), (95, 107), (85, 96)],
}


def locate(image: Image.Image, template: np.ndarray) -> tuple[int, int, float]:
    gray = np.asarray(image.convert("RGB"), dtype=np.float64).mean(axis=2)[15:125, 55:140]
    centered = template - template.mean()
    ones = np.ones_like(template)
    numerator = correlate2d(gray, centered, mode="valid")
    sums = correlate2d(gray, ones, mode="valid")
    squares = correlate2d(gray * gray, ones, mode="valid")
    denominator = np.sqrt(np.maximum((squares - sums * sums / ones.size) * np.sum(centered * centered), 1e-9))
    scores = numerator / denominator
    y, x = np.unravel_index(np.argmax(scores), scores.shape)
    return int(x + 55), int(y + 15), float(scores[y, x])


def register_to_idle(image: Image.Image) -> Image.Image:
    """Bring the retained 151 px east action body to Bill's 155 px idle."""
    rgba = np.asarray(image, dtype=np.float32) / 255
    alpha = rgba[:, :, 3]
    premultiplied = np.dstack((rgba[:, :, :3] * alpha[:, :, None], alpha))
    yy, xx = np.mgrid[:184, :184]
    source_x = xx - 2
    source_y = (yy - 175) / SCALE_Y + 172
    warped = np.dstack([
        map_coordinates(premultiplied[:, :, channel], [source_y, source_x], order=1, mode="constant", cval=0)
        for channel in range(4)
    ])
    out_alpha = warped[:, :, 3:4]
    rgb = np.divide(warped[:, :, :3], out_alpha, out=np.zeros_like(warped[:, :, :3]), where=out_alpha > 1e-5)
    return Image.fromarray(np.clip(np.dstack((rgb, out_alpha)) * 255, 0, 255).astype(np.uint8), "RGBA")


def match_idle_matte(image: Image.Image, lock_red: bool) -> Image.Image:
    """Match retained action cloth and patches to the installed east idle."""
    pixels = np.asarray(image, dtype=np.float32).copy()
    rgb = pixels[:, :, :3]
    luminance = rgb.mean(axis=2)
    target = np.interp(
        luminance,
        [0, 25, 40, 51, 65, 85, 120, 255],
        [0, 15, 30, 41, 54, 74, 109, 244],
    )
    warm = np.clip((rgb[:, :, 0] - rgb[:, :, 2] - 20) / 20, 0, 1)
    target -= warm * 4
    pixels[:, :, :3] = np.clip(
        rgb + (target - luminance)[:, :, None] + np.array([0, -2, 1], dtype=np.float32),
        0,
        255,
    )
    rgb = pixels[:, :, :3]
    luminance = rgb.mean(axis=2)
    neutral = (
        (pixels[:, :, 3] > 200)
        & ((rgb.max(axis=2) - rgb.min(axis=2)) < 12)
        & (luminance > 20) & (luminance < 110)
    )
    if np.count_nonzero(neutral) > 100:
        neutral_delta = np.clip(45 - np.median(luminance[neutral]), -7, 7)
        rgb[neutral] = np.clip(rgb[neutral] + neutral_delta * 0.6, 0, 255)
    if lock_red:
        red = (
            (pixels[:, :, 3] > 200)
            & ((rgb[:, :, 0] - rgb[:, :, 2]) > 20)
            & ((rgb[:, :, 0] - rgb[:, :, 1]) > 10)
            & (luminance > 25) & (luminance < 130)
        )
        if np.count_nonzero(red) > 40:
            red_delta = np.clip(56 - np.median(luminance[red]), -22, 22)
            rgb[red] = np.clip(rgb[red] + red_delta, 0, 255)
    return Image.fromarray(pixels.astype(np.uint8), "RGBA")


def mute_retired_collar(image: Image.Image, tx: int, ty: int) -> Image.Image:
    """Remove the old helmet's bright tan crossbar below the new neck ring."""
    pixels = np.asarray(image, dtype=np.float32).copy()
    for dy in range(35, 43):
        row = pixels[ty + dy, tx - 5:tx + 35]
        red, green, blue, alpha = [row[:, channel] for channel in range(4)]
        old_metal = (
            (alpha > 150) & (red > 65)
            & (red > green + 5) & (red < green + 35)
            & (green > blue + 3) & (green < blue + 26)
        )
        luma = row[:, :3].mean(axis=1)
        row[old_metal, :3] = luma[old_metal, None] * np.array([0.54, 0.55, 0.56])
    return Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8), "RGBA")


def clear_retired_helmet(image: Image.Image, tx: int, ty: int) -> Image.Image:
    pixels = np.asarray(image, dtype=np.uint8).copy()
    pixels[ty - 8:ty + 33, tx - 8:tx + 40] = 0
    return Image.fromarray(pixels, "RGBA")


def selected_helmet(idle: Image.Image) -> Image.Image:
    """Use the accepted idle helmet/face, omitting the stationary shoulder."""
    pixels = np.asarray(idle.crop((69, 18, 114, 58)), dtype=np.uint8).copy()
    return Image.fromarray(pixels, "RGBA")


def seal_neck_join(image: Image.Image, helmet_x: int, helmet_y: int) -> tuple[Image.Image, int]:
    """Bridge isolated one-pixel gaps between the shell ring and old suit."""
    pixels = np.asarray(image, dtype=np.uint8).copy()
    filled = 0
    for y in range(helmet_y + 39, helmet_y + 45):
        for x in range(helmet_x + 9, helmet_x + 38):
            if pixels[y, x, 3] >= 250:
                continue
            above = pixels[y - 1, x].astype(np.float32)
            below = pixels[y + 1, x].astype(np.float32)
            if above[3] < 120 or below[3] < 200:
                continue
            pixels[y, x, :3] = np.clip((above[:3] + below[:3]) / 2, 0, 255).astype(np.uint8)
            pixels[y, x, 3] = 255
            filled += 1
    return Image.fromarray(pixels, "RGBA"), filled


def interact_from_idle(idle: Image.Image, donor: Image.Image, frame: int) -> Image.Image:
    """Move only the retained reaching arm over Bill's accepted idle body.

    Keeping the idle torso, legs, face and helmet avoids a full-body model swap
    on the first interaction frame. The donor arm retains its authored pose.
    """
    mask = Image.new("L", idle.size)
    ImageDraw.Draw(mask).polygon(INTERACT_ARM_POLYGONS[frame], fill=255)
    # Include the shoulder and upper arm, and clear the old hanging arm where
    # the moving donor is transparent.
    ImageDraw.Draw(mask).polygon([(76, 59), (89, 57), (101, 65), (104, 76), (143, 76), (147, 112), (111, 123), (88, 123), (77, 105)], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0.6))
    result = Image.composite(donor, idle, mask)
    result.paste(idle.crop((0, 0, 184, 58)), (0, 0))
    result.paste(idle.crop((0, 125, 184, 184)), (0, 125))
    return result


def main() -> None:
    equipped_pack = json.loads((EQUIPPED / "manifest.json").read_text(encoding="utf-8"))
    bare_pack = json.loads((BARE / "manifest.json").read_text(encoding="utf-8"))
    equipped_states = {s["id"]: s for s in equipped_pack["states"]}
    bare_states = {s["id"]: s for s in bare_pack["states"]}
    approved_pack = json.loads((APPROVED / "manifest.json").read_text(encoding="utf-8"))
    approved_idle_state = next(s for s in approved_pack["states"] if s["id"] == "idle-east")
    approved_idle = Image.open(APPROVED / approved_idle_state["frameFiles"][0]).convert("RGBA")
    bare_idle_pack = json.loads((BARE_IDLE / "manifest.json").read_text(encoding="utf-8"))
    bare_idle_state = next(s for s in bare_idle_pack["states"] if s["id"] == "idle-east")
    bare_idle = Image.open(BARE_IDLE / bare_idle_state["frameFiles"][0]).convert("RGBA")
    head = selected_helmet(approved_idle)
    reference = Image.open(EQUIPPED / equipped_states["interact-east"]["frameFiles"][0]).convert("RGBA")
    x0, y0, x1, y1 = TEMPLATE_BOX
    template = np.asarray(reference.convert("RGB"), dtype=np.float64).mean(axis=2)[y0:y1, x0:x1]

    result = {k: v for k, v in equipped_pack.items() if k != "states"}
    result.update(name="Bill shared-helmet east action study", status="east_action_helmet_review", states=[])
    bare_result = {k: v for k, v in bare_pack.items() if k != "states"}
    bare_result.update(name="Bill registered east action body", status="matched_to_installed_east_idle", states=[])
    checks = {}
    for key in STATES:
        state = dict(equipped_states[key])
        bare_state = dict(bare_states[key])
        if state["frameDurationsMs"] != bare_state["frameDurationsMs"]:
            raise AssertionError(f"Bare/equipped timing differs: {key}")
        state["frameFiles"] = []
        state["frameCount"] = len(equipped_states[key]["frameFiles"])
        state["provenance"] = "retained east action pose plus accepted Bill east helmet"
        bare_state["frameFiles"] = []
        bare_state["frameCount"] = len(bare_states[key]["frameFiles"])
        equipped_folder = HERE / "frames" / key
        equipped_folder.mkdir(parents=True, exist_ok=True)
        bare_folder = BARE_OUT / "frames" / key
        bare_folder.mkdir(parents=True, exist_ok=True)
        positions = []
        for i, rel in enumerate(equipped_states[key]["frameFiles"]):
            source = Image.open(EQUIPPED / rel).convert("RGBA")
            tx, ty, score = locate(source, template)
            if score < 0.55:
                raise AssertionError(f"Uncertain head anchor {key}/{i}: {score:.3f}")
            body = match_idle_matte(register_to_idle(clear_retired_helmet(mute_retired_collar(source, tx, ty), tx, ty)), True)
            hx = 69 + tx - 75
            hy = 18 + round((ty - 25) * SCALE_Y)
            body.alpha_composite(head, (hx, hy))
            body, seal_pixels = seal_neck_join(body, hx, hy)
            bare_source = Image.open(BARE / bare_states[key]["frameFiles"][i]).convert("RGBA")
            bare_body = match_idle_matte(register_to_idle(bare_source), False)
            # Use the matching uncovered suit rather than retaining fragments
            # of the obsolete equipped collar across the shoulder/chest.
            body = match_idle_matte(register_to_idle(bare_source), True)
            pixels = np.asarray(body).copy()
            pixels[:hy + 35, hx + 3:hx + 58] = 0
            pixels[hy + 35:hy + 40, hx + 36:hx + 58] = 0
            body = Image.fromarray(pixels, "RGBA")
            body.alpha_composite(head, (hx, hy))
            body, seal_pixels = seal_neck_join(body, hx, hy)
            if key == "interact-east" and i in INTERACT_ARM_POLYGONS:
                body = interact_from_idle(approved_idle, body, i)
                bare_body = interact_from_idle(bare_idle, bare_body, i)
            if (key in ("interact-east", "kneel-east") and i == 0) or (key in ("interact-east", "stand-east") and i == 5):
                body = approved_idle.copy()
                bare_body = bare_idle.copy()
            dest = equipped_folder / f"{i:03d}.png"
            body.save(dest)
            state["frameFiles"].append(str(dest.relative_to(HERE)).replace("\\", "/"))
            bare_dest = bare_folder / f"{i:03d}.png"
            bare_body.save(bare_dest)
            bare_state["frameFiles"].append(str(bare_dest.relative_to(BARE_OUT)).replace("\\", "/"))
            positions.append({"frame": i, "template": [tx, ty], "helmet": [hx, hy], "neckSealPixels": seal_pixels, "match": round(score, 3)})
        result["states"].append(state)
        bare_result["states"].append(bare_state)
        checks[key] = positions
    (HERE / "manifest.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (HERE / "checks.json").write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")
    (BARE_OUT / "manifest.json").write_text(json.dumps(bare_result, indent=2) + "\n", encoding="utf-8")
    print(f"Bill east action study: {sum(map(len, checks.values()))} frames; minimum anchor score {min(p['match'] for v in checks.values() for p in v):.3f}")


if __name__ == "__main__":
    main()
