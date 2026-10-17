"""Review outputs and exhaustive frame/atlas validation for the rover pack."""
from pathlib import Path
import json, hashlib
from PIL import Image, ImageDraw
import numpy as np
R=Path(__file__).resolve().parent
D=json.loads((R/'manifest.json').read_text())
order=['north','northeast','east','southeast','south','southwest','west','northwest']
board=Image.new('RGBA',(1344,1000),'#17272e');draw=ImageDraw.Draw(board)
for i,h in enumerate(order):
    p=Image.open(R/D['headings'][h]['pose']).convert('RGBA')
    x=i%4*336;y=i//4*500
    draw.text((x+16,y+15),h.upper(),fill='#c5d7d9')
    board.alpha_composite(p.resize((336,336),Image.Resampling.LANCZOS),(x,y+40))
    small=p.resize((152,152),Image.Resampling.LANCZOS)
    board.alpha_composite(small,(x+12,y+340))
    draw.rectangle((x+176,y+340,x+335,y+499),fill='#c2c5bd')
    board.alpha_composite(small,(x+180,y+340))
board.convert('RGB').save(R/'review/directions.png')
comparison=Image.new('RGBA',(660,340),'#17272e');cd=ImageDraw.Draw(comparison)
construction=R.parent/'drone-motion-v2-2026-09-26/polish/poses/south.png'
for i,(name,path) in enumerate([('Construction',construction),('Mining rover',R/'poses/south.png')]):
    p=Image.open(path).convert('RGBA');p=p.resize((round(p.width*.34),round(p.height*.34)),Image.Resampling.LANCZOS)
    x=165+i*330;comparison.alpha_composite(p,(x-p.width//2,100-p.height//2))
    cd.text((x-65,190),name+' / 0.34x',fill='#c5d7d9')
    q=p.resize((p.width*2,p.height*2),Image.Resampling.NEAREST)
    # Native pixels above are the sizing reference; avoid enlarging artwork independently.
cd.text((24,260),'Shared library-pixel scale; proposed review footprint.',fill='#829ba7')
comparison.convert('RGB').save(R/'review/construction-mining-scale.png')
clips={e['id']:e for e in D['states']};jobs=[]
for n in range(0,180,3):
    b=Image.new('RGBA',(896,950),'#17272e');dr=ImageDraw.Draw(b)
    for i,h in enumerate(['north','east','south','west']):
        e=clips['mine-'+h];x=i%2*448;y=i//2*475
        dr.text((x+15,y+10),h.upper()+' / '+e['phases'][n],fill='#c5d7d9')
        p=Image.open(R/e['frameFiles'][n]).convert('RGBA');p.alpha_composite(Image.open(R/e['effectFiles'][n]).convert('RGBA'))
        b.alpha_composite(p,(x,y+27))
    jobs.append(b.convert('RGB'))
jobs[0].save(R/'review/mining-jobs.gif',save_all=True,append_images=jobs[1:],duration=100,loop=0)
checks=[];total=0
assert len(clips)==112 and len(D['headings'])==8
for e in D['states']:
    body=Image.open(R/e['atlas']['path']).convert('RGBA');fx=Image.open(R/e['effectAtlas']['path']).convert('RGBA')
    base=Image.open(R/D['headings'][e['heading']]['pose']).convert('RGBA')
    cargo=Image.open(R/e['cargoAtlas']['path']).convert('RGBA') if 'cargoAtlas' in e else None
    assert len(e['frameFiles'])==len(e['effectFiles'])==len(e['phases'])==e['frameCount']
    for n,(bp,fp) in enumerate(zip(e['frameFiles'],e['effectFiles'])):
        im=Image.open(R/bp).convert('RGBA');eff=Image.open(R/fp).convert('RGBA')
        assert im.size==eff.size==(448,448)
        bbox=im.getbbox();assert bbox and min(bbox[:2])>0 and max(bbox[2:])<448,(e['id'],n,bbox)
        box=(n%6*448,n//6*448,(n%6+1)*448,(n//6+1)*448)
        assert im.tobytes()==body.crop(box).tobytes() and eff.tobytes()==fx.crop(box).tobytes()
        if cargo is not None:
            ci=Image.open(R/e['cargoFiles'][n]).convert('RGBA');assert ci.size==(448,448) and ci.tobytes()==cargo.crop(box).tobytes()
            cb=ci.getbbox();assert cb is None or (min(cb[:2])>0 and max(cb[2:])<448)
        if e['state'] in ['drive','reverse']:assert im.getchannel('A').tobytes()==base.getchannel('A').tobytes()
        if e['state']=='mine' and n in [0,e['frameCount']-1]:assert im.tobytes()==base.tobytes()
        total+=1
    checks.append({'clip':e['id'],'frames':e['frameCount'],'result':'pass'})
for h in ['north','east','south','west']:
    collect=clips['collect-'+h];unload=clips['unload-'+h];carry=clips['carry-'+h]
    assert Image.open(R/collect['cargoFiles'][-1]).tobytes()==Image.open(R/unload['cargoFiles'][0]).tobytes()==Image.open(R/carry['cargoFiles'][0]).tobytes()
    assert Image.open(R/collect['cargoFiles'][0]).tobytes()==Image.open(R/unload['cargoFiles'][-1]).tobytes()
for e in D['states']:
    if 'lampSamples' in e:assert len(e['lampSamples'])==e['frameCount'] and all(0<=a<=1 for a in e['lampSamples'])
for s in D['sourceFiles']:assert hashlib.sha256((R/s['path']).read_bytes()).hexdigest()==s['sha256']
result={'clips':len(clips),'bodyFrames':total,'effectFrames':total,'atlasParity':'all frames','clipping':'none','travelAlpha':'unchanged','miningEndpoints':'match idle','sourceHashes':'pass','checks':checks}
(R/'review/final-validation.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='checks'}),flush=True)
