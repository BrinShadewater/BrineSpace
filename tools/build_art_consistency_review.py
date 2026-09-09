"""Build the local review board from this pass's native captures and inventory.

Run after audit_art_consistency.py and preview_art_consistency.gd.
This assembles evidence; it does not retouch production art or grant acceptance.
"""
from pathlib import Path
from html import escape
from urllib.parse import quote
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
CAPTURES = ROOT / 'output/art-consistency'
DEST = ROOT / 'docs/art-consistency-2026-09-09'


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    summary = json.loads((CAPTURES / 'inventory-summary.json').read_text(encoding='utf-8'))
    render = json.loads((CAPTURES / 'render-report.json').read_text(encoding='utf-8'))
    definitions = (ROOT / 'scripts/room_database.gd').read_text(encoding='utf-8')
    rooms = {m[0]: {'name': m[1], 'category': m[2]} for m in re.findall(
        r'"id"\s*:\s*"([^"]+)"[^{}]*?"display_name"\s*:\s*"([^"]+)"[^{}]*?"category"\s*:\s*"([^"]+)"', definitions)}
    cards = dict(re.findall(r'"([a-z_]+)"\s*:\s*"res://([^"]+\.png)"',
                           (ROOT / 'scripts/room_card_art.gd').read_text(encoding='utf-8')))
    reviewed = sorted(set(r['room'] for r in render))
    assert len(reviewed) == 47 and len(render) == 188
    assert all(not r['differences'] for r in render)
    palettes = {
        'Core': 'Pearl ivory, aquatic teal; deliberate bright focal room.',
        'Engineering': 'Charcoal, steel, amber and ochre equipment accents.',
        'Science': 'Slate blue and subdued cyan instruments.',
        'Bio': 'Sage, grey, foliage green; amber process equipment.',
        'Crew': 'Warm cream, rust fabric, brown wood; restrained amber lighting.',
        'Medical': 'Pale cream, grey and teal; clinical rather than corroded.',
        'Drone': 'Industrial slate, worn metal and limited amber markings.',
        'Security': 'Dark steel, restrained red status lights.',
        'Anomaly': 'Near-black violet/slate, localized cyan emission.',
    }
    ledger = []
    for identity in reviewed:
        data = rooms[identity]
        ledger.append({'id': identity, **data, 'card': cards[identity],
                       'orientations_reviewed': 4, 'layout_differences': 0,
                       'decision': 'retain', 'palette': palettes.get(data['category'], 'Department materials retained.'),
                       'note': 'Owner-restored furnishing exception retained.' if identity == 'brine_core' else 'Approved sparse layout retained.'})
    report = {'date': '2026-09-09', 'inventory': summary, 'rooms': ledger,
              'installed': ['character/portraits-realism-v2/' + i + '.png' for i in ['bill','veld','branforth','marsh','river','josh','margot']],
              'coverage': {'rooms': 47, 'native_room_orientations': 188, 'portrait_identities': 8,
                           'representative_runtime_sprite_samples': 66, 'native_habitats': 7},
              'limits': ['Raster inventory includes retained history, not 9,000 live assets.',
                         'Animation review uses representative runtime frames, not every frame or transition.',
                         'Title key art retains its earlier, more illustrated style.',
                         'Some ground patterns show mirrored repeats; color coherence does not establish seamless tiling.',
                         'No executable rebuild or exported-package art acceptance in this pass.']}
    (DEST / 'audit.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    evidence = ['runtime-sprites.png', 'comms-bill-1600.png', 'picker-margot-960.png', 'checkpoint-portraits.png']
    evidence += ['native-rooms-%d.png' % i for i in range(6)]
    for filename in evidence:
        shutil.copy2(CAPTURES / filename, DEST / filename)
    shutil.copy2(ROOT / 'output/title-screen.png', DEST / 'title-context.png')
    for biome in ['sulfur','sponge','brine','kelp','coral','nodules','iron']:
        shutil.copy2(CAPTURES / ('habitat-'+biome+'.png'), DEST / ('habitat-'+biome+'.png'))
    def source(path):
        assert (ROOT / path).is_file(), path
        return quote('../../' + path)
    def figure(path, label, extra=''):
        return f'<figure {extra}><a href="{path}"><img loading="lazy" src="{path}" alt="{escape(label)}"></a><figcaption>{escape(label)}</figcaption></figure>'
    portraits = figure(source('character/brine-comms-v13/portrait.png'), 'BRINE / unchanged reference')
    old = {'bill':'character/crew-portraits-v1/bill.png','veld':'character/crew-portraits-v1/veld.png',
           'branforth':'character/crew-portraits-v1/branforth.png','marsh':'character/marsh-portrait-v3/portrait.png',
           **{i:f'character/companions/{i}-portrait.png' for i in ['river','josh','margot']}}
    for identity, previous in old.items():
        new = source('character/portraits-realism-v2/'+identity+'.png')
        portraits += f'<figure><img loading="lazy" src="{new}" data-new="{new}" data-old="{source(previous)}" alt="{identity}"><figcaption>{identity.title()} / V2 installed</figcaption></figure>'
    room_html = ''.join(figure(source(r['card']), r['name']+' / '+r['category'], f'data-category="{r["category"]}"') for r in ledger)
    options = ''.join(f'<option>{escape(c)}</option>' for c in sorted(set(r['category'] for r in ledger)))
    native = ''.join(figure('native-rooms-%d.png'%i, 'Native rotations / sheet %d'%(i+1)) for i in range(6))
    habitats = ''.join(figure('habitat-'+b+'.png',b.title()+' / runtime tint') for b in ['sulfur','sponge','brine','kelp','coral','nodules','iron'])
    html = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BrineSpace / art consistency review</title>
<style>body{margin:0;background:#0a1920;color:#d7d8ce;font:16px/1.55 system-ui}main{max-width:1320px;margin:auto;padding:32px}h1{font-size:38px;font-weight:500}h2{margin-top:48px;color:#a5c8bf}p{max-width:900px}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}.wide{grid-template-columns:repeat(2,1fr)}figure{margin:0;background:#11282d;padding:10px;min-width:0}img{display:block;width:100%;height:auto}figcaption{padding:8px 0;font-size:14px}a{color:#a5c8bf}button,select{background:#17383d;color:#e1e1d4;border:1px solid #55736c;padding:10px 16px;margin:0 12px 18px 0;font:inherit;cursor:pointer}button:focus-visible,select:focus-visible{outline:2px solid #c4bf85}.swatches{display:flex;flex-wrap:wrap;gap:12px}.swatches span{padding:14px;border-top:12px solid var(--c);background:#11282d}small{color:#a2b4af}nav{display:flex;flex-wrap:wrap;gap:20px}@media(max-width:700px){main{padding:16px}.grid{grid-template-columns:repeat(2,1fr)}.wide{grid-template-columns:1fr}}</style>
<main><small>BRINESPACE / 09 SEPTEMBER 2026 / SOURCE REVIEW</small><h1>One station. Distinct departments.</h1>
<p>The strongest production mismatch was the portrait cast. Seven owner-selected V2 portraits now share BRINE’s realistic pixel finish, cool station backgrounds and restrained material shading. Room layouts and department identities remain intact.</p>
<nav><a href="#cast">Portrait changes</a><a href="#rooms">47 rooms</a><a href="#native">188 rotations</a><a href="#world">World &amp; sprites</a><a href="#limits">Findings &amp; limits</a><a href="audit.json">Audit data</a></nav>
<h2>Shared palette direction</h2><p>These are art-direction anchors, not a palette quantization filter. Warm departments, crew identities, biological color and functional warnings retain their differences.</p><div class="swatches"><span style="--c:#0a1920">Deep petrol</span><span style="--c:#455459">Steel slate</span><span style="--c:#c9c9b8">Warm ivory</span><span style="--c:#66877a">Sage / jade</span><span style="--c:#ad793f">Ochre / amber</span><span style="--c:#487b8a">Aquatic blue</span></div>
<h2 id="cast">Portrait consistency pass</h2><button onclick="portraits('new')">Installed V2</button><button onclick="portraits('old')">Before this pass</button><div class="grid">''' + portraits + '''</div>
<p>Names, uniform colors, Josh’s shoulder construction and Margot’s frog hat are preserved. Continue previews now preserve the portrait’s aspect ratio.</p><div class="grid wide">''' + figure('comms-bill-1600.png','Native communications / 1600 × 900') + figure('picker-margot-960.png','Native companion selection / 960 × 540') + figure('checkpoint-portraits.png','Native Continue preview / all four architects') + '''</div>
<h2 id="rooms">Room palette review</h2><p>All 47 room families and all four rotations reviewed. Matte steel and muted accents unite the library. Medical cream, biology green and warmer habitation materials are intentional. BRINE’s restored room remains the bright focal exception.</p><label>Department <select onchange="filterRooms(this.value)"><option>All</option>''' + options + '''</select></label><div id="room-grid" class="grid">''' + room_html + '''</div>
<h2 id="native">Native rotations</h2><p>188 fresh Godot captures using a read-only copy of the owner’s saved layouts. Editor/runtime prop rectangles matched in every orientation. Click a sheet for full size.</p><div class="grid wide">''' + native + '''</div>
<h2 id="world">World and character scale</h2><p>The detailed seafloor is deliberately subdued by runtime tint and scale. Pale salt, coral, sulfur and iron remain recognizable habitats. Dry suits share charcoal construction and department accents; Marsh’s ivory casing and companion silhouettes retain their identities.</p>''' + figure('runtime-sprites.png','66 representative frames from the actual loaded runtime sprite packs') + '<div class="grid wide">' + habitats + '''</div>
<h2 id="limits">Findings and limits</h2><p><strong>Retained:</strong> room palettes, authored sparse layouts, shared door materials, industrial drone finishes, navigation badge colors and ambient water treatment. Bright warning indicators and small resource icons serve readability; they are not room surface colors.</p>
<p><strong>Remaining art-direction outlier:</strong> the title cover has a stronger outlined illustration style and brighter cyan than the new portrait cast. Its existing animated layers and owner cover composition were retained. A coordinated title redraw is the clearest next art improvement; a global darkening filter would not solve its rendering-style difference.</p>''' + figure('title-context.png','Retained title illustration / style difference documented') + '''<p><strong>Separate texture issue:</strong> mirrored repetition is visible in some habitat ground patterns, especially salt and sulfur. The palette is coherent, but this pass does not certify seamless terrain tiling.</p>
<p>''' + str(summary['raster_files']) + ''' Git-visible rasters were decoded and inventoried, including retained source revisions. No raster decode errors. Animation review sampled families; it was not a frame-by-frame acceptance of every clip. Native source checks do not certify a new exported executable.</p>
<p><a href="../ART_CONSISTENCY_2026-09-09.md">Detailed handoff and checks</a></p></main><script>function portraits(v){document.querySelectorAll('img[data-new]').forEach(i=>i.src=i.dataset[v])}function filterRooms(v){document.querySelectorAll('#room-grid figure').forEach(f=>f.hidden=v!=='All'&&f.dataset.category!==v)}</script></html>'''
    (DEST / 'review.html').write_text(html, encoding='utf-8')
    print(f'Review board: {len(ledger)} rooms, seven installed portraits, {len(evidence)+8} evidence images')


if __name__ == '__main__':
    main()
