"""Selected floor pickup -> authored release -> existing stow, candidate only."""
from pathlib import Path
import json
from PIL import Image, ImageDraw

P=Path(__file__).resolve().parent
reg=json.loads((P/'registration.json').read_text())
case=Image.open(P/'case.png').convert('RGBA')
case_at=tuple(reg['casePosition'])
durations=[50,80,60,80,80,70,60]
frames=[]; contact=Image.new('RGB',(7*220,330),'#303b40')
cd=ImageDraw.Draw(contact)
for slot in range(7):
    elapsed=sum(durations[:slot])/1000
    # Existing return speed and nominal CELL384 physical artwork scale.
    offset=round(72*elapsed/(384*.17/148))
    board=Image.new('RGB',(1000,370),'#303b40');d=ImageDraw.Draw(board)
    d.text((12,8),'West case release join candidate / offline / not installed',fill='white')
    d.text((12,28),f'Slot {slot} — physical return illustration 72 units/s — fixed selected case',fill='white')
    for row,gear in enumerate(['bare','helmet']):
        if slot==0:
            im=Image.open(P.parent/f'james-water-cargo-west-v1/frames/{gear}/swim-pickup/001.png').convert('RGBA')
            origin=Image.new('RGBA',(450,190));origin.alpha_composite(im,(125,-75))
        else:
            path=P/f'body-{gear}.png' if slot==1 else (P/f'followthrough/{gear}/{slot-1:03d}.png' if slot<6 else P.parent/'james-water-torch-stow-west-v1'/('frames/bare' if gear=='bare' else 'frames')/'005.png')
            im=Image.open(path).convert('RGBA')
            origin=Image.new('RGBA',(450,190));origin.alpha_composite(im,(125+offset,-75));origin.alpha_composite(case,(125+case_at[0],case_at[1]-75))
        top=65+row*145
        crop=origin.crop((0,0,450,120));board.paste(crop,(12,top),crop)
        small=crop.resize((round(450*82/148),round(120*82/148)),Image.Resampling.LANCZOS)
        board.paste(small,(570,top+25),small)
        d.text((12,top+120),gear+' / shared 148px ruler',fill='white')
        d.text((570,top+120),'native 82px ruler',fill='white')
        # Registered pose sheet deliberately removes physical translation to review anatomy.
        layer=im.copy()
        if slot:layer.alpha_composite(case,case_at)
        crop=layer.crop((35,80,235,180));contact.paste(crop,(slot*220+10,row*155+35),crop)
        cd.text((slot*220+10,row*155+10),gear+' slot '+str(slot),fill='white')
    frames.append(board)
frames[0].save(P/'join-review.gif',save_all=True,append_images=frames[1:],duration=[400]+durations[1:-1]+[600],loop=0,disposal=2)
contact.save(P/'join-contact.png')
(P/'join-study.json').write_text(json.dumps({'status':'offline_candidate_not_installed','scope':'One selected West floor-pickup1 release join per gear; not all indexed profiles, world anchor, persistence or master-height acceptance.','durationsMs':durations,'durationMs':sum(durations),'bodyOffsetsSourcePixels':[round(72*sum(durations[:i])/1000/(384*.17/148)) for i in range(7)],'casePosition':case_at,'physicalRuler':'CELL384 * .17 / standingHeight148; native preview82/148','sequence':['exact selected pickup1','new authored release','selected stow1','selected stow2','selected stow3','selected stow4','exact selected swim0']},indent=2)+'\n')
print('Built paired seven-pose join study; 480ms candidate, no production edit.')
