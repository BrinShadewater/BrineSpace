from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
refs=json.loads((p/'rise-reference-evidence.json').read_bytes())
assert all(hashlib.sha256((r/c['source']).read_bytes()).hexdigest()==c['sha256'] for c in refs['sources'])
metrics={}
for mode in ['bare','helmet']:
    files=[r/next(c['source'] for c in refs['sources'] if c['gear']==mode and c['index']==4),p/'rise-v1'/mode/'000.png',p/'rise-v1'/mode/'001.png',r/next(c['source'] for c in refs['sources'] if c['gear']==mode and c['index']==5)]
    board=Image.new('RGB',(2048,570),'#303b40');draw=ImageDraw.Draw(board)
    for i,path in enumerate(files):
        image=Image.open(path).convert('RGBA');alpha=image.getchannel('A').point(lambda v:255 if v>=128 else 0)
        bounds=alpha.getbbox();body=alpha.crop((0,0,256,194)).getbbox()
        metrics[mode+str(i)]={'path':str(path.relative_to(r)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'alpha128Bounds':bounds,'bodyAboveCaseBounds':body}
        scaled=image.resize((512,512),Image.Resampling.NEAREST);board.paste(scaled,(i*512,25),scaled)
        draw.text((i*512+6,6),['original crouch4','draft interior1','draft interior2','original standing5'][i],fill='white')
        draw.text((i*512+6,542),'alpha top%d / bottom%d / body width%d'%(bounds[1],bounds[3],body[2]-body[0]),fill='white')
    board.save(p/(mode+'-rise-v1-review.png'))
(p/'rise-v1-review-evidence.json').write_text(json.dumps({'selected':False,'visualReviewPending':True,'scaleScope':'One uniform44/138case ruler and per-cell floor translations; original endpoints never resized relative to common256canvas/p128224/H148. Alpha metrics are diagnostics, not permission to normalize every pose height.','metrics':metrics},indent=2)+'\n')
print(json.dumps({k:{'top':v['alpha128Bounds'][1],'bottom':v['alpha128Bounds'][3],'bodyWidth':v['bodyAboveCaseBounds'][2]-v['bodyAboveCaseBounds'][0]} for k,v in metrics.items()}))
