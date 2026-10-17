"""Reuse the scoped player review with own-North names and independent UID."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/prepare_marsh_loaded_swim_west_native01_generated.py').read_text()
for a,b in [('west-loop-01','north-loop-03'),('swim-carry-west','swim-carry-north'),('loaded-swim-west-native-01','loaded-swim-north-native-03'),('idle-west','idle-north'),('WholeWest01','WholeNorth03'),('West master','North master'),('SWIM WEST01','SWIM NORTH03'),('"west"','"north"'),('review_marsh_loaded_swim_west01.gd','review_marsh_loaded_swim_north03.gd'),('uid://cnwq2txp6ge','uid://cj7p5n3sv1kt'),('marsh-loaded-swim-east-material02-unselected','marsh-loaded-swim-north-material03-unselected'),('four whole02 figures','four whole North03 figures')]:s=s.replace(a,b)
p=ROOT/'tools/prepare_marsh_loaded_swim_north_native03_generated.py';p.write_text(s)
exec(compile(s,str(p),'exec'))
