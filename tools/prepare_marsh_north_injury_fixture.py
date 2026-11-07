"""Create independent North impact fixture from established South harness."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'tools/review_marsh_north_injury_actor.gd'
assert not path.exists(),'already prepared; preserve fixture'
source=(ROOT/'tools/review_marsh_south_injury_actor.gd').read_text()
source=source.replace('south-injury-actor-01','north-injury-actor-01').replace('marsh-south-injury-material-v1','marsh-north-injury-material-v1').replace('south','north').replace('SOUTH','NORTH')
path.write_text(source)
path.with_suffix('.gd.uid').write_text('uid://ce4nhinjm9v72\n')
print('Prepared independent North impact/recovery fixture and pairedUID.')
