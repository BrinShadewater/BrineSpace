from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'pickup-runtime-v47';inventory=json.loads((r/'character/james-full-set-review-2026-10-02/current-selection-v31/source-inventory.json').read_bytes());native=json.loads((out/'native-evidence.json').read_bytes());records=[]
for facing in ['west','east','north','south']:
    board=Image.new('RGBA',(7*256,2*281),(48,59,63,255));draw=ImageDraw.Draw(board)
    for row,mode in enumerate(['bare','helmet']):
        for col,keyslot in enumerate([('idle-'+facing,0)]+[('pickup-'+facing,i) for i in range(6)]):
            key,slot=keyslot;s=inventory['states'][mode][key];f=r/s['frameFiles'][slot];im=Image.open(f).convert('RGBA');assert im.size==(s['frameWidth'],s['frameHeight']) and s['standingHeight']==148
            x=col*256+128-int(s['pivot'][0]);y=row*281+25+224-int(s['pivot'][1]);board.alpha_composite(im,(x,y));draw.text((col*256+4,row*281+5),mode+' '+('selected idle0' if col==0 else 'pickup'+str(slot)),fill='white');records.append(dict(file=f.relative_to(r).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),mode=mode,direction=facing,slot=slot,key=key))
    board.convert('RGB').save(out/(facing+'-source-review.png'))
    rows=[row for row in native['results'] if row['facing']==facing];files=[Path(f.removeprefix('res://')) for row in rows for f in row['captures']];ims=[Image.open(f).convert('RGB') for f in files];w=max(im.width for im in ims);h=max(im.height for im in ims);b=Image.new('RGB',(3*w,2*(h+24)),(48,59,63));d=ImageDraw.Draw(b)
    for i,(f,im) in enumerate(zip(files,ims)):
        x=i%3*w;y=i//3*(h+24);b.paste(im,(x,y+24));d.text((x+3,y+5),f.stem,fill='white')
    b.save(out/(facing+'-room-review.png'))
(out/'visual-inputs.json').write_text(json.dumps(dict(sourceRecords=records,sourcePoses=48,selectedIdleReferenceSlots=8,roomCaptures=24,scope='Same148ruler and physical foot registration only; no silhouette fit, pose rescale or grade. Reference is effective selected idle0, not newly certified original master.'),indent=2)+'\n')
print('Four paired source boards cover48pickup poses/eight selected idle references; four room boards cover24captures.')
