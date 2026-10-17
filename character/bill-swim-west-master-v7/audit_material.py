from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
P=Path(__file__).resolve().parent;R=P.parent
old=json.loads((R/'bill-swim-west-master-v5/review.json').read_text(encoding='utf-8'))
new=json.loads((P/'body-source/review.json').read_text(encoding='utf-8'))
rows=[]
for prior,after in zip(old['frames'],new['frames']):
    a=np.array(Image.open(R/prior['source']).convert('RGBA'));b=np.array(Image.open(R/after['source']).convert('RGBA'))
    assert a.shape==b.shape
    ma=a[:,:,3]>180;mb=b[:,:,3]>180
    def bbox(mask):
        y,x=np.where(mask);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
    rows.append(dict(name=after['name'],rawOpaqueMaskIoU=float((ma&mb).sum()/(ma|mb).sum()),opaqueMaskExact=bool(np.array_equal(ma,mb)),alphaExact=bool(np.array_equal(a[:,:,3],b[:,:,3])),opaqueBoundsBeforeAfter=[bbox(ma),bbox(mb)],RGBAChangedPixels=int(np.any(a!=b,axis=2).sum()),priorTranslation=prior['translation'],newTranslation=after['translation'],registeredHipMarker=after['registeredHipMarker'],scope='Material-only prompt treated as whole-source replacement; silhouette overlap is not anatomical or visual acceptance.'))
for gear in ['bare','helmet']:
    board=Image.new('RGB',(2112,720),'#182932');d=ImageDraw.Draw(board)
    for row,folder in enumerate([R/'bill-swim-west-master-v6',P]):
        for i,rec in enumerate(new['frames']):
            im=Image.open(folder/gear/f'frames/swim-west/{i:03}.png').convert('RGBA');board.paste(im,(i*352,row*360+25),im)
            d.text((i*352+4,row*360+4),('Before ' if row==0 else 'Matte ')+gear+' '+rec['name'],fill='white')
    board.save(P/f'{gear}-material-comparison.png')
# Native-scale original master and extended phase compare material without fitting.
density=148/956
master=Image.open(R/'crew-side-masters-v1/bill-side-master-01.png').convert('RGBA').crop((850,0,1280,1024))
master=master.resize((round(master.width*density),round(master.height*density)),Image.Resampling.LANCZOS)
ref=Image.new('RGBA',(352,320));ref.alpha_composite(master,(125,round(224-977*density)))
board=Image.new('RGB',(1056,720),'#182932');draw=ImageDraw.Draw(board)
for row,g in enumerate(['bare','helmet']):
    for col,(title,im) in enumerate([('Original bare master',ref),('Previous extend',Image.open(R/f'bill-swim-west-master-v6/{g}/frames/swim-west/000.png').convert('RGBA')),('Matte extend',Image.open(P/g/'frames/swim-west/000.png').convert('RGBA'))]):
        board.paste(im,(col*352,row*360+25),im);draw.text((col*352+4,row*360+4),g+' '+title,fill='white')
board.save(P/'master-material-review.png')
report=dict(materialEditedSources=rows,normalSelected=False,nativeAcceptance=False,wholeSourceProtectionClaim=False)
(P/'whole-bank-material-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(IoUByPhase=[(r['name'],round(r['rawOpaqueMaskIoU'],4)) for r in rows],allRawAlphaExact=all(r['alphaExact'] for r in rows))))
