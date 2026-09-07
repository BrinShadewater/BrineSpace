from PIL import Image, ImageDraw
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT / "output/cover-tools"))
import cv2, numpy as np, math, random, subprocess, json, os
import imageio_ffmpeg
FFMPEG=imageio_ffmpeg.get_ffmpeg_exe()
ASSETS=ROOT / "brineui/title"
OUTPUT=ROOT / "output"
W,H=1584,672
FPS,N=48,384
src=Image.open(ASSETS / 'cover-clean.png').convert('RGB').resize((W,H),Image.Resampling.NEAREST)
original=np.array(src)
assert src.size==(W,H)
yy,xx=np.indices((H,W))
person=Image.new('L',(W,H))
d=ImageDraw.Draw(person)
d.polygon([(790,158),(807,161),(824,169),(832,183),(835,204),(833,231),(823,251),(814,259),(816,270),(842,277),(854,286),(861,302),(865,329),(874,372),(884,412),(899,461),(899,474),(904,493),(901,512),(890,523),(878,516),(876,495),(879,477),(875,465),(864,443),(850,405),(842,375),(839,352),(836,373),(839,405),(850,430),(858,454),(862,484),(858,514),(850,549),(842,584),(839,617),(841,642),(840,671),(804,671),(801,644),(803,619),(799,586),(796,541),(796,496),(789,496),(788,541),(786,585),(783,619),(786,645),(785,671),(750,671),(746,645),(747,617),(743,586),(734,548),(727,515),(726,484),(730,455),(734,431),(742,406),(748,377),(744,350),(738,379),(727,417),(713,453),(708,466),(707,480),(710,502),(707,519),(700,522),(690,512),(683,499),(684,482),(689,465),(697,435),(707,399),(715,363),(719,329),(722,302),(729,285),(744,278),(769,270),(769,258),(758,246),(751,229),(749,208),(751,190),(756,175),(769,164)],fill=255)
# Extract the foreground sprite from the generated plate using a guided mask.
seed=np.array(person)>0
sure=cv2.erode(seed.astype('uint8'),np.ones((19,19),np.uint8))>0
possible=cv2.dilate(seed.astype('uint8'),np.ones((17,17),np.uint8))>0
gc=np.zeros((H,W),np.uint8)
gc[possible]=cv2.GC_PR_BGD
gc[seed]=cv2.GC_PR_FGD
gc[sure]=cv2.GC_FGD
cv2.grabCut(original,gc,None,np.zeros((1,65),np.float64),np.zeros((1,65),np.float64),5,cv2.GC_INIT_WITH_MASK)
person_mask=(gc==cv2.GC_FGD)|(gc==cv2.GC_PR_FGD)
water=(xx>=613)&(xx<=988)&(yy>=215)&~person_mask
background=np.array(Image.open(ASSETS / 'cover-background.png').convert('RGB').resize((W,H),Image.Resampling.NEAREST))
base=original.copy()
base[person_mask]=background[person_mask]
if '--layers-only' in sys.argv:
    Image.fromarray(base).save(ASSETS / 'cover-stage.png')
    foreground=np.dstack((original,person_mask.astype('uint8')*255))
    Image.fromarray(np.pad(foreground,((0,8),(0,0),(0,0)),mode='edge')).save(ASSETS / 'cover-character.png')
    print('Exported lossless stage and transparent character layers')
    sys.exit(0)
tank=(xx>=613)&(xx<=988)&(yy>=195)
surface=(xx>615)&(xx<988)&(yy>=151)&(yy<205)&~person_mask
rng=random.Random(42)
particles=[(rng.uniform(624,978),rng.random(),rng.choices([1,2,3,4],[5,5,2,1])[0],rng.uniform(0,6.28)) for _ in range(52)]
polys=[[(119,191),(204,204),(195,276),(108,264)],[(113,326),(197,330),(191,392),(112,390)],[(512,311),(551,313),(553,346),(510,344)],[(537,374),(558,373),(563,416),(543,417)],[(1089,391),(1140,389),(1132,422),(1080,420)],[(1320,327),(1375,322),(1382,368),(1321,372)],[(1514,321),(1536,320),(1536,351),(1514,352)]]
screens=[]
for poly in polys:
    transform=cv2.getPerspectiveTransform(np.float32([[0,0],[119,0],[119,89],[0,89]]),np.float32(poly))
    m=Image.new('L',(W,H));ImageDraw.Draw(m).polygon(poly,fill=255)
    screens.append((transform,np.array(m)>0))
