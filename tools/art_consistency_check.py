"""Flag art that will look inconsistent in game, before it goes in (owner, Sept 26).

Two checks, both read-only:
  crew   Each character's clips against that character's typical clip: brightness,
         contrast and colour of opaque pixels (Lab). The Sept 26 bunk clips were painted
         darker and crisper than the walk cycles and visibly changed colour on climbing in.
  props  Pixel density (source pixels per world unit) of every station prop against the
         catalog median, and the crew's density beside it. Mixed densities read as
         mixed art styles once scaled to the same station.

  python tools/art_consistency_check.py            # both checks, flagged items only
  python tools/art_consistency_check.py crew --all # every clip, flagged or not
  python tools/art_consistency_check.py --strict   # exit 1 when anything is flagged
"""
from pathlib import Path
import argparse
import json
import statistics
import sys

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CREW = ["major-bill-v3", "dr-veld-v2", "chief-engineer-branforth-v2", "marsh-v2"]
OPAQUE = 200
# Differences a player notices at station scale (Lab units; contrast is a ratio).
MAX_BRIGHTNESS = 3.0
MAX_COLOUR = 3.0
CONTRAST_RANGE = (0.85, 1.18)
DENSITY_RANGE = (0.8, 1.25)
STANDING_WORLD_UNITS = 65.28  # grid_canvas: cell * 0.17 per standing height, CELL 384


def _lab(rgb):
    c = rgb / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 216 / 24389, np.cbrt(xyz), (24389 / 27 * xyz + 16) / 116)
    return np.stack([116 * f[:, 1] - 16, 500 * (f[:, 0] - f[:, 1]), 200 * (f[:, 1] - f[:, 2])], axis=1)


def clip_stats(paths):
    pixels = []
    for path in paths:
        rgba = np.asarray(Image.open(path).convert("RGBA"), dtype=np.float64).reshape(-1, 4)
        pixels.append(rgba[rgba[:, 3] > OPAQUE, :3])
    pixels = np.concatenate(pixels) if pixels else np.zeros((0, 3))
    if len(pixels) == 0:
        return None
    lab = _lab(pixels)
    return {"L": lab[:, 0].mean(), "contrast": lab[:, 0].std(), "a": lab[:, 1].mean(), "b": lab[:, 2].mean()}


def clips(revision: Path, variant: str):
    """Every folder of frames for one variant (bare/helmet): state clips and supplements."""
    found = {}
    for folder in sorted((revision / "frames" / variant).glob("*")):
        if folder.is_dir():
            found[folder.name] = sorted(folder.glob("*.png"))
    for folder in sorted((revision / "supplemental").glob(f"*/{variant}")):
        found["supplemental/" + folder.parent.name] = sorted(folder.glob("*.png"))
    return {k: v for k, v in found.items() if v}


def facing(key: str) -> str:
    """Last direction word in a clip name; turns and unnamed clips share one group."""
    for word in reversed(key.replace("/", "-").split("-")):
        if word in ["north", "south", "east", "west"]:
            return word
    return "other"


