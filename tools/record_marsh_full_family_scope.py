"""Bound current Marsh review evidence to exact sources; no art acceptance gate."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "character/marsh-full-family-audit-2026-10-03"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


inventory = read("character/marsh-full-family-audit-2026-10-03/inventory.json")
installation = read("character/marsh-master-repair-v1/installation.json")
closeout = read("character/marsh-master-repair-v1/closeout-selection.json")
receipts = installation["frames"]
selected = {}
for state, data in inventory["states"].items():
    if "marsh-master-repair-v1/" not in data["manifest"]:
        continue
    frames = []
    for frame in data["frames"]:
        current = sha(ROOT / frame["path"])
        receipt = receipts.get(frame["path"], {})
        frames.append({"path": frame["path"], "currentSha256": current,
                       "inventoryMatches": current == frame["sha256"],
                       "installationReceiptPresent": frame["path"] in receipts,
                       "installationMatches": current == receipt.get("sha256")})
    selected[state] = {"frames": frames,
                       "unchangedInstalledSources": all(f["inventoryMatches"] and f["installationMatches"] for f in frames)}

manifests = []
for entry in closeout["orderedBodyManifests"]:
    if "marsh-master-repair-v1/" in entry["path"]:
        current = sha(ROOT / entry["path"])
        manifests.append({**entry, "currentSha256": current, "unchanged": current == entry["sha256"]})
contract = closeout["runtimeContract"]
current_contract = sha(ROOT / contract["path"])
seen_families = ["equip-helmet", "torch-draw", "weld", "sit-down", "eat", "swim"]
reviewed_boards = []
for name in seen_families:
    path = OUT / (name + "-contact.png")
    reviewed_boards.append({"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path), "review": "Static whole-frame visual review only; no continuous contact acceptance."})
for direction in ["east", "west", "north", "south"]:
    path = OUT / ("swim-cross-" + direction + ".png")
    reviewed_boards.append({"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path), "review": "Exact-source common-pivot cross-family comparison; pose bounds do not establish scale or camera acceptance."})

report = {
    "date": "2026-10-03", "selectedStates": inventory["selectedStates"],
    "selectedSlots": inventory["selectedSlots"], "generatedFamilyBoards": len(inventory["boards"]),
    "currentInventorySha256": sha(OUT / "inventory.json"),
    "selectedMasterRepairStates": len(selected),
    "selectedMasterRepairSlots": sum(len(v["frames"]) for v in selected.values()),
    "unchangedInstalledSourceStates": sum(v["unchangedInstalledSources"] for v in selected.values()),
    "receiptMatchedSlots": sum(f["installationMatches"] for v in selected.values() for f in v["frames"]),
    "receiptAbsentSlots": sum(not f["installationReceiptPresent"] for v in selected.values() for f in v["frames"]),
    "receiptMismatchSlots": sum(f["installationReceiptPresent"] and not f["installationMatches"] for v in selected.values() for f in v["frames"]),
    "masterRepairManifests": manifests, "selectedMasterRepairEvidence": selected,
    "september30RuntimeContract": {**contract, "currentSha256": current_contract, "unchanged": current_contract == contract["sha256"]},
    "visuallyReviewedBoardsThisTurn": reviewed_boards,
    "scope": "228-state selected inventory includes private ordered overlays; no normal catalogue admission.",
    "reuseLimit": "Matching installed frame bytes and manifests permit reuse of scoped source-art evidence. They do not revalidate the current controller, contacts, or the entire changed runtime contract.",
    "helmetLimit": "Marsh needs_air is false and begin_helmet_action returns false. Retained helmet art is latent; no normal helmet gameplay acceptance requirement or behavior change is introduced.",
    "findings": [
        "Helmet drawings remain generic broad glove/interact poses without helmet props; retained latent art requires review within the full set.",
        "Construction torch-draw/weld, sit-down and eat show usable whole poses statically; legacy location alone is not a defect.",
        "Loaded and unloaded swimming differ in arm spread, case occlusion and knee flexion in every direction. Per-pose occupied-bound fitting would damage legitimate pose variation.",
        "Loaded East calves appear paler than unloaded counterparts; grade, camera, body root and kick require moving comparison before correction.",
        "South drain04 first join improves on rejected studies but neutral width, low kneeling second pose and third-pose height remain unresolved."
    ],
    "remaining": "Review uninspected current families and continuous cross-family joins; repair demonstrated whole-pose defects; validate normal supported construction, furniture and expedition contacts plus save/continue; decide coherent admission only after full-set consistency/polish.",
    "normalAdmission": False, "fullGoalComplete": False,
}
report["uncoveredInstallationSources"] = [f for v in selected.values() for f in v["frames"] if not f["installationReceiptPresent"]]
report["changedInstallationSources"] = [f for v in selected.values() for f in v["frames"] if f["installationReceiptPresent"] and not f["installationMatches"]]
assert all(f["inventoryMatches"] for v in selected.values() for f in v["frames"]), "Inventory source changed during review"
(OUT / "scope-evidence.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: report[k] for k in ["selectedStates", "selectedSlots", "generatedFamilyBoards", "selectedMasterRepairStates", "selectedMasterRepairSlots", "unchangedInstalledSourceStates", "normalAdmission", "fullGoalComplete"]}))
print("September 30 whole runtime contract unchanged:", report["september30RuntimeContract"]["unchanged"])
