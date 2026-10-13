"""Prepare independent selected West whole-figure comparison guides."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];target=ROOT/'tools/prepare_marsh_west_damage_guides.py';assert not target.exists()
text=(ROOT/'tools/prepare_marsh_east_damage_guides.py').read_text().replace('east','west').replace('East','West')
target.write_text(text)
print('Prepared West guide helper; selected manifest controls preview registration.')
