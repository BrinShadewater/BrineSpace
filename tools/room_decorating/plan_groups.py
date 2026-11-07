"""Plan working groups for rooms the owner has not decorated: output/decorate/plan2.json.

    python tools/room_decorating/plan_groups.py        (from the repo root)

Each room is two or three groups of things one person uses together; the first of a group
is its anchor. Props are found by the start of their title. See
skills/brinespace-room-pipeline/references/room-decorating.md for why.
"""
import json, os, sys, re, random
sys.path.insert(0, "tools/tileset_library")
from common import *
# Working groups: things one person uses together. First of each group is its anchor.
G = {
 "maintenance_bay": [["workbench", "tool chest", "tool board", "stool"], ["welding", "gas cylinders"], ["robot arm", "parts bins"]],
 "crew_hab": [["bunk bed", "lockers|locker", "bedside"], ["desk", "office chair"], ["sofa", "potted"]],
 "bio_lab": [["lab bench", "microscope", "stool"], ["specimen tank", "specimen jar"], ["fume hood|biosafety", "biohazard"]],
 "clone_lab": [["stasis tube", "cryo pod", "vitals monitor"], ["medical bed", "iv stand"], ["bioreactor", "control cabinet"]],
 # Engineering, not a holding cell: the database calls it "Reserve power and emergency
 # branch isolation controls". Reading the name as a strongroom furnished it with a cot,
 # a strongbox, a hard case and packing crates.
 "isolation_vault": [["switchgear", "breaker box|fuse box", "*electrical cabinet"], ["transformer", "power coupling"], ["battery rack|battery bank", "control cabinet"]],
 "current_turbine": [["generator", "control cabinet", "gauge"], ["transformer", "breaker"], ["tool chest", "electric motor"]],
 "biomass_digester": [["*vat|culture vat|fluid tank", "pump", "pipe valve"], ["hopper cart", "sack"], ["control cabinet", "drum"]],
 "heat_recovery": [["boiler", "pump station", "valve wheel"], ["control cabinet", "gauge"], ["electric motor", "tool chest"]],
 "airlock": [["suit pod", "suit pod", "locker"], ["bench", "hard case"], ["gas cylinders", "hose"]],
 "construction_drone_bay": [["robot arm", "workbench", "parts bins"], ["pallet racking", "crate"], ["forklift", "power cell"]],
 "brine_core": [["reactor core", "control console"], ["coolant", "fluid tank"], ["server rack", "breaker"]],
 "solar_array": [["battery bank", "control cabinet", "breaker"], ["transformer", "power box"], ["terminal", "tool chest"]],
 "reactor": [["reactor control", "control console", "gauge"], ["coolant canister", "hazard canister"], ["fire suppression", "warning beacon"]],
 "battery_array": [["battery bank", "battery rack", "fuse box"], ["power cell crate", "battery cell"], ["control cabinet", "tool chest"]],
 "salvage_drone_bay": [["workbench", "parts box", "tool chest"], ["pallet racking", "crate"], ["hover drone", "ore bin"]],
 "gravity_loom": [["twin coil emitter", "control console", "power coupling"], ["holo globe|holo projector", "terminal"], ["server rack", "junction hub"]],
 "tidal_condenser": [["water tank", "pump station", "pipe valve"], ["water basin", "filter canister"], ["control cabinet", "water drum"]],
 "hydroponics_bay": [["hydroponic trough", "hydroponic trough", "nutrient canister"], ["grow rack", "grow tube"], ["garden cart", "seed sack"]],
 # Bio: "Cultivates edible tissue from Biomass. The trays do not require sunlight."
 "mycelium_nursery": [["grow rack", "bioreactor", "nutrient"], ["culture vat|specimen tank", "sample cabinet|petri"]],
 "life_support": [["life support tank", "life support tank", "control cabinet"], ["air handling", "vent fan"], ["gas cylinders", "filter canister"]],
 "quarantine_cell": [["medical bed|hospital bed", "iv stand", "vitals monitor"], ["cot", "side table"], ["sink", "biohazard bin"]],
 "data_archive": [["server rack", "server rack", "server cabinet"], ["computer desk", "office chair"], ["filing cabinet", "drawer cabinet"]],
 "storage_bay": [["pallet racking", "pallet racking", "pallet jack"], ["crate", "crate", "drum"], ["shelf", "hand truck"]],
 "biodome": [["planter bed", "planter bed", "garden cart"], ["bench", "potted"], ["water basin", "*palm"]],
 "anomaly_lab": [["holo globe", "scanner pod", "terminal"], ["lab bench", "stool"], ["specimen tube", "warning beacon"]],
 "command_center": [["command console", "office chair", "desk monitor"], ["bridge screen", "chart console"], ["holo briefing|holo projector", "pilot seat"]],
 "holographic_core": [["holo projector", "holo emitter", "control console"], ["server cabinet", "server rack"], ["holo display", "terminal"]],
 "med_center": [["hospital bed", "iv stand", "vitals monitor"], ["*ct scanner|scanner bed", "stool"], ["medicine cabinet", "sink"]],
 "med_office": [["desk", "office chair", "laptop"], ["exam", "medicine cabinet"], ["waiting chair", "potted"]],
 "radio_lab": [["radio base station", "console desk", "office chair"], ["server rack", "radio transceiver"], ["satellite dish", "circuit bench"]],
 "shield_generator": [["twin coil", "power coupling", "control cabinet"], ["transformer", "breaker"], ["generator", "gauge"]],
 "observation_room": [["sofa", "coffee table", "armchair"], ["*telescope|camera on tripod", "stool"], ["bookshelf|shelf unit", "potted"]],
 "salvage_workshop": [["workbench", "tool board", "parts box"], ["drill press", "milling"], ["crate", "ore cart"]],
 "galley": [["stove", "sink counter", "*fridge"], ["dining table", "dining table"], ["vending", "coffee"]],
 "cold_store": [["chest freezer", "chest freezer", "*fridge"], ["crate", "cargo case", "hand truck"], ["shelf", "drum"]],
}
JUNK = re.compile(r"bottle|cushion|flag|pennant|cocktail|\bsign\b|poster|sliver|partial|fragment|glove|helmet|tin\b|bar,|bars,|spaceman|skeleton|zombie|robot, |wall |ceiling|porthole|hatch|door|panel|window|floor ", re.I)
props = load_props(); rng = random.Random(11)
ok = [e for e in props if e["category"] not in ("Derelict & damaged", "Offworld surface") and 26 <= e["region"][2] <= 150 and 26 <= e["region"][3] <= 150 and not JUNK.search(e.get("title", ""))]
cat = json.load(open("rooms/full-wall-v1/editor-catalog.json", encoding="utf-8")); plan = {}
for entry in cat:
    groups = G.get(entry["room"])
    if not groups: continue
    seen, out = set(), []
    for gi, names in enumerate(groups):
        members = []
        for ni, w in enumerate(names):
            rx = re.compile(w[1:] if w.startswith("*") else "|".join("^" + a for a in w.split("|")), re.I)
            hits = [e for e in ok if rx.search(e.get("title", "")) and e["id"] not in seen]
            if not hits: continue
            hits.sort(key=lambda e: -(e["region"][2] * e["region"][3]))
            e = rng.choice(hits[:5] if ni == 0 else hits[len(hits) // 4:len(hits) // 4 + 6] or hits[:5]); seen.add(e["id"])
            # The owner's props cover about 3,700 square units each. They pick big art at 50-72%; this picks
            # mid-sized art, so it needs a larger scale to reach the same presence in the room.
            scale = [0.95, 0.88, 0.8][gi] if ni == 0 else rng.choice([0.68, 0.72, 0.78])
            members.append({"id": "library/tileset-" + e["id"], "title": e["title"], "w": e["region"][2], "h": e["region"][3], "s": scale})
        if members: out.append(members)
    plan[entry["asset"]] = out
os.makedirs("output/decorate", exist_ok=True)
json.dump(plan, open("output/decorate/plan2.json", "w"), indent=1)
print(len(plan), "rooms; props per room:", sorted(sum(len(g) for g in v) for v in plan.values()))
for k in ("room-galley", "room-med_center"): print(k, [[m["title"] for m in g] for g in plan[k]])
