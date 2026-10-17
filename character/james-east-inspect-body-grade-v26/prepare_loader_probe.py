from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];template=r/'character/james-tablet-east-matte-v3/validate.gd'
code=template.read_text().replace('james-tablet-east-matte-v3','james-east-inspect-body-grade-v26')
code=code.replace('var player=grid.branforth_player','''var player=grid.branforth_player
    player.load_manifest(BODY,true)
    check(player.load_equipment_manifest("diving-helmet",HELMET),"Staged material override on normal loaded player")''')
code=code.replace('All new East inspection/interaction source references and sealed-meal compatibility substitutes through normal loader. All-direction inspection seams/clocks retained. Native route/gear journeys not exercised.',
 'Staged paired candidate appended to actual normal-loaded player, all East references/clocks/pivots sampled and native four-size captures. Other cardinal seams and sealed-meal semantics retained. Not normally installed, room/route/Continue or uninterrupted motion acceptance.')
(p/'validate.gd').write_text(code,encoding='utf-8')
files=[Path(__file__),template,p/'validate.gd',p/'bare-manifest.json',p/'helmet-manifest.json',p/'package-review.json',r/'scripts/crew_sprite_player.gd',r/'scripts/grid_canvas.gd',r/'character/james-side-motion-review-2026-10-02/run_validation.py']
for mode in ['bare','helmet']:
 data=json.loads((p/(mode+'-manifest.json')).read_bytes())
 for state in data['states']:files.extend((p/f).resolve() for f in state['frameFiles'])
(p/'loader-inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in set(files)}),indent=2)+'\n')
print('Staged material loader probe frozen; source grid loader remains unchanged.')
