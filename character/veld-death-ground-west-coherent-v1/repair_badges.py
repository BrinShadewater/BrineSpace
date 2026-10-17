"""Extract generated insignia edits; preserve original pose alpha and other RGB."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
BOXES=[[268,179,306,220],[717,219,758,269],[1216,336,1254,378],[176,780,219,827],[629,776,679,826],[1143,804,1190,851]]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    source=P/'sources/death-v1.png';edit=P/'sources/death-badge-v2.png'
    a=np.array(Image.open(source).convert('RGBA'));b=np.array(Image.open(edit).convert('RGBA'))
    assert a.shape==b.shape==(1024,1536,4)
    mask=np.zeros(a.shape[:2],bool);records=[]
    for box in BOXES:
        x0,y0,x1,y1=box
        av=a[y0:y1,x0:x1,:3].astype(float);bv=b[y0:y1,x0:x1,:3].astype(float)
        blue=lambda v:(v[:,:,2]>1.15*v[:,:,0])&(v[:,:,2]>1.02*v[:,:,1])
        m=(blue(av)|blue(bv))&(a[y0:y1,x0:x1,3]>200)
        mask[y0:y1,x0:x1]=m
        records.append({'box':box,'extractedPixels':int(m.sum())})
        assert m.sum()>150
    out=a.copy();out[mask,:3]=b[mask,:3]
    assert np.array_equal(out[:,:,3],a[:,:,3])
    assert np.array_equal(out[~mask],a[~mask])
    assert np.any(out[mask,:3]!=a[mask,:3])
    target=P/'sources/death-badge-local-v2.png';Image.fromarray(out).save(target)
    Image.fromarray((mask*255).astype('uint8')).save(P/'sources/badge-transfer-mask.png')
    data={'generation':'exec-a539ba56-a4db-42db-a98c-43679f7cb84a','originalSha256':sha(source),'generatedSha256':sha(edit),'outputSha256':sha(target),'alphaExact':True,'outsideBadgePixelsExact':True,'badgeRegions':records,'scope':'six authored insignia regions only; anatomy/material fitting and runtime remain unproven'}
    (P/'sources/badge-transfer.json').write_text(json.dumps(data,indent=2)+'\n')
    board=Image.new('RGB',(1536,400),'#202a30')
    for i,box in enumerate(BOXES):
        for row,im in enumerate([Image.fromarray(a),Image.fromarray(out)]):
            crop=im.crop(box);crop.thumbnail((160,160));crop=crop.resize((crop.width*4,crop.height*4),Image.Resampling.NEAREST)
            board.paste(crop,(i*256,row*200),crop)
    board.save(P/'sources/badge-comparison.png')
    print(json.dumps({'alphaExact':True,'outsideBadgePixelsExact':True,'badgePixels':int(mask.sum()),'regions':6}))
if __name__=='__main__':main()
