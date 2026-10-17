from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[2]
board=Image.new('RGB',(1280,300),'#202a30');draw=ImageDraw.Draw(board)
rows=[('Walk raw32',P/'full-clip-frames/032.png'),('Walk raw48',P/'full-clip-frames/048.png'),('V2 first source key',P.parent/'diagnostic-frames-v2/000.png'),('Original-guided held',R/'character/veld-east-held-original-master-v1/frames/bare/000.png'),('Original empty body',R/'character/veld-cargo-east-original-master-v3/frames/bare/005.png')]
for i,(label,path) in enumerate(rows):
 im=Image.open(path).convert('RGBA');assert im.size==(256,256)
 board.paste(im,(i*256,25),im);draw.text((i*256+4,4),label,fill='white')
board.save(P/'same-scale-master-grade-review.png')
print('Five complete figures at unchanged native scale/baseline; no RGB edits.')
