from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent
v=json.loads((P/'verification.json').read_text());errors=[];checks=0
def check(condition,message):
    global checks
    checks+=1
    if not condition:errors.append(message)
for path,digest in v['sourceHashes'].items():check(hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,'source changed: '+path)
source=json.loads((R/'character/crew-runtime-matte-v1/bill/manifest.json').read_text())
records={(r['variant'],r['state'],r['frame']):r for r in v['records']}
for variant in ['bare','helmet']:
    m=json.loads((P/f'{variant}-manifest.json').read_text())
    for name in ['frameWidth','frameHeight','pivot','standingHeight']:check(m[name]==source[name],'profile changed: '+name)
    for state in m['states']:
        old=next(s for s in source['states'] if s['id']==state['id'])
        check(state['frameDurationsMs']==old['frameDurationsMs'],'timing changed')
        check(state['loop']==old['loop'],'loop changed')
        anim=Image.open(P/f'review/{variant}-{state["id"]}.png');check(anim.n_frames==len(state['frameFiles']),'APNG frame count')
        for i,path in enumerate(state['frameFiles']):
            rec=records[variant,state['id'],i];a=np.array(Image.open(R/rec['source']).convert('RGBA'));b=np.array(Image.open(P/path).convert('RGBA'))
            mask=np.array(Image.open(P/rec['editMask']))>0
            check(np.array_equal(a[~mask],b[~mask]),'body/shell changed outside explicit mask: '+path)
            check(np.array_equal(a[112:],b[112:]),'lower body changed: '+path)
            if variant=='helmet':check(np.array_equal(a[:,:,3],b[:,:,3]),'shell silhouette changed: '+path)
            anim.seek(i);check(np.array_equal(np.array(anim.convert('RGBA')),b),'APNG pixels differ: '+path)
            check(not np.any(b[[0,-1],:,3]) and not np.any(b[:,[0,-1],3]),'edge clipping: '+path)
for direction in ['south','east','north','west']:
    board=Image.new('RGB',(1000,660),'#272b2e');d=ImageDraw.Draw(board)
    for row,variant in enumerate(['bare','helmet']):
        m=json.loads((P/f'{variant}-manifest.json').read_text());state=next(s for s in m['states'] if s['id']=='walk-'+direction)
        for j,i in enumerate(np.linspace(0,len(state['frameFiles'])-1,10,dtype=int)):
            im=Image.open(P/state['frameFiles'][int(i)]).crop((65,14,119,75)).resize((200,226),Image.Resampling.NEAREST)
            x=(j%5)*200;y=(row*2+j//5)*160;im=im.resize((130,146),Image.Resampling.NEAREST)
            board.paste(im,(x+35,y),im);d.text((x+20,y+146),f'{variant} {direction} / {i}',fill='white')
    board.save(P/f'review/{direction}-neck-review.png')
report={'checks':checks,'frames':len(v['records']),'errors':errors,'sourceHashesUnchanged':not any(e.startswith('source changed') for e in errors)}
(P/'review/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'checks':checks,'frames':len(v['records']),'errors':errors[:8],'errorCount':len(errors)}));assert not errors
