"""Derive the cardinal candidate fixture from the reviewed per-direction contract."""
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1]
src=R/'tools/review_veld_swim_carry_south_coherent_v1.gd'
s=src.read_text().replace('veld-swim-carry-south-coherent-v1','veld-swim-carry-matrix-coherent-v1').replace('VELD SOUTH WATER CARGO CANDIDATE','VELD MATRIX WATER CARGO CANDIDATE').replace('review_veld_swim_carry_south_coherent_v1','review_veld_swim_carry_matrix_coherent_v1')
s=s.replace('Rect2(0,0,1600,650)','Rect2(0,0,1600,2600)').replace('Vector2i(1600,650)','Vector2i(1600,2600)')
start=s.index('  var m:Dictionary=');end=s.index(' board.queue_redraw();',start)
body=s[start:end];body=body.replace(';var state:Dictionary=m.states[0]','')
lines=body.splitlines();body=lines[0]+'\n  for state in m.states:\n   var direction:String=state.id.trim_prefix("swim-carry-")\n   var axis:Vector2={"east":Vector2.RIGHT,"west":Vector2.LEFT,"north":Vector2.UP,"south":Vector2.DOWN}[direction]\n'+'\n'.join(' '+x for x in lines[1:])+'\n'
body=body.replace('"swim-carry","south"','"swim-carry",direction').replace('Vector2(0,float(i)*.16/6.0+.000001)','axis*(float(i)*.16/6.0+.000001)')
s=s[:start]+body+s[end:]
(R/'tools/review_veld_swim_carry_matrix_coherent_v1.gd').write_text(s)
w=(R/'character/veld-swim-carry-south-coherent-v1/check_native.py').read_text().replace('south','matrix').replace('SOUTH','MATRIX')
(H/'check_native.py').write_text(w)
print('Cardinal candidate fixture prepared; every paired state and actual cardinal axis.')
