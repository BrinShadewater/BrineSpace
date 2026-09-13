"""Prepare the authored communal table, preserving bench gaps and source evidence."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
p=Path(__file__).resolve().parents[1]/'assets/galley-owner-v2'
raw=p/'table-raw.png'
im=Image.open(raw).convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(int)
key=(rgb[:,:,0]-rgb[:,:,1]>35)&(rgb[:,:,2]-rgb[:,:,1]>35)
a[key]=0
clean=Image.fromarray(a);crop=clean.getbbox();clean=clean.crop(crop)
for q,turn in enumerate([clean,clean.transpose(Image.Transpose.ROTATE_270),clean.transpose(Image.Transpose.ROTATE_180),clean.transpose(Image.Transpose.ROTATE_90)]):turn.save(p/f'table-q{q}.png')
record={'source_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'source_size':im.size,'crop':crop,'clean_size':clean.size,'key':'R-G>35 and B-G>35, including bench gaps','stage':'cleaned, not selected','remaining':'native crew scale, layout access, integration'}
(p/'table-review.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
