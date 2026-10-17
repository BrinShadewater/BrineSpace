from pathlib import Path
import hashlib,json
from PIL import Image
P=Path(__file__).resolve().parent
source=P/'raw-far-swing-v20.png';box=(535,455,845,710)
Image.open(source).crop(box).save(P/'case-surface-edit-target.png')
(P/'case-surface-edit-target.json').write_text(json.dumps({'source':source.name,'sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'crop':box,'role':'Exact source crop for localized generated equipment-material edit; no pose guide or independent anatomy.'},indent=2)+'\n',encoding='utf-8')
source=P/'raw-passing-v16.png';box=(615,468,930,728)
Image.open(source).crop(box).save(P/'case-passing-edit-target.png')
(P/'case-passing-edit-target.json').write_text(json.dumps({'source':source.name,'sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'crop':box,'role':'Exact passing-source case crop; preserve anatomy.'},indent=2)+'\n',encoding='utf-8')
