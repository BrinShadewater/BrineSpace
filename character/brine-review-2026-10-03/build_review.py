from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json, re

p = Path(__file__).resolve().parent
root = p.parents[1]
body_path = root/'character/brine-slim-v14-2026-10-03/body.png'
sheet_path = root/'character/brine-reference-v4-2026-10-03/reference-sheet.png'
bill_path = root/'character/crew-runtime-matte-v1/bill/frames/idle-south-matte-v2/000.png'
portrait_path = root/'character/brine-comms-v14/portrait.png'
body = Image.open(body_path).convert('RGBA')
assert body.size == (56,148)
sheet = Image.open(sheet_path).convert('RGB')
bill = Image.open(bill_path).convert('RGBA')
bill_bounds = bill.getbbox()
bill_alpha_height = bill_bounds[3]-bill_bounds[1]
bill_reference = bill.crop(bill_bounds)
bill_reference = bill_reference.resize((round(bill_reference.width*148/bill_alpha_height),148),Image.Resampling.LANCZOS)
board = Image.new('RGB',(1100,640),(23,33,41))
d = ImageDraw.Draw(board)
d.text((24,18),'BRINE - FACE, MASTER AND STATION SCALE',fill='white')
portrait = Image.open(portrait_path).convert('RGB')
portrait.thumbnail((230,230),Image.Resampling.LANCZOS)
board.paste(portrait,(25,65))
d.text((25,310),'Installed profile portrait',fill='white')
reference = sheet.crop((142,49,339,591))
reference = reference.resize((round(reference.width*148/reference.height),148),Image.Resampling.LANCZOS)
for x,label,im in [(325,'Reference front',reference),(505,'Accepted float',body),(685,'Selected Bill',bill_reference)]:
    # Common 148px height, displayed 2x with nearest sampling for readability.
    im = im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST)
    if im.mode=='RGBA': board.paste(im,(x+(148-im.width)//2,65),im)
    else: board.paste(im,(x+(148-im.width)//2,65))
    d.text((x,385),label,fill='white')
d.text((325,410),'All three: common 148px height; 2x display',fill=(174,192,204))
station_path=root/'output/brine-v14-native-2026-10-03/q0-on-a.png'
station=Image.open(station_path).convert('RGB').crop((170,39,307,274))
board.paste(station,(900,65));d.text((875,330),'Native chamber crop',fill='white')
face=sheet.crop((435,640,735,966));face.thumbnail((170,185),Image.Resampling.LANCZOS)
board.paste(face,(25,355));d.text((25,558),'Sheet face detail',fill='white')
d.text((325,465),'Warm skin / blue eyes / gathered brown hair / blue suit',fill='white')
d.text((325,490),'56 x 148 source; source aspect retained in chamber',fill='white')
d.text((325,515),'Eight-second float / chamber and Continue checks passed',fill='white')
d.text((325,570),'Reference sheet: owner review pending. Floating model: accepted.',fill=(174,192,204))
board.save(p/'consistency-board.png')

gif_path=root/'character/brine-slim-v14-2026-10-03/production-float.gif'
gif=Image.open(gif_path);durations=[]
for i in range(gif.n_frames):
    gif.seek(i);durations.append(gif.info['duration'])
assert len(durations)==200 and sum(durations)==8000 and set(durations)=={40}
runtime=(root/'rooms/underwater/brine-core/brine_core_view.gd').read_text(encoding='utf-8')
assert 'res://character/brine-slim-v14-2026-10-03/body.png' in runtime
assert 'Vector2(56.0,148.0)*(184.8/148.0)' in runtime
for consumer in ['scripts/crew_comms.gd','scripts/meta_shop.gd']:
    assert 'res://character/brine-comms-v14/portrait.png' in (root/consumer).read_text(encoding='utf-8')
manifest=json.loads((body_path.parent/'manifest.json').read_text(encoding='utf-8'))
for name in ['body.png','source.png','production-float.gif']:
    assert hashlib.sha256((body_path.parent/name).read_bytes()).hexdigest()==manifest['outputs'][name]
report={'checks':'Source dimensions/aspect, installed portrait consumers, accepted source hashes and 200-frame/8000ms GIF verified','runtime_model':'character/brine-slim-v14-2026-10-03/body.png','reference_sheet':'character/brine-reference-v4-2026-10-03/reference-sheet.png','bill_native_alpha_height':bill_alpha_height,'comparison_height':148,'visual_review':'Review board provided; all comparison bodies normalized to 148px for documentation. Bill native alpha height includes fringe/shadow and is not exactly 148px. These crops are not runtime sprite exports.','outputs':{'consistency-board.png':hashlib.sha256((p/'consistency-board.png').read_bytes()).hexdigest()}}
(p/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('Consistency checks pass; board saved. GIF:200frames,8000ms. Runtime unchanged.')
