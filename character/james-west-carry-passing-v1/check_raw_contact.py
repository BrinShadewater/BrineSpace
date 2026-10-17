from pathlib import Path
from PIL import Image
import json
p=Path(__file__).resolve().parent
rows=[]
for name in ['passing-near-support','passing-far-support','passing-far-support-v2']:
    if not (p/(name+'-native-crop.png')).exists():continue
    native=Image.open(p/(name+'-native-crop.png')).convert('RGBA');alpha=native.getchannel('A');box=alpha.point(lambda x:255 if x>=128 else 0).getbbox()
    below=alpha.crop((0,80,96,96));count=sum(v>=128 for v in below.get_flattened_data())
    rgba=native.get_flattened_data();reds=sum(a>=128 and red>150 and red>g*1.8 and red>b*1.8 for red,g,b,a in rgba)
    rows.append({'pose':name,'rawNativeBounds':box,'rawBottomWorld':box[3]+144 if box else None,'rawAlpha128PixelsAtOrBelowWorld224':count,'rawRedGuidePixels':reds})
(p/'raw-contact-review.json').write_text(json.dumps({'poses':rows,'scope':'Actual raw native crop before admission: baseline overshoot and guide contamination diagnostics. Not support/swing ownership or gait acceptance.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps(rows))
