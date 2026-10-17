from pathlib import Path
from PIL import Image
p=Path(__file__).resolve().parent
paths=sorted((p/'captures').glob('frame-*.png'))
assert len(paths)==200
frames=[Image.open(f).convert('RGB').resize((480,670),Image.Resampling.NEAREST) for f in paths]
# One palette across every frame avoids animated palette shifts.
sample=Image.new('RGB',(480*5,670))
for i,n in enumerate([0,40,80,120,160]): sample.paste(frames[n],(480*i,0))
palette=sample.quantize(colors=256)
indexed=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
indexed[0].save(p/'float-preview.gif',save_all=True,append_images=indexed[1:],duration=40,loop=0,disposal=2,optimize=False)
sheet=Image.new('RGB',(960,670))
for i,n in enumerate(range(0,200,25)): sheet.paste(frames[n].resize((240,335)),((i%4)*240,(i//4)*335))
sheet.save(p/'motion-review.png')
print('200 native samples, 25 fps, 8 seconds, shared-palette GIF.')
