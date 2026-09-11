#!/usr/bin/env python3
"""Point Godot's importer at each tracked raster's actual release role.

Three roles, driven by assets/runtime-release.json (run tools/
build_release_manifest.py first; tools/export_release.ps1 runs both):
  - Rasters referenced by .tscn/.tres stay on the normal texture importer
    (their .tres consumers need the imported Texture2D chain).
  - Manifest rasters get importer="keep": no .ctex is generated, and the
    export's selected-resources pass ships the raw file byte-identical.
  - Every other tracked raster gets importer="skip": never imported, never
    exported. This is what removes ~2.4 GB of unread .ctex and ~3.4 GB of
    QA/source rasters from every release.

.import sidecars are local editor state (gitignored). Rerun after art or
manifest changes, then let the editor rescan (godot --headless --import).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RASTER = {".png", ".jpg", ".jpeg", ".webp"}
KEEP = "[remap]\n\nimporter=\"keep\"\n"
SKIP = "[remap]\n\nimporter=\"skip\"\n"


def resource_rasters() -> set:
    referenced = set()
    tracked = subprocess.run(["git", "ls-files", "*.tscn", "*.tres"], cwd=ROOT,
                             capture_output=True, text=True, check=True)
    for name in tracked.stdout.splitlines():
        text = (ROOT / name).read_text(encoding="utf-8-sig", errors="replace")
        for match in re.findall(r"res://[^\"']+", text):
            if Path(match).suffix.lower() in RASTER:
                referenced.add(match[len("res://"):])
    return referenced


def main() -> int:
    manifest_path = ROOT / "assets/runtime-release.json"
    if not manifest_path.exists():
        print("ERROR: run tools/build_release_manifest.py first "
              "(assets/runtime-release.json is required)")
        return 1
    shipped = {entry["path"][len("res://"):]
               for entry in json.loads(manifest_path.read_text())["files"]
               if Path(entry["path"]).suffix.lower() in RASTER}
    imported = resource_rasters()
    # RichTextLabel [img] tags load through ResourceLoader only, so the icons in
    # main.gd's RESOURCE_ICON_PATHS need the normal texture importer too (the
    # export plugin also packs their raw bytes for code that reads them raw).
    main_src = (ROOT / "scripts/main.gd").read_text(encoding="utf-8-sig")
    icon_block = re.search(r"const RESOURCE_ICON_PATHS := \{(.*?)\n\}", main_src, re.S)
    if icon_block is None:
        print("ERROR: RESOURCE_ICON_PATHS not found in scripts/main.gd")
        return 1
    imported |= {m[len("res://"):] for m in re.findall(r'"(res://[^"]+)"', icon_block.group(1))}
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT,
                             capture_output=True, text=True, check=True)
    counts = {"normal": 0, "keep": 0, "skip": 0}
    for name in tracked.stdout.splitlines():
        if Path(name).suffix.lower() not in RASTER:
            continue
        if name in imported:
            counts["normal"] += 1
            sidecar = ROOT / (name + ".import")
            # A stale keep/skip stub blocks the normal importer; remove it so
            # Godot regenerates a default texture import on the next scan.
            if sidecar.exists() and sidecar.read_text(encoding="utf-8") in (KEEP, SKIP):
                sidecar.unlink()
            continue
        content = KEEP if name in shipped else SKIP
        counts["keep" if name in shipped else "skip"] += 1
        sidecar = ROOT / (name + ".import")
        if not (sidecar.exists() and sidecar.read_text(encoding="utf-8") == content):
            sidecar.write_text(content, encoding="utf-8")
    print(f"raster import roles: normal(resource)={counts['normal']} "
          f"keep(shipped raw)={counts['keep']} skip(unshipped)={counts['skip']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
