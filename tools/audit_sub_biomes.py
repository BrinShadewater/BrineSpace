"""Audit immutable sources and build the local sub-biome catalogue; no image editing."""
import html
import json
from pathlib import Path
from audit_environment_pack import inspect_pack

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets/environment/sub-biomes-v1"

def main():
    # Validate immutable source selections before writing derived metadata or HTML.
    audit = inspect_pack(PACK / "source-ledger.json")
    ledger = json.loads((PACK / "source-ledger.json").read_text(encoding="utf-8"))
    selections = {asset["id"]: asset for asset in ledger["assets"]}
    brief = json.loads((PACK / "generation-record.json").read_text(encoding="utf-8"))
    expansion = json.loads((PACK / "expansion-record.json").read_text(encoding="utf-8"))
    brief["assets"] += expansion["assets"]
    brief["assets"] += json.loads((PACK / "iron-seep-record.json").read_text(encoding="utf-8"))["assets"]
    if {entry["id"] for entry in brief["assets"]} != set(selections):
        raise ValueError("Prompt identities and source-ledger identities differ")
    assets, cards = [], []
    for entry in brief["assets"]:
        choice = selections[entry["id"]]
        selected = PACK / choice["selected_source"]
        record = dict(entry)
        record.pop("prompt")
        record["selected_source"] = selected.name
        record["versions"] = []
        for source in audit["sources"]:
            if source["id"] != entry["id"]:
                continue
            version = dict(source)
            version["size"] = version.pop("native_size")
            version["rejection"] = next(v.get("rejection") for v in choice["versions"] if v["file"] == source["file"])
            record["versions"].append(version)
        record["state"] = "decorative only; no collision, rewards or hazard effects"
        record["pivot"] = [0.5, 0.5]
        assets.append(record)
        label = html.escape(entry["id"].replace("-", " ").title())
        selected_width = next(v["size"][0] for v in record["versions"] if v["selected"])
        cards.append(f'<article data-biome="{entry["biome"]}"><a href="{selected.name}"><img loading="lazy" src="{selected.name}" alt="{label}"></a><h2>{label}</h2><p>{entry["category"]} · original pixels · {selected_width} px wide</p></article>')
    manifest = {"version": 2, "source_ledger": "source-ledger.json", "unregistered_candidates": audit["unregistered_candidates"], "assets": assets, "runtime": "sub_biome_view.gd", "source_count": sum(len(a["versions"]) for a in assets), "identity_count": len(assets)}
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BRINE — Sub-biome library</title>
<style>body{margin:0;background:#071b23;color:#c4d4cd;font:16px/1.6 system-ui}main{max-width:1320px;margin:auto;padding:36px 24px}h1{font-size:36px}p{max-width:900px;color:#8fa9a5}a{color:#9ecfbc}nav{margin:24px 0}button{background:#17323a;color:#c4d4cd;border:1px solid #46615f;padding:12px 18px;margin:0 8px 8px 0;cursor:pointer}button[aria-pressed=true]{background:#385950}section{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}article{background:#132c34;padding:14px}article img{width:100%;aspect-ratio:1;object-fit:contain}h2{font-size:20px}article p{font-size:14px}#sheet{width:100%}[hidden]{display:none}@media(max-width:750px){section{grid-template-columns:1fr}}</style>
<main><small>BRINE / ENVIRONMENT EXPANSION</small><h1>Seven habitats beneath the station</h1><p>Vent sediment, sponge reef, salt flats, kelp meadow, cold coral and manganese nodules. Seven ground materials and fourteen matching props, with stable placement and soft terrain transitions in Godot.</p>
<img id="sheet" src="../../../output/sub-biomes-v1/asset-sheet.png" alt="Native Godot review of three ground transitions and six scenery props">
<img style="width:100%" src="../../../output/sub-biomes-v1/asset-sheet-2.png" alt="Native Godot review of kelp meadow, cold coral garden and manganese nodule field">
<p>In-game previews: <a href="../../../output/sub-biomes-v1/sulfur-1600.png">Sulfur basin</a> · <a href="../../../output/sub-biomes-v1/sponge-1600.png">Sponge reef</a> · <a href="../../../output/sub-biomes-v1/brine-1600.png">Brine flats</a></p>
<p>New previews: <a href="../../../output/sub-biomes-v1/kelp-1600.png">Kelp meadow</a> · <a href="../../../output/sub-biomes-v1/coral-1600.png">Cold coral</a> · <a href="../../../output/sub-biomes-v1/nodules-1600.png">Nodule field</a></p>
<p>Iron seep: <a href="../../../output/sub-biomes-v1/iron-1600.png">In-game preview</a> · <a href="iron-seep-record.json">Exact prompts</a></p><img style="width:100%" src="../../../output/sub-biomes-v1/asset-sheet-3.png" alt="Iron seep native material and scenery review"><nav aria-label="Filter biome"><button data-filter="all" aria-pressed="true">All twenty-one assets</button><button data-filter="sulfur" aria-pressed="false">Sulfur basin</button><button data-filter="sponge" aria-pressed="false">Sponge reef</button><button data-filter="brine" aria-pressed="false">Salt flats</button><button data-filter="kelp" aria-pressed="false">Kelp meadow</button><button data-filter="coral" aria-pressed="false">Cold coral</button><button data-filter="nodules" aria-pressed="false">Nodule field</button><button data-filter="iron" aria-pressed="false">Iron seep</button></nav><section>''' + "\n".join(cards) + '''</section><p><a href="generation-record.json">First batch prompts</a> · <a href="expansion-record.json">Expansion prompts</a> · <a href="manifest.json">Dimensions, alpha and provenance</a> · <a href="README.md">Integration and limits</a></p></main>
<script>document.querySelectorAll('button').forEach(b=>b.onclick=()=>{document.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.querySelectorAll('article').forEach(a=>a.hidden=b.dataset.filter!=='all'&&a.dataset.biome!==b.dataset.filter);});</script></html>'''
    (PACK / "index.html").write_text(page, encoding="utf-8")
    print(f'{len(assets)} identities / {manifest["source_count"]} original sources audited; manifest and catalogue written')

if __name__ == "__main__":
    main()
