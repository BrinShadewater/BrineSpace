"""Prepare own front quarters for actual directed player validation."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
side=sys.argv[1];assert side in ('east','west')
name=side+'south01';pair=side+'-south'
s=(ROOT/'tools/prepare_marsh_loaded_swim_turn_westnorth_native01_generated.py').read_text()
for a,b in [('west-north-01',pair+'-01'),('west-north',pair),('north-west','south-'+side),('westnorth-native-01',side+'south-native-01'),('westnorth01',name),('WESTNORTH01',name.upper()),('West-North/North-West',side.title()+'-South/South-'+side.title()),('East-North/North-East',side.title()+'-South/South-'+side.title()),('Selected North master','Selected South master'),('character/marsh-v2/frames/bare/idle-north/000.png','character/marsh-south-idle-material-v1/candidate-01/000.png'),('uid://cx7mj2h8p4vn','uid://'+('cm8r5fq2vn7k' if side=='east' else 'by9s4pm6kh3t'))]:s=s.replace(a,b)
exec(compile(s,str(__file__),'exec'))
f=(ROOT/'tools/fingerprint_marsh_loaded_swim_turn_westnorth01.py').read_text().replace('west-north-01',pair+'-01').replace('marsh_loaded_swim_turn_westnorth','marsh_loaded_swim_turn_'+side+'south')
f=f.replace("paths +=list((ROOT/'tools').glob", "paths +=[ROOT/'tools/pack_marsh_loaded_swim_turn_south01.py',ROOT/'tools/prepare_marsh_loaded_swim_turn_south_native01.py']\npaths +=list((ROOT/'tools').glob")
(ROOT/f'tools/fingerprint_marsh_loaded_swim_turn_{name}.py').write_text(f)
