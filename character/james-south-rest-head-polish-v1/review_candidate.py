from pathlib import Path
from PIL import Image, ImageDraw
import hashlib,json,numpy as np
P=Path(__file__).resolve().parent;R=P.parents[1];S=R/'character/james-rest-material-continuity-v1'
original=Image.open(S/'frames/bare/lie-down-south/002.png').convert('RGBA')
master=Image.open(S/'frames/bare/lie-down-south/000.png').convert('RGBA')
generated=Image.open(P/'generated-frame-edit.png').convert('RGBA')
scaled=generated.resize(original.size,Image.Resampling.LANCZOS)
board=Image.new('RGB',(3*512,560),'#303b40');d=ImageDraw.Draw(board)
for i,(label,im) in enumerate([('standing master',master),('current reclining pose',original),('generated candidate, canvas normalized',scaled)]):
    enlarged=im.resize((512,512),Image.Resampling.NEAREST);board.paste(enlarged,(i*512,40),enlarged);d.text((i*512+10,10),label,fill='white')
board.save(P/'candidate-comparison.png')
a,b=np.array(original),np.array(scaled)
e={'method':'Built-in image_gen edit; original raw output retained. Canvas normalization is review-only, not accepted registration or a runtime source.','prompt':'frame-edit-prompt.txt','output':'generated-frame-edit.png','outputSha256':hashlib.sha256((P/'generated-frame-edit.png').read_bytes()).hexdigest(),'originalSize':list(original.size),'outputSize':list(generated.size),'originalAlphaBounds':original.getchannel('A').getbbox(),'normalizedCandidateAlphaBounds':scaled.getchannel('A').getbbox(),'normalizedChangedAlphaPixels':int(np.count_nonzero(a[:,:,3]!=b[:,:,3])),'normalizedChangedRGBAPixels':int(np.any(a!=b,2).sum()),'decision':'Not installed: raw edit changes complete source geometry/material/equipment despite head-only request. Face appears less round, but precise head registration, master width and adjacent-pose/helmet continuity are unproven. Do not use a full-frame replacement.','references':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [S/'frames/bare/lie-down-south/002.png',S/'frames/bare/lie-down-south/000.png']}}
(P/'generation-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
print(json.dumps({k:e[k] for k in ['originalSize','outputSize','originalAlphaBounds','normalizedCandidateAlphaBounds','normalizedChangedAlphaPixels','normalizedChangedRGBAPixels','decision']}))
