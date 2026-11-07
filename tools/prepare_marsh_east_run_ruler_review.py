"""Whole unchanged native-density ruler/idle/action comparison, no art edits."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1';OUT=BASE/'actor-review-v1';OUT.mkdir(exist_ok=True)
poses=[ROOT/'character/marsh-v2/frames/bare/idle-east/000.png',BASE/'candidate-01/ruler.png',ROOT/'character/marsh-v2/frames/bare/walk-east/000.png',BASE/'candidate-01/000.png']
# Resolve the actual selected walk from frozen guide, not guessed registry layout.
import json
guide=json.loads((BASE/'sources/guide-provenance.json').read_text());poses[2]=ROOT/guide['primarySourceFrames'][2]['path']
board=Image.new('RGB',(4*552,610),'#293b40');draw=ImageDraw.Draw(board)
for i,p in enumerate(poses):
    f=Image.open(p).convert('RGBA');pivot=[92,172] if i!=2 else guide['primarySourceFrames'][2]['metadata']['pivot'];registered=Image.new('RGBA',(184,184));registered.alpha_composite(f,(92-int(pivot[0]),172-int(pivot[1])));f=registered.resize((552,552),Image.Resampling.NEAREST);board.paste(f,(i*552,50),f);draw.text((i*552+8,8),['Selected East idle','Generated neutral ruler','Selected East gait0','Generated run contact0'][i],fill='white')
board.save(OUT/'source-ruler-comparison.png');print('Prepared whole selected/generated ruler/action comparison, nearest3x only.')
