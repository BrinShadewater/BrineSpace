"""Prepare an independent East whole-cell builder at selected occupied density."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
target=ROOT/'tools/build_marsh_east_collapse.py';assert not target.exists()
text=(ROOT/'tools/build_marsh_north_collapse.py').read_text()
text=text.replace('north','east').replace('North','East').replace('occupied146height','occupied147height')
text=text.replace('Dark exposed sole material preserved.','Warm ivory boot uppers and dark matte soles preserved.')
target.write_text(text)
print('Prepared East whole-source builder; no pose fitting.')
