"""Retain heavily occluded source draft and translate complete droplet inserts."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1];base=ROOT/'character/marsh-west-injury-material-v1'
shutil.copytree(base/'candidate-01',base/'occluded-glove-draft',dirs_exist_ok=False)
path=ROOT/'tools/build_marsh_west_injury_material.py';text=path.read_text()
assert 'anchors={1:(78,124),2:(82,142)}' in text
text=text.replace('anchors={1:(78,124),2:(82,142)}','anchors={1:(70,124),2:(72,142)}');path.write_text(text)
print('Retained3/30visiblepixel draft; whole drop translations revised, exact anatomy preserved.')
