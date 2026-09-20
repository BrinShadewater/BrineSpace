"""Measure the library's tone against the owner's own props, and repair what is too dark.

    python tools/tileset_library/tone.py measure --sources "C:/New Tilesets" "C:/Another Pass/extracted"
    python tools/tileset_library/tone.py repair  --sources ... [--dry-run]

Targets are measured from the owner's painted room props (legacy/**/pack/*.png), not
chosen. The conversion alone lands well under them, and the owner named the symptoms one
at a time (dark computers, dark plants, black screens, rocks gone near-black) before
anyone measured the distribution. Measure first.

Rules the repair keeps:
  * only ever brighten, with curves that cannot clip a highlight;
  * touch only what is under target, inside that prop's own region, never twice;
  * never lift a prop past 90% of its source: coal, rubble and blacked-out screens are
    dark because their subject is, and that cap is what keeps a re-run from creeping;
  * stop a touch under the owner's numbers. "A bit more" is cheaper than "too much".

A sheet is matched to its source by ALPHA IDENTITY, never by file name: packs share names
like tile-B-01.png, and a name match once repaired sheets against the wrong source.

Use `--only <set-folder>` after adding a pack. The first library was repaired with an
earlier rule that blended the lift by mask strength, so a library-wide run today would
lift mask-fringe pixels on most sheets once more (a dry run reports about 8.6M pixels).
That is an art change: run it across the library only when the owner asks for it. The
rule here is a fixed per-pixel target, so after one run a second changes nothing.
"""
import argparse, collections, glob, hashlib, os

import numpy as np
from PIL import Image

from common import LUMA, OPAQUE, REPO, load_props, load_rgba, save_png_atomic, sheet_of

PLANT_TARGET = 0.28
INTENT = 0.52            # the conversion's own brightness factor
CRUSHED = 0.45           # darker than this share of the source is past the intended curve
SOURCE_CAP = 0.90
GAMMA_MIN = 0.45
SCREEN_KEEP, GREY_KEEP = 0.82, 0.62   # owner's screens 0.417 / source 0.51; greys 0.276 / 0.443


def lum(rgb):
    return (np.asarray(rgb, np.float32) / 255.0) @ LUMA


def masks(O, a):
    """Emissive blue/cyan glass and mid-grey metal, from the SOURCE sheet. The same
    tests serve measurement and repair; when they differed, most measured pixels never
    qualified for the lift."""
    r, g, b = O[..., 0], O[..., 1], O[..., 2]
    lo = lum(O[..., :3]); mx = O[..., :3].max(-1); mn = O[..., :3].min(-1)
    screen = np.clip((b - r - 22) / 16.0, 0, 1) * np.clip((b - g + 3) / 16.0, 0, 1) * np.clip((lo - 0.26) / 0.08, 0, 1) * a
    grey = np.clip((34 - (mx - mn)) / 12.0, 0, 1) * np.clip((lo - 0.25) / 0.06, 0, 1) * np.clip((0.65 - lo) / 0.06, 0, 1) * a * (1 - screen)
    return screen, grey, lo


def owner_targets():
    """Median and darkest decile of the owner's props, plus their screens and greys."""
    L, S, G = [], [], []
    for f in glob.glob(str(REPO / "legacy" / "**" / "pack" / "*.png"), recursive=True):
        if os.path.getsize(f) < 2000: continue            # an LFS pointer, not an image
        A = load_rgba(f).astype(np.float32); a = A[..., 3] > 128
        if a.sum() < 200: continue
        l = lum(A[..., :3]); r, g, b = A[..., 0], A[..., 1], A[..., 2]
        mx = A[..., :3].max(-1); mn = A[..., :3].min(-1)
        L.append(l[a].mean())
        s = a & (b > r + 30) & (b > g + 5) & (l > 0.20); gr = a & ((mx - mn) < 28) & (l > 0.12) & (l < 0.7)
        if s.sum() >= 30: S.append(l[s].mean())
        if gr.sum() >= 60: G.append(l[gr].mean())
    if not L:
        return dict(median=0.275, floor=0.194, screens=0.417, greys=0.276, n=0)
    return dict(median=float(np.median(L)), floor=float(np.percentile(L, 10)),
                screens=float(np.median(S)), greys=float(np.median(G)), n=len(L))


