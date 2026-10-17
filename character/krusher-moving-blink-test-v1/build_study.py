from pathlib import Path
import copy,hashlib,json,shutil
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;PACK=P.parent/'krusher-runtime-candidate-v1';BLINK=P.parent/'krusher-blink-study-v1';HEAD=P.parent/'krusher-bill-base-test-v2'
P.mkdir(exist_ok=True);(P/'frames/idle-south').mkdir(parents=True,exist_ok=True)
source_manifest=json.loads((PACK/'bare-manifest.json').read_text());state=next(s for s in source_manifest['states'] if s['id']=='idle-south');records=json.loads((HEAD/'verification.json').read_text())['records']
closed=np.array(Image.open(BLINK/'south-head-closed.png').convert('RGBA'));mask=np.array(Image.open(BLINK/'eye-mask.png'))>0
baseline=copy.deepcopy(source_manifest);baseline['states']=[copy.deepcopy(state)];baseline['name']='Krusher Dom / existing south idle reference';baseline['states'][0]['frameFiles']=['../krusher-runtime-candidate-v1/'+s for s in state['frameFiles']]
candidate=copy.deepcopy(baseline);candidate['name']='Krusher Dom / moving south blink study';candidate['states'][0]['frameFiles']=[];candidate['status']='unselected south bare blink study';candidate['precomposed']=True
results=[];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();clock=0
for i,(path,hold) in enumerate(zip(state['frameFiles'],state['frameDurationsMs'])):
    source=PACK/path;original=np.array(Image.open(source).convert('RGBA'));out=original.copy();changed=i in [47,48]
    head=next(r for r in records if r['variant']=='bare' and r['state']=='idle-south' and r['frame']==i);x,y=head['headPaste'];fullmask=np.zeros(original.shape[:2],bool)
    if changed:
        region=out[y:y+28,x:x+23].copy();region[mask,:3]=closed[mask,:3];out[y:y+28,x:x+23]=region;fullmask[y:y+28,x:x+23]=mask
    dest=f'frames/idle-south/{i:03}.png';Image.fromarray(out).save(P/dest);candidate['states'][0]['frameFiles'].append(dest)
    results.append({'index':i,'startMs':clock,'durationMs':hold,'blinkClosed':changed,'headPaste':[x,y],'source':source.relative_to(R).as_posix(),'sourceSha256':sha(source),'output':dest,'outsideMaskExact':bool(np.array_equal(original[~fullmask],out[~fullmask])),'alphaExact':bool(np.array_equal(original[:,:,3],out[:,:,3])),'changedPixels':int(np.any(original!=out,axis=2).sum())});clock+=hold
(P/'baseline-manifest.json').write_text(json.dumps(baseline,indent=2)+'\n');(P/'blink-manifest.json').write_text(json.dumps(candidate,indent=2)+'\n')
report={'records':results,'cycleDurationMs':clock,'closedIntervalMs':[1958,2042],'closedDurationMs':84,'method':'Two source-aligned closed-eye presentations; original body poses and every source hold preserved. Generated eye pixels only; not an authored half-close.','limitations':['South bare idle only','Native readability and natural motion review pending','No normal selections or existing package changes']}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n');assert all(r['outsideMaskExact'] and r['alphaExact'] for r in results);print(json.dumps({'frames':len(results),'changedFrames':sum(r['blinkClosed'] for r in results),'cycleMs':clock,'closedMs':84}))
