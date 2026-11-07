"""Whole figures only: current selected body/gait and revised first half."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1';OUT=BASE/'actor-review-v3';OUT.mkdir(exist_ok=True)
guide=json.loads((BASE/'sources/guide-provenance.json').read_text())
poses=[ROOT/'character/marsh-v2/frames/bare/idle-east/000.png',BASE/'half-09-unselected/ruler.png',ROOT/guide['primarySourceFrames'][2]['path'],BASE/'candidate-03/000.png']
board=Image.new('RGB',(2208,610),'#293b40');draw=ImageDraw.Draw(board)
for i,p in enumerate(poses):
    f=Image.open(p).convert('RGBA');pivot=[92,172] if i!=2 else guide['primarySourceFrames'][2]['metadata']['pivot'];registered=Image.new('RGBA',(184,184));registered.alpha_composite(f,(92-int(pivot[0]),172-int(pivot[1])));assert np.count_nonzero(np.array(registered)[:,:,3])==np.count_nonzero(np.array(f)[:,:,3]);large=registered.resize((552,552),Image.Resampling.NEAREST);board.paste(large,(i*552,50),large);draw.text((i*552+8,8),['Selected East idle','New09 neutral ruler','Selected East walk0','New09 near-contact'][i],fill='white')
board.save(OUT/'source-ruler-comparison.png')
print('Whole idle/ruler/walk/contact at common pivot, nearest3x, no clipping.')
