"""Recover source in-betweens with the selected transform and timing boundaries.

This is extraction of existing authored motion, never cross-fading or frame synthesis.
Outputs are independent studies and do not alter production manifests.
"""
from pathlib import Path
import contextlib, io, json, sys
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
sys.path.insert(0,str(REPO/'tools'))
from extract_crew_motion_cycle import extract

def main():
    baseline=json.loads((ROOT/'review/baseline.json').read_text())
    summaries={}
    for actor in ['veld','branforth','marsh']:
        states=[];count=0
        for direction in ['south','north','east','west']:
            key='walk-'+direction
            old=baseline[actor]['bodyStates'][key]
            if actor=='veld':
                folder=REPO/'character/veld-identity-correction-v1/review'/(
                    'walk-video-cycle-01' if direction=='east' else f'walk-{direction}-video-cycle-01')
                reg=json.loads((folder/'registration.json').read_text())
                recipe=dict(source=reg['source'],sourceFrames=[r['sourceFrame'] for r in reg['records']],
                    sourceCycle=reg['sourceCycle'],durations=reg['durations'],sourceSize=[1248,1664],
                    fps=24,scale=reg['scale'],position=reg['position'],canvas=[256,256],pivot=[128,224],state=key)
            else:
                recipe=json.loads((REPO/f'character/{actor}-motion-polish-v1/{direction}-cycle-recipe.json').read_text())
            original=list(recipe['sourceFrames'])
            ends=original[1:]+[recipe['sourceCycle'][1]]
            slots=[];durations=[]
            # Every original pose still starts at exactly its selected cumulative time.
            for index,end,ms in zip(original,ends,old['durations']):
                span=end-index
                assert span>0
                for frame in range(index,end):
                    slots.append(frame);durations.append(ms/span)
            recipe.update(sourceFrames=slots,durations=durations,
                output=f'character/crew-polish-v1/motion/{actor}/{direction}',
                limits=['More samples from the same authored source; no new painted detail.',
                        'Unselected study: native contact, transitions and equipment pending.'])
            path=ROOT/f'sources/{actor}-{direction}-dense-recipe.json'
            path.write_text(json.dumps(recipe,indent=2)+'\n')
            with contextlib.redirect_stdout(io.StringIO()):extract(path)
            folder=REPO/recipe['output'];files=[]
            for i,source_frame in enumerate(slots):
                full=Image.open(folder/f'{key}-{i:03}.png').convert('RGBA')
                im=full.crop((36,52,220,236))
                assert full.getchannel('A').getbbox()==tuple(v+o for v,o in zip(im.getbbox(),[36,52,36,52])), 'Crop clips pose'
                if source_frame in original:
                    old_im=Image.open(REPO/old['frames'][original.index(source_frame)]['path']).convert('RGBA')
                    assert np.array_equal(np.asarray(im),np.asarray(old_im)),(actor,direction,source_frame,'Baseline reproduction failed')
                out=ROOT/f'motion/{actor}/frames/{key}/{i:03}.png'
                out.parent.mkdir(parents=True,exist_ok=True);im.save(out)
                files.append(out.relative_to(ROOT/f'motion/{actor}').as_posix())
            assert abs(sum(durations)-sum(old['durations']))<1e-8
            states.append(dict(id=key,frameFiles=files,frameDurationsMs=durations,loop=True))
            count+=len(files)
        pack=dict(name=actor+' source-motion study',frameWidth=184,frameHeight=184,pivot=[92,172],
                  standingHeight=148,states=states,status='unselected source-motion study')
        (ROOT/f'motion/{actor}/manifest.json').write_text(json.dumps(pack,indent=2)+'\n')
        summaries[actor]=dict(states=4,frames=count,preservedOriginalPoses=24)
    (ROOT/'review/motion-checks.json').write_text(json.dumps(summaries,indent=2)+'\n')
    print(json.dumps(summaries))

if __name__=='__main__':main()
