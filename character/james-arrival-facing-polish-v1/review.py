from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
report=json.loads((P/'installed-evidence.json').read_text())
assert report['failures']==0 and report['mismatches']==0
dry=Image.new('RGB',(720,1440),'#303b40');dd=ImageDraw.Draw(dry)
for row,mode in enumerate(['bare','helmet']):
    water=Image.new('RGB',(1320,720),'#303b40');dw=ImageDraw.Draw(water)
    for r,facing in enumerate(['east','south','west','north']):
        for medium in ['dry','flooded']:
            case=next(c for c in report['results'] if c['mode']==mode and c['medium']==medium and c['incoming']==facing)
            for i,ref in enumerate(case['captures']):
                im=Image.open(R/ref.removeprefix('res://')).convert('RGB')
                x,y=im.width//2,im.height//2
                crop=im.crop((x-105,y-100,x+105,y+70))
                if medium=='dry':
                    dry.paste(crop,(i*240,(row*4+r)*180+10));dd.text((i*240+4,(row*4+r)*180),mode+' diagnostics '+facing+' '+Path(ref).stem.split('-')[-1],fill='white')
                else:
                    water.paste(crop,(i*220,r*180+10));dw.text((i*220+4,r*180),mode+' stop '+facing+' '+str(i),fill='white')
    water.save(P/('native-arrival-stops-'+mode+'.png'))
dry.save(P/'native-arrival-diagnostics.png')
print('72 actual arrival captures:24 directional dry diagnostic samples and48 same-facing water stop poses')
