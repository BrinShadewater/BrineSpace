"""Native-scale visual comparison and corroborating colour metrics, not approval."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parents[1]
LOCK=json.loads((PROJECT/'docs/BRINESPACE_ART_REFERENCE_LOCK_2026-09-26.json').read_text(encoding='utf-8'))
EXPORT=Path(LOCK['local_root'])
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
SMALL=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)

def cropped(p):
    im=Image.open(p).convert('RGBA')
    return im.crop(im.getchannel('A').point(lambda a:255 if a>64 else 0).getbbox())

def width(im,w):
    return im.convert('RGBa').resize((w,round(im.height*w/im.width)),Image.Resampling.LANCZOS).convert('RGBA')

def metrics(im):
    a=np.array(im);rgb=a[:,:,:3].astype(float)/255
    hsv=np.array(im.convert('RGB').convert('HSV')).astype(float)/255
    mask=(a[:,:,3]>230)&(hsv[:,:,0]>.45)&(hsv[:,:,0]<.56)&(hsv[:,:,1]>.2)&(hsv[:,:,2]>.2)
    return {'cyanPixelCount':int(mask.sum()),'medianCyanRGB':np.round(np.median(rgb[mask],axis=0)*255,1).tolist(),
            'medianCyanSaturation':round(float(np.median(hsv[:,:,1][mask])),3),
            'medianCyanValue':round(float(np.median(hsv[:,:,2][mask])),3)}

accepted=cropped(ROOT/'sources/construction-approved-v10.png')
raw=Image.open(ROOT/'sources/construction-tool-poses-v2.png').convert('RGBA')
pilot=raw.crop((0,0,round(raw.width/2),round(raw.height/2)))
pilot=pilot.crop(pilot.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox())
refs=[]
for id in ['sp-engineering-extra3-3','sp-science-extra11-2']:
    entry=next(a for a in LOCK['assets'] if a['id']==id)
    path=EXPORT/entry['native']['path']
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest==entry['native']['sha256'],id+' reference hash mismatch'
    refs.append((id,Image.open(path).convert('RGBA')))
report={'referenceHashes':'pass','referenceIds':[r[0] for r in refs],
        'approvedV10':metrics(accepted),'generatedNeutral':metrics(pilot),
        'density':{'worldUnitsPerLibraryPixel':.34,'pilotHullPixels':69.12/.34,'provisionalWorldWidth':69.12,'v10MotionStudyWidthPixels':85},
        'limits':'Cyan metrics include painted panels and lens; visual panel comparison remains authoritative. Room width is provisional, not owner-approved.'}
out=ROOT/'review';out.mkdir(exist_ok=True)
(out/'style-metrics.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
for theme,bg,fg in [('dark','#192930','#d9e5e9'),('light','#d7dde0','#20323a')]:
    board=Image.new('RGB',(1160,670),bg);d=ImageDraw.Draw(board)
    d.text((22,16),'BIBLE CHECK / v10 identity + locked industrial reference family',font=FONT,fill=fg)
    subjects=[('Accepted v10 master -> 203 px',width(accepted,203)),('New tool-pose neutral -> 203 px',width(pilot,203)),
              ('Accepted v10 preview / 85 px',width(accepted,85)),('New neutral / 85 px',width(pilot,85))]
    for i,(label,im) in enumerate(subjects):
        x=25+i*285;d.text((x,55),label,font=SMALL,fill=fg);board.paste(im,(x,87),im)
    d.text((22,280),'Same-size comparison above. Locked native library exports below (no enlargement).',font=SMALL,fill=fg)
    for i,(label,im) in enumerate(refs):
        x=25+i*570;d.text((x,314),label,font=SMALL,fill=fg);board.paste(im,(x,345),im)
    d.text((22,643),'Palette measurements support visual review; they do not certify material style, camera or animation.',font=SMALL,fill=fg)
    board.save(out/f'bible-comparison-{theme}.png')
print(json.dumps(report))
