"""Indexed East pickup cancellation with exact entrances and whole-body release."""
from pathlib import Path
import os,json
from PIL import Image
P=Path(__file__).resolve().parent
for gear in ['bare','helmet']:
    cargo=P.parent/'james-water-cargo-east-v1'
    cm=json.loads((cargo/f'{gear}-manifest.json').read_text())
    source=next(s for s in cm['states'] if s['id']=='swim-pickup-east')
    stow=P.parent/'james-water-torch-stow-east-v1'
    sm=json.loads((stow/f'{gear}-manifest.json').read_text())['states'][0]
    states=[]
    for index in range(1,6):
        files=[cargo/source['frameFiles'][i] for i in range(index,0,-1)]+[P/f'body-{gear}.png']+[stow/f for f in sm['frameFiles'][1:]]
        durations=[50]*index+[80]+sm['frameDurationsMs'][1:]
        assert sum(durations)==430+50*index
        assert all(Image.open(f).size==(256,276) for f in files)
        states.append({'id':f'swim-cancel-release-pickup-{index}-east','frameFiles':[Path(os.path.relpath(f,P)).as_posix() for f in files],'frameDurationsMs':durations,'loop':False,'waterPoses':[True]*len(files),'waterKinds':['swim']*len(files),'facings':['east']*len(files),'depthOffsets':[0.0]*len(files),'caseReleaseMs':50*index,'provenance':{'entrance':'exact selected pickup '+str(index),'sequence':'whole selected reverse to1, authored empty release, four authored empty-handed interiors, exact selected swim0','case':'saved site-owned original selected case from release boundary; no cargo/reward change'}})
    manifest={'name':'James East indexed case release '+gear,'frameWidth':256,'frameHeight':276,'pivot':[128,128],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'selected_runtime_east_case_release','states':states}
    (P/f'runtime-{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Built 10 paired indexed release states; exact source entrances, 480..680ms.')
import runpy
runpy.run_path(str(P/'build_followthrough.py'))
