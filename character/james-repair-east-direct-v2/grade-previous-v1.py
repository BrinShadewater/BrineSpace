"""Apply one measured cloth correction, preserving raw extracted frames."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def main():
    reference=json.loads((HERE/'reference.json').read_text());idle=np.array(Image.open(ROOT/reference['source']).convert('RGBA'))
    first=np.array(Image.open(HERE/'frames/000.png').convert('RGBA'));yy=np.indices(first.shape[:2])[0]
    def sample(a):
        rgb=a[:,:,:3].astype(float);lum=rgb.mean(2)
        return (a[:,:,3]>240)&(yy>67)&(yy<145)&(np.ptp(rgb,2)<35)&(lum>20)&(lum<95)
    source=np.median(first[:,:,:3][sample(first)],axis=0);target=np.median(idle[:,:,:3][sample(idle)],axis=0);gain=target/source
    dest=HERE/'graded';dest.mkdir(exist_ok=True);frames=[];records=[]
    for path in sorted((HERE/'frames').glob('*.png')):
        a=np.array(Image.open(path).convert('RGBA'));rgb=a[:,:,:3].astype(float);lum=rgb.mean(2)
        ys=np.where(a[:,:,3]>192)[0];head_end=int(ys.min())+38
        # Neutral suit and silver hardware only. Preserve head and yellow patches.
        weight=np.clip((42-np.ptp(rgb,2))/12,0,1)*np.clip((205-lum)/40,0,1)*np.clip((lum-12)/13,0,1)*np.clip((yy-head_end)/8,0,1)*(a[:,:,3]>16)
        matched=rgb*gain
        target_chroma=target-target.mean()
        neutral=matched.mean(2)[:,:,None]+target_chroma
        corrected=matched*.15+neutral*.85
        b=a.copy();b[:,:,:3]=np.clip(np.rint(rgb+weight[:,:,None]*(corrected-rgb)),0,255).astype('uint8')
        assert np.array_equal(a[:,:,3],b[:,:,3]);assert np.array_equal(a[weight==0],b[weight==0])
        Image.fromarray(b).save(dest/path.name);frames.append(Image.fromarray(b));records.append({'frame':path.name,'changedPixels':int(np.any(a!=b,axis=2).sum())})
    previews=[]
    for index,im in enumerate(frames):
        board=Image.new('RGB',(760,260),'#303b40');d=ImageDraw.Draw(board);d.text((8,8),'Installed idle / revised James kneel-work-rise / gameplay scales',fill='white')
        refim=Image.fromarray(idle);board.paste(refim,(0,45),refim)
        for h,x in [(148,220),(82,445),(54,565),(27,665)]:
            side=round(184*h/148);s=im.resize((side,side),Image.Resampling.BILINEAR);board.paste(s,(x,45+172-round(side*172/184)),s)
        previews.append(board)
    checks=json.loads((HERE/'checks.json').read_text());fps=checks['fps']
    previews[0].save(HERE/'graded-review.gif',save_all=True,append_images=previews[1:],duration=round(1000/fps),loop=0)
    sheet=Image.new('RGB',(1104,660),'#303b40');d=ImageDraw.Draw(sheet)
    for j,index in enumerate(np.linspace(0,len(frames)-1,18).astype(int)):
        pos=(j%6*184,j//6*220+20);sheet.paste(frames[index],pos,frames[index]);d.text((pos[0]+5,pos[1]-15),str(index),fill='white')
    sheet.save(HERE/'graded-contact.png')
    report=dict(sourceClothMedian=source.tolist(),targetClothMedian=target.tolist(),fixedGain=gain.tolist(),neutralChromaBlend=.85,targetChroma=(target-target.mean()).tolist(),alphaExact=True,outsideMaskExact=True,frames=len(frames),records=records)
    (HERE/'grade-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='records'}))
if __name__=='__main__':main()
