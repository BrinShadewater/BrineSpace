"""Prepare independently scoped East native source publisher."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];target=ROOT/'tools/publish_marsh_east_collapse_actor.py';assert not target.exists()
text=(ROOT/'tools/publish_marsh_north_collapse_actor.py').read_text()
text=text.replace('north','east').replace('North','East').replace('candidate-02','candidate-01').replace('east-collapse-actor-02','east-collapse-actor-01')
text=text.replace('explicit unselected candidate02: complete milder first dip and four retained later source01 figures.','explicit unselected candidate01: five complete generated lowered figures and exact selected idle0.')
text=text.replace('63 bounded inputs stable;','Bounded inputs stable;').replace('Warm ivory/sage and exposed dark soles retained.','Warm ivory/sage body and ivory boot uppers retained; dark soles remain distinct.')
target.write_text(text)
print('Prepared East staged native publisher.')
