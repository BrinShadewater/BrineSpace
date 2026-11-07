from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-carry-entry-master-v1';O=R/'output/bill-east-carry-entry-native-v2';N=D/'native';N.mkdir(exist_ok=True)
v=json.loads((O/'validation.json').read_text());q=json.loads((O/'report.json').read_text());assert v['passed'] and v['checks']==249 and v['captures']==7
for name in ['report.json','validation.json','inputs-before.json','inputs-after.json']:shutil.copy2(O/name,N/name)
for c in q['captures']:
 for name in ['worldFile','sourceFile']:shutil.copy2(O/c[name],N/c[name])
pages=[]
for start in range(0,7,4):
 board=Image.new('RGBA',(1200,560),'#17252d');draw=ImageDraw.Draw(board)
 for i,c in enumerate(q['captures'][start:start+4]):
  x=i%2*600;y=i//2*280
  world=Image.open(O/c['worldFile']).convert('RGBA');world.thumbnail((400,225));board.alpha_composite(world,(x,y+30))
  sprite=Image.open(O/c['sourceFile']).convert('RGBA');sprite.thumbnail((184,184));board.alpha_composite(sprite,(x+410,y+40));draw.text((x+8,y+8),c['label'],fill='white')
 name=f'entry-moving-{start//4+1}.png';board.save(N/name);pages.append(name)
html=(D/'index.html').read_text(encoding='utf-8');html+='<h2>Actual moving controller</h2><p>249 checks passed: all six entry holds submitted while Bill moves through a legal East floor segment, followed by the existing .104-second gait resume. Exact pickup and gait endpoints. Saved progress unchanged. Prescribed route; natural workshop turns and normal installation remain separate.</p>'+''.join(f'<img src="native/{p}" alt="Moving carry entry {i+1}">' for i,p in enumerate(pages));(D/'index.html').write_text(html,encoding='utf-8')
r=json.loads((D/'review.json').read_text());r.update(nativeTested=True,nativeValidation=v,nativeScope=q['scope'],nativePages=pages);(D/'review.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'checks':249,'failures':0,'movingHolds':6,'nativePages':2}))
