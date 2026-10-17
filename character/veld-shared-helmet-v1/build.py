"""Build Veld's shared-helmet idle and walk study from her approved bare clips."""

import json
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BARE = ROOT / "crew-runtime-matte-v1" / "veld"
SOUTH = ROOT / "veld-shared-helmet-south-v1"
SOURCES = {
    "east": ROOT / "veld-helmet-east-fit-v3" / "source.png",
    "west": ROOT / "shared-helmet-standard-v1" / "veld-west-reference.png",
    "north": ROOT / "shared-helmet-standard-v1" / "james-north-reference.png",
}
SIZES = {"east": (34, 38), "west": (34, 38), "north": (33, 35)}
# Veld's accepted side walks sit horizontally apart from their idle sources.
POSITIONS = {
    "idle-east": (82, 17), "walk-east": (70, 15),
    "idle-west": (68, 17), "walk-west": (80, 17),
    "idle-north": (76, 17), "walk-north": (77, 17),
}
HEAD_CLEAR = {
    "idle-east": (80, 19, 119, 48), "walk-east": (69, 18, 107, 48),
    "idle-west": (66, 19, 103, 48), "walk-west": (79, 18, 116, 48),
    "idle-north": (78, 20, 106, 48), "walk-north": (77, 20, 111, 48),
}


def fitted(source: Path, size: tuple[int, int]) -> Image.Image:
    im = Image.open(source).convert("RGBA")
    box = im.getchannel("A").point(lambda a: 255 if a > 24 else 0).getbbox()
    if box is None:
        raise ValueError(source)
    im = im.crop(box).resize(size, Image.Resampling.LANCZOS)
    pixels = np.asarray(im, dtype=np.uint8).copy()
    rgb = pixels[:, :, :3].astype(np.float32)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    skin = (r > g * 1.17) & (g > b * 1.12) & (r > 110)
    rgb[skin] *= np.array([0.83, 0.83, 0.85])
    if source == SOURCES["west"]:
        rgb[skin] *= np.array([1.05, 1.06, 1.06])
    neutral = (np.max(rgb, axis=2) - np.min(rgb, axis=2) < 38) & (rgb.mean(axis=2) > 145)
    if source != SOURCES["north"]:
        neutral[:12, 13:22] = False  # white lamp remains legible
    rgb[neutral] *= 0.86
    pixels[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return Image.fromarray(pixels, "RGBA")


def main() -> None:
    bare = json.loads((BARE / "manifest.json").read_text(encoding="utf-8"))
    helmets = {direction: fitted(source, SIZES[direction]) for direction, source in SOURCES.items()}
    for direction, helmet in helmets.items():
        helmet.save(HERE / f"fitted-{direction}.png")
    result = {k: v for k, v in bare.items() if k != "states"}
    result["name"] = "Veld shared helmet four-direction study v1"
    result["status"] = "installed_shared_helmet_idle_walk"
    result["provenance"] = {k: str(v.relative_to(ROOT)).replace("\\", "/") for k, v in SOURCES.items()}
    result["provenance"]["south"] = "character/veld-shared-helmet-south-v1"
    result["states"] = []
    counts = {}
    for state in bare["states"]:
        key = state["id"]
        motion, direction = key.split("-")
        outf = HERE / "frames" / key
        outf.mkdir(parents=True, exist_ok=True)
        dest_state = {k: v for k, v in state.items() if k != "sourceFrames"}
        dest_state["frameFiles"] = []
        for i, rel in enumerate(state["frameFiles"]):
            body = Image.open(BARE / rel).convert("RGBA")
            if direction == "south":
                composed = Image.open(SOUTH / motion / f"{i:03d}.png").convert("RGBA")
            else:
                composed = body.copy()
                x0, y0, x1, y1 = HEAD_CLEAR[key]
                composed.paste((0, 0, 0, 0), (x0, y0, x1, y1))
                composed.alpha_composite(helmets[direction], POSITIONS[key])
            if composed.crop((0, 58, 184, 184)).tobytes() != body.crop((0, 58, 184, 184)).tobytes():
                raise AssertionError(f"Approved suit changed below head: {key}/{i}")
            dest = outf / f"{i:03d}.png"
            composed.save(dest)
            dest_state["frameFiles"].append(str(dest.relative_to(HERE)).replace("\\", "/"))
        counts[key] = len(dest_state["frameFiles"])
        assert counts[key] == int(state["frameCount"])
        result["states"].append(dest_state)
    (HERE / "manifest.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (HERE / "checks.json").write_text(json.dumps({"counts": counts, "bodyBelow58Exact": True, "installed": True}, indent=2), encoding="utf-8")
    print(f"Veld helmet study: {sum(counts.values())} frames in {len(counts)} states")


if __name__ == "__main__":
    main()
