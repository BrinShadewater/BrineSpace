from pathlib import Path
import json
from PIL import Image
H=Path(__file__).resolve().parent; R=H.parents[1]; checks=0
def check(value):
    global checks
    assert value
    checks+=1
def pixels(p):
    with Image.open(p) as im: return im.tobytes()
provenance=json.loads((H/'provenance.json').read_text())['states']; pairs={}
for gear in ['bare','helmet']:
    m=json.loads((H/(gear+'-manifest.json')).read_text());check(m['pivot']==[128,128] and m['standingHeight']==148 and m['precomposed']);check(len(m['states'])==12)
    states={s['id']:s for s in m['states']};pairs[gear]=states
    for key,s in states.items():
        record=provenance[gear+'/'+key]; n=len(s['frameFiles']);half='route' in record
        check(not s['loop']);check(n==(11 if half else 6));check(sum(s['frameDurationsMs'])==(1040 if half else 520))
        for field in ['facings','waterKinds','waterPoses','depthOffsets']:check(len(s[field])==n)
        for p,r in zip(s['frameFiles'],record['frames']):
            with Image.open(H/p) as im:check(im.size==(256,256) and im.mode=='RGBA')
            check(pixels(H/p)==pixels(R/r['source']))
        a,c=key.removeprefix('swim-turn-').split('-')
        for direction,frame in [(a,s['frameFiles'][0]),(c,s['frameFiles'][-1])]:
            base=R/'character'/('veld-water-'+direction+'-coherent-v1'); bm=json.loads((base/(gear+'-manifest.json')).read_text());loop=next(x for x in bm['states'] if x['id']=='swim-'+direction)
            check(pixels(H/frame)==pixels(base/loop['frameFiles'][0]))
        reverse=states[f'swim-turn-{c}-{a}'];check(s['frameDurationsMs']==list(reversed(reverse['frameDurationsMs'])))
        check(all(pixels(H/p)==pixels(H/q) for p,q in zip(s['frameFiles'],reversed(reverse['frameFiles']))))
        if half:
            middle=record['route'][1];check(s['frameDurationsMs'][5]==140)
            check(pixels(H/s['frameFiles'][5])==pixels(H/states[f'swim-turn-{a}-{middle}']['frameFiles'][-1]))
for key,b in pairs['bare'].items():
    e=pairs['helmet'][key]
    for f in ['frameDurationsMs','facings','waterKinds','waterPoses','depthOffsets','loop']:check(b[f]==e[f])
(H/'validation-checks.json').write_text(json.dumps(dict(checks=checks,failures=0,installed=False,scope='Packaging/source reproduction/endpoints/middle joins/reverses/paired clocks; not motion acceptance'),indent=2)+'\n')
print(checks,'matrix checks PASS')
