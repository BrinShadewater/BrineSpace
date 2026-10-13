"""Prepare composed North/South actual directed player gate."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/prepare_marsh_loaded_swim_turn_opposite_ew_native01.py').read_text()
for a,b in [('opposite-ew','opposite-ns'),('opposite_ew','opposite_ns'),('east-west','north-south'),('west-east','south-north'),('East-West/West-East','North-South/South-North'),('west-north-01-unselected/ruler.png','east-south-01-unselected/ruler.png'),('OPPOSITE EW01','OPPOSITE NS01'),('uid://bj6kv3pm5q8t','uid://dh8k6nv4mp2s')]:s=s.replace(a,b)
s=s.replace("p=ROOT/'tools/review", "s=s.replace('character/marsh-v2/frames/bare/idle-north/000.png','character/marsh-south-idle-material-v1/candidate-01/000.png').replace('Selected North master','Selected South master')\np=ROOT/'tools/review")
exec(compile(s,str(__file__),'exec'))
f=(ROOT/'tools/fingerprint_marsh_loaded_swim_turn_opposite_ew01.py').read_text().replace('opposite-ew','opposite-ns').replace('opposite_ew','opposite_ns').replace("['east-north-02','west-north-01']","['east-north-02','east-south-01','west-south-01']")
(ROOT/'tools/fingerprint_marsh_loaded_swim_turn_opposite_ns01.py').write_text(f)
