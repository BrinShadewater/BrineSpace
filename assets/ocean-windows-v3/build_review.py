"""Read-only source audit and an HTML gallery; does not repaint or resize PNGs."""
from pathlib import Path
from PIL import Image
import hashlib
import html
import json

PACK = Path(__file__).resolve().parent
records = []
catalog = json.loads((PACK/'calibrated/catalog.json').read_text())
for path in sorted((PACK/'sources').glob('*.png')):
    original = path
    render = next(v for v in catalog.values() if Path(v['input']).stem == path.stem)
    path = PACK.parents[1] / render['input'].removeprefix('res://')
    im = Image.open(path)
    alpha = im.getchannel('A')
    bounds = alpha.point(lambda a: 255 if a >= 128 else 0).getbbox()
    records.append({'id':path.stem,'source':str(path.relative_to(PACK)).replace('\\','/'),
                    'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                    'original_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),
                    'render':render,'size':im.size,'alpha_extrema':alpha.getextrema(),
                    'registration_alpha_threshold':128,'registration_bounds_xyxy':bounds,
                    'stage':'integrated; native review captured; owner acceptance pending'})
(PACK/'manifest.json').write_text(json.dumps({'tool':'built-in image_gen','assets':records,
    'processing':'Original masters preserved. Seven separate imagegen finish/exposure refinements. All fourteen runtime textures calibrated to approximately 5 texels per reference display unit using offline cubic reduction, alpha-edge repair and transparent padding. Original logical aspects and mounts retained. Square glazing keeps its opaque dark inset backing.',
    'placement':'Room side reserves lowered 7 units to center them in the inset panels; sizes and horizontal positions unchanged. A 56-unit square center mount stays within the 92-by-79 central panel, only when raised north wall has no north door or exterior hatch. Corridors: sealed screen-north riser segments, no north entry or connected boundary.',
    'verification':'See verification.json and native-review.log. Existing live project updated; packaged exports unchanged.'},indent=2))
cards = ''.join(f'<figure><img loading="lazy" src="{r["source"]}"><figcaption>{html.escape(r["id"])}</figcaption></figure>' for r in records)
captures = ''.join(f'<figure><a href="review/{p.name}"><img loading="lazy" src="review/{p.name}"></a><figcaption>{html.escape(p.stem)}</figcaption></figure>' for p in sorted((PACK/'review').glob('*.png')))
page = '''<!doctype html><meta charset="utf-8"><title>BrineSpace · Ocean windows</title>
<style>body{margin:32px;background:#172126;color:#d6dddb;font:16px system-ui}h1{font-size:28px}p{max-width:900px;line-height:1.6}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}figure{margin:0;padding:12px;background:#293238}img{width:100%;height:220px;object-fit:contain}figcaption{padding-top:8px;color:#b6c8c9}.native img{height:auto;image-rendering:pixelated}a{color:#a7ceda}</style>
<h1>Ocean-floor windows</h1><p>Fourteen pressure-window designs, including three large square middle-wall viewing windows in graphite steel, warm ivory and deep forest green. The square windows now fit a smaller 56-unit central mount only when the north bay is sealed. Raised door artwork is also 10% smaller, anchored at its threshold. Corridor, corner and tee fittings stay on sealed north-facing riser segments. Source artwork below is enlarged; the native Godot captures show actual fit and pixel density.</p>
<p>Live project integrated. Owner visual acceptance pending. Native profile was isolated; concurrently open game activity changed real-profile fingerprints, which were preserved. Packaged executables and baked cards have not been rebuilt.</p><h2>Source designs</h2><section>'''+cards+'''</section><h2>Native room and corridor review</h2><p>q0–q3 show four orientations. Corridor v1 = utility; v2 = observation; no suffix = transit. Click a capture for the original 512px image.</p><section class="native">'''+captures+'</section>'
page = page.replace('<h2>Source designs</h2>', '<h2>Consistency pass</h2><p>All fourteen windows now use approximately five texture pixels per display unit, matching the wall sources more closely. Three green frames share a cleaner matte finish; brass is duller; porthole, octagonal and blue ocean views have more balanced exposure. Existing mounts, sizes and doorway exclusions are retained. Original artwork is preserved.</p><h2>Current source designs</h2>')
comparisons = ''.join(f'<figure><img src="before-consistency/{name}-q0.png"><figcaption>{name} · before</figcaption></figure><figure><img src="review/{name}-q0.png"><figcaption>{name} · current</figcaption></figure>' for name in ['biomass_digester','galley','salvage_workshop'])
page += '<h2>Before / current</h2><section class="native">'+comparisons+'</section>'
(PACK/'index.html').write_text(page,encoding='utf-8')
print(f'{len(records)} source records; {len(list((PACK/"review").glob("*.png")))} native views; gallery written')
