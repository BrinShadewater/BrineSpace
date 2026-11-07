"""Register authored whole-body walk without freezing torso or normalizing each pose."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary,chroma
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/veld-identity-correction-v1'

def main():
    source=BASE/'sources/walk-east-fullbody-03.png';raw=binary(chroma(source))
    assert raw.size==(2172,724)
    alpha=np.asarray(raw)[:,:,3];edges=np.diff(np.r_[False,alpha.any(0),False].astype(int))
    starts,ends=np.where(edges==1)[0],np.where(edges==-1)[0]
    assert len(starts)==len(ends)==6
    # Recorded pelvis centers in the raw source; do not center on swinging hands/feet.
    pelvis=[185,537,883,1245,1594,1973]
    scale=140/562;ground=640;durations=[170,130,150,170,130,150]
    out=BASE/'review/walk-east-fullbody-01';out.mkdir(exist_ok=True)
    poses=[];records=[];sheet=Image.new('RGB',(1536,256),'#293b40')
    for i,(left,right) in enumerate(zip(starts,ends)):
        left=int(left)-2;right=int(right)+2
        tile=raw.crop((left,0,right,724));dense=binary(tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX),True)
        at=(round(128-(pelvis[i]-left)*scale),round(223-ground*scale))
        pose=Image.new('RGBA',(256,256));pose.alpha_composite(dense,at);pose.save(out/f'walk-east-{i:03}.png');poses.append(pose)
        sheet.paste(pose,(i*256,0),pose)
        records.append(dict(sourceCrop=[left,0,right,724],pelvisX=pelvis[i],position=at,bounds=pose.getbbox()))
    sheet.save(out/'contact.png')
    previews=[]
    for pose in poses:
        canvas=Image.new('RGB',(256,256),'#293b40');ImageDraw.Draw(canvas).line((0,224,256,224),fill='#839597');canvas.paste(pose,(0,0),pose);previews.append(canvas)
    previews[0].save(out/'stationary-loop.gif',save_all=True,append_images=previews[1:],duration=durations,loop=0)
    (out/'registration.json').write_text(json.dumps(dict(status='unselected_fullbody_motion_study',source=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scale=scale,ground=ground,pivot=[128,224],durations=durations,records=records,limits=['Pelvis anchors require movement review, not inferred world-space planting.','Loop phase/foot contact, native travel cadence and fitted equipment remain open.','Source has visible full-body changes; no old torso or leg cutouts are pasted over it.']),indent=2)+'\n')
    print('Prepared six whole-body gait study frames with fixed scale/ground; not selected.')
if __name__=='__main__':main()
