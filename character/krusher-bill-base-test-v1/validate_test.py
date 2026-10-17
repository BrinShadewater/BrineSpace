from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent
m=json.loads((P/'manifest.json').read_text());v=json.loads((P/'verification.json').read_text())
errors=[];checks=0
def check(condition,message):
    global checks
    checks+=1
    if not condition:errors.append(message)
for path,digest in v['sourceHashes'].items():check(hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,'source changed: '+path)
base=json.loads((R/'character/crew-runtime-matte-v1/bill/manifest.json').read_text())
for s in m['states']:
    original=next(t for t in base['states'] if t['id']==s['id'])
    check(s['frameDurationsMs']==original['frameDurationsMs'],'timing changed')
    check(s['loop']==original['loop'],'loop changed')
    apng=Image.open(P/'review'/str(s['id']+'.png'));check(apng.n_frames==len(s['frameFiles']),'APNG frame count')
    for i,path in enumerate(s['frameFiles']):
        record=next(r for r in v['records'] if r['state']==s['id'] and r['frame']==i)
        a=np.array(Image.open(R/record['source']).convert('RGBA'));b=np.array(Image.open(P/path).convert('RGBA'))
        mask=np.array(Image.open(P/f'masks/{s["id"]}-{i:03}-head.png'))>0
        mask |= np.array(Image.open(P/f'masks/{s["id"]}-{i:03}-markings.png'))>0
        x,y=record['headPaste'];w,h=v['nativeHeadSize'];mask[y:y+h,x:x+w]=True
        check(np.array_equal(a[~mask],b[~mask]),'body changed outside edit: '+path)
        check(np.array_equal(a[112:],b[112:]),'lower body/foot changed: '+path)
        apng.seek(i);check(np.array_equal(np.array(apng.convert('RGBA')),b),'APNG decode differs: '+path)
        check(not np.any(b[[0,-1],:,3]) and not np.any(b[:,[0,-1],3]),'edge clipping: '+path)
board=Image.new('RGB',(900,660),'#272b2e');d=ImageDraw.Draw(board)
for k,i in enumerate(range(0,59,4)):
    im=Image.open(P/f'frames/walk-south/{i:03}.png').crop((66,18,116,73)).resize((150,165),Image.Resampling.NEAREST)
    x=(k%6)*150;y=(k//6)*210;board.paste(im,(x,y),im);d.text((x+12,y+178),f'Walk frame {i}',fill='white')
board.save(P/'review/walk-neck-review.png')
report={'checks':checks,'errors':errors,'frames':len(v['records']),'headAxis':{s['id']:sorted(set(r['headAxis'] for r in v['records'] if r['state']==s['id'])) for s in m['states']}}
(P/'review/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));assert not errors,errors[:5]
