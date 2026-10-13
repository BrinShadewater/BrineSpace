"""Enlarged complete poses for visible thigh/knee/boot continuity review."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1'
names=['candidate-01/001.png','candidate-01/002.png','candidate-01/005.png','half-02-unselected/opposite-flight.png','half-02-unselected/opposite-contact.png','farpass-08-unselected/passing.png']
board=Image.new('RGB',(1656,1180),'#293b40');draw=ImageDraw.Draw(board)
for i,name in enumerate(names):
    f=Image.open(BASE/name).convert('RGBA');assert f.size==(184,184);large=f.resize((552,552),Image.Resampling.NEAREST);x=(i%3)*552;y=(i//3)*590
    board.paste(large,(x,y+30),large);draw.text((x+5,y+5),name,fill='white')
board.save(BASE/'half-02-unselected/leg-continuity-review.png')
print('Six complete unchanged figures at nearest3x for phase review.')
