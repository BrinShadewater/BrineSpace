"""Assemble unchanged native captures for owner-note review."""
import json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/(sys.argv[1] if len(sys.argv)>1 else 'output/studio-owner-notes-2026-09-08')
rows=json.loads((OUT/'catalog/runtime.json').read_text())
south={r['id'] for r in json.loads((ROOT/'assets/south-wall-facing-v3/manifest.json').read_text())}
groups={'south':[(r,2) for r in rows if len(r['views'])>2 and any(p.get('side_view')=='south' and p['id'].removeprefix('full_wall_') in south for p in r['views'][2]['props'])], 'repairs':[(r,0) for r in rows if r['views'] and any(p['id'] in ['full_wall_drone-service-wall','full_wall_ore-refinery-wall','full_wall_mycelium-cultivation-wall','full_wall_crew-lounge-built-in','full_wall_maintenance-repair-wall'] for p in r['views'][0]['props'])]}
for label,items in groups.items():
    sheet=Image.new('RGB',(4*400,((len(items)+3)//4)*440),'#20383d'); draw=ImageDraw.Draw(sheet)
    for n,(r,q) in enumerate(items):
        im=Image.open(ROOT/r['images'][q].removeprefix('res://')).convert('RGBA'); im.thumbnail((400,400))
        x=n%4*400;y=n//4*440;sheet.paste(im,(x,y),im)
        draw.text((x+8,y+402),r['name'],font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18),fill='white')
    sheet.save(OUT/(label+'-native.jpg'),quality=95)
    print(label,len(items))

