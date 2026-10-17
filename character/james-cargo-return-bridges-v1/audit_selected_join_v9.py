from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw

p=Path(__file__).resolve().parent;r=p.parents[1]
out=p/'selected-join-audit-v9';out.mkdir(exist_ok=True)
board=Image.new('RGB',(7*256,800),'#303b40');draw=ImageDraw.Draw(board)
report={'scope':'Current normal V9 source join; exact pivot alignment, no per-pose height normalization. Upper rectangle is a diagnostic region, not anatomical head segmentation. No native motion/master/full-set acceptance.', 'gears':{},'inputs':{}}
refs=json.loads((p/'reference-evidence.json').read_bytes())['sources']
for row,gear in enumerate(['bare','helmet']):
    mp=p/(gear+'-joined-manifest-v9.json');m=json.loads(mp.read_bytes())
    report['inputs'][str(mp.relative_to(r))]=hashlib.sha256(mp.read_bytes()).hexdigest()
    images=[];stats=[]
    for i,ref in enumerate(m['states'][0]['frameFiles']):
        path=r/ref[6:] if ref.startswith('res://') else p/ref
        im=Image.open(path).convert('RGBA');assert im.size==(256,256)
        report['inputs'][str(path.relative_to(r))]=hashlib.sha256(path.read_bytes()).hexdigest()
        images.append(im)
        box=im.getchannel('A').point(lambda a:255 if a>=32 else 0).getbbox()
        stats.append({'index':i,'alpha32Bounds':box,'crownAbovePivot':224-box[1],'lowestVisibleRow':box[3]-1})
        x=i*256;y=row*400
        draw.text((x+5,y+5),gear+' / '+str(i)+' crown '+str(224-box[1]),fill='white')
        board.paste(im,(x,y+25),im)
        draw.line((x,y+249,x+255,y+249),fill='#a6b0b0')
        # Nearest enlarged diagnostic crop; does not alter selected artwork.
        bg=Image.new('RGBA',(256,256),'#303b40');bg.alpha_composite(im)
        crop=bg.crop((101,73,160,124)).convert('RGB').resize((118,102),Image.Resampling.NEAREST)
        board.paste(crop,(x+70,y+290))
    idle=next(x for x in refs if x['mode']==gear and x['key']=='idle-west')
    ip=r/idle['path'];im=Image.open(ip).convert('RGBA');reg=Image.new('RGBA',(256,256))
    reg.alpha_composite(im,(round(128-idle['pivot'][0]),round(224-idle['pivot'][1])))
    report['inputs'][str(ip.relative_to(r))]=hashlib.sha256(ip.read_bytes()).hexdigest()
    x=6*256;y=row*400;board.paste(reg,(x,y+25),reg)
    draw.text((x+5,y+5),gear+' / selected idle reference',fill='white')
    draw.line((x,y+249,x+255,y+249),fill='#a6b0b0')
    transitions=[]
    for i,(a,b) in enumerate(zip(images,images[1:])):
        aa=list(a.crop((0,0,256,110)).get_flattened_data());bb=list(b.crop((0,0,256,110)).get_flattened_data())
        transitions.append({'from':i,'to':i+1,'upperRegionChangedRgbaPixels':sum(x!=y for x,y in zip(aa,bb))})
    report['gears'][gear]={'frames':stats,'transitions':transitions}
board.save(out/'registered-sources-and-collars.png')
(out/'audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report['gears']))
