"""Pack independently authored front quarters using one own South ruler."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
side=sys.argv[1];assert side in ('east','west')
generation=sys.argv[2];assert generation.startswith('exec-')
s=(ROOT/'tools/pack_marsh_loaded_swim_turn_westnorth01.py').read_text()
for a,b in [('west-north-01',side+'-south-01'),('west-north',side+'-south'),('north-west','south-'+side),('westnorth01',side+'south01'),('exec-0dd0f7c4-7c73-4ab3-be0e-f72ab9b4b91e',generation),('exact West01','exact '+side.title()+('02' if side=='east' else '01')),('exact North04','exact South01'),('own North master','own South master'),('character/marsh-v2/frames/bare/idle-north/000.png','character/marsh-south-idle-material-v1/candidate-01/000.png'),('146','147')]:s=s.replace(a,b)
exec(compile(s,str(__file__),'exec'))
