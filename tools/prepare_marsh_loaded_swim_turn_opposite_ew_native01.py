"""Actual directed800ms turn playback using the composed whole figures."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-turn-material-v1'
r=json.loads((B/'sources/opposite-ew-01.request.json').read_text())
s=(ROOT/'tools/review_marsh_loaded_swim_turn_eastnorth02.gd').read_text()
for a,b in [('loaded-swim-turn-eastnorth-native-02-2026-10-02','loaded-swim-turn-opposite-ew-native-01-2026-10-03'),('east-north-02-unselected/manifest.json','opposite-ew-01-unselected/manifest.json'),('east-north-02-unselected/ruler.png','west-north-01-unselected/ruler.png'),('["east-north","north-east"]','["east-west","west-east"]'),('is_equal_approx(player.cycle_seconds(key),.4)','is_equal_approx(player.cycle_seconds(key),.8)'),('finite400ms','finite800ms'),('player.frames[key][4]','player.frames[key][8]'),('[4-slot]','[8-slot]'),('range(5)','range(9)'),('range(22)','range(42)'),('step>=20','step>=40'),('var elapsed:float=step*.02','var elapsed:float=0 if step==0 else step*.02+.001'),('else 4-slot','else 8-slot'),('pair=="east-north"','pair=="east-west"'),('seen.size()==5','seen.size()==9'),('five finite poses','nine finite poses'),('samples.size()==44 and captures.size()==10 and restores==10','samples.size()==84 and captures.size()==18 and restores==18'),('East-North/North-East finite400ms','East-West/West-East finite800ms'),('10snapshot','18snapshot'),('EASTNORTH02','OPPOSITE EW01')]:s=s.replace(a,b)
line=next(q for q in s.splitlines() if 'var slot:int=' in q)
s=s.replace(line,'\t\t\tvar slot:int=0 if elapsed<.06 else 1 if elapsed<.15 else 2 if elapsed<.25 else 3 if elapsed<.34 else 4 if elapsed<.46 else 5 if elapsed<.55 else 6 if elapsed<.65 else 7 if elapsed<.74 else 8')
line=next(q for q in s.splitlines() if 'var oldpaths:Array=' in q)
s=s.replace(line,'\tvar oldpaths:Array='+json.dumps(['res://'+q['path'] for q in r['sourceFrames']]))
s=s.replace('East-North/North-East','East-West/West-East').replace('finite400ms','finite800ms').replace('at20ms steps','at20ms steps (+1ms after initial sample to avoid floating boundary ambiguity)')
p=ROOT/'tools/review_marsh_loaded_swim_turn_opposite_ew01.gd';p.write_text(s);p.with_suffix('.gd.uid').write_text('uid://bj6kv3pm5q8t\n')
print('Composed opposite800ms player fixture prepared:18pose restores/captures,84samples.')
