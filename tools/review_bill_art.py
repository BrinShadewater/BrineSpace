"""Build a compact contact sheet and timed browser review of every Bill state."""
from pathlib import Path
import json
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'character/major-bill-v3'
OUT=ROOT/'output/bill-full-replacement-2026-09-12'
OUT.mkdir(parents=True,exist_ok=True)
catalog=json.loads((ART/'catalog.json').read_text());states={};timings={}
for variant in ['body','equipment']:
    for rel in catalog[variant]:
        path=ART/rel;data=json.loads(path.read_text())
        for e in data['states']:
            timings[e['id']]={'durations':e['frameDurationsMs'],'loop':e['loop']}
            states.setdefault(e['id'],{})[variant]=[(path.parent/f).resolve() for f in e['frameFiles']]
keys=sorted(states)
for page in range((len(keys)+23)//24):
    sheet=Image.new('RGB',(1200,900),'#293b40');d=ImageDraw.Draw(sheet)
    for slot,key in enumerate(keys[page*24:page*24+24]):
        x=(slot%4)*300;y=(slot//4)*150;d.text((x+6,y+4),key,fill='white')
        for col,variant in enumerate(['body','equipment']):
            if variant not in states[key]:continue
            im=Image.open(states[key][variant][2]).convert('RGBA');im.thumbnail((142,125),Image.Resampling.NEAREST)
            sheet.paste(im,(x+col*150+(150-im.width)//2,y+21),im)
    sheet.save(OUT/f'contact-{page+1}.png')
html='<!doctype html><meta charset="utf-8"><title>Bill complete replacement review</title><style>body{background:#293b40;color:#eee;font:15px sans-serif}main{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}article{background:#203035;padding:8px}img{width:48%;image-rendering:pixelated}</style><h1>Bill — full replacement</h1><p>Original source detail; bare / helmet. All runtime states.</p><main>'
for key in keys:
    html+='<article>'+key+'<br>'
    for variant in ['body','equipment']:
        if variant not in states[key]:continue
        frames=[p.as_uri() for p in states[key][variant]]
        html+='<img data-clip=\''+json.dumps({'frames':frames,**timings[key]})+'\' src="'+frames[0]+'">'
    html+='</article>'
html+='</main><p>Authored durations; one-shot actions hold their final pose for one second before review replay.</p><script>const start=performance.now();function draw(now){document.querySelectorAll("img").forEach(i=>{let c=JSON.parse(i.dataset.clip),total=c.durations.reduce((a,b)=>a+b,0),t=(now-start)%(total+(c.loop?0:1000)),n=0;while(n<c.frames.length-1&&t>=c.durations[n])t-=c.durations[n++];if(i.src!==c.frames[n])i.src=c.frames[n]});requestAnimationFrame(draw)}requestAnimationFrame(draw)</script>'
(OUT/'review.html').write_text(html)
print(f'{len(keys)} states; {(len(keys)+23)//24} contact sheets')
