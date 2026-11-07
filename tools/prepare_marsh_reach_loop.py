"""Register the active reach strip and assemble an unselected complete sequence."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary,chroma
from audit_marsh_tool_reach import hot_tip_pixels

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/crew-action-detail-v2'

def main():
    source=BASE/'sources/marsh-low-reach-loop-candidate-01.png'
    raw=binary(chroma(source))
    if raw.size!=(2064,762):raise ValueError('Remeasure changed loop source')
    # Endpoint upper-body crown y112 to boot support y172 = 60 pixels.
    # All source poses share crown y200 and boot support y430: one fixed ruler.
    scale=60/230
    out=BASE/'review/marsh-low-reach-sequence-01';out.mkdir(parents=True,exist_ok=True)
    endpoint=Image.open(BASE/'review/marsh-low-reach-pose-04/registered.png').convert('RGBA')
    active=[endpoint.copy()]
    for i in range(4):
        tile=raw.crop((i*516,0,(i+1)*516,762))
        dense=binary(tile.resize((round(516*scale),round(762*scale)),Image.Resampling.BOX),True)
        pose=Image.new('RGBA',(184,272))
        pose.alpha_composite(dense,(round(92-260*scale),round(172-430*scale)))
        active.append(pose)
    active.append(endpoint.copy())
    draw=[Image.open(BASE/f'review/marsh-low-reach-transition-02/draw-{i:03}.png').convert('RGBA') for i in range(6)]
    groups={'torch-draw':draw,'weld':active,'torch-stow':list(reversed(draw))}
    sheet=Image.new('RGB',(1104,888),'#293b40');review=[];tips=[]
    for row,(state,frames) in enumerate(groups.items()):
        for i,frame in enumerate(frames):
            frame.save(out/f'south-{state}-{i:03}.png')
            sheet.paste(frame,(i*184,row*296+24),frame)
            still=Image.new('RGB',(184,272),'#293b40');still.paste(frame,(0,0),frame);review.append(still)
            if state=='weld':
                y,x=hot_tip_pixels(np.asarray(frame),150)
                tips.append({'frame':i,'tip':[float(x.mean()),float(y.mean())],'gapToLeaf':187-(160+(float(y.mean())-172)*65.28/148)})
    labels=ImageDraw.Draw(sheet)
    for row,state in enumerate(groups):
        for i in range(6):labels.text((i*184+4,row*296+4),f'{state} {i}',fill='white')
    sheet.save(out/'contact.png')
    review[0].save(out/'sequence-review.gif',save_all=True,append_images=review[1:],duration=[90]*6+[150]*6+[90]*6,loop=0)
    assert draw[-1].tobytes()==active[0].tobytes()==active[-1].tobytes()
    report={'status':'unselected_complete_sequence_study','source':source.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scale':scale,'support':[260,430],'pivot':[92,172],'tips':tips,'limits':'Source registration and exact joins only; complete native motion/contact review pending.'}
    (out/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':main()
