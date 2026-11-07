"""Create independent East guide preparation before coolant placement review."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];target=ROOT/'tools/prepare_marsh_east_injury_material.py';assert not target.exists()
text=(ROOT/'tools/prepare_marsh_north_injury_material.py').read_text()
text=text.replace('north','east').replace('North','East').replace('candidate-02','candidate-01')
text=text.replace('inspect rear-view guide first','inspect East side-view guide first').replace('right-screen glove anchor','visible side-view glove anchor')
target.write_text(text)
print('Prepared independent East injury guide helper.')
