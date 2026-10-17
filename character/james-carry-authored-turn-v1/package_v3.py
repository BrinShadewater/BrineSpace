from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
source=(p/'package.py').read_text(encoding='utf-8')
source=source.replace("for name in ['early','late']:","for name in ['early-v3','late-v2']:").replace('(r/k).read_bytes()','(p/k).read_bytes()')
for old,new in [('early-pose.png','early-v3-pose.png'),('late-pose.png','late-v2-pose.png'),("p/'frames'","p/'frames-v3'"),('whole-chronology.png','v3-whole-chronology.png'),('upper-chronology.png','v3-upper-chronology.png'),('legs-chronology.png','v3-legs-chronology.png'),('station-preview.apng','v3-station-preview.apng'),('station-chronology.png','v3-station-chronology.png'),('candidate-manifest.json','v3-candidate-manifest.json'),('review.json','v3-review.json'),('early22.5 intended','early20 intended v3'),('late67.5 intended','late70 intended v2')]:source=source.replace(old,new)
exec(compile(source,str(p/'package.py'),'exec'),{'__file__':str(p/'package.py')})
report=p/'v3-review.json';data=json.loads(report.read_bytes());data['packagingBaseSha256']=hashlib.sha256((p/'package.py').read_bytes()).hexdigest();data['packagingVariantSha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();report.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
