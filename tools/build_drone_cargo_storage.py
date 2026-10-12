#!/usr/bin/env python3
"""Build cropped storage for the mining rover's large cargo sheets.

Each listed sheet is a grid of 448x448 frames in which the cargo covers a small area. The
derived PNG keeps, for every frame, only the area any frame uses plus a one-pixel transparent
border. scripts/drone_animation.gd uploads those small frames instead of the whole sheet.
Every visible pixel must reconstruct exactly and everything outside the kept area must be
fully transparent, or nothing is written.

Drawing from cropped frames is not byte-identical to drawing from the full sheet when the
cargo is scaled: some rows or columns pick the neighbouring source pixel. The owner accepted
that on October 11, 2026 (output/cargo-crop-comparison-2026-10-11.png).

Original artwork is only read. The catalog records both hashes: an edited original no longer
matches and the game falls back to it.

  python tools/build_drone_cargo_storage.py           # write missing/changed storage + catalog
  python tools/build_drone_cargo_storage.py --check   # verify files and catalog, write nothing
"""
import argparse
import hashlib
import io
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "scripts/drone_cargo_storage_catalog.gd"
MANIFEST = ROOT / "assets/drone-runtime-2026-09-26/mining.json"
BORDER = 1
# Whole paths on purpose: the release manifest follows whole quoted paths only.
SOURCES = {
    "res://assets/mining-rover-v1-2026-09-26/completion/atlases/collect-north-cargo.png":
        "res://assets/mining-rover-v1-2026-09-26/cargo-storage/collect-north-cargo-frames.png",
    "res://assets/mining-rover-v1-2026-09-26/completion/atlases/collect-east-cargo.png":
        "res://assets/mining-rover-v1-2026-09-26/cargo-storage/collect-east-cargo-frames.png",
    "res://assets/mining-rover-v1-2026-09-26/completion/atlases/collect-south-cargo.png":
        "res://assets/mining-rover-v1-2026-09-26/cargo-storage/collect-south-cargo-frames.png",
    "res://assets/mining-rover-v1-2026-09-26/completion/atlases/collect-west-cargo.png":
        "res://assets/mining-rover-v1-2026-09-26/cargo-storage/collect-west-cargo-frames.png",
    "res://assets/mining-rover-v1-2026-09-26/completion/atlases/unload-north-cargo.png":
        "res://assets/mining-rover-v1-2026-09-26/cargo-storage/unload-north-cargo-frames.png",
    "res://assets/mining-rover-v1-2026-09-26/completion/atlases/unload-east-cargo.png":
        "res://assets/mining-rover-v1-2026-09-26/cargo-storage/unload-east-cargo-frames.png",
    "res://assets/mining-rover-v1-2026-09-26/completion/atlases/unload-south-cargo.png":
        "res://assets/mining-rover-v1-2026-09-26/cargo-storage/unload-south-cargo-frames.png",
    "res://assets/mining-rover-v1-2026-09-26/completion/atlases/unload-west-cargo.png":
        "res://assets/mining-rover-v1-2026-09-26/cargo-storage/unload-west-cargo-frames.png",
}
Image.MAX_IMAGE_PIXELS = None


def local(path: str) -> Path:
    return ROOT / path[len("res://"):]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def manifest_records() -> tuple[dict, int, int]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    records = {}
    for clip in manifest["states"].values():
        if "cargoAtlas" in clip:
            records[clip["cargoAtlas"]["path"]] = clip["cargoAtlas"]
    return records, int(manifest["frameWidth"]), int(manifest["frameHeight"])


