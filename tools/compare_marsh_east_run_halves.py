"""Show unchanged complete figures; no playable sequence or fitting."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1'
rows=[['candidate-01/000.png','half-02-unselected/opposite-contact.png'],['candidate-01/002.png','half-02-unselected/opposite-flight.png'],['candidate-01/ruler.png','half-02-unselected/ruler.png']]
board=Image.new('RGB',(736,3*405),'#293b40');draw=ImageDraw.Draw(board);records=[]
for y,row in enumerate(rows):
    for x,name in enumerate(row):
        path=BASE/name;f=Image.open(path).convert('RGBA');assert f.size==(184,184)
        large=f.resize((368,368),Image.Resampling.NEAREST);board.paste(large,(x*368,y*405+35),large);draw.text((x*368+4,y*405+5),name,fill='white')
        records.append({'path':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
board.save(BASE/'half-02-unselected/first-half-join-comparison.png')
(BASE/'half-02-unselected/join-comparison.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'operation':'Complete unchanged184canvas at nearest2x; common runtime foot pivot. Different poses are not equal-height geometry tests.','sources':records},indent=2)+'\n')
print('Created six-figure held comparison; no source mutation or manifest.')
