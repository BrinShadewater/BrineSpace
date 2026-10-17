from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent
for folder in ['parts/source','parts/native','review']:(P/folder).mkdir(parents=True,exist_ok=True)
source=Image.open(P/'source-02.png').convert('RGBA');records=[];parts={};scale=None
directions=['south','east','north','west']
row_edges=[0,400,780,1086] # Actual transparent row gutters, not assumed equal cells.
for row,kind in enumerate(['closed-terminal','open-terminal','data-cartridges']):
    for col,direction in enumerate(directions):
        box=(round(col*source.width/4),row_edges[row],round((col+1)*source.width/4),row_edges[row+1])
        cell=source.crop(box);a=np.array(cell.getchannel('A'));ys,xs=np.where(a>100)
        assert len(xs) and xs.min()>1 and ys.min()>1 and xs.max()<cell.width-2 and ys.max()<cell.height-2,(kind,direction,'cell boundary')
        bounds=(int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1);im=cell.crop(bounds)
        name=kind+'-'+direction;im.save(P/f'parts/source/{name}.png')
        if scale is None:scale=16/im.height
        native=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.LANCZOS)
        native.save(P/f'parts/native/{name}.png');parts[name]=native
        records.append({'id':name,'cell':list(box),'trim':list(bounds),'sourceSize':list(im.size),'nativeSize':list(native.size),'scale':scale,'path':f'parts/native/{name}.png','mirrored':False})
board=Image.new('RGB',(1000,720),'#272b2e');draw=ImageDraw.Draw(board)
draw.text((20,15),'KRUSHER DOM / EQUIPMENT FIT STUDY — STANDING ONLY',fill='white')
fit_records=[]
attachments={
 'south':[('closed-terminal-south',(106,90)),('data-cartridges-south',(75,92))],
 'east':[('data-cartridges-east',(92,93))],
 'north':[('closed-terminal-north',(75,97)),('data-cartridges-north',(103,97))],
 'west':[('closed-terminal-west',(88,92))]}
for col,direction in enumerate(directions):
    file=R/f'character/krusher-bill-base-test-v2/frames/bare/idle-{direction}/000.png';bare=Image.open(file).convert('RGBA');fitted=bare.copy();mask=Image.new('L',bare.size)
    for name,pos in attachments[direction]:
        im=parts[name];fitted.alpha_composite(im,pos);mask.paste(im.getchannel('A'),pos)
    # Existing hanging forearms remain in front of the hip accessories.
    old=np.array(bare);new=np.array(fitted);yy,xx=np.mgrid[:184,:184]
    forearm=(old[:,:,3]>0)&(yy>96)&(yy<132)&((xx<76)|(xx>111)) if direction in ['south','north'] else np.zeros((184,184),bool)
    new[forearm]=old[forearm];fitted=Image.fromarray(new)
    fitted.save(P/f'review/fitted-{direction}.png');mask.save(P/f'review/attachment-mask-{direction}.png')
    for row,im in enumerate([bare,fitted]):
        large=im.resize((230,230),Image.Resampling.NEAREST);board.paste(large,(col*250+10,row*290+45),large);draw.text((col*250+20,row*290+280),direction+(' / base' if row==0 else ' / fitted study'),fill='white')
    small=fitted.resize((92,92),Image.Resampling.LANCZOS);board.paste(small,(col*250+80,620),small)
    allowed=np.array(mask)>0;fit_records.append({'direction':direction,'source':str(file.relative_to(R)),'sourceSha256':hashlib.sha256(file.read_bytes()).hexdigest(),'attachments':attachments[direction],'outsideAttachmentsExact':bool(np.array_equal(old[~allowed],new[~allowed])),'path':f'review/fitted-{direction}.png'})
board.save(P/'review/equipment-fit.png')
report={'source':'source-02.png','sourceSha256':hashlib.sha256((P/'source-02.png').read_bytes()).hexdigest(),'method':'builtin imagegen source; deterministic cell extraction and one common native density; static attachment comparison','parts':records,'fit':fit_records,'limitations':['Static fit only; no motion registration or hand contacts proved','Far-side terminal hidden in east view; far-side cartridges hidden in west','Generated open terminal remains a concept; exact folding geometry needs motion review'],'sourceAlphaRange':list(source.getchannel('A').getextrema())}
(P/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'parts':len(records),'sourceAlpha':report['sourceAlphaRange'],'nativeSizes':{r['id']:r['nativeSize'] for r in records},'outsideAttachmentsExact':all(r['outsideAttachmentsExact'] for r in fit_records)}))
assert all(r['outsideAttachmentsExact'] for r in fit_records)
