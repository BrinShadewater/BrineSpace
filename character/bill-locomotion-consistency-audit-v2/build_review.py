"""Same-density current selected walk/run comparisons; visual evidence, not acceptance."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
inventory=R/'character/bill-selected-source-audit-2026-10-01-locomotion-v13/source-inventory.json';audit=json.loads(inventory.read_text())
block=(R/'scripts/grid_canvas.gd').read_text(encoding='utf-8').split('func _load_major_bill_animations() -> void:',1)[1].split('\nfunc ',1)[0]
assert hashlib.sha256(block.encode()).hexdigest()==audit['loaderBlockSha256'],'Selection snapshot changed: take a new source inventory'
records=[]
for direction in ['east','west','south','north']:
 board=Image.new('RGB',(2304,1536),(34,52,62));draw=ImageDraw.Draw(board)
 for row,(gear,state) in enumerate([('bare','walk'),('bare','run'),('helmet','walk'),('helmet','run')]):
  y=row*384;src=audit['selectedStateSources'][gear][state+'-'+direction];count=src['frames'];indices=list(range(count)) if count<=8 else [round(i*(count-1)/7) for i in range(8)]
  master=R/f'character/bill-seated-{"helmet-" if gear=="helmet" else ""}{direction}-coherent-v1/frames/sit-down-{direction}/000.png'
  choices=[(master,[128,224],148,'Master')]+[(R/src['sourceFiles'][i][6:],src['pivot'],src['standingHeight'],str(i)+'/'+str(count)) for i in indices]
  for column,(f,pivot,height,caption) in enumerate(choices):
   im=Image.open(f).convert('RGBA');scale=148/height
   for target,baseline in [(148,y+224),(82,y+355)]:
    s=target/height;scaled=im.resize((round(im.width*s),round(im.height*s)),Image.Resampling.LANCZOS);pos=(round(column*256+128-pivot[0]*s),round(baseline-pivot[1]*s));board.paste(scaled,pos,scaled)
   draw.text((column*256+12,y+245),caption,fill='white')
  draw.text((12,y+365),gear+' '+state+' '+direction,fill='white')
  records.append({'gear':gear,'state':state,'direction':direction,'selectedManifest':src['manifest'],'phaseIndices':indices,'master':master.relative_to(R).as_posix(),'sourceHashes':{str(f.relative_to(R).as_posix()):hashlib.sha256(f.read_bytes()).hexdigest() for f,_,_,_ in choices}})
 board.save(P/(direction+'-review.png'))
(P/'source-review.json').write_text(json.dumps({'scope':'Current literal-selected cardinal walk/run source comparisons at148 and82 anatomical pixels. Eight uniformly indexed walk samples, all six run poses. Not engine playback, reachability, all-frame inspection or owner acceptance.','inventorySha256':hashlib.sha256(inventory.read_bytes()).hexdigest(),'loaderBlockSha256':audit['loaderBlockSha256'],'rows':records},indent=2)+'\n')
print('Built16 current cardinal walk/run comparison rows at148/82 density')
