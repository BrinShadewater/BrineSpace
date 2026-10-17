from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
indices=list(range(8,25));board=Image.new('RGB',(6*352,3*292),'#303b40');draw=ImageDraw.Draw(board)
for slot,i in enumerate(indices):
    im=Image.open(P/'frames/bare/east'/f'{i:03d}.png').convert('RGBA');crop=im.crop((68,64,138,116)).resize((350,260),Image.Resampling.NEAREST);at=(slot%6*352,slot//6*292);board.paste(crop,(at[0],at[1]+25),crop);draw.text((at[0]+6,at[1]+8),'East tablet lift '+str(i),fill='white')
board.save(P/'east-tablet-lift-detail.png')
