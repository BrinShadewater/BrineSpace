from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib
p=Path(__file__).resolve().parent
root=p.parents[1]
im=Image.open(p/'source-v1.png').convert('RGBA')
# The source has a low-opacity diffuse halo. Extract the authored near-opaque body;
# retain original RGB, no invented pixels or palette grading. Threshold is explicit.
mask=im.getchannel('A').point(lambda a:255 if a>=240 else 0)
box=mask.getbbox()
assert box and box[0]>0 and box[1]>0 and box[2]<im.width and box[3]<im.height
im.putalpha(mask)
crop=im.crop(box)
out=crop.convert('RGBa').resize((round(crop.width*148/crop.height),148),Image.Resampling.LANCZOS).convert('RGBA')
out.save(p/'body.png')
board=Image.new('RGBA',(650,260),'#53616b');d=ImageDraw.Draw(board)
d.text((16,12),'BRINE / reference-derived float candidate',fill='white')
old=Image.open(root/'character/brine-face-v7-2026-09-26/body.png').convert('RGBA')
old=old.resize((round(old.width*148/old.height),148),Image.Resampling.LANCZOS)
bill=Image.open(root/'character/crew-runtime-matte-v1/bill/frames/idle-south-matte-v2/000.png').convert('RGBA')
board.alpha_composite(old,(45,45));board.alpha_composite(out,(160,45));board.alpha_composite(bill,(255,21))
d.text((24,209),'Previous',fill='white');d.text((143,209),'New float',fill='white');d.text((303,209),'Current Bill',fill='white')
enlarged=out.resize((out.width*2,296),Image.Resampling.NEAREST)
board.alpha_composite(enlarged,(470,38))
d.text((467,240),'2x detail crop',fill='white')
board.convert('RGB').save(p/'body-review.png')
data={'status':'candidate, not installed','source':'source-v1.png','alpha_threshold':240,'source_crop':box,'export_size':out.size,'reference_height':148,'source_ids':['exec-55d4269c-de43-407b-becb-453506fee41f.png','exec-69fa0ef9-9195-46b8-93e9-63d35d9f98a6.png'],'rejected':'cutout-v2 changed source anatomy/face and retained halo; source-v1 selected for extraction','hashes':{name:hashlib.sha256((p/name).read_bytes()).hexdigest() for name in ['source-v1.png','rejected-cutout-v2.png','body.png','prompt.txt','cutout-prompt.txt']},'extraction_limits':'Threshold discards faint source fringe/hair as well as halo; native silhouette review required.'}
(p/'manifest.json').write_text(json.dumps(data,indent=2)+'\n')
print('Body:',out.size,'source crop:',box,'alpha range:',out.getchannel('A').getextrema())
