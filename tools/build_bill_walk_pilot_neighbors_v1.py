"""Expose adjacent stride joins without changing selected animation sources."""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1';F=R/'character/bill-walk-east-material-v1/frames/bare/walk-east';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
tiles=[('Selected23',F/'023.png'),('Selected24',F/'024.png'),('Candidate24',P/'candidate-024.png'),('Selected25',F/'025.png'),('Original master',P/'original-master.png')]
board=Image.new('RGB',(1600,650),'#17252d');draw=ImageDraw.Draw(board);inputs={}
for n,(label,path) in enumerate(tiles):
 inputs[str(path)]=sha(path);im=Image.open(path).convert('RGBA')
 if im.size!=(256,256):im=im.resize((256,256),Image.Resampling.LANCZOS)
 body=im.resize((320,320),Image.Resampling.NEAREST);board.paste(body,(n*320,35),body);draw.text((n*320+10,12),label,fill='white');head=im.crop((100,66,160,126)).resize((240,240),Image.Resampling.NEAREST);board.paste(head,(n*320+40,400),head)
board.save(P/'neighbor-comparison.png');(P/'neighbor-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n',encoding='utf-8');print('Five whole figures and fixed head diagnostics; three unchanged selected stride phases retained.')
