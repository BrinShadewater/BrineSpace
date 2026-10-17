"""Register one generated head candidate; retain the original whole body."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
source=R/'character/james-rest-material-continuity-v1/frames/bare/lie-down-south/002.png'
master=R/'character/james-rest-material-continuity-v1/frames/bare/lie-down-south/000.png'
old=Image.open(source).convert('RGBA')
raw=Image.open(P/'generated-frame-edit.png').convert('RGBA')
# Full canvas normalization is used only to extract the authored head. All
# original body pixels outside the explicitly declared head/neck window survive.
normalized=raw.resize(old.size,Image.Resampling.LANCZOS)
window=(112,105,144,135)
out=old.copy();out.paste(normalized.crop(window),window[:2])
a,b=np.array(old),np.array(out);mask=np.zeros(a.shape[:2],bool);mask[105:135,112:144]=True
assert np.array_equal(a[~mask],b[~mask])
assert np.array_equal(a[135:],b[135:])
out.save(P/'candidate-bare-lie-down-south-002.png')
board=Image.new('RGB',(3*400,460),'#303b40');d=ImageDraw.Draw(board)
for i,(label,im,box) in enumerate([('master',Image.open(master).convert('RGBA'),(104,66,154,116)),('current',old,(103,99,153,149)),('head-only candidate',out,(103,99,153,149))]):
    crop=im.crop(box).resize((400,400),Image.Resampling.NEAREST);board.paste(crop,(i*400,40),crop);d.text((i*400+8,8),label,fill='white')
board.save(P/'registered-head-comparison.png')
e={'status':'staged_representative_only_not_installed','source':str(source.relative_to(R)),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'generatedSource':'generated-frame-edit.png','generatedSourceSha256':hashlib.sha256((P/'generated-frame-edit.png').read_bytes()).hexdigest(),'canvasNormalization':'LANCZOS raw1254x1254 to canonical256x256, used only for extracted head/neck candidate','extractionWindow':window,'neckBoundaryY':135,'registration':'Original canonical coordinates, no sprite bounding-box scale or translation; original head/neck interval112..144/105..135 replaced by the normalized generated interval.','unchangedOutsideWindow':True,'unchangedOriginalBodyAtAndBelowNeck':True,'changedPixels':int(np.any(a!=b,2).sum()),'changedAlphaPixels':int(np.count_nonzero(a[:,:,3]!=b[:,:,3])),'timingPivotHeightProductionChanges':False,'scope':'One bare pose2 authored-head candidate. No full sequence, helmet-face, cadence, controller, native furniture or master-identity acceptance.'}
(P/'representative-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
print(json.dumps({'changedPixels':e['changedPixels'],'changedAlphaPixels':e['changedAlphaPixels'],'outsideWindowExact':True,'bodyBelowNeckExact':True,'installed':False}))
