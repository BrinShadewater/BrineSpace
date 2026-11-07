"""Fit the existing east helmet to staged Branforth bunk poses; no generation."""
from pathlib import Path
import hashlib
import json
import sys
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent.parent
sys.path.insert(0,str(PROJECT/'tools'))
from rebuild_bill_art import HelmetRebaker

overlay=HelmetRebaker(None).overlay('east',(34,36))
head_boxes=[None,(121,108,151,141),(85,111,115,146),(106,148,137,182),(76,160,108,193),(67,171,101,204),(49,195,83,226)]
poses=[None,(136,125,-10),(100,128,0),(121,165,0),(91,176,20),(83,186,45),(66,211,85)]
out=ROOT/'branforth-entry-helmet';out.mkdir(exist_ok=True)
records=[]
for i,pose in enumerate(poses):
    body=Image.open(ROOT/'branforth-entry'/f'{i:03d}.png').convert('RGBA')
    if i==0:
        original=Image.open(PROJECT/'character/chief-engineer-branforth-v2/frames/helmet/idle-east/000.png').convert('RGBA')
        frame=Image.new('RGBA',(256,256));frame.alpha_composite(original,(36,52))
        records.append({'frame':i,'derivation':'exact canonical equipped idle padded (36,52)'})
    else:
        x,y,angle=pose
        helmet=overlay.rotate(angle,Image.Resampling.NEAREST,expand=True)
        at=(round(x-helmet.width/2),round(y-helmet.height/2))
        # Tuck source hair inside the shell, preserving the authored visor opening.
        # This changes only the equipped composition, never the bare source.
        coverage=overlay.getchannel('A').copy()
        ImageDraw.Draw(coverage).rectangle((19,10,33,24),fill=255)
        coverage=coverage.rotate(angle,Image.Resampling.NEAREST,expand=True)
        cover=Image.new('L',(256,256));cover.paste(coverage,at)
        frame=body.copy()
        x0,y0,x1,y1=head_boxes[i]
        for py in range(y0,y1):
            for px in range(x0,x1):
                if cover.getpixel((px,py))==0:frame.putpixel((px,py),(0,0,0,0))
        frame.alpha_composite(helmet,at)
        records.append({'frame':i,'head_center':[x,y],'angle':angle,'top_left':at,
            'head_cleanup_box':head_boxes[i],'visor_keep_rect':[19,10,33,24],
            'body_sha256':hashlib.sha256((ROOT/'branforth-entry'/f'{i:03d}.png').read_bytes()).hexdigest()})
    frame.save(out/f'{i:03d}.png')
manifest=json.loads((ROOT/'branforth-entry/manifest.json').read_text())
manifest['precomposed']=True
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(out/'recipe.json').write_text(json.dumps({'source':'existing crew-underwater-v1 east helmet via canonical HelmetRebaker.overlay',
    'overlay_size':[34,36],'overlay_rgba_sha256':hashlib.sha256(overlay.tobytes()).hexdigest(),
    'records':records,'status':'staged equipment fit; no runtime catalog binding'},indent=2)+'\n')
