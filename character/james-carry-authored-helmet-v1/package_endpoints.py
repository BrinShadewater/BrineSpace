from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];rect=(102,62,155,110);rows=[];records=[]
for name,index in [('south',0),('west',4)]:
    bareFile=r/'character/james-carry-headcaps-v1/frames'/f'{index:03}.png';masterFile=p/(name+'-standing.png')
    bare=Image.open(bareFile).convert('RGBA');master=Image.open(masterFile).convert('RGBA');paired=bare.copy();paired.paste(master.crop(rect),rect[:2]);paired.save(p/(name+'-helmet.png'))
    a=bare.copy();b=paired.copy()
    for im in [a,b]:im.paste((0,0,0,0),rect)
    assert a.tobytes()==b.tobytes();rows.extend([bare,paired,master]);records.append({'direction':name,'bareSource':bareFile.relative_to(r).as_posix(),'bareSourceSha256':hashlib.sha256(bareFile.read_bytes()).hexdigest(),'masterFile':masterFile.name,'masterSha256':hashlib.sha256(masterFile.read_bytes()).hexdigest(),'nativeAlpha128Bounds':paired.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox(),'protectedOutsidePixels':62992,'protectedOutsideExact':True})
out=Image.new('RGBA',(3*256,2*282),(48,59,63,255));d=ImageDraw.Draw(out)
for i,item in enumerate(rows):
    x=i%3*256;y=i//3*282;out.alpha_composite(item,(x,y+26));d.text((x+5,y+7),['bare carried','exact master helmet region','standing helmet source'][i%3],fill='white')
out.convert('RGB').save(p/'endpoint-comparison.png')
(p/'endpoint-review.json').write_text(json.dumps({'records':records,'admissionRegion':rect,'perPoseFit':False,'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'Two carried endpoint bodies with exact same-position selected standing helmet head regions; torso/contact/gear joins require review.'},indent=2)+'\n',encoding='utf-8');print(json.dumps({'endpointBounds':[v['nativeAlpha128Bounds'] for v in records],'outsideExact':62992}))
