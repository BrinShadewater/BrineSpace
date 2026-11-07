"""One-time migration of the recorded biome manifest; never recalculate its hashes."""
import hashlib
import json
from pathlib import Path

PACK = Path(__file__).resolve().parents[1] / "assets/environment/sub-biomes-v1"


def main():
    destination = PACK / "source-ledger.json"
    if destination.exists():
        raise ValueError("Source ledger already exists; migration cannot reset provenance")
    old = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
    assets = []
    for original in old["assets"]:
        for version in original["versions"]:
            data = (PACK / version["file"]).read_bytes()
            if hashlib.sha256(data).hexdigest() != version["sha256"]:
                raise ValueError("Existing source differs from recorded hash: " + version["file"])
        assets.append({"id": original["id"], "kind": original["category"],
                       "biome": original["biome"], "selected_source": original["selected_source"],
                       "stage": "integrated; native reviewed; owner approval pending",
                       "versions": [{key: v[key] for key in ("file", "sha256", "rejection")}
                                    for v in original["versions"]]})
    mapping = {a["id"]: a["selected_source"] for a in assets}
    registry_path = PACK / "sub_biome_view.gd"
    registry = registry_path.read_text(encoding="utf-8")
    old_constant = 'const REVISED := ["sulfur-anhydrite","sponge-vase-sponges","sponge-sea-fans"]'
    old_loader = '\t\t\tvar version := "v2" if REVISED.has(id) else "v1"\n\t\t\tif source.load(ROOT+id+"-"+version+".png")==OK:'
    if old_constant not in registry or old_loader not in registry:
        raise ValueError("Runtime source contract changed; inspect before migration")
    registry = registry.replace(old_constant, "const SOURCES := " + json.dumps(mapping, indent=4))
    registry = registry.replace(old_loader, '\t\t\tif source.load(ROOT+SOURCES[id])==OK:')
    ledger = {"schema_version": 1, "runtime_registry": "sub_biome_view.gd",
              "provenance_origin": "Copied existing manifest SHA256 values only after comparing all 24 source files; not recomputed as a new baseline",
              "assets": assets}
    destination.write_text(json.dumps(ledger, indent=2)+"\n", encoding="utf-8")
    registry_path.write_text(registry, encoding="utf-8")
    print(f"Migrated {len(assets)} identities with original recorded hashes and identical selected paths")


if __name__ == "__main__":
    main()
