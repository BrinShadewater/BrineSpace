from pathlib import Path
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent
files=['frames-v9/bare/001.png','frames-v9/bare/002.png','collar-v10-bare.png','frames-v9/bare/003.png']
board=Image.new('RGB',(4*512,700),'#303b40')
draw=ImageDraw.Draw(board)
for i,f in enumerate(files):
    im=Image.open(p/f).convert('RGBA');bg=Image.new('RGBA',im.size,'#303b40');bg.alpha_composite(im)
    draw.text((i*512+8,8),['previous','original target','repaired target','next'][i],fill='white')
    board.paste(bg.convert('RGB').resize((512,512),Image.Resampling.NEAREST),(i*512,26))
    crop=bg.crop((102,70,164,125)).convert('RGB').resize((310,165),Image.Resampling.NEAREST)
    board.paste(crop,(i*512+100,535))
board.save(p/'collar-v10-review.png')
print('Four paired-context source presentations plus neck/shoulder crops; not native motion.')
