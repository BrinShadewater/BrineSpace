"""Prescribed room source audit, with per-capture camera crop explicitly recorded."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-lounge-partial-fall-north-contact-v1'
records=json.loads((O/'records.json').read_text())['records'];crops={}
for gear in ['bare','helmet']:
 board=Image.new('RGB',(1536,660),'#202a30');d=ImageDraw.Draw(board)
 for i in range(6):
  name=f'{gear}-pose-{i}';room=Image.open(O/f'{name}-room.png').convert('RGB')
  box=(255,476,376,595) if gear=='bare' and i==0 else (255,282,376,401)
  crop=room.crop(box).resize((242,238),Image.Resampling.NEAREST);board.paste(crop,(i*256+7,24));crops[name]=box
  source=Image.open(O/f'{name}-source.png').convert('RGBA');board.paste(source,(i*256,290),source)
  d.text((i*256+6,4),f'{gear} room pose {i}',fill='white');d.text((i*256+6,272),'Exact submitted source',fill='white')
  r=next(r for r in records if r['name']==name);d.text((i*256+6,580),f'Seat amount {r["seatAmount"]}',fill='white')
  d.text((i*256+6,600),f'Depth {r["rendered"]["depth"]:.2f}',fill='white')
 board.save(P/f'{gear}-native-contact.png')
(P/'native-crops.json').write_text(json.dumps({'boxes':crops,'displayZoom':2,'reason':'Camera settles between first and later captured source poses. Crops show the same real chair context; not a continuous native movie.'},indent=2)+'\n',encoding='utf-8')
html='''<!doctype html><meta charset="utf-8"><title>Veld Partial North lounge fall contact audit</title><style>body{background:#202a30;color:#ddd;font:17px sans-serif;margin:28px}img{max-width:100%}a{color:#afd6da}</style><h1>Partial North lounge fall — chair contact audition</h1><p>Both variants in the actual default lounge, rotation 0. Partial entry and buckle retain 0.3125 of registered chair offset, knee brace retains half that offset, roll and rest on that clear floor. These are prescribed source poses and a provisional root path; no production mortality, continuous fall or save/Continue proof yet.</p><img src="bare-native-contact.png"><img src="helmet-native-contact.png"><p>68 native checks passed. Physical navigation foot remains fixed and each source is actually submitted by the room renderer. Original captures retained; individual crops account for camera settling. Chair and owner layout unchanged.</p><p><a href="./?v=source-contact-v1">Source animation and master comparison</a> · <a href="HANDOFF.md">Handoff and next checks</a></p>'''
(P/'native-review.html').write_text(html,encoding='utf-8');print('12 source/room presentations saved; per-capture crop coordinates retained')
