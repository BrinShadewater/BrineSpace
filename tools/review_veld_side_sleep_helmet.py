"""Nonselected, reproducible fitted equipment study for Veld east sleep revision 06."""
from pathlib import Path
import json
from PIL import Image, ImageDraw
from extract_crew_seating_study import main as extract
from rebuild_human_crew_art import HumanRebaker, HumanHelmet
from crew_sleeping_revision import SIDE_POSES as POSES

ROOT=Path(__file__).resolve().parents[1]
# Centers are measured in the extracted 256px body canvas, not old helmet art.

def main():
    frames=extract('veld','east','06','sleeping','gutter',True)
    overlay=HumanHelmet(HumanRebaker('veld')).overlay('east',(30,32))
    out=ROOT/'character/crew-action-detail-v2/review/veld-sleeping-east-06-helmet'
    out.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(6*256,4*256),'#293b40');draw=ImageDraw.Draw(sheet)
    records=[]
    for row,state in enumerate(['lie-down','sleep']):
        for i,body in enumerate(frames[state]):
            x,y,angle=POSES[i] if row==0 else POSES[-1]
            fitted=overlay.rotate(angle,Image.Resampling.NEAREST,expand=True)
            position=(round(x-fitted.width/2),round(y-fitted.height/2))
            equipped=body.copy();equipped.alpha_composite(fitted,position)
            equipped.save(out/f'{state}-{i:03}.png')
            sheet.paste(body,(i*256,row*512),body)
            sheet.paste(equipped,(i*256,row*512+256),equipped)
            draw.text((i*256+4,row*512+4),f'{state} {i}',fill='white')
            records.append(dict(state=state,frame=i,center=[x,y],angle=angle,topLeft=position))
    sheet.save(out/'contact.png')
    (out/'registration.json').write_text(json.dumps(dict(status='study_not_selected',bodyRevision='06',helmetSize=[30,32],frames=records),indent=2)+'\n')
    print(out.relative_to(ROOT))

if __name__=='__main__':main()
