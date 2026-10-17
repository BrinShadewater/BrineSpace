"""Publish source-clock water action chains and bounded native journey evidence."""
from pathlib import Path
import hashlib,html,json,re
from PIL import Image,ImageDraw
from publish_marsh_gesture_review import selected,save_webp
from publish_marsh_remaining_review import registered,panel

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-water-actions-v1'
OUT=BASE/'review'
EVIDENCE=ROOT/'output/marsh-water-actions-2026-10-15'

def main():
    OUT.mkdir(exist_ok=True);d=selected();cards={name:[] for name in ['Flooding and departure','Empty-handed drainage','Underwater salvage and pickup']}
    def chain(name,direction,parts,note):
        frames=[];durations=[]
        for key,repeats in parts:
            state=d[key][2]
            for _ in range(repeats):
                frames.extend(panel(registered(d[key],i)) for i in range(len(state['frameFiles'])))
                durations.extend(round(t) for t in state['frameDurationsMs'])
        file=f'{name}-{direction}.webp';save_webp(frames,durations,OUT/file)
        return f'<article><h3>{direction.title()}</h3><img src="{file}" alt="{html.escape(name)} {direction}"><p>{note}</p></article>'
    for direction in ['south','north','east','west']:
        cards['Flooding and departure'].append(chain('lift',direction,[(f'water-lift-{direction}',1),(f'tread-{direction}',1),(f'swim-start-{direction}',1),(f'swim-{direction}',2)],'Standing → buoyancy → tread → swimming.'))
        cards['Empty-handed drainage'].append(chain('settle',direction,[(f'tread-{direction}',1),(f'water-settle-{direction}',1),(f'idle-{direction}',1)],'Tread → feet lower → standing.'))
        cards['Underwater salvage and pickup'].append(chain('work',direction,[(f'swim-{direction}',1),(f'water-salvage-enter-{direction}',1),(f'water-salvage-{direction}',3),(f'swim-pickup-{direction}',1),(f'swim-carry-{direction}',2)],'Swim → brake → reach and pull → cargo pickup → loaded swimming.'))
    report=json.loads((EVIDENCE/'native/report.json').read_text());assert report['failures']==0
    native=[]
    for journey in report['journeys']:
        captures=journey['captures'];rotation=journey['rotation'];mode=journey['mode']
        requests=[('water-lift-',2),('water-salvage-',2),('water-salvage-',3),('swim-pickup-',3)] if mode=='delivery' else [('water-lift-',2),('water-settle-',1),('water-settle-',2),('water-settle-',3)]
        board=Image.new('RGB',(1200,276),'#26333c');draw=ImageDraw.Draw(board)
        for col,(prefix,slot) in enumerate(requests):
            matches=[c for c in captures if c['key'].startswith(prefix) and c['slot']==slot and (prefix!='water-salvage-' or not c['key'].startswith('water-salvage-enter-'))]
            assert matches,(rotation,mode,prefix,slot)
            c=matches[0];im=Image.open(EVIDENCE/'native'/c['file']).convert('RGB');assert im.size==(600,480)
            board.paste(im.resize((300,240),Image.Resampling.NEAREST),(col*300,36))
            draw.text((col*300+6,6),c['key']+' / '+str(slot),fill='white')
        file=f'native-q{rotation}-{mode}.png';board.save(OUT/file)
        native.append(f'<article class="wide"><h3>Airlock rotation {rotation} · {mode}</h3><a href="{file}"><img src="{file}" alt="Native journey sampled poses"></a></article>')
    sections=''.join(f'<h2>{title}</h2><section>'+''.join(group)+'</section>' for title,group in cards.items())
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Marsh · water actions</title><style>body{background:#142129;color:#dbe4e6;font:16px system-ui;margin:32px auto;max-width:1480px;padding:0 20px}h1,h2,h3{font-weight:550}p{max-width:1060px;line-height:1.6}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}article{background:#26333c;padding:12px;border-radius:10px}img{width:350px;max-width:100%;image-rendering:pixelated}article.wide{margin-bottom:16px}.wide img{width:1200px}a{color:#a7d6cc}button{background:#b2d4cc;border:0;padding:9px 16px;border-radius:5px;cursor:pointer}</style><h1>Marsh · water actions</h1><p>New whole-body poses for rising into buoyancy, settling as an empty airlock drains, and working underwater. All four facings use the same 148-pixel standing ruler as the accepted library. Existing loaded drainage stays selected.</p><button id="motion">Pause previews</button><p>Source chains below replay for review. Flooding and settling show the authored one-second sequence; the game advances those poses with chamber water level between 30% and 60%. Work shows three 900 ms source cycles; the game fits six cycles after a 400 ms braking entry into its existing 5.48-second work timer. Viewer replay and idle holds are separate from game timing.</p>'''+sections+'''<h2>Actual game journeys</h2><p>Eight controlled native journeys cover delivery and empty return through all four airlock rotations. These are separate sampled poses, held here as stills for inspection. Open a board for its full image. All four lift/settle facings were observed. These routes reached east, south and west salvage; north salvage is checked in source and clock tests.</p>'''+''.join(native)+f'''<p>Native journey checks: {report['checks']:,}, zero failures. Includes pause, power loss, disk save/restore and delivery/resource checks. Source contracts: 244 selected states / 1,274 holds; 16 new water states, with four existing pickup entry holds changed to the shared tread pose. All 1,198 prior source holds remain untouched on disk.</p><p><a href="../../../docs/MARSH_WATER_ACTIONS_2026-10-15.md">Evidence and handoff</a> · <a href="../../marsh-scale-density-review-2026-10-14/review/index.html">Earlier size/density review</a></p><script>let paused=false;const button=document.querySelector('#motion');button.onclick=()=>{{paused=!paused;document.querySelectorAll('section img').forEach(img=>{{if(paused){{img.dataset.loop=img.src;const c=document.createElement('canvas');c.width=img.naturalWidth;c.height=img.naturalHeight;c.getContext('2d').drawImage(img,0,0);img.src=c.toDataURL();}}else img.src=img.dataset.loop;}});button.textContent=paused?'Play previews':'Pause previews';}};</script></html>'''
    (OUT/'index.html').write_text(page,encoding='utf-8')
    # Decode every exported animation and require all local review assets to resolve.
    for path in OUT.glob('*.webp'):
        with Image.open(path) as im:
            for i in range(im.n_frames):im.seek(i);im.load()
    for link in re.findall(r'(?:src|href)="([^"]+)"',page):
        if not link.endswith('.md'):assert (OUT/link).is_file(),link
    receipt={'states':len(d),'holds':sum(len(v[2]['frameFiles']) for v in d.values()),'sourceChains':12,'nativeJourneys':len(report['journeys']),'nativeChecks':report['checks'],'nativeFailures':report['failures'],'nativeWorkFacings':['east','south','west'],'assets':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.suffix in ['.webp','.png']}}
    (OUT/'publication.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('12 decoded source chains;8 native sample boards; local asset links resolve')

if __name__=='__main__':main()
