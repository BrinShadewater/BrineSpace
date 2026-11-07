from pathlib import Path
import hashlib,json,subprocess,sys
from PIL import Image
root=Path(__file__).resolve().parent
m=json.loads((root/'manifest.json').read_text());before={e['path']:e['sha256'] for e in m['files']}
checks=0
for e in m['files']:
    p=root/e['path'];im=Image.open(p)
    assert list(im.size)==e['dimensions'];checks+=1
    assert im.mode=='RGBA';checks+=1
    assert hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256'];checks+=1
    assert im.getchannel('A').getextrema()[0]==0;checks+=1
    if e.get('tintable'):
        r,g,b,a=im.split();assert r.tobytes()==g.tobytes()==b.tobytes();checks+=1
subprocess.run([sys.executable,str(root/'bake.py')],check=True)
after={e['path']:e['sha256'] for e in json.loads((root/'manifest.json').read_text())['files']}
assert before==after;checks+=1
print('CARD PACK:',checks,'checks, 0 failures')
