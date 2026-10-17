from pathlib import Path
import json,copy
from posixpath import normpath
P=Path(__file__).resolve().parent
family=json.loads((P.parent/'james-meal-family-v1/bare-manifest.json').read_bytes())
bowl=json.loads((P.parent/'james-meal-pickup-north-v1/manifest.json').read_bytes())
hands=json.loads((P.parent/'james-cup-pickup-north-v1/handoffs-manifest.json').read_bytes())
clips={}
for folder,pack in [('james-meal-family-v1',family),('james-meal-pickup-north-v1',bowl),('james-cup-pickup-north-v1',hands)]:
    for row in pack['states']:
        if not row['id'].endswith('-north'):continue
        r=copy.deepcopy(row)
        r['frameFiles']=['res://'+normpath(path.removeprefix('res://') if path.startswith('res://') else 'character/'+folder+'/'+path) for path in r['frameFiles']]
        clips[row['id'].removesuffix('-north')]=r
states=[]
for action in ['meal-acquire','eat','meal-deposit','cup-acquire','drink','cup-deposit']:
    row=clips[action]
    for index in range(6):
        if action.endswith('deposit'):
            files=row['frameFiles'][index:];times=row['frameDurationsMs'][index:]
        else:
            files=[row['frameFiles'][index]] if action in ['eat','drink'] and index in [0,5] else list(reversed(row['frameFiles'][:index+1]))
            times=[80]*len(files)
            if action in ['eat','drink']:
                tail=clips['meal-deposit' if action=='eat' else 'cup-deposit']
                files+=tail['frameFiles'][1:];times+=tail['frameDurationsMs'][1:]
        states.append(dict(id=f'meal-return-{action}-{index}-north',frameCount=len(files),frameFiles=files,frameDurationsMs=times,loop=False,facings=['north']*len(files),waterPoses=[False]*len(files),depthOffsets=[0]*len(files),provenance=dict(derivation='Whole selected current pose followed by reverse acquisition/gesture or remaining deposit poses; no new drawn body, mirroring or body splice.',sourceAction=action,sourceIndex=index)))
pack=dict(name='James North interrupted meal returns',frameWidth=184,frameHeight=192,pivot=[92,172],standingHeight=148,textureFilter='linear',precomposed=True,status='native_return_review_pending',states=states)
(P/'manifest.json').write_text(json.dumps(pack,indent=2)+'\n')
print('36 exact-current-pose whole-source returns; maximum',max(sum(s['frameDurationsMs'])/1000 for s in states),'seconds; no new raster')
