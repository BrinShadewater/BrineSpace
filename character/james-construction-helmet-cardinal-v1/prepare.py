from pathlib import Path
import json, hashlib
P = Path(__file__).resolve().parent
R = P.parents[1]
source = (R/'character/james-construction-helmet-v1/north.gd').read_text(encoding='utf-8')
for side, direction in enumerate(['north','east','south','west']):
    if side == 0:
        continue
    text = source.replace('return [0]', f'return [{side}]').replace('return "north"', f'return "{direction}"')
    text = text.replace('res://character/james-construction-helmet-v1/', 'res://character/james-construction-helmet-cardinal-v1/')
    text = text.replace('if lane()=="south" and not game.hand_collapsed:', 'if not game.hand_collapsed:')
    text = text.replace('Bare only; no fresh Continue inside new motion yet.', 'Helmeted '+direction+' only; six actual interruption cases. Supported prescribed worn gear, not locker fitting. No new fresh Continue in this fixture.')
    (P/(direction+'.gd')).write_text(text,encoding='utf-8')
files = list(json.loads((R/'character/james-construction-helmet-v1/runtime-input-before.json').read_text()))
(P/'runtime-input-before.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in files},indent=2)+'\n',encoding='utf-8')
print('Three other-facing helmet construction interruption fixtures; no production changes')
