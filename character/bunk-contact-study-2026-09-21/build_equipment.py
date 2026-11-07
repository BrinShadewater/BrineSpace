"""Fit the existing east helmet to staged Veld bunk poses; no generation."""
from pathlib import Path
import hashlib
import json
import sys
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent.parent
sys.path.insert(0,str(PROJECT/'tools'))
from rebuild_bill_art import HelmetRebaker

overlay=HelmetRebaker(None).overlay('east',(30,32))
head_boxes=[None,(117,94,145,123),(86,115,116,146),(96,152,131,182),(71,153,108,183),(46,169,83,198),(49,196,81,224)]
poses=[None,(132,110,-8),(102,131,-10),(116,169,0),(92,168,12),(68,186,30),(64,210,85)]
out=ROOT/'veld-entry-helmet';out.mkdir(exist_ok=True)
records=[]
for i,pose in enumerate(poses):
    body=Image.open(ROOT/'veld-entry'/f'{i:03d}.png').convert('RGBA')
    if i==0:
        original=Image.open(PROJECT/'character/dr-veld-v2/frames/helmet/idle-east/000.png').convert('RGBA')
        frame=Image.new('RGBA',(256,256));frame.alpha_composite(original,(36,52))
        records.append({'frame':i,'derivation':'exact canonical equipped idle padded (36,52)'})
    else:
        x,y,angle=pose
        helmet=overlay.rotate(angle,Image.Resampling.NEAREST,expand=True)
        at=(round(x-helmet.width/2),round(y-helmet.height/2))
        # Tuck source hair inside the shell, preserving the authored visor opening.
        # This changes only the equipped composition, never the bare source.
        coverage=overlay.getchannel('A').copy()
        ImageDraw.Draw(coverage).rectangle((17,9,29,21),fill=255)
        coverage=coverage.rotate(angle,Image.Resampling.NEAREST,expand=True)
        cover=Image.new('L',(256,256));cover.paste(coverage,at)
        frame=body.copy()
        x0,y0,x1,y1=head_boxes[i]
        for py in range(y0,y1):
            for px in range(x0,x1):
                if cover.getpixel((px,py))==0:frame.putpixel((px,py),(0,0,0,0))
        frame.alpha_composite(helmet,at)
        records.append({'frame':i,'head_center':[x,y],'angle':angle,'top_left':at,
            'head_cleanup_box':head_boxes[i],'visor_keep_rect':[17,9,29,21],
            'body_sha256':hashlib.sha256((ROOT/'veld-entry'/f'{i:03d}.png').read_bytes()).hexdigest()})
    frame.save(out/f'{i:03d}.png')
manifest=json.loads((ROOT/'veld-entry/manifest.json').read_text())
manifest['precomposed']=True
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(out/'recipe.json').write_text(json.dumps({'source':'existing crew-underwater-v1 east helmet via canonical HelmetRebaker.overlay',
    'overlay_size':[30,32],'overlay_rgba_sha256':hashlib.sha256(overlay.tobytes()).hexdigest(),
    'records':records,'status':'staged equipment fit; no runtime catalog binding'},indent=2)+'\n')
