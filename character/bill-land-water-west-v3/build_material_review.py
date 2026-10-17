from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;OLD=P.parent/'bill-land-water-west-v2'
board=Image.new('RGB',(1600,720),'#182932');d=ImageDraw.Draw(board);records=[]
for col,i in enumerate([2,3]):
    old=Image.open(OLD/f'bare/frames/land-swim-west/{i:03}.png').convert('RGBA')
    new=Image.open(P/f'bare/frames/land-swim-west/{i:03}.png').convert('RGBA')
    a=np.array(old);b=np.array(new)
    oa=a[:,:,3]>180;na=b[:,:,3]>180
    intersection=np.count_nonzero(oa&na);union=np.count_nonzero(oa|na)
    records.append({'pose':i,'opaqueAlphaThresholdExclusive':180,'oldAlphaBBox':old.getchannel('A').getbbox(),'newAlphaBBox':new.getchannel('A').getbbox(),'opaqueSilhouetteIoU':intersection/union,'identicalRGBA':old.tobytes()==new.tobytes(),'scope':'Silhouette overlap diagnostic, not anatomy/texture/grade acceptance.'})
    x,y=(147,114) if i==2 else (141,118)
    rect=(x-45,y-10,x+55,y+75)
    for row,im in enumerate([old,new]):
        crop=im.crop(rect).resize((400,340),Image.Resampling.NEAREST)
        board.paste(crop,(col*800,row*360+20),crop)
        d.text((col*800+5,row*360+3),('V2' if row==0 else 'V3')+f' pose{i} /native4x ruler',fill='white')
        crop=im.crop((x-10,y+25,x+45,y+80)).resize((220,220),Image.Resampling.NEAREST)
        board.paste(crop,(col*800+450,row*360+40),crop)
        d.text((col*800+450,row*360+3),'Sleeve, badge and hip detail /4x',fill='white')
board.save(P/'material-detail-comparison.png')
e=json.loads((P/'review.json').read_text())
e.update(generationMode='built-in image_gen',materialGeometryDiagnostics=records,priorSourceBank='bill-land-water-west-v2',visualAcceptance='pending comparative material/detail source review; no new native proof')
sources=[]
for reg in e['registrations'].values():sources.extend([P.parent/reg['source'],P.parent/reg['prompt']])
e['rawAndPromptSHA256']={str(f.relative_to(P.parent)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sources}
(P/'review.json').write_text(json.dumps(e,indent=2)+'\n')
print(json.dumps(records))
