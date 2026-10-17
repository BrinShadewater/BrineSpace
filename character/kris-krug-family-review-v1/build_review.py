"""Compare complete source figures at declared density and shared foot pivot."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json, shutil

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent
sources=[
 ('Bill: current east idle','character/crew-runtime-matte-v1/bill/frames/idle-east-breathing-v1/000.png',148,[92,172]),
 ('Kris: standing master','character/kris-krug-masters-v1/rotations/east.png',147,[92,172]),
 ('Kris: walk neutral','character/kris-krug-walk-east-v1/frames/000.png',147,[92,172]),
 ('Kris: tablet neutral','character/kris-krug-tablet-draw-east-v1/frames/00.png',147,[92,172]),
]
board=Image.new('RGB',(1120,760),'#30373c');draw=ImageDraw.Draw(board)
draw.text((20,16),'CURRENT BILL / KRIS EAST SOURCE CONTINUITY',fill='white')
draw.text((20,38),'Shared 148px declared standing ruler; complete figures, pivot anchored. No per-pose fit.',fill='#c2ced2')
records=[]
for i,(label,path,height,pivot) in enumerate(sources):
    im=Image.open(REPO/path).convert('RGBA');factor=148/height
    for zoom,baseline in [(2,430),(1,655)]:
        resized=im.resize((round(im.width*factor*zoom),round(im.height*factor*zoom)),Image.Resampling.NEAREST)
        x=140+i*280-round(pivot[0]*factor*zoom);y=baseline-round(pivot[1]*factor*zoom)
        board.paste(resized,(x,y),resized)
    draw.text((16+i*280,455),label,fill='white')
    records.append({'label':label,'path':path,'sha256':hashlib.sha256((REPO/path).read_bytes()).hexdigest(),'standingHeight':height,'pivot':pivot})
for y in [430,655]:draw.line((20,y,1100,y),fill='#65818d')
draw.text((20,704),'Source comparison only: no motion smoothness or world foot-plant acceptance.',fill='#c2ced2')
board.save(ROOT/'neutral-comparison.png')
(ROOT/'sources.json').write_text(json.dumps({'reference_selection':'Current runtime matte pack, confirmed by grid_canvas loader and October 1 selected-source audit','scale_method':'148/declaredStandingHeight; common pivot; no alpha-bounds fitting','sources':records},indent=2),encoding='utf-8')
for src,name in [('character/kris-krug-walk-east-v1/locomotion-preview.mp4','walk.mp4'),('character/kris-krug-tablet-draw-east-v1/action-preview.mp4','tablet.mp4')]:
    shutil.copyfile(REPO/src,ROOT/name)
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kris Krüg — source continuity</title><style>body{margin:0;background:#252c30;color:#eee;font:18px system-ui}main{max-width:1120px;margin:auto;padding:24px}p{line-height:1.5;color:#c3cfd4}img,video{width:100%;height:auto}h2{font-size:22px}</style><main><h1>Kris Krüg — source continuity</h1><p>Cognitive Concordance Specialist · Intent Harmonisation</p><img src="neutral-comparison.png" alt="Current selected Bill east idle beside Kris standing, walk neutral and tablet neutral at matching declared density"><p>These are separate candidate source families. Shared pivots and standing rulers do not establish matching anatomy or seamless joins.</p><h2>East walk study</h2><video src="walk.mp4" controls loop playsinline preload="metadata"></video><h2>Alignment tablet study</h2><video src="tablet.mp4" controls loop playsinline preload="metadata"></video><p>Standalone preserved motion previews. No station integration, new gameplay perk or normal art selection.</p></main></html>'''
(ROOT/'index.html').write_text(html,encoding='utf-8')
print('Built fixed-density four-source board and consolidated motion preview.')
