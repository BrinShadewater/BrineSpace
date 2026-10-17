"""Read-only density/palette audit; source images are never modified."""
import hashlib
import json
import statistics
from pathlib import Path
from PIL import Image

PACK = Path(__file__).resolve().parent
ROOT = PACK.parents[1]
manifest = json.loads((PACK/'manifest.json').read_text())
rows = []
for item in manifest['assets']:
    name = item['id']
    image = Image.open(PACK/item['source']).convert('RGBA')
    bounds = image.getchannel('A').point(lambda a: 255 if a>=128 else 0).getbbox()
    x,y,right,bottom = bounds
    width,height = right-x,bottom-y
    mount = (56,56) if name.startswith('square-') else (110,23) if name.startswith(('corridor-','tee-')) else (78.4,23) if name.startswith('corner-') else (80,32)
    ratio = max(width/mount[0],height/mount[1])
    rows.append({'id':name,'sha256':hashlib.sha256((PACK/item['source']).read_bytes()).hexdigest(),
        'registered_size':[width,height],'representative_mount':mount,
        'displayed_size':[round(width/ratio,2),round(height/ratio,2)],
        'source_pixels_per_display_unit':round(ratio,2),
        'note':'Corridor mount varies by segment; room/center mounts are current renderer dimensions.'})

def swatch(path):
    im=Image.open(path).convert('RGBA')
    x,y,r,b=im.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
    # Small hand-selected top-frame patch avoids glass and top-center bolts.
    points=[im.getpixel((px,py)) for px in range(int(x+(r-x)*.35),int(x+(r-x)*.45))
            for py in range(int(y+(b-y)*.035),int(y+(b-y)*.065))]
    points=[p for p in points if p[3]>=240]
    rgb=[round(statistics.median(p[c] for p in points)) for c in range(3)]
    return {'median_srgb':rgb,'rgb_hex':'#'+''.join(f'{c:02x}' for c in rgb)}

green=[]
for name in ['bulkhead-sage','viewing-sage-divided','square-viewing-sage']:
    green.append({'id':name,'previous_frame_patch':swatch(PACK/'previous-sage'/f'{name}.png'),
                  'current_frame_patch':swatch(PACK/'sources'/f'{name}.png')})
walls=json.loads((ROOT/'assets/architecture-rollout-2026-09-26/walls.json').read_text())
wall_ratios={name:{'horizontal':round(walls[name]['base']['face'][2]/368,2),
                  'vertical':round(walls[name]['base']['face'][3]/79,2)}
             for name in ['galley','cold_store','biomass_digester','salvage_workshop']}
result={'scope':'14 current windows, representative native mounts; static audit only',
        'windows':rows,'wall_source_pixels_per_unit':wall_ratios,'green_frame_patches':green,
        'limitations':'Source sampling density is not an artistic pixel-grid measurement. Patch swatches are descriptive, not accessibility contrast scores. No motion/zoom shimmer or performance measurement.'}
(PACK/'consistency-audit.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'source_density_range':[min(r['source_pixels_per_display_unit'] for r in rows),max(r['source_pixels_per_display_unit'] for r in rows)],'green_frame_patches':green},indent=2))