def match_sources(sheets, roots):
    """repo sheet -> untouched source, by the hash of the alpha channel."""
    index = collections.defaultdict(list)
    for root in roots:
        for p in glob.glob(root.replace("\\", "/").rstrip("/") + "/**/*.png", recursive=True):
            p = p.replace("\\", "/")
            if "Auto-tile" in p or "Tile_A" in p: continue
            index[hashlib.sha1(load_rgba(p)[..., 3].tobytes()).hexdigest()].append(p)
    by_name = collections.defaultdict(list)
    for paths in index.values():
        for p in paths: by_name[os.path.basename(p)].append(p)
    found, missing = {}, []
    for sheet in sheets:
        alpha = load_rgba(REPO / sheet)[..., 3]
        hits = index.get(hashlib.sha1(alpha.tobytes()).hexdigest(), [])
        hits = [h for h in hits if os.path.basename(h) == os.path.basename(sheet)] or hits
        if not hits:
            # A swept sheet has blanked regions: accept the same-named source whose art contains ours.
            for cand in by_name.get(os.path.basename(sheet), []):
                oa = load_rgba(cand)[..., 3]
                if oa.shape != alpha.shape: continue
                ours, theirs = alpha >= 24, oa >= 24
                # Swept sheets have less art than the source; un-keyed sheets have a little
                # more (filled holes). Same sheet if nearly all of our art sits on theirs.
                extra = (ours & ~theirs).sum() / float(max(1, ours.sum()))
                if extra <= 0.06 and ours.sum() >= 0.4 * theirs.sum():
                    hits = [cand]; break
        if hits: found[sheet] = hits[0]
        else: missing.append(sheet)
    return found, missing


def solve_gamma(p, target):
    lo, hi = GAMMA_MIN, 1.0
    for _ in range(26):
        g = (lo + hi) / 2
        if float(((p ** g) @ LUMA).mean()) < target: hi = g
        else: lo = g
    return (lo + hi) / 2


