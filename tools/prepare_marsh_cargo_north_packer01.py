"""Adapt the reviewed whole-cell packer for rear boot registration, not pixel edits."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
text=(ROOT/'tools/pack_marsh_cargo_east_unload01.py').read_text()
text=text.replace('East','North').replace('east','north')
text=text.replace('scale=147/(nb[3]-nb[1])','scale=146/(nb[3]-nb[1])')
text=text.replace("stop=b[0]+round((b[2]-b[0])*.45)","stop=b[2]")
text=text.replace('Body boots occupy left 45% of the action silhouette; exclude floor case.','Rear boots span both sides; floor band uses complete foot span.')
text=text.replace('left boot floor-band midpoint','both rear boots floor-band midpoint')
text=text.replace("'neutralTargetHeight':147","'neutralTargetHeight':146").replace('one neutral147 BOX scale','one neutral146 BOX scale')
(ROOT/'tools/pack_marsh_cargo_north_unload01.py').write_text(text)
print('North whole packer prepared; one146 ruler and whole rear boot registration')
