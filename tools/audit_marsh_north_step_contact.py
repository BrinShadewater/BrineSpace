"""Measure floor-depth evidence before choosing any North root-travel curve."""
from pathlib import Path
import argparse, json, hashlib
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-north-step-v1'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--version',required=True); parser.add_argument('--raw',action='store_true')
    args=parser.parse_args(); candidate=BASE/('candidate-'+args.version)
    if args.raw:
        rawpath=BASE/'sources'/('north-step-'+args.version+'.png'); raw=Image.open(rawpath).convert('RGBA')
        cells=[]
        for i in range(6):
            a=np.array(raw.crop((round(i*raw.width/6),0,round((i+1)*raw.width/6),raw.height)))
            a[:,:,3]=np.where(a[:,:,3]>=128,255,0); a[a[:,:,3]==0]=0; cells.append(Image.fromarray(a))
        neutral=cells[5].getbbox(); idle=Image.open(ROOT/'character/marsh-v2/frames/bare/idle-north/000.png')
        scale=(idle.getbbox()[3]-idle.getbbox()[1])/(neutral[3]-neutral[1]); measurements=[]
        for i,im in enumerate(cells):
            a=np.array(im); yy,xx=np.indices(a[:,:,3].shape); box=im.getbbox(); split=(box[0]+box[2])/2
            # A toe can cross the torso midline. Exclude a narrow middle band so
            # the other shoe cannot silently supply a side's floor measurement.
            margin=.03*(box[3]-box[1])
            soles={side:int(np.where((a[:,:,3]>0)&(yy>=box[1]+.65*(box[3]-box[1]))&((xx<split-margin) if side=='left' else (xx>=split+margin)))[0].max()) for side in ['left','right']}
            measurements.append({'cell':i,'soleEdges':soles,'leftAheadDensePixels':(soles['right']-soles['left'])*scale})
        result={'rawSha256':sha(rawpath),'neutralScale':scale,'centralExclusionFraction':.03,'measurements':measurements,'limits':'Raw outer silhouette floor-depth measurements; do not establish anatomical support or acceptance.'}
        (BASE/'sources'/('north-step-'+args.version+'.contact.json')).write_text(json.dumps(result,indent=2)+'\n')
        print('Raw dense left-ahead offsets:',[round(m['leftAheadDensePixels'],2) for m in measurements]); return
    records=[]; panels=[]
    for slot in range(7):
        path=candidate/('%03d.png'%slot); im=Image.open(path).convert('RGBA'); a=np.array(im)
        yy,xx=np.indices(a[:,:,3].shape); box=im.getbbox(); split=(box[0]+box[2])/2
        feet={}
        for side,left in [('left',True),('right',False)]:
            mask=(a[:,:,3]>0)&(yy>=145)&((xx<split) if left else (xx>=split))
            bottom=int(np.where(mask)[0].max())
            feet[side]=[float(np.median(np.where(mask & (yy>=bottom-2))[1])),bottom]
        records.append({'slot':slot,'sourceSha256':sha(path),'split':split,'soleEdges':feet,'leftAheadPixels':feet['right'][1]-feet['left'][1]})
        panel=Image.new('RGB',(368,420),'#293b40'); big=im.resize((368,368),Image.Resampling.NEAREST); panel.paste(big,(0,26),big); draw=ImageDraw.Draw(panel)
        draw.text((8,6),'Slot%d L%d R%d' % (slot,feet['left'][1],feet['right'][1]),fill='white')
        for side,color in [('left','#70dfbb'),('right','#ecbe70')]:
            x,y=feet[side]; draw.line((x*2-13,y*2+26,x*2+13,y*2+26),fill=color,width=2)
        panels.append(panel)
    board=Image.new('RGB',(368*7,420))
    for i,panel in enumerate(panels): board.paste(panel,(368*i,0))
    board.save(candidate/'contact-audit.png')
    landing=records[3]['leftAheadPixels']
    result={'candidate':args.version,'measurements':records,'landingDepthPixels':landing,'density':65.28/148,'impliedNorthLength':landing*65.28/148,'requiredRouteUnits':[5,7],'requiredDensePixels':[5*148/65.28,7*148/65.28],'landingDepthCompatible':5<=landing*65.28/148<=7,'rootContactVerified':False,'scope':'Binary silhouette sole edges belowrow145, split at figure bounds center; visual anatomical/support interpretation still required. This is not actor travel acceptance.'}
    (candidate/'contact-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Landing depth:',landing,'dense pixels; implied',round(result['impliedNorthLength'],3),'world units; compatible',result['landingDepthCompatible'])
if __name__=='__main__': main()
