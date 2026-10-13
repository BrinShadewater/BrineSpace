"""Prepare exact-source q0 boards and own-West endpoint diagnostics."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/publish_marsh_loaded_swim_world05.py').read_text().replace('loaded-swim-east-world-05','loaded-swim-west-world-01').replace('east-loop-02-world-review','west-loop-01-world-review')
s=s.replace("+[B/'east-loop-02-unselected/manifest.json']","+[B/'east-loop-02-unselected/manifest.json',B/'west-loop-01-unselected/manifest.json']")
s=s.replace("selected['swim-carry-east'][0]","selected['swim-carry-west'][0]")
s=s.replace("[('swim-pickup-east',-1),('swim-carry-turn-west-east',-1),('swim-carry-turn-east-north',0),('cargo-drain-east',0)]","[('swim-pickup-west',-1),('swim-carry-turn-east-west',-1),('swim-carry-turn-west-south',0),('cargo-drain-west',0)]")
s=s.replace('sameAsNewEastLoop0','sameAsNewWestLoop0').replace('staged East only','staged East02/West01 loops')
(ROOT/'tools/publish_marsh_loaded_swim_west_world01.py').write_text(s)
