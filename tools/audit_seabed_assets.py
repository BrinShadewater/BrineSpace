"""Read-only image audit plus generated manifest and local HTML asset catalogue."""
import hashlib
import html
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'assets/environment/seabed-v1'
REJECTED_V1 = {
    'trench-edge': 'Excessive frontal cliff height; replace with overhead fissure.',
    'vent-chimney': 'Tall frontal towers; replace with low overhead vent mouths.',
    'silt-plume': 'Solid rock silhouettes in a particle-only layer.',
    'current-wisp': 'Unrequested station machinery in a particle-only layer.',
}
LIVE = {'silt-plain', 'coral-garden', 'tube-worms', 'hull-fragment', 'pipe-fragment', 'wreck-cargo'}

def main():
    manifest = json.loads((PACK / 'manifest.json').read_text(encoding='utf-8-sig'))
    cards = []
    for asset in manifest['assets']:
        candidates = sorted(PACK.glob(asset['id'] + '-source-v*.png'))
        if not candidates:
            raise ValueError('Missing source: ' + asset['id'])
        selected = PACK / 'vent-chimney-source-v2.png' if asset['id'] == 'vent-chimney' else candidates[-1]
        asset['versions'] = []
        for path in candidates:
            with Image.open(path) as im:
                alpha = im.convert('RGBA').getchannel('A')
                counts = alpha.histogram()
                if path == selected and asset['category'] != 'texture' and counts[0] == 0:
                    raise ValueError('Opaque sprite: ' + path.name)
                asset['versions'].append({
                    'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                    'size': list(im.size), 'mode': im.mode,
                    'transparent_pixels': counts[0], 'partial_alpha_pixels': sum(counts[1:255]),
                    'visible_bounds': alpha.getbbox(), 'processing': 'none; original generated pixels',
                    'rejection': ('Opaque painted checkerboard; retain transparent v2.' if path.name == 'vent-chimney-source-v3.png' else REJECTED_V1.get(asset['id']) if path.name.endswith('-v1.png') else None),
                })
        asset['selected_source'] = selected.name
        asset['status'] = 'generated; alpha audited; visual owner review pending'
        asset['pivot_normalized'] = [0.5, 0.5]
        asset['gameplay_state'] = 'none; visual asset only'
        asset['live_background'] = asset['id'] in LIVE
        if asset['id'] == 'vent-chimney':
            asset['visual_note'] = 'v2 retains a soft exterior sediment halo; use over dark ground. v3 extraction rejected.'
        if asset['category'] == 'water':
            asset['emitter_anchor_normalized'] = [0.5, 0.85]
            asset['anchor_status'] = 'provisional; adjust to source silhouette before effect integration'
        label = html.escape(asset['id'].replace('-', ' ').title())
        src = html.escape(asset['selected_source'])
        with Image.open(selected) as chosen:
            dimensions = f'{chosen.width} × {chosen.height}'
        cards.append(f'<article data-category="{asset["category"]}"><a href="{src}"><img loading="lazy" src="{src}" alt="{label}"></a><h2>{label}</h2><p>{asset["category"]} · {dimensions} px</p></article>')
    manifest['status'] = 'All listed identities generated. Native integration is a subset; see README.md.'
    (PACK / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BRINE / Seabed asset library</title>
<style>body{background:#071b23;color:#dce8e5;font:16px system-ui;margin:0;padding:36px}header{max-width:900px;margin-bottom:28px}h1{font-size:36px;margin:12px 0}header p{color:#9eb9b9;line-height:1.6}.eyebrow{color:#64b9ad;letter-spacing:3px;font-size:12px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px}article{background:#102832;border:1px solid #28414a;border-radius:8px;overflow:hidden}img{width:100%;aspect-ratio:1;object-fit:contain;image-rendering:auto;background:radial-gradient(#28424b,#10232c)}h2{font-size:17px;margin:14px 16px 4px}article p{color:#91acb1;font-size:13px;margin:0 16px 18px}a{color:#83d1c2}button{background:#193d46;border:1px solid #376069;color:#dce8e5;padding:9px 14px;border-radius:4px;margin:0 6px 8px 0;cursor:pointer}button[aria-pressed=true]{background:#33695f}nav{margin-bottom:22px}</style>
<header><div class="eyebrow">BRINE / ENVIRONMENT 01</div><h1>The station has a seabed.</h1><p>Reusable terrain, marine growth, hazards, wreckage and water layers. Click any asset for its full-resolution PNG. Transparent sprites are shown on ocean blue. Sources retain their original pixels; hazard and salvage mechanics are separate work.</p><a href="README.md">Integration and review notes</a></header><nav aria-label="Asset categories">'''
    cats = ['all'] + sorted({a['category'] for a in manifest['assets']})
    page += ''.join(f'<button type="button" data-filter="{c}" aria-pressed="{str(c=="all").lower()}">{c.title()}</button>' for c in cats)
    page += '</nav><main class="grid">' + ''.join(cards) + '</main><script>document.querySelectorAll("button").forEach(b=>b.onclick=()=>{document.querySelectorAll("button").forEach(x=>x.setAttribute("aria-pressed",x===b));document.querySelectorAll("article").forEach(a=>a.hidden=b.dataset.filter!=="all"&&a.dataset.category!==b.dataset.filter)});</script></html>'
    (PACK / 'index.html').write_text(page, encoding='utf-8')
    print(f'{len(manifest["assets"])} identities audited; source hashes, alpha, bounds and gallery saved')

if __name__ == '__main__':
    main()
