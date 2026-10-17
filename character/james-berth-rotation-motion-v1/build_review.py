from pathlib import Path
import json, hashlib, math
from PIL import Image, ImageDraw

P=Path(__file__).resolve().parent
R=P.parents[1]
e=json.loads((P/'evidence.json').read_bytes())
before=json.loads((P/'runtime-inputs-before.json').read_bytes())
changed=[rel for rel,h in before.items() if hashlib.sha256((R/rel).read_bytes()).hexdigest()!=h]
assert not changed, changed
for case in e['cases']:
    rows=[r for r in e['records'] if r['case']==case['id']]
    board=Image.new('RGB',(1440,40+math.ceil(len(rows)/6)*235),'#263238')
    draw=ImageDraw.Draw(board)
    draw.text((8,8),case['id']+' | actual chronological rest source changes | fixed viewport crop | nearest x1.5',fill='white')
    for i,row in enumerate(rows):
        im=Image.open(R/row['capture'].removeprefix('res://')).convert('RGB')
        x,y=row['footViewport']; crop=im.crop((round(x)-105,round(y)-140,round(x)+55,round(y)+5))
        crop=crop.resize((240,218),Image.Resampling.NEAREST)
        px,py=(i%6)*240,40+(i//6)*235
        board.paste(crop,(px,py))
        draw.text((px+4,py+219),row['key'].removesuffix('-north')+' '+str(row['index']),fill='white')
    board.save(P/(case['id']+'-chronological.png'))
preview=Image.new('RGB',(960,348),'#263238')
draw=ImageDraw.Draw(preview)
for j,mode in enumerate(['bare','helmet']):
    rows=[r for r in e['records'] if r['case']==mode+'-q0']
    for i,(key,index) in enumerate([('lie-down',0),('lie-down',2),('lie-down',5),('sleep',2),('get-up',3),('get-up',5)]):
        row=next(r for r in rows if r['key']==key+'-north' and r['index']==index)
        im=Image.open(R/row['capture'].removeprefix('res://')).convert('RGB'); x,y=row['footViewport']
        preview.paste(im.crop((round(x)-105,round(y)-140,round(x)+55,round(y)+5)),(i*160,j*174+20))
        draw.text((i*160+3,j*174+3),mode+' '+key+' '+str(index),fill='white')
preview.save(P/'native-key-poses.png')
(P/'review-evidence.json').write_text(json.dumps({'unchangedInputs':len(before),'changedInputs':changed,'nativeRecords':len(e['records']),'boards':[c['id']+'-chronological.png' for c in e['cases']],'scope':'Fixed viewport crops of every captured source change. Repeated breathing cycles retained; not continuous rendered footage.'},indent=2)+'\n')
print(len(e['records']),'native poses;',len(before),'frozen inputs unchanged; eight chronological boards')
