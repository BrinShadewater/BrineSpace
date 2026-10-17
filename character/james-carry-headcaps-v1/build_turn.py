from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
base=r/'character/james-carry-authored-turn-v1/package.py'
source=base.read_text(encoding='utf-8')
start=source.index("for name in ['early','late']:");end=source.index('sources=[',start)
source=source[:start]+source[end:]
source=source.replace("p/'late-pose.png'","p/'late-meter-pose.png'").replace('early22.5 intended','early20 roof repaired').replace('late67.5 intended','late70 tool repaired')
exec(compile(source,str(base),'exec'),{'__file__':str(p/'build_turn.py')})
report=p/'review.json';data=json.loads(report.read_bytes());data.update(packagingBaseSha256=hashlib.sha256(base.read_bytes()).hexdigest(),packagingVariantSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),scope='Five bare authored carrying poses with local early/late roof and late duplicate-meter repairs; reused cardinal/middle originals. No paired helmet/native/normal admission.')
report.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
# Separate reverse preview uses the same saved source poses in reverse order.
im=Image.open(p/'station-preview.apng');decoded=[]
for i in range(im.n_frames):im.seek(i);decoded.append(im.convert('RGB').copy())
rev=list(reversed(decoded))
rev[0].save(p/'reverse-station-preview.apng',save_all=True,append_images=rev[1:],duration=[100,200,200,200,600],loop=0)
test=Image.open(p/'reverse-station-preview.apng');assert test.n_frames==5
for i,item in enumerate(rev):test.seek(i);assert test.convert('RGB').tobytes()==item.tobytes();assert test.info['duration']==[100,200,200,200,600][i]
print('Forward/reverse preview source RGB/durations checked; no continuous/native claim.')
