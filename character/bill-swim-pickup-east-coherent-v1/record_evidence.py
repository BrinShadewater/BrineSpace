from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
out=ROOT/'output/bill-pickup-east-candidate-native-v1'
paths=[out/'validation.json',out/'native.log',ROOT/'tests/test_bill_pickup_east_candidates.gd']
for folder in [P,P.parent/'bill-swim-pickup-helmet-east-coherent-v1']:
 m=json.loads((folder/'manifest.json').read_text(encoding='utf-8'));paths.append(folder/'manifest.json');paths.extend(folder/f for f in m['states'][0]['frameFiles'])
(P/'native-evidence.json').write_text(json.dumps({'passed':json.loads((out/'validation.json').read_text(encoding='utf-8'))['passed'],'files':{p.relative_to(ROOT).as_posix():sha(p) for p in paths},'scope':'explicit candidate injection;82 native checks;not runtime promotion or arbitrary loop-exit proof'},indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(1024,512),(29,43,51));d=ImageDraw.Draw(board)
for row,gear in enumerate(['bare','helmet']):
 work='bill-salvage-east-coherent-v1' if gear=='bare' else 'bill-salvage-helmet-east-coherent-v1'
 pick=P if gear=='bare' else P.parent/'bill-swim-pickup-helmet-east-coherent-v1'
 for col,(folder,file,text) in enumerate([(P.parent/work,'frames/salvage-east/003.png','Nominal work exit: pose3'),(pick,'frames/swim-pickup-east/000.png','Stored pickup start: pose0'),(pick,'frames/swim-pickup-east/004.png','Last authored interior'),(pick,'frames/swim-pickup-east/005.png','Exact selected cargo')]):
  im=Image.open(folder/file).convert('RGBA');board.paste(im,(col*256,row*256),im);d.text((col*256+6,row*256+12),text,fill='white');d.text((col*256+6,row*256+32),gear,fill='white')
board.save(P/'boundary-audit.png')
