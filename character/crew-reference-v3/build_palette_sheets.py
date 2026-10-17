"""Compose unmodified source sheets and exact SVG palette strips; no image regeneration."""
from pathlib import Path
import base64
import hashlib
import html
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
palette = json.loads((ROOT / 'palette-reference.json').read_text(encoding='utf-8'))
cast = json.loads((ROOT / 'cast.json').read_text(encoding='utf-8'))
records = []
for actor in cast:
    source = actor.get('artwork_sheet', actor['sheet'])
    raw = (ROOT / source).read_bytes()
    colours = {**palette['shared_materials'], **palette['character_materials'][actor['id']]}
    assert len(colours) == 24
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1536" height="1540" viewBox="0 0 1536 1540">',
             '<rect width="1536" height="1540" fill="#192127"/>',
             f'<image width="1536" height="1024" href="data:image/png;base64,{base64.b64encode(raw).decode()}"/>',
             '<g font-family="Arial, sans-serif" fill="#E1E6E3">',
             '<text x="32" y="1060" font-size="24" font-weight="bold">MATERIAL COLOUR REFERENCE / sRGB</text>',
             '<text x="32" y="1088" font-size="16">Exact design targets for all poses and helmet states. Flat swatches below take priority over painted samples above.</text>']
    for i, label in enumerate(palette['order']):
        x, y = 32 + (i % 8) * 185, 1110 + (i // 8) * 116
        colour = colours[label]
        assert len(colour) == 7 and colour.startswith('#')
        int(colour[1:], 16)
        parts += [f'<rect x="{x}" y="{y}" width="164" height="46" fill="{colour}" stroke="#73818A"/>',
                  f'<text x="{x}" y="{y+68}" font-size="16">{html.escape(label)}</text>',
                  f'<text x="{x}" y="{y+91}" font-family="monospace" font-size="19">{colour}</text>']
    parts += ['<text x="32" y="1480" font-size="16">Graphite, straps, steel and helmet white are shared. Accent = burgundy / cobalt / burnt orange / sage.</text>',
              '<text x="32" y="1506" font-size="16">Visor tint: 8% overlay guide. Veld hair light = silver streak. Artwork and runtime pixels have not been remapped.</text>', '</g></svg>']
    target = f"{actor['id']}-reference-palette-01.svg"
    output = '\n'.join(parts)
    ET.fromstring(output)
    (ROOT / target).write_text(output, encoding='utf-8')
    # The embedded illustration is byte-for-byte the existing sheet.
    tree = ET.fromstring(output)
    encoded = tree.find('{http://www.w3.org/2000/svg}image').attrib['href'].split(',', 1)[1]
    assert base64.b64decode(encoded) == raw
    actor.update(artwork_sheet=source, sheet=target, palette_reference='palette-reference.json')
    records.append({'actor':actor['id'], 'file':target, 'source':source,
                    'source_sha256':hashlib.sha256(raw).hexdigest(),
                    'sha256':hashlib.sha256(output.encode()).hexdigest(), 'swatches':len(colours)})
(ROOT / 'cast.json').write_text(json.dumps(cast, indent=2)+'\n', encoding='utf-8')
(ROOT / 'palette-sheet-manifest.json').write_text(json.dumps(records, indent=2)+'\n', encoding='utf-8')
page = ROOT / 'index.html'
markup = page.read_text(encoding='utf-8')
for actor in cast:
    markup = markup.replace(actor['artwork_sheet'], actor['sheet'])
page.write_text(markup, encoding='utf-8')
print(f'Built {len(records)} self-contained sheets; 96 labelled swatches; source images unchanged.')
