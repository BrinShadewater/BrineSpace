"""Transfer only the newly authored third source pose; preserve the other five."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    original=P/'sources/death-v1.png';edited=P/'sources/death-kneel-v2.png'
    a=np.array(Image.open(original).convert('RGBA'));b=np.array(Image.open(edited).convert('RGBA'));assert a.shape==b.shape==(1024,1536,4)
    box=[1024,0,1536,620];out=a.copy();out[0:620,1024:1536]=b[0:620,1024:1536]
    protected=np.ones(a.shape[:2],bool);protected[0:620,1024:1536]=False;assert np.array_equal(out[protected],a[protected])
    target=P/'sources/death-local-kneel-v2.png';Image.fromarray(out).save(target)
    data={'generation':'exec-1d90414f-2d02-4966-8b6b-f2780709d8a5','originalSha256':sha(original),'generatedSha256':sha(edited),'outputSha256':sha(target),'cell':box,'otherFivePosesExact':True,'scope':'third authored kneel replaces raised palms with ground brace; alpha/anatomy intentionally changes only in this cell'}
    (P/'sources/kneel-transfer.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({'otherFivePosesExact':True,'cell':box}))
if __name__=='__main__':main()
