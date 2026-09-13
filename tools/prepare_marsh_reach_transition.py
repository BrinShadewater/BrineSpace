"""Extract an unselected reach transition with immutable identity/work endpoints."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
from rebuild_bill_art import binary,chroma

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/crew-action-detail-v2'

def main(revision='01'):
    source=BASE/'sources/marsh-low-reach-transition-candidate-01.png'
    raw=binary(chroma(source))
    if raw.size!=(2062,763):raise ValueError('Source dimensions changed; remeasure landmarks')
    # Common head-width ruler; never scale each crouch to standing height.
    scale=24/88
    anchors=[(250,622),(756,620),(1275,619),(1804,529)]
    out=BASE/f'review/marsh-low-reach-transition-{revision}';out.mkdir(parents=True,exist_ok=True)
    frames=[Image.open(BASE/'sources/marsh-welding-south-identity-01.png').convert('RGBA')]
    for i,(ax,ay) in enumerate(anchors):
        x0=i*raw.width//4;x1=(i+1)*raw.width//4
        tile=raw.crop((x0,0,x1,raw.height))
        dense=binary(tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX),True)
        pose=Image.new('RGBA',(184,272))
        pose.alpha_composite(dense,(round(92-(ax-x0)*scale),round(172-ay*scale)))
        frames.append(pose)
    frames.append(Image.open(BASE/'review/marsh-low-reach-pose-04/registered.png').convert('RGBA'))
    intermediate=None
    if revision=='02':
        intermediate=BASE/'sources/marsh-low-reach-intermediate-candidate-01.png'
        raw_mid=binary(chroma(intermediate))
        if abs(raw_mid.height/raw_mid.width-272/184)>.01:raise ValueError('Intermediate aspect changed')
        frames[4]=binary(raw_mid.resize((184,272),Image.Resampling.BOX),True)
    sheet=Image.new('RGB',(1104,296),'#293b40')
    previews=[]
    for i,frame in enumerate(frames):
        frame.save(out/f'draw-{i:03}.png')
        frame.save(out/f'stow-{5-i:03}.png')
        sheet.paste(frame,(184*i,24),frame)
        preview=Image.new('RGB',(184,272),'#293b40');preview.paste(frame,(0,0),frame)
        previews.append(preview.resize((368,544),Image.Resampling.NEAREST))
    labels=ImageDraw.Draw(sheet)
    for i in range(6):
        labels.text((184*i+4,4),f'draw {i}',fill='white')
        labels.line((184*i,196,184*(i+1)-1,196),fill='#839597')
    sheet.save(out/'contact.png')
    sequence=previews+list(reversed(previews))
    sequence[0].save(out/'transition-review.gif',save_all=True,append_images=sequence[1:],duration=[400]+[90]*4+[500,500]+[90]*4+[400],loop=0)
    report=dict(status='unselected_transition_study',source=str(source.relative_to(ROOT)),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scale=scale,headWidthRuler=[24,88],supportAnchors=anchors,pivot=[92,172],frames=6,stow='exact_reverse',limits='Anatomy, continuity and native motion review pending; active loop not authored.')
    if intermediate:report['intermediateOverride']={'source':intermediate.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(intermediate.read_bytes()).hexdigest(),'slot':4}
    (out/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision',choices=['01','02'],default='01')
    main(parser.parse_args().revision)
