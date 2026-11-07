"""Registered south floor-work study; fixed supports, never torch-tip anchoring."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
from rebuild_bill_art import binary,chroma

ROOT=Path(__file__).resolve().parents[1]
SELECTED=True
REACH_SELECTED=True

def main():
    root=ROOT/'character/crew-action-detail-v2'
    if REACH_SELECTED:
        from prepare_marsh_reach_pose import main as pose_build
        from prepare_marsh_reach_transition import main as transition_build
        from prepare_marsh_reach_loop import main as reach_build
        pose_build('04');transition_build('02');reach_build()
        selected=root/'review/marsh-low-reach-sequence-01'
        return {state+'-south':[Image.open(selected/f'south-{state}-{i:03}.png').convert('RGBA') for i in range(6)] for state in ['torch-draw','weld','torch-stow']}
    source=root/'sources/marsh-welding-low-south-candidate-01.png'
    raw=binary(chroma(source))
    if raw.size!=(1774,887):raise ValueError('Recalibrate support anchors for changed source dimensions')
    identity=Image.open(root/'sources/marsh-welding-south-identity-01.png').convert('RGBA')
    # Measured standing crown/sole and each row's boot support line. The torch
    # extends below these lines and must not lift the whole body during tracing.
    scale=148/(402-60)
    baselines=[402,809]
    centers=[150,446,740,1034,1330,1630]
    out=root/'review/marsh-welding-low-south-01';out.mkdir(parents=True,exist_ok=True)
    rows=[]
    for row,(y0,y1) in enumerate([(0,443),(443,887)]):
        frames=[]
        for i in range(6):
            x0=i*raw.width//6;x1=(i+1)*raw.width//6
            tile=raw.crop((x0,y0,x1,y1))
            dense=binary(tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX),True)
            pose=Image.new('RGBA',(184,208))
            pose.alpha_composite(dense,(round(92-(centers[i]-x0)*scale),round(172-(baselines[row]-y0)*scale)))
            if pose.getbbox()[3]>=208:raise ValueError('Tool exceeds the padded study profile')
            pose.save(out/f'source-{row}-{i:03}.png');frames.append(pose)
        rows.append(frames)
    draw=rows[0];draw[0]=identity.copy()
    weld=[draw[-1].copy(),rows[1][1],rows[1][2],rows[1][3],rows[1][4],draw[-1].copy()]
    result={'torch-draw-south':draw,'weld-south':weld,'torch-stow-south':list(reversed(draw))}
    sheet=Image.new('RGB',(6*184,3*232),'#293b40');labels=ImageDraw.Draw(sheet)
    for row,(key,frames) in enumerate(result.items()):
        state=key.rsplit('-',1)[0]
        for i,pose in enumerate(frames):
            pose.save(out/f'south-{state}-{i:03}.png')
            sheet.paste(pose,(i*184,row*232+24),pose);labels.text((i*184+4,row*232+4),f'{state} {i}',fill='white')
    sheet.save(out/'contact.png')
    (out/'registration.json').write_text(json.dumps(dict(status='selection_recorded_separately',
        source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        standingCrown=60,standingSole=402,scale=scale,supportBaselines=baselines,anchorX=centers,pivot=[92,172],
        loopSources=['draw5','loop1','loop2','loop3','loop4','draw5'],
        limits='Fixed source support lines; construction contact requires native review.'),indent=2)+'\n')
    print(out.relative_to(ROOT));return result

if __name__=='__main__':main()
