"""Build a compact contact sheet and timed browser review of every candidate human crew state."""
from pathlib import Path
import json
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
import argparse
import fnmatch
import base64
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('actor',choices=['veld','branforth','marsh'])
parser.add_argument('--states',nargs='+',help='Optional state-name glob filters for focused motion review')
parser.add_argument('--portable',action='store_true',help='Embed selected frames so the HTML opens without file URL permissions')
parser.add_argument('--filmstrips',action='store_true',help='Write every selected pose at native density for stride and transition review')
parser.add_argument('--review-name',help='Keep a focused review in its own named folder')
args=parser.parse_args()
ART=ROOT/'character'/({'veld':'dr-veld-v2','branforth':'chief-engineer-branforth-v2','marsh':'marsh-v2'}[args.actor])
OUT=ROOT/'output/crew-replacement-2026-09-12'/args.actor
if args.states: OUT=OUT/'focused'
if args.review_name:
    if Path(args.review_name).name!=args.review_name or args.review_name in ['.','..']:
        parser.error('review-name must be one folder name')
    OUT=OUT/args.review_name
OUT.mkdir(parents=True,exist_ok=True)
catalog=json.loads((ART/'catalog.json').read_text());states={};timings={}
for variant in ['body','equipment']:
    for rel in catalog[variant]:
        path=ART/rel;data=json.loads(path.read_text())
        for e in data['states']:
            timings[e['id']]={'durations':e['frameDurationsMs'],'loop':e['loop']}
            states.setdefault(e['id'],{})[variant]=[(path.parent/f).resolve() for f in e['frameFiles']]
keys=sorted(states)
unmatched=[pattern for pattern in (args.states or []) if not any(fnmatch.fnmatchcase(key,pattern) for key in keys)]
if args.states: keys=[key for key in keys if any(fnmatch.fnmatchcase(key,pattern) for pattern in args.states)]
if not keys: raise ValueError('No states match the review selection')
if args.filmstrips:
    for key in keys:
        variants=list(states[key])
        frames=max(len(v) for v in states[key].values())
        sizes=[Image.open(path).size for paths in states[key].values() for path in paths]
        column=max(size[0] for size in sizes)
        row_height=max(size[1] for size in sizes)+36
        sheet=Image.new('RGB',(column*frames,row_height*len(variants)),'#293b40')
        for row,variant in enumerate(variants):
            for slot,path in enumerate(states[key][variant]):
                im=Image.open(path).convert('RGBA')
                sheet.paste(im,(slot*column,row*row_height+25),im)
                ImageDraw.Draw(sheet).text((slot*column+4,row*row_height+4),f'{key} {variant} {slot}',fill='white')
        sheet.save(OUT/(key+'-filmstrip.png'))
for page in range((len(keys)+23)//24):
    sheet=Image.new('RGB',(1200,900),'#293b40');d=ImageDraw.Draw(sheet)
    for slot,key in enumerate(keys[page*24:page*24+24]):
        x=(slot%4)*300;y=(slot//4)*150;d.text((x+6,y+4),key,fill='white')
        for col,variant in enumerate(['body','equipment']):
            if variant not in states[key]:continue
            im=Image.open(states[key][variant][min(2,len(states[key][variant])-1)]).convert('RGBA');im.thumbnail((142,125),Image.Resampling.NEAREST)
            sheet.paste(im,(x+col*150+(150-im.width)//2,y+21),im)
    sheet.save(OUT/f'contact-{page+1}.png')
html='<!doctype html><meta charset="utf-8"><title>Crew replacement review</title><style>body{background:#293b40;color:#eee;font:15px sans-serif}main{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}article{background:#203035;padding:8px}img{width:48%;image-rendering:pixelated}</style><h1>'+args.actor.title()+' — full replacement</h1><p>Preserved source detail and fitted source revisions; body / helmet. All runtime states.</p><main>'
if args.states:html=html.replace('All runtime states.',f'Focused selection: {len(keys)} states.').replace(' — full replacement',' — focused review')
for key in keys:
    html+='<article>'+key+'<br>'
    for variant in ['body','equipment']:
        if variant not in states[key]:continue
        frames=[('data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()) if args.portable else p.as_uri() for p in states[key][variant]]
        html+='<img data-clip=\''+json.dumps({'frames':frames,**timings[key]})+'\' src="'+frames[0]+'">'
    html+='</article>'
html+='</main><p>Authored durations; one-shot actions hold their final pose for one second before review replay.</p><script>const start=performance.now();function draw(now){document.querySelectorAll("img").forEach(i=>{let c=JSON.parse(i.dataset.clip),total=c.durations.reduce((a,b)=>a+b,0),t=(now-start)%(total+(c.loop?0:1000)),n=0;while(n<c.frames.length-1&&t>=c.durations[n])t-=c.durations[n++];if(i.src!==c.frames[n])i.src=c.frames[n]});requestAnimationFrame(draw)}requestAnimationFrame(draw)</script>'
(OUT/'review.html').write_text(html)
print(f'{len(keys)} states; {(len(keys)+23)//24} contact sheets')
if unmatched:print('Unmatched state patterns: '+', '.join(unmatched))
(OUT/'selection.json').write_text(json.dumps({'actor':args.actor,'patterns':args.states,'states':keys,'unmatchedPatterns':unmatched},indent=2)+'\n')
