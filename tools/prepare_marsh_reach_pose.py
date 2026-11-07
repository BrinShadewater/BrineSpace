"""Register one forward-reach study without selecting it for runtime."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary,chroma
from audit_marsh_tool_reach import hot_tip_pixels

ROOT=Path(__file__).resolve().parents[1]

def main(revision='01'):
    base=ROOT/'character/crew-action-detail-v2'
    source=base/f'sources/marsh-low-reach-pose-candidate-{revision}.png'
    raw=binary(chroma(source))
    ratio=raw.width/296
    expected_height=592 if revision=='04' else 500
    if abs(raw.height/ratio-expected_height)>1:raise ValueError('Changed aspect ratio requires new registration')
    scale=(148/342)/ratio
    # Revision 04 reframed its support despite the prompt. Measured right boot
    # sole is raw y1295 on its 886px-wide source; compensate at fixed scale.
    support_y=1295*296/886 if revision=='04' else 402
    # Reference is column six cropped at x1478 from the original source:
    # registered support x1630 becomes x152, with support baseline y402.
    dense=binary(raw.resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.BOX),True)
    pose=Image.new('RGBA',(184,272 if revision=='04' else 224));pose.alpha_composite(dense,(round(92-152*ratio*scale),round(172-support_y*ratio*scale)))
    out=base/f'review/marsh-low-reach-pose-{revision}';out.mkdir(parents=True,exist_ok=True)
    pose.save(out/'registered.png')
    old=Image.open(base/'review/marsh-welding-low-south-01/south-weld-000.png').convert('RGBA')
    sheet=Image.new('RGB',(368,max(280,pose.height+24)),'#293b40')
    # main.get_marsh_position() cancels the subsequent renderer lift.
    target=172+(187-160)/(65.28/148)
    for col,im in enumerate([old,pose]):sheet.paste(im,(col*184,24),im)
    draw=ImageDraw.Draw(sheet)
    for col,im in enumerate([old,pose]):
        draw.line((col*184,196,(col+1)*184-1,196),fill='#839597')
        draw.line((col*184,round(target+24),(col+1)*184-1,round(target+24)),fill='#d0a05a')
        draw.text((col*184+4,4),['Selected / support line','Reach study / leaf target'][col],fill='white')
    sheet.save(out/'comparison.png')
    a=np.asarray(pose);yy,xx=hot_tip_pixels(a,150)
    if not len(xx):raise ValueError('No hot tip pixels found')
    tip=[float(xx.mean()),float(yy.mean())]
    overlay=Image.new('RGBA',(184,max(256,pose.height)),'#293b40');overlay.alpha_composite(pose)
    marker=ImageDraw.Draw(overlay)
    marker.line((0,round(target),183,round(target)),fill='#d0a05a')
    for y,x in zip(yy,xx):overlay.putpixel((int(x),int(y)),(0,255,255,255))
    overlay.resize((overlay.width*2,overlay.height*2),Image.Resampling.NEAREST).save(out/'tip-mask-review.png')
    gap=187-(160+(tip[1]-172)*65.28/148)
    report=dict(status='unselected_source_study',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                sourceSize=list(raw.size),scale=scale,referenceAnchor=[152,support_y],pivot=[92,172],tip=tip,gapToLeaf=gap,
                targetTipY=target,remainingSourcePixels=target-tip[1],netRendererFootOffset=0,
                limitations='Single-pose source registration; does not prove transitions or native contact.')
    (out/'registration.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision',default='01',choices=['01','02','03','04'])
    main(parser.parse_args().revision)
