from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
source=(p/'package.py').read_text(encoding='utf-8')
source=source.replace("for name in ['early','late']:","for name in ['early-v2','late-v2']:").replace('(r/k).read_bytes()','(p/k).read_bytes()')
for old,new in [('early-pose.png','early-v2-pose.png'),('late-pose.png','late-v2-pose.png'),("p/'frames'","p/'frames-v2'"),('whole-chronology.png','v2-whole-chronology.png'),('upper-chronology.png','v2-upper-chronology.png'),('legs-chronology.png','v2-legs-chronology.png'),('station-preview.apng','v2-station-preview.apng'),('station-chronology.png','v2-station-chronology.png'),('candidate-manifest.json','v2-candidate-manifest.json'),('review.json','v2-review.json'),('early22.5 intended','early20 intended v2'),('late67.5 intended','late70 intended v2')]:source=source.replace(old,new)
exec(compile(source,str(p/'package.py'),'exec'),{'__file__':str(p/'package.py')})
report=p/'v2-review.json';data=json.loads(report.read_bytes());data['packagingBaseSha256']=hashlib.sha256((p/'package.py').read_bytes()).hexdigest();data['packagingVariantSha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();report.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
