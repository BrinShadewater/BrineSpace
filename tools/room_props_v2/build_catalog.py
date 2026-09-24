"""Turn extract.py output into the Studio catalog and the rooms' default layouts.

    python tools/room_props_v2/build_catalog.py --cut <extract --out dir> --designs "<design folder>"

Writes assets/station-props-v2/<id>.png, rooms/station-props-v2/props.json and
replaces the redesigned rooms' entries in rooms/full-wall-v1/default-layouts.json.

Each design is the room at 0 degrees. The props never turn, so the other three
rotations move each prop's centre around the room centre, push it back inside
the walls (keeping it against the wall it rotated onto), off the doorway lanes
and apart from its neighbours. Anything still clashing is printed for hand work
in the Studio.
"""
import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "assets" / "station-props-v2"
CATALOG = ROOT / "rooms" / "station-props-v2" / "props.json"
DEFAULTS = ROOT / "rooms" / "full-wall-v1" / "default-layouts.json"
EDITOR = ROOT / "rooms" / "full-wall-v1" / "editor-catalog.json"
HERE = Path(__file__).resolve().parent

KEEP_PREFIXES = ("floor/", "tile/")
HALF = 180.0  # room interior is -180..180 on both axes (RoomLayoutStore envelope)
LANE = 36.0   # half width of a doorway lane (RoomLayoutStore.door_lane)
MOUTH = 90.0  # how far into the room the doorway is kept clear
CENTRE = 60.0 # props centred this close to the middle are centrepieces
SIDES = ["north", "east", "south", "west"]
# Rooms that keep their current art for now (owner, 2026-09-24).
EXEMPT = {"brine_core", "corridor", "corner", "tee_corridor"}
THEMES = {
    "Operations": "operations", "Engineering": "engineering", "Science": "science",
    "Life Support": "life_support", "Recreation": "recreation", "Anomaly": "anomaly",
}


def room_themes():
    """Room id -> Studio theme, from RoomDatabase categories after the six-department rename."""
    old_to_new = {"Core": "operations", "Security": "operations", "Engineering": "engineering",
                  "Drone": "engineering", "Science": "science", "Medical": "science",
                  "Bio": "life_support", "Crew": "recreation", "Anomaly": "anomaly",
                  "Operations": "operations", "Life Support": "life_support", "Recreation": "recreation"}
    text = (ROOT / "scripts" / "room_database.gd").read_text(encoding="utf-8")
    result = {}
    import re
    for match in re.finditer(r'"id"\s*:\s*"([a-z_]+)".{0,200}?"category"\s*:\s*"([A-Za-z ]+)"', text, re.S):
        result[match.group(1)] = old_to_new.get(match.group(2), "engineering")
    return result


def turn(x, y, q):
    for _ in range(q % 4):
        x, y = -y, x
    return x, y


def overlaps(a, b, gap=2.0):
    return a[0] < b[0] + b[2] + gap and b[0] < a[0] + a[2] + gap and a[1] < b[1] + b[3] + gap and b[1] < a[1] + a[3] + gap


def lanes(doors):
    rects = []
    for side in doors:
        s = SIDES.index(side)
        # Only the doorway mouth: the designs put centrepieces in the middle on
        # purpose, so a lane running to the centre would evict them.
        rects.append([(-LANE, -HALF, 2 * LANE, MOUTH), (HALF - MOUTH, -LANE, MOUTH, 2 * LANE),
                      (-LANE, HALF - MOUTH, 2 * LANE, MOUTH), (-HALF, -LANE, MOUTH, 2 * LANE)][s])
    return rects


def clamp(rect):
    x, y, w, h = rect
    return [min(max(x, -HALF), HALF - w), min(max(y, -HALF), HALF - h), w, h]


