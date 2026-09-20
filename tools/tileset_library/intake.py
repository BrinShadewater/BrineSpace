"""Take in a reviewed titles file for one set: names, categories, removals, splits, holes.

    python tools/tileset_library/intake.py NAMING/reactor-hall-titles.json [--dry-run]

A titles file is what a reviewer (a person or an agent) writes after reading a set's
numbered pages from `titles.py sheet`:

    {"set": "...", "index": ".../reactor-hall-index.json",
     "titles": {"0": "Coolant pump, twin", "1": ["Control desk", "Screens & computers"]},
     "remove": {"14": "armoured truck: outdoor vehicle"},
     "split":  [22], "holes": [5]}

Nothing is trusted: the file is checked before anything is written (every number covered
once, known categories, sane titles), and what it asks for is bounded:
  * removals over MAX_REMOVE_SHARE of a set stop the intake for a human to look;
  * a split is only made where split.py finds a real seam, otherwise it is reported;
  * holes are only recorded, in hole-report.json, for the owner to have patched by hand.
A family of look-alikes follows its first member: named, re-filed or removed together.
"""
import argparse, re, sys

from common import LIB, PREFIX, load_json, load_props, save_json
from register import KIND
import split as splitter
import sweep as sweeper
import titles as titler

MAX_REMOVE_SHARE = 0.60
# Brands and places only. "apple" and "earth" were here once and refused an apple tree.
BANNED = re.compile(r"\b(amazon|nasa|ikea|coca|pepsi|sony|usa|mars)\b", re.I)


def check(spec, index):
    problems = []
    n = len(index)
    titles, remove = spec.get("titles", {}), spec.get("remove", {})
    for i in range(n):
        k = str(i)
        if (k in titles) == (k in remove):
            problems.append(f"{k}: must be in exactly one of titles / remove")
    for k, v in titles.items():
        if not k.isdigit() or int(k) >= n: problems.append(f"{k}: not a prop number"); continue
        title, cat = (v, None) if isinstance(v, str) else (v[0], v[1] if len(v) > 1 else None)
        words = title.split()
        if not (1 <= len(words) <= 8) or len(title) > 60: problems.append(f"{k}: title length: {title!r}")
        if BANNED.search(title): problems.append(f"{k}: real-world name in title: {title!r}")
        if cat is not None and cat not in KIND: problems.append(f"{k}: unknown category {cat!r}")
    for key in ("split", "holes"):
        for i in spec.get(key, []):
            if not isinstance(i, int) or i >= n: problems.append(f"{key}: bad number {i}")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("titles"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--allow-removals", action="store_true", help="a human has looked at a set that removes most of itself")
    args = ap.parse_args()
    spec = load_json(args.titles); index = load_json(spec["index"])
    problems = check(spec, index)
    if problems:
        for p in problems[:25]: print("  " + p)
        sys.exit(f"{spec['set']}: {len(problems)} problem(s); nothing written")
    families = {f[0]: f[1:] for f in load_json(LIB / "variants.json", {}).get("groups", [])}
    remove = {index[int(k)]: why for k, why in spec.get("remove", {}).items()}
    for lead, why in list(remove.items()):
        for follower in families.get(lead, []): remove.setdefault(follower, why + " (same family)")
    in_set = [e for e in load_props() if e["tileset"] == spec["set"]]
    share = len(remove) / float(max(1, len(in_set)))
    print(f"{spec['set']}: {len(spec['titles'])} titled, {len(remove)} to remove ({100 * share:.0f}% of {len(in_set)}), "
          f"{len(spec.get('split', []))} to split, {len(spec.get('holes', []))} with holes")
    if share > MAX_REMOVE_SHARE and not args.allow_removals:
        sys.exit("that is most of the set: look at it, then re-run with --allow-removals")
    if args.dry_run:
        print("dry run: nothing written"); return

    titler.apply(args.titles, dry_run=False)
    if remove: sweeper.remove_ids(remove)
    done, refused = [], []
    have = {e["id"] for e in load_props()}
    for i in spec.get("split", []):
        pid = index[i]
        if pid + "b" in have:                    # already split: a re-run must not cut a half in half
            done.append(pid); continue
        (done if splitter.split_prop(pid) else refused).append(pid)
    report = load_json(LIB / "hole-report.json", {})
    for i in spec.get("holes", []): report[index[i]] = spec["set"]
    for pid in refused: report.setdefault("needs-split", [])
    if refused: report["needs-split"] = sorted(set(report.get("needs-split", [])) | set(refused))
    save_json(LIB / "hole-report.json", report, indent=1)
    print(f"   split {len(done)}, no clear seam for {len(refused)} (listed under needs-split); holes recorded {len(spec.get('holes', []))}")


if __name__ == "__main__":
    main()