def check_crew(show_all: bool) -> int:
    """Compare each clip with the character's typical clip (the median over all clips).

    The walk cycle was the first reference tried, but on Sept 26 it proved to be the odd
    one out itself (lighter and flatter than nearly every other clip), so every clip
    differed from it. A clip is flagged only when it is also an outlier among its siblings.
    """
    flagged = 0
    for name in CREW:
        revision = ROOT / "character" / name
        for variant in ["bare", "helmet"]:
            stats = {key: clip_stats(paths) for key, paths in clips(revision, variant).items()}
            stats = {key: value for key, value in stats.items() if value is not None}
            if len(stats) < 3:
                continue
            # Compare within a facing: a north clip shows the back, which is naturally darker.
            groups: dict = {}
            for key in stats:
                groups.setdefault(facing(key), []).append(key)
            typical_by = {}
            for group, keys in groups.items():
                pool = keys if len(keys) >= 3 else list(stats)
                typical_by[group] = {m: statistics.median(stats[k][m] for k in pool) for m in ["L", "contrast", "a", "b"]}
            typical = {m: statistics.median(v[m] for v in stats.values()) for m in ["L", "contrast", "a", "b"]}
            spread_l = statistics.median(abs(v["L"] - typical_by[facing(k)]["L"]) for k, v in stats.items()) or 0.5
            rows = []
            for key, value in stats.items():
                typical = typical_by[facing(key)]
                d_l = value["L"] - typical["L"]
                d_colour = float(np.hypot(value["a"] - typical["a"], value["b"] - typical["b"]))
                ratio = value["contrast"] / max(typical["contrast"], 1e-6)
                bad = (abs(d_l) > max(MAX_BRIGHTNESS, 3 * spread_l) or d_colour > MAX_COLOUR
                       or not CONTRAST_RANGE[0] <= ratio <= CONTRAST_RANGE[1])
                if bad or show_all:
                    rows.append((abs(d_l) + d_colour + abs(ratio - 1) * 10, key, d_l, d_colour, ratio, bad))
            typical = {m: statistics.median(v[m] for v in stats.values()) for m in ["L", "contrast", "a", "b"]}
            walk = [v for key, v in stats.items() if key.startswith("walk-")]
            flagged += sum(1 for row in rows if row[5])
            if rows or show_all:
                print(f"\n{name} ({variant}) vs its typical clip, same facing ({len(stats)} clips)")
                if walk:
                    w_l = statistics.mean(v["L"] for v in walk) - typical["L"]
                    w_c = statistics.mean(v["contrast"] for v in walk) / typical["contrast"]
                    print(f"  info walk cycle overall                 brightness {w_l:+5.1f}                    contrast x{w_c:.2f}")
                for _, key, d_l, d_colour, ratio, bad in sorted(rows, reverse=True)[: None if show_all else 12]:
                    mark = "FLAG" if bad else "ok  "
                    print(f"  {mark} {key:<34} brightness {d_l:+5.1f}  colour shift {d_colour:4.1f}  contrast x{ratio:.2f}")
    return flagged


def check_props(show_all: bool) -> int:
    catalog = json.loads((ROOT / "rooms/station-props-v2/props.json").read_text(encoding="utf-8"))
    densities = []
    for prop in catalog:
        width = float(prop.get("display_width", 0) or 0)
        if width > 0:
            densities.append((float(prop["region"][2]) / width, prop["id"]))
    median = statistics.median(d for d, _ in densities)
    print(f"\nStation props: median {median:.2f} source px per world unit across {len(densities)} props")
    for name in CREW:
        manifest = ROOT / "character" / name / "catalog.json"
        if manifest.exists():
            height = float(json.loads(manifest.read_text(encoding="utf-8")).get("standingHeight", 74))
            density = height / STANDING_WORLD_UNITS
            note = "FLAG" if not DENSITY_RANGE[0] <= density / median <= DENSITY_RANGE[1] else "ok  "
            print(f"  {note} crew {name:<32} {density:.2f} px/unit (x{density / median:.2f} of props)")
    flagged = 0
    for density, prop_id in sorted(densities, key=lambda item: abs(item[0] / median - 1), reverse=True):
        bad = not DENSITY_RANGE[0] <= density / median <= DENSITY_RANGE[1]
        flagged += bad
        if bad or show_all:
            print(f"  {'FLAG' if bad else 'ok  '} {prop_id:<34} {density:.2f} px/unit (x{density / median:.2f})")
    return flagged


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("check", nargs="?", choices=["crew", "props", "all"], default="all")
    parser.add_argument("--all", action="store_true", help="list items that pass too")
    parser.add_argument("--strict", action="store_true", help="exit 1 when anything is flagged")
    args = parser.parse_args()
    flagged = 0
    if args.check in ["crew", "all"]:
        flagged += check_crew(args.all)
    if args.check in ["props", "all"]:
        flagged += check_props(args.all)
    print(f"\n{flagged} item(s) flagged.")
    return 1 if args.strict and flagged else 0


if __name__ == "__main__":
    sys.exit(main())
