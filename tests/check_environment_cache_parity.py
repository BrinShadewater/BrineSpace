#!/usr/bin/env python3
"""Pixel-compare the env-parity capture pairs written by
tests/test_environment_cache_parity.gd (run that natively first).
Retained and direct environment rendering must be byte-identical."""
import sys
from pathlib import Path

from PIL import Image

OUT = Path(__file__).resolve().parents[1] / "output"


def main() -> int:
    pairs = sorted(OUT.glob("env-parity-*-cached.png"))
    if not pairs:
        print("ERROR: no env-parity captures found; run test_environment_cache_parity.gd natively first")
        return 1
    failures = 0
    for cached_path in pairs:
        direct_path = Path(str(cached_path).replace("-cached.png", "-direct.png"))
        if not direct_path.exists():
            print(f"ERROR: missing direct capture for {cached_path.name}")
            failures += 1
            continue
        cached = Image.open(cached_path).convert("RGBA")
        direct = Image.open(direct_path).convert("RGBA")
        if cached.size != direct.size or cached.tobytes() != direct.tobytes():
            print(f"ERROR: pixel mismatch {cached_path.name} vs {direct_path.name}")
            failures += 1
    label = cached_pairs_label(len(pairs))
    print(f"ENVIRONMENT CACHE PARITY {'PASS' if failures == 0 else 'FAIL'}: {label}")
    return 1 if failures else 0


def cached_pairs_label(count: int) -> str:
    return f"{count} capture pairs byte-identical" if count else "no pairs"


if __name__ == "__main__":
    sys.exit(main())
