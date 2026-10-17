from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
K=Path(__file__).resolve().parent;R=K.parents[2]
P=K/'complete-action-study-v2';P.mkdir(exist_ok=True)
assert not (P/'full-source-record.json').exists(),'Keep frozen evidence; use new version.'
bind={};reports={}
for name in ['draw-video-v1','operate-video-v2','stow-video-v1']:
    A=K/name
    verdict=A/'VERDICT.json'
    if verdict.exists():assert not json.loads(verdict.read_bytes())['status'].startswith('rejected'), 'Rejected source cannot enter candidate chain: '+name
    r=json.loads((A/'SOURCE_REVIEW.json').read_bytes())
    assert all(hashlib.sha256((R/f).read_bytes()).hexdigest()==h for f,h in r['bindings'].items())
    bind.update(r['bindings']);reports[name]=r
    for f in [A/'SOURCE_REVIEW.json',A/'generation.json']:
        bind[f.relative_to(R).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
inventory_path=R/'character/veld-master-consistency-current-v2/selected-library.json'
inventory=json.loads(inventory_path.read_bytes())
shellpath=R/'character/veld-shared-helmet-south-v1/fitted-helmet.png';shell=Image.open(shellpath).convert('RGBA')
def fitted(im):
    result=im.copy();result.paste((0,0,0,0),(111,77,143,102));result.alpha_composite(shell,(110,69));return result
checks=0
for gear in ['bare','helmet']:
    parts=[json.loads((K/name/f'{gear}-source-manifest.json').read_bytes())['states'][0] for name in ['draw-video-v1','operate-video-v2','stow-video-v1']]
    joined=dict(parts[0]);joined.update(id='source-interact-south',frameCount=sum(x['frameCount'] for x in parts))
    for key in ['frameFiles','frameDurationsMs','facings','waterKinds','waterPoses','depthOffsets']:
        joined[key]=sum((part[key] for part in parts), [])
    data=json.loads((K/'draw-video-v1'/f'{gear}-source-manifest.json').read_bytes());data['states']=[joined]
    for stateid,path in [('reference-south',K.parent/'original-idle-master.png'),('held-south',K/'native-held-key.png')]:
        im=Image.open(path).convert('RGBA');im=im if gear=='bare' else fitted(im)
        dest=P/f'{gear}-{stateid}.png';im.save(dest)
        data['states'].append(dict(id=stateid,frameCount=1,frameFiles=['res://'+dest.relative_to(R).as_posix()],frameDurationsMs=[1000],loop=True))
    entry=inventory['resolved'][gear]['idle-south'];selected=R/entry['frameFiles'][0]
    assert hashlib.sha256(selected.read_bytes()).hexdigest()==inventory['sourceBindings'][entry['frameFiles'][0]]
    im=Image.open(selected).convert('RGBA');plate=Image.new('RGBA',(256,256));px,py=entry['pivot'];plate.alpha_composite(im,(128-round(px),224-round(py)))
    dest=P/f'{gear}-selected-idle.png';plate.save(dest)
    data['states'].append(dict(id='idle-south',frameCount=1,frameFiles=['res://'+dest.relative_to(R).as_posix()],frameDurationsMs=[1000],loop=True))
    data.update(name='Veld complete original-guided South scanner '+gear,status='staged_full_source_join_review_not_installed')
    path=P/f'{gear}-native-manifest.json';path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    for state in data['states']:
        for ref in state['frameFiles']:
            f=R/ref[6:];bind[f.relative_to(R).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
    for f in [path,selected,R/entry['manifest']]:bind[f.relative_to(R).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
    frames=[Image.open(R/ref[6:]).convert('RGBA') for ref in joined['frameFiles']]
    replaypath=P/f'{gear}-complete-source.png';frames[0].save(replaypath,save_all=True,append_images=frames[1:],duration=joined['frameDurationsMs'],loop=1,disposal=0,blend=0)
    with Image.open(replaypath) as replay:
        runs=[]
        for i,im in enumerate(frames):
            if runs and im.tobytes()==frames[runs[-1][0]].tobytes():runs[-1][1]+=joined['frameDurationsMs'][i];runs[-1][2].append(i)
            else:runs.append([i,joined['frameDurationsMs'][i],[i]])
        assert replay.n_frames==len(runs)
        for j,(first,hold,slots) in enumerate(runs):
            replay.seek(j);assert round(replay.info['duration'])==hold;checks+=1
            for i in slots:assert replay.convert('RGBA').tobytes()==frames[i].tobytes();checks+=1
        (P/f'{gear}-replay-source-runs.json').write_text(json.dumps(dict(authoredSlots=len(frames),encodedFrames=len(runs),runs=runs),indent=2)+'\n',encoding='utf-8')
    starts=[0]
    for part in parts:starts.append(starts[-1]+part['frameCount'])
    slots=[0,starts[1]-1,starts[1],starts[2]-1,starts[2],len(frames)-1]
    labels=['Original','Draw start','Draw end','Operate start','Operate end','Stow start','Return','Held key']
    board=Image.new('RGB',(2048,560),'#202a30');d=ImageDraw.Draw(board)
    ims=[Image.open(P/f'{gear}-reference-south.png').convert('RGBA')]+[frames[i] for i in slots]+[Image.open(P/f'{gear}-held-south.png').convert('RGBA')]
    for j,im in enumerate(ims):
        board.paste(im,(j*256,24),im);d.text((j*256+3,4),labels[j],fill='white')
        crop=im.crop((94,65,174,145)).resize((256,256),Image.Resampling.NEAREST);board.paste(crop,(j*256,288),crop)
    board.save(P/f'{gear}-boundary-comparison.png')
for f in [inventory_path,Path(__file__),K/'KEY_REVIEW.json',K/'raw-source.png',K/'prompt.txt',K/'INPUTS.json',K/'generation.json']:
    bind[f.relative_to(R).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
record=dict(frameCount=joined['frameCount'],durationMs=sum(joined['frameDurationsMs']),sourceChecks=checks,sourceFailures=0,bindings=bind,scope='Complete unchanged draw, operate and stow sources joined consecutively without interior omissions. Native appearance evidence does not establish semantic/material/boundary/controller acceptance.')
(P/'full-source-record.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:record[k] for k in ['frameCount','durationMs','sourceChecks','sourceFailures']}))