def place(props, q, doors):
    """props: list of (id, rect_at_q0, walls_at_q0). Returns {id: rect} for quarter q."""
    placed = {}
    for pid, (x, y, w, h), walls in props:
        cx, cy = turn(x + w / 2, y + h / 2, q)
        rect = clamp([cx - w / 2, cy - h / 2, w, h])
        for wall in walls:
            side = (SIDES.index(wall) + q) % 4
            if side == 0: rect[1] = -HALF
            elif side == 1: rect[0] = HALF - w
            elif side == 2: rect[1] = HALF - h
            else: rect[0] = -HALF
        placed[pid] = rect
    blockers = lanes(doors)
    for _ in range(40):
        moved = False
        for pid, rect in placed.items():
            central = abs(rect[0] + rect[2] / 2) < CENTRE and abs(rect[1] + rect[3] / 2) < CENTRE
            for lane in blockers:
                # A centrepiece is the room's point; it stays put and is reported instead.
                if q and not central and overlaps(rect, lane, 0):
                    # Slide along the lane's cross axis to whichever side is nearer.
                    if lane[2] < lane[3]:  # vertical lane (north/south door)
                        left, right = lane[0] - rect[2] - 1, lane[0] + lane[2] + 1
                        rect[0] = left if abs(left - rect[0]) < abs(right - rect[0]) else right
                    else:
                        up, down = lane[1] - rect[3] - 1, lane[1] + lane[3] + 1
                        rect[1] = up if abs(up - rect[1]) < abs(down - rect[1]) else down
                    rect[:] = clamp(rect)
                    moved = True
            for other, orect in placed.items():
                # At 0 degrees the painting is the layout; touching art is deliberate.
                if q == 0 or other <= pid or not overlaps(rect, orect):
                    continue
                # Push the pair apart along the axis with the smaller overlap.
                dx = min(rect[0] + rect[2], orect[0] + orect[2]) - max(rect[0], orect[0]) + 4
                dy = min(rect[1] + rect[3], orect[1] + orect[3]) - max(rect[1], orect[1]) + 4
                # The smaller prop gives way, so centrepieces hold the middle.
                big, small = (rect, orect) if rect[2] * rect[3] >= orect[2] * orect[3] else (orect, rect)
                if dx < dy:
                    s = 1 if small[0] + small[2] / 2 >= big[0] + big[2] / 2 else -1
                    small[0] += s * dx
                else:
                    s = 1 if small[1] + small[3] / 2 >= big[1] + big[3] / 2 else -1
                    small[1] += s * dy
                small[:] = clamp(small)
                moved = True
        if not moved:
            break
    problems = []
    ids = list(placed)
    for i, pid in enumerate(ids):
        for lane in blockers:
            if overlaps(placed[pid], lane, 0):
                problems.append("%s blocks a doorway" % pid)
        for other in ids[i + 1:]:
            if q and overlaps(placed[pid], placed[other], 0):
                problems.append("%s overlaps %s" % (pid, other))
    return placed, problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cut", required=True)
    ap.add_argument("--designs", required=True)
    args = ap.parse_args()
    cut = Path(args.cut)
    records = json.loads((cut / "props.json").read_text())
    manifest = {e["id"]: e for e in json.loads((Path(args.designs) / "source-manifest.json").read_text())}
    tags = json.loads((HERE / "tags.json").read_text())
    common = set(tags.get("common", []))
    roles = tags.get("roles", {})
    not_default = set(tags.get("not_default", []))
    anchors = tags.get("live_anchors", {})
    themes = room_themes()

    if ART.exists():
        shutil.rmtree(ART)
    ART.mkdir(parents=True)
    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    catalog = []
    by_room = {}
    for r in records:
        pid = "sp-" + r["id"]
        n = r["id"].rsplit("-", 1)[1]
        shutil.copy(cut / r["sheet"] / (n + ".png"), ART / (pid + ".png"))
        x0, y0, x1, y1 = r["interior"]
        scale = 2 * HALF / float(x1 - x0)
        w, h = r["size"]
        room = r["room"]
        category = "common" if r["id"] in common else (r["theme"] or themes.get(room, "engineering"))
        label = (room or r["sheet"]).replace("_", " ").replace("-", " ").title() + " " + n
        entry = {
            "id": pid, "label": label, "category": category,
            "source": "res://assets/station-props-v2/%s.png" % pid,
            "region": [0, 0, w, h], "pieces": [[[0, 0], [w, 0], [w, h], [0, h]]],
            # Top-down art: the front half of the picture is what stands on the floor.
            "footprint": [0.0, 0.45, 1.0, 0.55],
            "display_width": round(w * scale, 1),
            "wall_contact": r["walls"],
            "default_rooms": [room] if room and r["id"] not in not_default else [],
            "design": r["design"],
        }
        if r["id"] in roles:
            entry["role"] = roles[r["id"]]
        catalog.append(entry)
        for live_id, size in anchors.get(r["id"], {}).items():
            # The drone and its dock keep their live art but take the painted pad's place.
            cx = ((r["box"][0] + r["box"][2]) / 2 - x0) * scale - HALF
            cy = ((r["box"][1] + r["box"][3]) / 2 - y0) * scale - HALF
            by_room.setdefault(room, []).append((live_id, clamp([cx - size[0] / 2, cy - size[1] / 2, size[0], size[1]]), []))
        if room and r["id"] not in not_default:
            rect = [(r["box"][0] - x0) * scale - HALF, (r["box"][1] - y0) * scale - HALF, w * scale, h * scale]
            by_room.setdefault(room, []).append(("library/" + pid, clamp(rect), r["walls"]))
    CATALOG.write_text(json.dumps(catalog, indent=1))

    editor = json.loads(EDITOR.read_text())
    assets = {e["room"]: e["asset"] for e in editor}
    defaults = json.loads(DEFAULTS.read_text())
    layouts = defaults["layouts"]
    report = []
    for room, asset in assets.items():
        if room in EXEMPT:
            continue
        spec = manifest.get(room)
        for q in range(4):
            doors = spec["rotations"][q] if spec else []
            placed, problems = place(by_room.get(room, []), q, doors)
            layout = {"__free_placement": True}
            # Floors stay: keep the room's floor finish and per-tile choices.
            for k, v in layouts.get("%s/%d" % (asset, q), {}).items():
                if k.startswith(KEEP_PREFIXES):
                    layout[k] = v
            for pid, rect in placed.items():
                layout[pid] = [round(rect[0], 1), round(rect[1], 1)]
            layouts["%s/%d" % (asset, q)] = layout
            report += ["%s q%d: %s" % (room, q, p) for p in problems]
    # Same shape as the hand-kept file (2-space JSON, CRLF) so diffs stay readable.
    DEFAULTS.write_bytes((json.dumps(defaults, indent=2) + "\n").replace("\n", "\r\n").encode())
    print("catalog", len(catalog), "props;", len(by_room), "rooms dressed")
    print("%d placement problems" % len(report))
    for line in report:
        print("  " + line)


if __name__ == "__main__":
    main()
