"""Prepare independent West whole-source packager using selected neutral density."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];target=ROOT/'tools/build_marsh_west_collapse.py';assert not target.exists()
text=(ROOT/'tools/build_marsh_east_collapse.py').read_text().replace('east','west').replace('East','West')
target.write_text(text)
print('Prepared independent West whole-cell builder; no reflected East bitmap.')
