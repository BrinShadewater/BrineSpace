from pathlib import Path
from PIL import Image,ImageDraw
import json,math,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];e=json.loads((P/'native-clock-evidence.json').read_bytes())
assert e['complete'] and e['failures']==0
before=json.loads((P/'selected-inputs.json').read_bytes());changed=[rel for rel,h in before.items() if hashlib.sha256((R/rel).read_bytes()).hexdigest()!=h]
assert not changed,changed
for case in e['cases']:
    rows=[r for r in e['records'] if r['case']==case['id']];board=Image.new('RGB',(1440,40+math.ceil(len(rows)/6)*245),'#303b40');d=ImageDraw.Draw(board)
    d.text((8,8),case['id']+' | normal actor timer + selected renderer, prescribed initial state, no furniture',fill='white')
    for i,row in enumerate(rows):
        im=Image.open(R/row['capture'].removeprefix('res://')).convert('RGB');x,y=row['footViewport']
        crop=im.crop((round(x)-100,round(y)-180,round(x)+100,round(y)+10)).resize((240,228),Image.Resampling.NEAREST);at=(i%6*240,40+i//6*245);board.paste(crop,at);d.text((at[0]+4,at[1]+229),row['key']+' '+str(row['index']),fill='white')
    board.save(P/(case['id']+'-native-chronological.png'))
(P/'native-review-evidence.json').write_text(json.dumps({'nativeCaptures':len(e['records']),'unchangedInputs':len(before),'boards':[c['id']+'-native-chronological.png' for c in e['cases']],'scope':'Every captured selected-source change including repeated breathing loops, fixed viewport crops. Chronological pose review, not continuous captured native video.'},indent=2)+'\n')
print(len(e['records']),'native poses;',len(before),'inputs unchanged;8 chronological boards.')
