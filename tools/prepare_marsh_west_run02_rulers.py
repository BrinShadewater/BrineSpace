"""Whole selected/near/far neutral/gait/contact comparison; no fitting."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-west-run-material-v1';OUT=BASE/'actor-review-v1';OUT.mkdir(exist_ok=True);guide=json.loads((BASE/'sources/guide-provenance.json').read_text())
poses=[ROOT/guide['primarySourceFrames'][0]['path'],BASE/'near-half-01-unselected/ruler.png',BASE/'far-half-02-unselected/ruler.png',ROOT/guide['primarySourceFrames'][2]['path'],BASE/'candidate-02/000.png'];labels=['Selected West idle','Near-source neutral33x148','Far-source neutral34x147','Selected West walk0','New West contact0']
board=Image.new('RGB',(1840,440),'#293b40');draw=ImageDraw.Draw(board)
for i,p in enumerate(poses):
    f=Image.open(p).convert('RGBA');pivot=guide['primarySourceFrames'][2]['metadata']['pivot'] if i==3 else [92,172];reg=Image.new('RGBA',(184,184));reg.alpha_composite(f,(92-int(pivot[0]),172-int(pivot[1])));assert np.count_nonzero(np.array(reg)[:,:,3])==np.count_nonzero(np.array(f)[:,:,3]);large=reg.resize((368,368),Image.Resampling.NEAREST);board.paste(large,(i*368,50),large);draw.text((i*368+4,5),labels[i],fill='white')
board.save(OUT/'source-ruler-comparison.png');print('Five complete selected/source rulers/gait/contact, common pivot nearest2x, no clipping.')
