"""Validate raster contracts, seams, hashes, and deterministic rebuild."""
from pathlib import Path
import hashlib,json,subprocess,sys
import numpy as np
from PIL import Image
root=Path(__file__).resolve().parent
manifest=json.loads((root/'manifest.json').read_text())
checks=0
def expect(value,label):
    global checks
    checks+=1
    assert value,label
before={p['path']:p['sha256'] for p in manifest['files']}
for entry in manifest['files']:
    path=root/entry['path'];im=Image.open(path).convert('RGBA');a=np.array(im)
    expect(list(im.size)==entry['dimensions'],entry['path']+' size')
    expect(hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256'],entry['path']+' hash')
    expect(entry['fps']==0,entry['path']+' static')
    if entry.get('seamless'):
        expect(np.array_equal(a[0],a[-1]),'vertical seam')
        expect(np.array_equal(a[:,0],a[:,-1]),'horizontal seam')
    else:
        expect(np.max(a[0,:,3])==0 and np.max(a[-1,:,3])==0,'transparent horizontal boundary')
        expect(np.max(a[:,0,3])==0 and np.max(a[:,-1,3])==0,'transparent vertical boundary')
subprocess.run([sys.executable,str(root/'bake.py')],check=True)
after=json.loads((root/'manifest.json').read_text())
expect(before=={p['path']:p['sha256'] for p in after['files']},'reproducible bake')
print('LIGHTING PACK:',checks,'checks, 0 failures')
