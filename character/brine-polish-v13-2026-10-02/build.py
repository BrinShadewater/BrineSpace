from pathlib import Path
from PIL import Image

p=Path(__file__).resolve().parent
image=Image.open(p/'source.png').convert('RGBA')
# Same explicit near-opaque extraction as v12: keep authored RGB; discard halo.
alpha=image.getchannel('A').point(lambda a:255 if a>=240 else 0)
box=alpha.getbbox()
assert box and box[0]>0 and box[1]>0 and box[2]<image.width and box[3]<image.height
image.putalpha(alpha)
crop=image.crop(box)
body=crop.convert('RGBa').resize((round(crop.width*148/crop.height),148),Image.Resampling.LANCZOS).convert('RGBA')
assert body.size==(58,148)
body.save(p/'body.png')
print('Rebuilt 58x148 body from immutable source; no generation call.')
