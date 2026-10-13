"""Prepare own West complete-body/effect guides before coolant placement."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];target=ROOT/'tools/prepare_marsh_west_injury_material.py';assert not target.exists()
text=(ROOT/'tools/prepare_marsh_east_injury_material.py').read_text().replace('east','west').replace('East','West')
text=text.replace("BODY/f'","BODY/f'")
text=text.replace("body=ROOT/'character/marsh-west-collapse-material-v1/candidate-01'","body=ROOT/'character/marsh-west-collapse-material-v1/candidate-02'")
target.write_text(text)
print('Prepared own West injury/recovery guide helper with corrected complete body.')