def run(sources, write, only=None):
    props = load_props()
    by = collections.defaultdict(list)
    for e in props:
        # --only keeps a repair to the pack just added; the rest of the library is accepted art.
        if only is None or sheet_of(e).split("/")[2] == only: by[sheet_of(e)].append(e)
    if not by:
        print(f"no sheets under assets/new-tilesets/{only}/"); return
    target = owner_targets()
    found, missing = match_sources(sorted(by), sources)
    print(f"owner's props (n={target['n']}): median {target['median']:.3f}, darkest decile {target['floor']:.3f}, "
          f"screens {target['screens']:.3f}, greys {target['greys']:.3f}")
    print(f"sources matched by alpha for {len(found)} of {len(by)} sheets" + (f"; unmatched: {missing[:4]}" if missing else ""))
    L, S, G = [], [], []; lifted = repaired_px = sheets_changed = 0
    for sheet, entries in sorted(by.items()):
        C = load_rgba(REPO / sheet).astype(np.float32)
        O = load_rgba(found[sheet]).astype(np.float32) if sheet in found else None
        if O is not None and O.shape != C.shape: O = None
        before = C.copy(); done = np.zeros(C.shape[:2], bool)
        for e in entries:
            x, y, w, h = [int(v) for v in e["region"]]
            sub = C[y:y + h, x:x + w]; m = (sub[..., 3] > 128) & ~done[y:y + h, x:x + w]
            if m.sum() < 40: continue
            p = sub[..., :3][m] / 255.0; cur = float((p @ LUMA).mean())
            want = PLANT_TARGET if e["category"] == "Plants & growing" else target["floor"]
            if O is not None:
                om = O[y:y + h, x:x + w]; k = om[..., 3] > 128
                if k.sum() >= 40:
                    orig = float(lum(om[..., :3])[k].mean())
                    if cur / max(orig, 1e-4) < CRUSHED: want = max(want, orig * INTENT)
                    want = min(want, orig * SOURCE_CAP)
            if cur < want - 0.004:
                g = solve_gamma(p, want)
                if g < 0.985:
                    sub[..., :3] = np.where(m[..., None], np.power(np.clip(sub[..., :3] / 255.0, 0, 1), g) * 255.0, sub[..., :3])
                    done[y:y + h, x:x + w] |= m; lifted += 1
        if O is not None:
            a = C[..., 3] > 128; screen, grey, lo = masks(O, a); lc = lum(C[..., :3])
            # The target is already weighted by the mask, so it is a fixed value per pixel:
            # a pixel at or above it is left alone and a second run changes nothing.
            # Blending the gain by the mask as well moved fringe pixels a little
            # further on every run.
            want = np.maximum(lc, np.maximum(screen * lo * SCREEN_KEEP, grey * lo * GREY_KEEP))
            gain = np.where((lc > 1e-4) & (want > lc + 0.004), want / np.maximum(lc, 1e-4), 1.0)
            rgb = C[..., :3] * gain[..., None]; peak = rgb.max(-1)
            C[..., :3] = np.where((peak > 255)[..., None], rgb * (255.0 / np.maximum(peak, 1e-4))[..., None], rgb)
            for e in entries:                                 # measure with the measurement's own hard tests
                x, y, w, h = [int(v) for v in e["region"]]
                om = O[y:y + h, x:x + w]; k = om[..., 3] > 128
                if k.sum() < 40: continue
                l_o = lum(om[..., :3]); l_c = lum(C[y:y + h, x:x + w, :3])
                r, g_, b = om[..., 0], om[..., 1], om[..., 2]; mx = om[..., :3].max(-1); mn = om[..., :3].min(-1)
                s = k & (b > r + 30) & (b > g_ + 5) & (l_o > 0.30); gr = k & ((mx - mn) < 28) & (l_o > 0.28) & (l_o < 0.62)
                if s.sum() >= 12: S.append(l_c[s].mean())
                if gr.sum() >= 30: G.append(l_c[gr].mean())
        for e in entries:
            x, y, w, h = [int(v) for v in e["region"]]; sub = C[y:y + h, x:x + w]; m = sub[..., 3] > 128
            if m.sum() >= 40: L.append(float(lum(sub[..., :3])[m].mean()))
        changed = int((np.abs(C[..., :3] - before[..., :3]).max(-1) >= 1.0).sum())
        if changed:
            repaired_px += changed; sheets_changed += 1
            if write: save_png_atomic(REPO / sheet, C.clip(0, 255))
    L = np.array(L)
    verb = "repaired" if write else "would change"
    print(f"library ({len(L)} props): median {np.median(L):.3f} (owner {target['median']:.3f}), "
          f"darkest decile {np.percentile(L, 10):.3f} (owner {target['floor']:.3f})")
    if S: print(f"screens {np.median(S):.3f} (owner {target['screens']:.3f}) | mid-greys {np.median(G):.3f} (owner {target['greys']:.3f})")
    print(f"{verb}: {lifted} props lifted, {repaired_px} pixels on {sheets_changed} sheets")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("action", choices=["measure", "repair"])
    ap.add_argument("--sources", nargs="+", required=True, help="folders holding the untouched packs")
    ap.add_argument("--only", help="set folder under assets/new-tilesets/ to limit the work to (e.g. undercity)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    run(args.sources, write=args.action == "repair" and not args.dry_run, only=args.only)


if __name__ == "__main__":
    main()
