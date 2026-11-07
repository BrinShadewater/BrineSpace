"""Whole current swimming sources beside own idle, preserving declared pivots."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-full-family-audit-2026-10-03';r=json.loads((B/'inventory.json').read_text());states=r['states'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
for side in ['east','west','north','south']:
    entries=[('idle-'+side,0)]+[('swim-'+side,i) for i in range(4)]+[('swim-carry-'+side,i) for i in range(4)]
    board=Image.new('RGB',(2016,238),'#293b40');d=ImageDraw.Draw(board)
    for col,(key,slot) in enumerate(entries):
        state=states[key];source=state['frames'][slot];p=ROOT/source['path'];assert sha(p)==source['sha256']
        im=Image.open(p).convert('RGBA');pivot=state['pivot'];assert state['standingHeight']==148
        offset=(round(112-pivot[0]),round(172-pivot[1]));bb=im.getbbox();assert offset[0]+bb[0]>=0 and offset[0]+bb[2]<=224 and offset[1]+bb[1]>=0 and offset[1]+bb[3]<=208
        board.paste(im,(224*col+offset[0],25+offset[1]),im);d.text((224*col+3,5),key+' '+str(slot),fill='white')
        records.append({'direction':side,'key':key,'slot':slot,'source':source['path'],'sha256':source['sha256'],'pivot':pivot,'standingHeight':148,'wholeTranslation':offset,'operations':'Whole original pixels at common pivot112,172; noresample/perposefit. Compare body construction/camera/kick, not totalbounds alone.'})
    board.save(B/f'swim-cross-{side}.png')
(B/'swim-cross-sources.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'records':records},indent=2)+'\n')
print('Four own-idle/unloaded4/loaded4 whole cross-family boards prepared;36sources exact.')
