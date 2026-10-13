"""Retain occluded draft and move the complete first drop swatch beside glove."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1];base=ROOT/'character/marsh-east-injury-material-v1'
shutil.copytree(base/'candidate-01',base/'occluded-first-drop-draft',dirs_exist_ok=False)
builder=ROOT/'tools/build_marsh_east_injury_material.py';text=builder.read_text()
assert '1:(98,114)' in text
text=text.replace('1:(98,114)','1:(106,124)')
builder.write_text(text)
print('Retained first draft with zero visible pose1 coolant pixels; whole swatch translated, body unchanged.')
