"""Package native capture frames without resizing their physical pixels."""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'output/room-transitions-v1'
frames=[Image.open(P/f'motion-{i:02}.png').convert('RGB').crop((244,226,1020,1180)) for i in range(24)]
swatches=Image.new('RGB',(frames[0].width,frames[0].height*len(frames)))
for i,frame in enumerate(frames):swatches.paste(frame,(0,i*frame.height))
palette=swatches.quantize(colors=256)
indexed=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
indexed[0].save(P/'room-and-ocean-motion-v1.gif',save_all=True,append_images=indexed[1:],duration=[240]*23+[1100],loop=0,optimize=False)
stages=Image.new('RGB',(frames[0].width*3,frames[0].height))
for i,index in enumerate([0,9,19]):stages.paste(frames[index],(i*frames[0].width,0))
stages.save(P/'motion-stages-v1.png')
print('Native motion preview:',frames[0].size,'24 frames; fixed palette; no physical-pixel resize')