def terminal(j,p):
    im=Image.new('RGB',(120,90),(5,22,39));d=ImageDraw.Draw(im)
    d.line((3,7,115,7),fill=(30,120,155),width=1)
    d.rectangle((4,3,32,4),fill=(84,204,225))
    for k in range(4):
        d.rectangle((88+k*7,3,91+k*7,4),fill=(91,221,226) if (int(p*8)+k+j)%4 else (24,71,97))
    if j%3==1:
        for y in range(16,81,13):d.line((3,y,116,y),fill=(13,48,66))
        for x in range(7,117,16):d.line((x,12,x,81),fill=(13,48,66))
        points=[]
        for x in range(4,117):
            z=((x/112+p*2+j*.1)%1)
            y=47+3*math.sin(z*math.pi*12)-26*math.exp(-((z-.47)/.018)**2)+14*math.exp(-((z-.51)/.022)**2)
            points.append((x,round(y)))
        d.line(points,fill=(92,239,237),width=2)
        cursor=4+int(p*112)
        d.line((cursor,14,cursor,79),fill=(39,112,128))
    else:
        shift=int(p*70)
        for row in range(7):
            y=13+(row*10-shift)%70
            d.rectangle((4,y,8,y+2),fill=(63,165,183))
            for col in range(4):
                length=5+(row*7+col*13+j*3)%17
                x=14+col*25
                d.rectangle((x,y,x+length,y+1),fill=(76,185,207) if col%2 else (31,106,143))
        for k in range(5):
            height=5+int(6*(1+math.sin(2*math.pi*(p+k/5))))
            d.rectangle((86+k*6,87-height,89+k*6,87),fill=(56,192,215))
    return np.array(im)
def frame(i):
    p=(i%N)/N;a=2*math.pi*p
    out=base.copy()
    light=2*np.sin(xx*.035+yy*.022-a)
    for c,s in enumerate([.2,.8,1.]):
        v=out[:,:,c].astype(float);v[water]+=light[water]*s
        out[:,:,c]=np.clip(v,0,255).astype('uint8')
    for j,(transform,m) in enumerate(screens):
        pixels=cv2.warpPerspective(terminal(j,p),transform,(W,H),flags=cv2.INTER_NEAREST)
        out[m]=pixels[m]
    layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
    for x0,phase,r,offset in particles:
        v=(phase-p)%1
        y=216+v*466
        x=x0+4*math.sin(a+offset)
        opacity=int(155*min(1,v*15,(1-v)*15))
        x,y=round(x),round(y)
        if r<3:d.rectangle((x,y,x+1,y+1),fill=(161,236,251,opacity))
        else:
            d.line([(x-r+2,y-r),(x+r-2,y-r),(x+r,y-r+2),(x+r,y+r-2),(x+r-2,y+r),(x-r+2,y+r),(x-r,y+r-2),(x-r,y-r+2),(x-r+2,y-r)],fill=(142,224,245,opacity),width=1)
            d.line((x-r+1,y-1,x-r+1,y-r+2),fill=(207,253,255,opacity),width=1)
    arr=np.array(layer)
    arr[:,:,3][~tank]=0
    out=np.array(Image.alpha_composite(Image.fromarray(out).convert('RGBA'),Image.fromarray(arr)).convert('RGB'))
    # Subpixel translation avoids the old one-pixel holds and jumps.
    bob=3.0*math.sin(a)
    transform=np.float32([[1,0,0],[0,1,bob]])
    alpha=person_mask.astype('float32')
    sprite=original.astype('float32')*alpha[:,:,None]
    moved=cv2.warpAffine(sprite,transform,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    mask=cv2.warpAffine(alpha,transform,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    out=np.clip(moved+out.astype('float32')*(1-mask[:,:,None]),0,255).astype('uint8')
    return Image.fromarray(out)
f0=np.array(frame(0))
assert np.array_equal(f0,np.array(frame(N)))
assert np.array_equal(f0[:140],original[:140])
assert np.array_equal(f0[person_mask],original[person_mask])
# Surface pixels outside the sprite's travel area must remain unchanged.
protected=(yy>=140)&(yy<190)&((xx<746)|(xx>840))
for k in [36,72,108]:
    assert np.array_equal(np.array(frame(k))[protected],f0[protected])
# Encode directly from rendered frames, avoiding an intermediate lossy video.
video=ASSETS / 'brinespace-title-clean.ogv'
proc=subprocess.Popen([FFMPEG,'-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libtheora','-q:v','10','-pix_fmt','yuv420p',str(video)],stdin=subprocess.PIPE)
for i in range(N):
    im=frame(i)
    proc.stdin.write(im.tobytes())
    if i in [0,96,192,288]:
        im.save(OUTPUT / f'cover-clean-frame-{i}.png')
proc.stdin.close()
assert proc.wait()==0
print(json.dumps({'duration':N/FPS,'fps':FPS,'frames':N,'exact_period':True,'animated_monitors':len(screens),'float_amplitude_pixels':3,'video_bytes':video.stat().st_size}))