def cells(pixels: np.ndarray, cell_w: int, cell_h: int) -> np.ndarray:
    """View a sheet as [row, column, y, x, channel]."""
    height, width = pixels.shape[:2]
    return pixels.reshape(height // cell_h, cell_h, width // cell_w, cell_w, 4).swapaxes(1, 2)


def used_box(pixels: np.ndarray, cell_w: int, cell_h: int) -> tuple[int, int, int, int]:
    """Area any frame draws in, grown by the border: x, y, width, height within a frame."""
    alpha = cells(pixels, cell_w, cell_h)[:, :, :, :, 3].max(axis=(0, 1))
    ys, xs = np.nonzero(alpha)
    if len(xs) == 0:
        raise ValueError("sheet is entirely transparent")
    x0, y0, x1, y1 = xs.min() - BORDER, ys.min() - BORDER, xs.max() + 1 + BORDER, ys.max() + 1 + BORDER
    if x0 < 0 or y0 < 0 or x1 > cell_w or y1 > cell_h:
        raise ValueError("cargo touches the frame edge; no room for the transparent border")
    return int(x0), int(y0), int(x1 - x0), int(y1 - y0)


def crop(pixels: np.ndarray, box, cell_w: int, cell_h: int) -> np.ndarray:
    x, y, w, h = box
    kept = cells(pixels, cell_w, cell_h)[:, :, y:y + h, x:x + w, :]
    rows, columns = kept.shape[:2]
    return np.ascontiguousarray(kept.swapaxes(1, 2).reshape(rows * h, columns * w, 4))


def reconstructs(derived: np.ndarray, pixels: np.ndarray, box, cell_w: int, cell_h: int) -> bool:
    x, y, w, h = box
    grid = cells(pixels, cell_w, cell_h)
    rows, columns = grid.shape[:2]
    if derived.shape != (rows * h, columns * w, 4):
        return False
    if not np.array_equal(crop(pixels, box, cell_w, cell_h), derived):
        return False
    outside = grid[:, :, :, :, 3].copy()
    outside[:, :, y:y + h, x:x + w] = 0
    return not outside.any()


def catalog_text(rows: dict) -> str:
    lines = [
        "extends RefCounted",
        "## Generated by tools/build_drone_cargo_storage.py - do not edit by hand.",
        "## Whole paths only. A hash mismatch on either file selects the original sheet.",
        "## box is x, y, width, height of the kept area inside one frame, border included.",
        "const DATA={",
    ]
    for source, row in rows.items():
        lines.append(json.dumps(source) + ":" + json.dumps(row, separators=(",", ":")) + ",")
    lines.append("}")
    return "\r\n".join(lines) + "\r\n"


def run(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="verify only; write nothing")
    args = parser.parse_args(argv)
    records, cell_w, cell_h = manifest_records()
    rows, problems = {}, []
    for source, target in SOURCES.items():
        if source not in records:
            problems.append(f"{source}: not a cargo sheet in the mining runtime manifest")
            continue
        columns = int(records[source]["columns"])
        source_bytes = local(source).read_bytes()
        with Image.open(io.BytesIO(source_bytes)) as opened:
            pixels = np.asarray(opened.convert("RGBA"))
        height, width = pixels.shape[:2]
        if width != columns * cell_w or height % cell_h:
            problems.append(f"{source}: size does not match the manifest frame grid")
            continue
        box = used_box(pixels, cell_w, cell_h)
        target_path = local(target)
        current = target_path.read_bytes() if target_path.exists() else b""
        exact = False
        if current:
            with Image.open(io.BytesIO(current)) as derived:
                exact = derived.mode == "RGBA" and reconstructs(np.asarray(derived), pixels, box, cell_w, cell_h)
        if not exact:
            if args.check:
                problems.append(f"{target}: missing or does not reconstruct {source}")
                continue
            buffer = io.BytesIO()
            Image.fromarray(crop(pixels, box, cell_w, cell_h), "RGBA").save(buffer, format="PNG", compress_level=9)
            current = buffer.getvalue()
            with Image.open(io.BytesIO(current)) as derived:
                if derived.mode != "RGBA" or not reconstructs(np.asarray(derived), pixels, box, cell_w, cell_h):
                    raise SystemExit(f"{source}: derived storage failed reconstruction; nothing written")
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_bytes(current)
            # Runtime PNG loading: keep the editor from importing the sheet as a texture.
            Path(str(target_path) + ".import").write_text('[remap]\n\nimporter="keep"\n')
            print("wrote", target)
        if local(source).read_bytes() != source_bytes:
            raise SystemExit(f"{source}: original changed during the run")
        rows[source] = {"path": target, "sha256": sha256(current), "width": width, "height": height,
                        "cell": [cell_w, cell_h], "columns": columns, "box": list(box),
                        "original_sha256": sha256(source_bytes)}
        frames = columns * (height // cell_h)
        print(f"{Path(target).name}: exact, {frames} frames of {box[2]}x{box[3]}, "
              f"RGBA {width * height * 4} -> {frames * box[2] * box[3] * 4} bytes")
    expected = catalog_text(rows) if not problems else ""
    existing = CATALOG.read_bytes().decode("utf-8") if CATALOG.exists() else ""
    # Line endings differ by checkout; compare content only.
    if not problems and existing.splitlines() != expected.splitlines():
        if args.check:
            problems.append("scripts/drone_cargo_storage_catalog.gd does not match the files on disk")
        else:
            CATALOG.write_bytes(expected.encode("utf-8"))
            print("wrote", CATALOG.relative_to(ROOT).as_posix())
    for problem in problems:
        print("FAIL", problem)
    print("DRONE_CARGO_STORAGE sheets=%d failures=%d" % (len(rows), len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(run())
