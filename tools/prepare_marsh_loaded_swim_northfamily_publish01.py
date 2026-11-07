"""Prepare exact selected-source publishing for the actual staged North-family q0."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/publish_marsh_loaded_swim_west_world01.py').read_text()
s=s.replace("B=ROOT/'character/marsh-loaded-swim-material-v1';A=ROOT/'output/marsh-animation-audit/loaded-swim-west-world-01-2026-10-02';O=B/'west-loop-01-world-review'", "B=ROOT/'character/marsh-loaded-swim-turn-material-v1';A=ROOT/'output/marsh-animation-audit/loaded-swim-northfamily-world-01-2026-10-03';O=B/'northfamily-world-01-review'")
old="[B/'east-loop-02-unselected/manifest.json',B/'west-loop-01-unselected/manifest.json']";assert old in s
s=s.replace(old,"[B/'opposite-ew-01-unselected/family-manifest.json']")
s=s.replace('Exact source / actual dispatched journey, staged East02/West01 loops','Exact source / q0 journey / private North-turn family')
s=s.replace("assert (A/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (A/'native.log').read_text()", "assert (A/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (A/'native.log').read_text() and 'WARNING:' not in (A/'native.log').read_text()")
p=ROOT/'tools/publish_marsh_loaded_swim_northfamily_world01.py';p.write_text(s)
exec(compile(s,str(p),'exec'))
