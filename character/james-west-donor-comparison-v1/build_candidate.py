from pathlib import Path
import json,copy,hashlib
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
review=json.loads((p/'review.json').read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in review['inputSha256'].items())
report={'selected':False,'visualReviewPending':True,'wholeSourceReused':True,'newAuthoredPoses':0,'durationMs':480,'candidatePoseCount':4,'gears':{},'scope':'Whole selected donor poses, exact bound endpoints; no painting, head overlay, grade, scale or position fitting. Existing candidate replaces four artificial intermediate rows with two actual authored angular poses; prescribed holds80/160/160/80. Not normal selection or full motion acceptance.'}
for gear in ['bare','helmet']:
    bridge=r/'character/james-cargo-return-bridges-v1'/f'{gear}-joined-manifest-v9.json';m=json.loads(bridge.read_bytes());state=copy.deepcopy(m['states'][0])
    paths=[]
    for file in [state['frameFiles'][0],state['frameFiles'][-1]]:
        paths.append(r/file[6:] if file.startswith('res://') else bridge.parent/file)
    donor=r/'character/james-cargo-turn-south-west-v1';dm=json.loads((donor/(gear+'-manifest.json')).read_bytes());ds=next(s for s in dm['states'] if s['id']=='carry-turn-south-west')
    sequence=[paths[0],donor/ds['frameFiles'][4],donor/ds['frameFiles'][3],paths[1]]
    state.update(frameFiles=['res://'+path.relative_to(r).as_posix() for path in sequence],frameCount=4,frameDurationsMs=[80,160,160,80],facings=['west']*4)
    for key in ['waterKinds','waterPoses','depthOffsets']:
        if key in state:state[key]=[state[key][0]]*4
    state['provenance']={'wholeDonorPoses':state['frameFiles'],'sourceAuthoring':'Existing whole SouthWest4/3 in reverse near-West angular progression; original actual endpoints exact','newAuthoredPoses':0,'poseFitting':False}
    m.update(name='James whole-source near-West settle '+gear,status='unselected_whole_donor_source_trial',states=[state])
    (p/(gear+'-candidate-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')
    board=Image.new('RGB',(1024,810),'#303b40');d=ImageDraw.Draw(board)
    rows=[]
    for i,path in enumerate(sequence):
        im=Image.open(path).convert('RGBA');assert im.size==(256,256)
        bg=Image.new('RGBA',im.size,'#303b40');bg.alpha_composite(im);bg=bg.convert('RGB');board.paste(bg,(i*256,24));d.text((i*256+4,4),f'{gear} {i} {state["frameDurationsMs"][i]}ms',fill='white')
        board.paste(bg.crop((96,56,160,120)).resize((256,256),Image.Resampling.NEAREST),(i*256,290))
        board.paste(bg.crop((96,192,160,256)).resize((256,256),Image.Resampling.NEAREST),(i*256,550))
        rows.append({'source':path.relative_to(r).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    name=gear+'-whole-candidate.png';board.save(p/name);report['gears'][gear]={'frames':rows,'board':name}
(p/'candidate-review.json').write_text(json.dumps(report,indent=2)+'\n')
print('Paired four-pose whole-source candidate; two existing intermediates; exact endpoints/480ms; no normal change.')
