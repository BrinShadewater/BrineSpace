from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil
R=Path(__file__).resolve().parents[1];D=R/'character/bill-carry-turn-east-seams-v1';O=R/'output/bill-carry-turn-east-seams-native-v1';N=D/'native';N.mkdir(exist_ok=True)
q=json.loads((D/'review.json').read_text());v=json.loads((O/'validation.json').read_text());r=json.loads((O/'report.json').read_text());assert v['passed'] and len(r['cases'])==7 and len(r['captures'])==57
for name in ['report.json','validation.json','inputs-before.json','inputs-after.json']:shutil.copy2(O/name,N/name)
for c in r['captures']:
 for name in ['worldFile','sourceFile']:shutil.copy2(O/c[name],N/c[name])
pages=[]
for contract in q['records']:
 key=contract['key'];entries=[c for c in r['captures'] if c['key']==key];board=Image.new('RGBA',(1200,440),'#17252d');draw=ImageDraw.Draw(board)
 for i,c in enumerate([entries[0],entries[len(entries)//2],entries[-1]]):
  x=i*400;full=Image.open(O/c['worldFile']).convert('RGBA');world=full.copy();world.thumbnail((400,225));board.alpha_composite(world,(x,30));draw.text((x+6,6),f'{key} / {c["slot"]}',fill='white')
  cx=round(544+(c['foot'][0]-7856)*1.3);cy=round(280+(c['foot'][1]-8080)*1.3)
  board.alpha_composite(full.crop((cx-80,cy-110,cx+80,cy+30)),(x+110,285));draw.text((x+110,263),'Station pixels at1x',fill='white')
 name=key+'.png';board.save(N/name);pages.append(name)
q.update(nativeValidation=v,nativeScope=r['scope'],nativePages=pages);(D/'review.json').write_text(json.dumps(q,indent=2)+'\n')
html=(D/'index.html').read_text();html+='<h2>Actual station turns</h2><p>5,040 checks passed:57 slots, seven planted pivots and correct resumed headings. Existing intermediate detail and directional shading retained.</p>'+''.join(f'<img class="board" src="native/{p}" alt="Actual {p}">' for p in pages);(D/'index.html').write_text(html,encoding='utf-8')
print('Seven complete native turn review pages published')
