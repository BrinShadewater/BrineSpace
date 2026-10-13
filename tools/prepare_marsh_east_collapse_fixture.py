"""Create independent East actual shutdown study from established North harness."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
target=ROOT/'tools/review_marsh_east_collapse_actor.gd';assert not target.exists()
text=(ROOT/'tools/review_marsh_north_collapse_actor.gd').read_text()
text=text.replace('north','east').replace('North','East').replace('NORTH','EAST')
text=text.replace('east-collapse-actor-02','east-collapse-actor-01').replace('candidate-02/manifest.json','candidate-01/manifest.json')
target.write_text(text);target.with_suffix('.gd.uid').write_text('uid://cg6ehclpm2v74\n')
print('Prepared independent East native shutdown fixture and pairedUID.')
