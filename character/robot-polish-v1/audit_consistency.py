"""Read-only frame/source diagnostics and a registered before/after contact sheet."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
DIRS=['south','west','north','east']
def head_colour(path):
    a=np.array(Image.open(path).convert('RGBA')).astype(float);ys,xs=np.where(a[:,:,3]>128)
    top,bottom=ys.min(),ys.max();y=np.indices(a.shape[:2])[0]
    mask=(a[:,:,3]>128)&(y<top+(bottom-top)*.32)&(a[:,:,2]>a[:,:,0]+15)&(a[:,:,0]>65)&(a[:,:,2]<230)
    rgb=np.median(a[:,:,:3][mask],axis=0)
    return rgb
report={'scope':'Josh and River active robot animations; image metrics are diagnostics, not visual certification','josh':{},'density':{}}
board=Image.new('RGB',(184*5,210*4),'#18252b');draw=ImageDraw.Draw(board)
for r,d in enumerate(DIRS):
    cases=[('idle reference',ROOT/'josh/frames'/('idle-'+d)/'000.png'),
           ('weld before',ROOT/'review/pre-consistency/josh/frames'/('torch-'+d)/'001.png'),
           ('weld corrected',ROOT/'josh/frames'/('torch-'+d)/'001.png'),
           ('standby before',ROOT/'review/pre-consistency/josh/frames'/('powerdown-'+d)/'000.png'),
           ('standby corrected',ROOT/'josh/frames'/('powerdown-'+d)/'000.png')]
    reference=head_colour(cases[0][1]);stats={}
    for c,(label,path) in enumerate(cases):
        im=Image.open(path).convert('RGBA');board.paste(im,(184*c,210*r+20),im);draw.text((184*c+5,210*r+5),label+' / '+d,fill='#cfddde')
        rgb=head_colour(path);stats[label]={'headPaintMedianRGB':rgb.round(1).tolist(),'blueMinusRed':round(float(rgb[2]-rgb[0]),1),'distanceFromIdleRGB':round(float(np.linalg.norm(rgb-reference)),2)}
    report['josh'][d]=stats
for who in ['josh','river']:
    manifest=json.loads((ROOT/who/'manifest.json').read_text());keys={s['id']:s for s in manifest['states']}
    sizes={};ranges={}
    for d in DIRS:
        boxes=[Image.open(ROOT/f).getbbox() for f in keys['walk-'+d]['frameFiles']]
        ranges[d]={'rollingHeightRange':[min(b[3]-b[1] for b in boxes),max(b[3]-b[1] for b in boxes)],'groundContactRange':[min(b[3] for b in boxes),max(b[3] for b in boxes)]}
    scales=json.loads((ROOT/'review/calibration.json').read_text())[who]
    maxscale=max(v for row in scales.values() for v in row.values());assert maxscale<=1
    report['density'][who]={'canvas':[184,184],'standingHeight':148,'pixelsPerWorldUnit':round(148/65.28,4),'maximumSourceResizeScale':maxscale,'upscaledSource':False,'rolling':ranges}
board.save(ROOT/'review/colour-consistency.png')
(ROOT/'review/consistency-audit.json').write_text(json.dumps(report,indent=2))
for d,stats in report['josh'].items():print(d,'weld chroma',stats['weld before']['blueMinusRed'],'->',stats['weld corrected']['blueMinusRed'],'idle',stats['idle reference']['blueMinusRed'],'standby',stats['standby before']['blueMinusRed'],'->',stats['standby corrected']['blueMinusRed'])
print(json.dumps(report['density']))
