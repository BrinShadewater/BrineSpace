"""Four-phase carry study using Marsh's own source legs and loaded upper body."""
from pathlib import Path
import copy,json
from PIL import Image,ImageDraw
from rebuild_marsh_art import source_clips
from repair_crew_walk import RIGS,build

ROOT=Path(__file__).resolve().parents[1]
SELECTED={'east','west','north','south'}

def corrected_rig(direction='east'):
    return copy.deepcopy(RIGS['marsh','walk-'+direction])

def main(direction='east'):
    clips=source_clips();key='walk-'+direction
    rig=corrected_rig(direction)
    # Two equal stance intervals per half-cycle; unused end-of-stance sample
    # gets zero duration in this construction rig, never in the runtime pack.
    rig['durations']=[125,125,0,125,125,0]
    axial=rig.get('projection')=='axial'
    if axial:
        # Loaded pickup boots extend beyond the walking donor's x68..116 mask.
        rig['legs']={'left':{'box':[65,121,93,184]},
                     'right':{'box':[93,121,118,184]}}
    # A loaded, neutral pickup endpoint avoids borrowing bent walking legs or
    # moving a front-facing crate onto the rear of the android.
    donor_key='pickup-'+direction if axial else key
    donor_index=len(clips[donor_key])-1 if axial else rig['sourceFrame']
    donor=clips[donor_key][donor_index]
    walk,_=build(donor,rig)
    cut=110
    upper=clips['carry-'+direction][0].crop((0,0,184,cut))
    frames=[];phases=[0,1,3,4]
    out=ROOT/f'character/crew-action-detail-v2/review/marsh-carry-{direction}-local-01'
    out.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(4*184,184),'#293b40');draw=ImageDraw.Draw(sheet)
    for i,phase in enumerate(phases):
        pose=walk[phase].copy()
        if not axial:
            pose.paste((0,0,0,0),(0,0,184,cut))
            pose.alpha_composite(upper,(0,rig.get('bodyBob',[0,-1,0,0,-1,0])[phase]))
        pose.save(out/f'carry-{i:03}.png');frames.append(pose)
        sheet.paste(pose,(i*184,0),pose);draw.text((i*184+4,4),str(i),fill='white')
    sheet.save(out/'contact.png')
    runtime_recipe={**rig,'durations':[180]*4}
    (out/'recipe.json').write_text(json.dumps(dict(status='source_rig_requires_runtime_review',actor='marsh',direction=direction,sourceLegClip=donor_key,sourceLegFrame=donor_index,sourceTorsoClip=donor_key if axial else 'carry-'+direction,sourceTorsoFrame=donor_index if axial else 0,phases=phases,rig=rig,recipe=runtime_recipe,strideDistanceCells=rig['travel']*2*65.28/148/384),indent=2)+'\n')
    print(out.relative_to(ROOT));return frames

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--direction',choices=['east','west','north','south'],default='east')
    main(p.parse_args().direction)
