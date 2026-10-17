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
        r,g,blue=rgb.transpose(2,0,1)
        # Cold neutral material, including upper shoulder/backpack and purple
        # highlights. Warm hair/skin and engineering yellow are excluded.
        warm=(r-blue>12)&(r-g>5)
        yellow=(r-blue>18)&(g-blue>10)
        neutral_mask=(~warm)&(~yellow)&(blue>=r-12)&(blue>=g-4)&(a[:,:,3]>0)
        strength=np.clip((lum-6)/10,0,1)*neutral_mask
        luma=rgb@np.array([.2126,.7152,.0722])
        corrected=np.repeat(luma[:,:,None],3,axis=2)
        b=a.copy();b[:,:,:3]=np.clip(np.rint(rgb+strength[:,:,None]*(corrected-rgb)),0,255).astype('uint8')
        # Warm facial pixels with blue above green have the same pink spill.
        # Keep red/green and luminance structure; restore warm blue relationship.
        ys=np.where(a[:,:,3]>192)[0];head_end=int(ys.min())+32
        skin=(yy<head_end)&warm&(lum>65)&(blue>g-5)&(~yellow)&(a[:,:,3]>0)
        b[:,:,2][skin]=np.minimum(b[:,:,2][skin],np.maximum(0,g[skin]-7)).astype('uint8')
        # The short dark cap at the head top is brown hair, not graphite.
        # Restore restrained warm chroma to cold source pixels in that region.
        hair=(yy<int(ys.min())+9)&neutral_mask&(lum>15)&(lum<100)
        hair_rgb=np.clip(luma[:,:,None]+np.array([6,0,-7]),0,255)
        b[:,:,:3][hair]=np.rint(hair_rgb[hair]).astype('uint8')
        weight=np.maximum(np.maximum(strength,skin.astype(float)),hair.astype(float))
        assert np.array_equal(a[:,:,3],b[:,:,3]);assert np.array_equal(a[weight==0],b[weight==0])
        Image.fromarray(b).save(dest/path.name);frames.append(Image.fromarray(b));records.append({'frame':path.name,'changedPixels':int(np.any(a!=b,axis=2).sum())})
    previews=[]
    for index,im in enumerate(frames):
        board=Image.new('RGB',(760,260),'#303b40');d=ImageDraw.Draw(board);d.text((8,8),'Installed idle / James north kneel-work-rise / gameplay scales',fill='white')
        refim=Image.fromarray(idle);board.paste(refim,(0,45),refim)
        for h,x in [(148,220),(82,445),(54,565),(27,665)]:
            side=round(184*h/148);s=im.resize((side,side),Image.Resampling.BILINEAR);board.paste(s,(x,45+172-round(side*172/184)),s)
        previews.append(board)
    checks=json.loads((HERE/'checks.json').read_text());fps=checks['fps']
    previews[0].save(HERE/'neutral-review-v1.gif',save_all=True,append_images=previews[1:],duration=round(1000/fps),loop=0)
    sheet=Image.new('RGB',(1104,660),'#303b40');d=ImageDraw.Draw(sheet)
    for j,index in enumerate(np.linspace(0,len(frames)-1,18).astype(int)):
        pos=(j%6*184,j//6*220+20);sheet.paste(frames[index],pos,frames[index]);d.text((pos[0]+5,pos[1]-15),str(index),fill='white')
    sheet.save(HERE/'neutral-contact-v1.png')
    report=dict(sourceClothMedian=source.tolist(),targetClothMedian=target.tolist(),fixedGain=gain.tolist(),neutralChromaBlend=1.0,targetChroma=[0,0,0],method='Cold neutral material to luminance-matched graphite including upper shoulders; facial blue spill and brown hair corrected separately',alphaExact=True,outsideMaskExact=True,frames=len(frames),records=records)
    (HERE/'neutral-checks-v1.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='records'}))
if __name__=='__main__':main()
