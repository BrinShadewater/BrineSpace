"""Register untouched riser masters and assemble review sheets; never edits source art."""
from pathlib import Path
import hashlib
import json
import re
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'assets/room-risers-v4'
BRIEFS = json.loads((PACK / 'briefs.json').read_text())
DATABASE_IDS = set(re.findall(r'"id"\s*:\s*"([a-z_]+)"', (ROOT / 'scripts/room_database.gd').read_text()))
assert set(BRIEFS) == DATABASE_IDS, 'Room brief coverage differs from database'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    registrations, records = {}, []
    overrides_path = PACK / 'registration-overrides.json'
    overrides = json.loads(overrides_path.read_text()) if overrides_path.exists() else {}
    for room_id, brief in BRIEFS.items():
        path = PACK / 'masters' / f'{room_id}.png'
        if not path.exists():
            records.append({'id': room_id, 'stage': 'awaiting_generation'})
            continue
        image = Image.open(path).convert('RGBA')
        alpha = np.asarray(image.getchannel('A'))
        labels, count = ndimage.label(alpha >= 128)
        sizes = np.bincount(labels.ravel())
        sizes[0] = 0
        component = int(sizes.argmax())
        ys, xs = np.nonzero(labels == component)
        box = [int(xs.min()), int(ys.min()), int(xs.max()+1), int(ys.max()+1)]
        x, y, right, bottom = box
        w, h = right-x, bottom-y
        # Default seam starts beneath the narrow generated top cap. Inspect sheets
        # and override per master if its actual construction differs.
        cap_h = round(h*.14)
        face = overrides.get(room_id, {}).get('face', [x, y+cap_h, w, h-cap_h])
        registrations[room_id] = {
            'source': f'res://assets/room-risers-v4/masters/{room_id}.png',
            'face': face, 'cap': [x, y, w, cap_h],
            'display_face': [-200, -258, 400, 82],
            'door_reserve': [-46, -258, 92, 82],
            'window_reserves': [[-152, -249, 80, 32], [72, -249, 80, 32]],
            'cap_policy': 'Use the host room draw_wall/draw_cap, not generated cap',
            'native_size': list(image.size), 'opaque_component_bounds': box,
            'sha256': sha(path),
        }
        records.append({'id': room_id, 'stage': 'generated_and_registered', 'brief': brief,
                        'source': registrations[room_id]['source'], 'sha256': sha(path),
                        'prompt_sha256': sha(PACK / 'prompts' / f'{room_id}.txt'),
                        'alpha_zero_pixels': int((alpha==0).sum()),
                        'alpha_full_pixels': int((alpha==255).sum()),
                        'visual_acceptance': 'pending_owner', 'production_installed': False})
    (PACK / 'registrations.json').write_text(json.dumps(registrations, indent=2)+'\n')
    (PACK / 'manifest.json').write_text(json.dumps({'expected_count': len(BRIEFS), 'generated_count':len(registrations), 'rooms':records},indent=2)+'\n')
    out = PACK / 'review'
    out.mkdir(exist_ok=True)
    font_path = Path('C:/Windows/Fonts/arial.ttf')
    font = ImageFont.truetype(str(font_path), 20) if font_path.exists() else ImageFont.load_default()
    ids = list(registrations)
    for page in range((len(ids)+7)//8):
        batch = ids[page*8:(page+1)*8]
        board = Image.new('RGB',(1400, len(batch)*220+55),'#182229')
        draw = ImageDraw.Draw(board)
        draw.text((24,15),'BRINESPACE / RISER V4 / SOURCE + RESERVED MOUNTING AREAS',font=font,fill='#dfe5e5')
        for row, room_id in enumerate(batch):
            reg = registrations[room_id]
            source = Image.open(ROOT / reg['source'].replace('res://','')).convert('RGBA')
            x,y,w,h = reg['face']
            sample = source.crop((x,y,x+w,y+h))
            sample.thumbnail((660,150),Image.Resampling.LANCZOS)
            top=55+row*220
            draw.text((24,top),room_id.replace('_',' ').upper(),font=font,fill='#dfe5e5')
            for col,bg in [(0,'#172127'),(1,'#aeb2ad')]:
                left=24+col*690
                draw.rectangle((left,top+30,left+660,top+190),fill=bg)
                at=(left+(660-sample.width)//2,top+35+(150-sample.height)//2)
                board.paste(sample,at,sample)
                if col==1:
                    sx,sy=sample.width/400,sample.height/82
                    for reserve,color in [(reg['door_reserve'],'#e7ba69')]+[(r,'#5cb8d8') for r in reg['window_reserves']]:
                        rx,ry,rw,rh=reserve
                        draw.rectangle((at[0]+(rx+200)*sx,at[1]+(ry+258)*sy,at[0]+(rx+200+rw)*sx,at[1]+(ry+258+rh)*sy),outline=color,width=2)
        board.save(out/f'page-{page+1:02}.png')
    html=['<!doctype html><meta charset="utf-8"><title>BrineSpace riser variations</title><style>body{background:#152027;color:#e0e6e8;font:16px system-ui;margin:30px}img{max-width:100%}a{color:#81c5d9}article{max-width:1400px;margin:0 auto 28px}</style><h1>BrineSpace — room riser variations</h1><p>47 room-specific designs. Amber: 92-unit door bay. Blue: future window/mounting panels. Generated faces; host room supplies the real perimeter cap. Owner review pending.</p>']
    for page in range((len(ids)+7)//8): html.append(f'<article><img src="page-{page+1:02}.png"></article>')
    (out/'index.html').write_text('\n'.join(html))
    print(f'Riser pack: {len(registrations)}/{len(BRIEFS)} generated; {len(BRIEFS)-len(registrations)} missing; {len(ids)} alpha records; {(len(ids)+7)//8} review pages')

if __name__=='__main__': main()
