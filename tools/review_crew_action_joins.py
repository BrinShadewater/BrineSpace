"""Report selected action joins in foot coordinates; differences require visual review."""
from pathlib import Path
import argparse
import json
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
PACKS={'veld':'dr-veld-v2','branforth':'chief-engineer-branforth-v2','marsh':'marsh-v2'}
JOINS=[('idle',0,'pickup',0),('unload',-1,'idle',0),
       ('sit-down',-1,'sit-idle',0),('sit-rise',-1,'idle',0),
       ('lie-down',-1,'sleep',0),('sleep',0,'get-up',0),('get-up',-1,'idle',0)]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('actor',choices=PACKS)
    args=parser.parse_args();art=ROOT/'character'/PACKS[args.actor]
    out=ROOT/'output/crew-replacement-2026-09-12'/args.actor/'action-joins'
    out.mkdir(parents=True,exist_ok=True)
    catalog=json.loads((art/'catalog.json').read_text());clips={}
    for variant in ['body','equipment']:
        for rel in catalog[variant]:
            manifest=art/rel;data=json.loads(manifest.read_text())
            for state in data['states']:
                clips[variant,state['id']]=(manifest.parent,state,data['pivot'])
    def frame(variant,key,index):
        root,state,pivot=clips[variant,key]
        im=Image.open(root/state['frameFiles'][index]).convert('RGBA')
        canvas=Image.new('RGBA',(384,320))
        canvas.alpha_composite(im,(round(192-pivot[0]),round(260-pivot[1])))
        a=np.array(canvas);a[a[:,:,3]==0]=0
        return Image.fromarray(a),a
    report=[]
    for direction in ['south','east','north','west']:
        for variant in ['body','equipment']:
            rows=[]
            for before,i,after,j in JOINS:
                a,b=before+'-'+direction,after+'-'+direction
                if (variant,a) not in clips or (variant,b) not in clips:continue
                left,x=frame(variant,a,i);right,y=frame(variant,b,j)
                changed=np.any(x!=y,axis=2);union=(x[:,:,3]>0)|(y[:,:,3]>0)
                count=int(changed.sum());fraction=float(count/max(1,union.sum()))
                record={'variant':variant,'from':a,'fromFrame':i,'to':b,'toFrame':j,
                        'differentPixels':count,'fractionOfVisibleUnion':fraction}
                report.append(record);rows.append((record,left,right))
            if not rows:continue
            sheet=Image.new('RGB',(768,len(rows)*220),'#293b40');draw=ImageDraw.Draw(sheet)
            for n,(record,left,right) in enumerate(rows):
                for col,im in enumerate([left,right]):
                    crop=im.crop((0,80,384,280));sheet.paste(crop,(col*384,n*220+20),crop)
                draw.text((4,n*220+3),f'{record["from"]} -> {record["to"]}: {record["differentPixels"]} changed pixels',fill='white')
            sheet.save(out/(direction+'-'+variant+'.png'))
    (out/'joins.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'actor':args.actor,'joins':len(report),'exact':sum(r['differentPixels']==0 for r in report),
                      'reviewDifferences':[r for r in report if r['differentPixels']>0]}))

if __name__=='__main__':main()
