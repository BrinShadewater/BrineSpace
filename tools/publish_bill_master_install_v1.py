"""Publish installed Bill source registry and retained actual-room evidence."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,re,shutil
R=Path(__file__).resolve().parents[1];D=R/'character/bill-master-install-v1';D.mkdir(exist_ok=True)
pages=[];reports={};validations={}
for label,folder,validation in [('jobs','bill-master-install-native-v2','validation-corrected.json'),('title','bill-master-title-native-v1','validation.json')]:
 O=R/'output'/folder;N=D/label;N.mkdir(exist_ok=True)
 v=json.loads((O/validation).read_text());q=json.loads((O/'report.json').read_text());assert v['passed']
 validations[label]=v;reports[label]=q
 for name in [validation,'report.json','inputs-before.json','inputs-after.json']:shutil.copy2(O/name,N/name)
 for c in q['captures']:
  for name in ['worldFile','sourceFile']:shutil.copy2(O/c[name],N/c[name])
 for start in range(0,len(q['captures']),6):
  board=Image.new('RGBA',(1200,780),'#17252d');draw=ImageDraw.Draw(board)
  for i,c in enumerate(q['captures'][start:start+6]):
   x=i%2*600;y=i//2*260
   world=Image.open(O/c['worldFile']).convert('RGBA');world.thumbnail((400,225));board.alpha_composite(world,(x,y+30))
   sprite=Image.open(O/c['sourceFile']).convert('RGBA')
   if sprite.size==(184,184):
    padded=Image.new('RGBA',(256,256));padded.alpha_composite(sprite,(36,52));sprite=padded
   assert sprite.size==(256,256);sprite.thumbnail((184,184));board.alpha_composite(sprite,(x+410,y+40))
   caption=c['label'].replace('bill-cardinal-arrival3-eastg3s4-southg3s2-westg2s2-northg2s2-rise1','older source version').replace('bill-east-master-family-v1-cardinal-arrival3','installed East version')
   draw.text((x+6,y+6),caption[:83],fill='white')
  name=f'{label}-review-{start//6+1}.png';board.save(D/name);pages.append(name)
script=(R/'scripts/bill_carry_player.gd').read_text();block=script.split('const MASTER_BANKS',1)[1].split(']',1)[0]
paths=re.findall(r'"(res://[^"]+\.json)"',block);assert len(paths)==10
states={};refs=0
for path in paths:
 m=json.loads((R/path.removeprefix('res://')).read_text())
 for state in m['states']:states[state['id']]=state;refs+=len(state['frameFiles'])
assert refs==310 and sum(len(s['frameFiles']) for s in states.values())==238 and len(states)==18
registry={'selectedBinding':'bill-east-master-family-v1-cardinal-arrival3','normalAdmission':True,'bankPaths':paths,'selectedStates':states,'manifestReferences':310,'uniqueLogicalSlots':238,'legacySourceVersionsRetained':3,'equipment':'Existing helmet rows retained exactly. New whole figure art applies to bare East and seven shared East carry-turn programs.','nativeValidation':validations,'nativePages':pages,'visualReviewed':False,'limits':'Title Continue uses fresh normal scenes in the same native process, bare legacy/current cases; four main disk restores include both gear variants. Prescribed legal routes and real paid/service dispatch, not unforced goal choice or a new export. Other direction, equipment, life and water sources retain their selections.'}
(D/'registry.json').write_text(json.dumps(registry,indent=2)+'\n')
html='''<!doctype html><meta charset="utf-8"><title>Bill — East family installed</title><style>body{margin:24px auto;max-width:1200px;background:#14212a;color:#e4edf2;font:17px system-ui}img{width:100%;margin:12px 0}a{color:#aacfe4}.stats{padding:16px;background:#263a43}</style><h1>Bill: East animation family installed</h1><p>The reviewed bare East idle, walking, reach, running, carrying, torch and cargo handoffs now load in the game. Seven shared carry-turn poses use the repaired held figure.</p><p class="stats">4,286 installation checks + 101 Title Continue checks passed. Actual paid construction and workshop cargo work complete. Four disk resumes and two fresh-scene Title Continue cases preserve source, feet and animation clock.</p><p>Older checkpoints keep their saved animation version. Existing helmet and other directions stay selected. These are sampled actual station captures and submitted sprites.</p><p><a href="../bill-carry-turn-east-seams-v1/">Carry-turn comparison</a> · <a href="registry.json">Installed source registry</a></p>'''
html+=''.join(f'<img src="{name}" alt="{name}">' for name in pages)
(D/'index.html').write_text(html,encoding='utf-8')
# Keep republishing the turn review from accumulating duplicate native sections.
turn=R/'character/bill-carry-turn-east-seams-v1/index.html';text=turn.read_text();marker='<h2>Actual station turns</h2>'
parts=text.split(marker)
if len(parts)>2:turn.write_text(parts[0]+marker+parts[1],encoding='utf-8')
print(json.dumps({'pages':pages,'logicalSlots':238,'manifestReferences':310,'checks':4387,'captures':48}))
