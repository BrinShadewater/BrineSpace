"""Present unmodified native screenshots and source captures with browser crop windows."""
from pathlib import Path
import json,html,shutil
P=Path(__file__).resolve().parent
R=P.parents[1]
O=R/'output/bill-carry-source-version-continue-v1'
d=json.loads((O/'records.json').read_text());v=json.loads((O/'validation.json').read_text())
assert v['passed'] and d['failures']==0 and len(d['records'])==8
cards=[]
(P/'version-captures').mkdir(exist_ok=True)
for r in sorted(d['records'],key=lambda r:(r['helmet'],r['phase'],r['name'])):
 x=255+(r['foot'][0]-7680)*398/384;y=287+(r['foot'][1]-8064)*398/384
 tag=r['name'];frames=[]
 for stage in ['before','after']:
  for kind in ['room','source']:
   name=f'{tag}-{stage}-{kind}.png';shutil.copy2(O/name,P/'version-captures'/name)
  url=f'version-captures/{tag}-{stage}-room.png'
  frames.append(f'<div><p>{stage.capitalize()} Continue</p><div class="crop"><img src="{url}" style="left:{90-x:.3f}px;top:{145-y:.3f}px"></div></div>')
 cards.append(f'<section><h2>{html.escape(tag.replace("-"," · "))}</h2><div class="pair">'+''.join(frames)+f'</div><p class="note">Exact source, physical foot and clock preserved; next 30 ticks match.</p></section>')
page='''<!doctype html><meta charset="utf-8"><title>Bill · North carrying Continue</title>
<style>body{background:#182932;color:#dde8e9;font:15px system-ui;margin:22px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(390px,420px));gap:16px}section{background:#22343e;padding:12px;border:1px solid #4c626d}h2{font-size:17px;margin:0}.pair{display:flex;gap:15px}.pair p{margin:8px 0}.crop{position:relative;width:180px;height:180px;overflow:hidden}.crop img{position:absolute;width:1280px;max-width:none;height:900px}.note{font-size:12px;margin:8px 0}p{max-width:860px}</style>
<h1>Bill · North carrying Continue</h1><p>New sessions use the more articulated North step. Existing saved sessions retain their original North art. These are actual station captures before and after fresh-scene Continue, in both equipment variants. Collision-clear North route is prescribed for this check; natural route selection remains a separate review.</p>
<p><a style="color:#adcddd" href="./">North master / first step / walking preview</a></p><main>CARDS</main>'''
(P/'version-continue.html').write_text(page.replace('CARDS',''.join(cards)),encoding='utf-8')
(P/'version-runtime-evidence.json').write_text(json.dumps({'validation':v,'records':d,'normalSelectionChanged':True,'sourceVersionPolicy':'New sessions use North gait2/start2; restored sessions retain gait1/start1 or gait2/start2 for their lifetime. No mid-pose automatic migration.','visualReview':'Pending separate native crop review.','scope':'Eight actual disk/fresh selected-main restores, both source versions, both gears, North entry and arrival; real service and prescribed clear North lane. Exact source/root/clock, pause, and30future ticks. Not natural routes or complete anatomical contact certification.'},indent=2)+'\n')
print('Eight native before/after cases presented without modifying capture pixels')
