"""Compact normal-loader matrix: exact captures, source chronology and masters."""
from pathlib import Path
import json,shutil
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-north-chair-falls-selected-native-v1'
native=json.loads((O/'validation.json').read_text());assert native['passed']
records=json.loads((O/'records.json').read_text());assert len(records)==28
assets=P/'replay-frames';assets.mkdir(exist_ok=True);tracks=[];boards=[]
def vec(s):return [float(x) for x in s.strip('()').split(',')]
for gear in ['bare','helmet']:
 master=Image.new('RGBA',(256,272))
 path=R/('character/veld-shared-helmet-v1/frames/idle-north/000.png' if gear=='helmet' else 'character/crew-runtime-matte-v1/veld/frames/idle-north-breathing-v1/000.png')
 master.alpha_composite(Image.open(path).convert('RGBA'),(36,52))
 for group in ['lower','rise','held']:
  selected=[record for record in records if record['name'].startswith(gear+'-'+group)]
  board=Image.new('RGB',(1152,len(selected)*320+28),'#202a30');draw=ImageDraw.Draw(board)
  for row,record in enumerate(selected):
   y=row*320+28;name=record['name']
   draw.text((4,y+2),name+' / normal loader',fill='white')
   im=master.resize((128,136),Image.Resampling.LANCZOS);board.paste(im,(0,y+26),im)
   room=Image.open(O/f'{name}-before-room.png').convert('RGB').crop((255,280,515,530)).resize((128,123),Image.Resampling.NEAREST)
   board.paste(room,(128,y+26));draw.text((128,y+4),'Actual entrance/chair',fill='white')
   slots=[s['tick'] for s in record['reference'] if 'rendered' in s]
   assert len(slots)==7,(name,len(slots))
   for col,tick in enumerate(slots):
    source=O/f'{name}-reference-tick-{tick:02d}-source.png';im=Image.open(source).convert('RGBA')
    pad=Image.new('RGBA',(256,272));pad.alpha_composite(im);small=pad.resize((128,136),Image.Resampling.LANCZOS)
    board.paste(small,((col+2)*128,y+26),small);draw.text(((col+2)*128+4,y+4),f'{(tick+1)*20}ms',fill='white')
    native_room=Image.open(O/f'{name}-reference-tick-{tick:02d}-room.png').convert('RGB').crop((255,280,515,530)).resize((128,123),Image.Resampling.NEAREST)
    board.paste(native_room,((col+2)*128,y+176))
    dest=assets/(record['reference'][tick]['pixels']+'.png')
    if not dest.exists():shutil.copy2(source,dest)
   tracks.append({'name':name,'reference':[{'pixels':s['pixels'],'offset':vec(s['offset']),'clock':s['clock'],'depth':s['depth']} for s in record['reference']],'resumed':[{'pixels':s['pixels'],'offset':vec(s['offset']),'clock':s['clock'],'depth':s['depth']} for s in record['resumed']]})
   draw.text((4,y+190),'Actual future /',fill='white');draw.text((4,y+208),'same source clocks',fill='white')
  filename=f'{gear}-{group}-normal-review.png';board.save(P/filename);boards.append(filename)
(P/'replay-traces.json').write_text(json.dumps(tracks,separators=(',',':'))+'\n')
template=(R/'character/veld-lounge-early-fall-north-v1/resume-review.html').read_text(encoding='utf-8')
template=template.replace('Early North lounge fall — saved continuation','North chair falls — normal selection and saved continuation').replace('exact incoming early lowering/rising pose','exact incoming lowering, rising or held breathing pose').replace('Eight saves loaded into fresh main scenes.','Twenty-eight saves loaded into fresh main scenes. All fall sources come from the normal production loader; the test injects no animation manifests.')
template=template.replace('Normal fall selection remains staged.','All six North lowering/rising entrances and held breathing now select normally.').replace('Targeted inputs unchanged during the native run;',f'{native["targetedInputCount"]} targeted inputs unchanged during the native run;').replace('natural hazard cadence, other partial seating poses and wider room contexts','natural hazard cadence and wider room contexts')
template=template.replace("const im=document.createElement('img');im.src='native-fall-'+t.name+'.png';im.alt=t.name+' paired actual room/source/master review';document.querySelector('#boards').append(im)",'')
gallery=''.join(f'<img src="{name}" alt="{name}">' for name in boards)
template=template.replace('<div id="boards"></div>','<p>Each case shows the standing master, actual room entrance, then exact submitted source changes above their matching native room captures. Sprites use the same half-scale anatomical ruler; room captures retain their original camera. Loaded future sources and room positions match uninterrupted traces in all 28 cases.</p><div id="boards">'+gallery+'</div>').replace('<a href="./?v=source-contact-v1">Source/master preview</a>','<a href="../veld-lounge-early-fall-north-v1/?v=source-contact-v1">Early source/master preview</a>')
(P/'resume-review.html').write_text(template,encoding='utf-8')
(P/'review-evidence.json').write_text(json.dumps({'normalLoaderOnly':True,'cases':28,'boards':boards,'pairedFutureNativeSourceCaptures':196,'exactReplaySources':len(list(assets.glob('*.png'))),'scope':'rotation0 prescribed death/actual disk/fresh-main-scene future actor traces; chronological source/native captures, not continuous native world video'},indent=2)+'\n')
print(f'28normal cases/six compact native-source-master boards/{len(list(assets.glob("*.png")))}replay sources')
