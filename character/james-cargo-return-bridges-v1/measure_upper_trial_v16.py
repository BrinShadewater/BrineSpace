from pathlib import Path
import json
from PIL import Image
p=Path(__file__).resolve().parent;r=p.parents[1]
def frames(version,mode):
    m=json.loads((p/f'{mode}-joined-manifest-v{version}.json').read_bytes());result=[]
    for ref in m['states'][0]['frameFiles']:
        path=r/ref[6:] if ref.startswith('res://') else p/ref
        result.append(Image.open(path).convert('RGBA'))
    return result
def stats(images):
    crowns=[];deltas=[]
    for im in images:
        box=im.getchannel('A').point(lambda a:255 if a>=32 else 0).getbbox();crowns.append(224-box[1])
    for a,b in zip(images,images[1:]):
        pa=list(a.crop((0,0,256,110)).get_flattened_data());pb=list(b.crop((0,0,256,110)).get_flattened_data())
        changed=sum(x!=y for x,y in zip(pa,pb))
        # Premultiplication prevents transparent RGB noise inflating the diagnostic.
        total=sum(sum(abs(x[c]*x[3]-y[c]*y[3])/255 for c in range(3))+abs(x[3]-y[3]) for x,y in zip(pa,pb))
        deltas.append({'changedRgbaPixels':changed,'premultipliedRgbaL1':total})
    return {'alpha32CrownAbovePivot':crowns,'maxCrownStep':max(abs(a-b) for a,b in zip(crowns,crowns[1:])),'upperRegionDeltas':deltas,'largestPremultipliedStep':max(x['premultipliedRgbaL1'] for x in deltas)}
report={'scope':'Upper region/crown diagnostics only; no pose segmentation or perceptual motion acceptance. Differences of painted images are not anatomical motion vectors.','gears':{}}
for mode in ['bare','helmet']:report['gears'][mode]={'normalV9':stats(frames(9,mode)),'stagedPair16':stats(frames(16,mode))}
(p/'upper-v16-transition-diagnostics.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({g:{v:{'crown':s['alpha32CrownAbovePivot'],'maxCrownStep':s['maxCrownStep'],'largestUpperStep':round(s['largestPremultipliedStep'])} for v,s in item.items()} for g,item in report['gears'].items()}))
