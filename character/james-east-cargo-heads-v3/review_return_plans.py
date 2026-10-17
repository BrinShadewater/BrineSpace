"""Registered presentations of staged plans; no raster artwork changes."""
from pathlib import Path
import json,re
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
loader=(r/'scripts/grid_canvas.gd').read_text().split('elif actor == "branforth":',1)[1].split('\n\t\tset(actor+',1)[0]
banks={'bare':{},'helmet':{}};profiles={'bare':{},'helmet':{}}
for kind,rel in re.findall(r'player\.(load_manifest|load_equipment_manifest)\([^\n]*?"res://([^"\n]+\.json)"',loader):
    path=r/rel;pack=json.loads(path.read_bytes());mode='bare' if kind=='load_manifest' else 'helmet'
    for state in pack['states']:
        if not state.get('frameFiles'):continue
        banks[mode][state['id']]=[(path.parent/f).resolve() for f in state['frameFiles']]
        profiles[mode][state['id']]=(pack.get('pivot',[46,86]),pack.get('standingHeight',74))
report=json.loads((p/'return-plan-probe-evidence.json').read_bytes())
probe=json.loads((p/'interruption-probe-evidence.json').read_bytes())
audit=json.loads((p/'interruption-source-audit.json').read_bytes())
presentations=[]
for case,binding in zip(probe['results'],audit['results']):
    key=case['beforeMotion']['clip'] if case['target']=='workshop_carry' else case['beforePose']+'-'+binding['endpointFacing']
    aliases=binding['captures'][0]['matches'];index=next(m['index'] for m in aliases if m['state']==key)
    gear='' if case['mode']=='bare' else 'diving-helmet'
    plan=next(x for x in report['plans'] if x['source']==key and x['sourceIndex']==index and x['gear']==gear)
    rows=plan['rows'];board=Image.new('RGB',(max(4,len(rows))*260,290),'#303b40');draw=ImageDraw.Draw(board)
    for col,row in enumerate(rows):
        mode=case['mode'];im=Image.open(banks[mode][row['key']][row['index']]).convert('RGBA')
        pivot,height=profiles[mode][row['key']];assert height==148
        x=col*260
        draw.text((x+3,4),f"{row['key']} / {row['index']}",fill='white')
        draw.text((x+3,18),f"{round(row['seconds']*1000)} ms",fill='white')
        board.paste(im,(x+128-int(pivot[0]),33+224-int(pivot[1])),im)
        draw.line((x,257,x+255,257),fill='#929d9f')
    filename=f"return-plan-{case['mode']}-{case['target']}.png";board.save(p/filename)
    presentations.append({'mode':case['mode'],'stage':case['target'],'source':key,'sourceIndex':index,'board':filename,'rows':len(rows),'gaps':plan['gaps']})
(p/'return-plan-review.json').write_text(json.dumps({'presentations':presentations,'visualReviewPending':True,'selected':False,'scope':'Six retained native interruption sources mapped to staged registered source-clock plans. Static full-source order only; no native controller, continuous motion, crate-floor or idle-join acceptance.'},indent=2)+'\n')
print('Six registered source-plan boards saved; remaining joins explicitly retained.')
