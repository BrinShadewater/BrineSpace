from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def bounds(a):
    ys, xs = np.where(a)
    return [int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)] if len(xs) else None
def panel(board, im, xy, scale=1):
    im = im.resize((im.width*scale, im.height*scale), Image.Resampling.NEAREST)
    board.paste(im, xy, im)

records = []
for key in ['bare-ready','helmet-ready','bare-rise','helmet-rise']:
    available = []
    for receipt in sorted(OUT.glob(f'generation-provenance-{key}-v*.json')):
        q = json.loads(receipt.read_text(encoding='utf-8'))
        assert sha(Path(q['savedPath']))==q['sha256']==sha(Path(q['originalPath']))
        assert sha(Path(q['promptFile']))==q['promptSha256']==q['submittedPromptSha256']
        for ref in q['references']: assert sha(Path(ref['path']))==ref['sha256']
        if not q.get('rejected'): available.append(q)
    if not available: continue
    p = max(available,key=lambda q:q['revision'])
    assert p['status']=='completed'
    assert sha(Path(p['promptFile']))==p['promptSha256']==p['submittedPromptSha256']
    assert sha(Path(p['sourcePath']))==p['sourceSha256']
    for ref in p['references']: assert sha(Path(ref['path']))==ref['sha256']
    raw = Path(p['savedPath'])
    assert sha(raw)==p['sha256']==sha(Path(p['originalPath']))
    im = Image.open(raw).convert('RGBA')
    assert im.width==im.height, (key,im.size)
    # Reverse only the documented square-canvas enlargement and bottom padding.
    candidate = im.resize((352,352), Image.Resampling.LANCZOS).crop((0,0,352,320))
    candidate.save(OUT/f'{key}-candidate.png')
    old = Image.open(p['sourcePath']).convert('RGBA')
    gait = Image.open(OUT/f'sources/{key}-actual-gait-reference-4x.png').convert('RGBA').resize((352,352),Image.Resampling.NEAREST).crop((0,0,352,320))
    aa=np.asarray(old)[:,:,3]>127; bb=np.asarray(candidate)[:,:,3]>127
    rec={'key':key,'revision':p['revision'],'rawSize':list(im.size),'uniformScale':352/im.width,'translation':[0,0],
         'crop':[0,0,352,320],'alphaIoU':float((aa&bb).sum()/(aa|bb).sum()),
         'oldBounds':bounds(aa),'candidateBounds':bounds(bb),'windows':{},'nativeAcceptance':False,'normalAdmission':False}
    rec['belowCollarIoU']=float((aa[125:]&bb[125:]).sum()/(aa[125:]|bb[125:]).sum())
    for name,box in [('headCollar',(125,55,195,125)),('hands',(110,105,190,175)),('boots',(120,185,215,240))]:
        x,y,r,b=box
        rec['windows'][name]={'box':list(box),'oldBounds':bounds(aa[y:b,x:r]),'candidateBounds':bounds(bb[y:b,x:r])}
    board=Image.new('RGB',(1500,760),(31,35,40)); d=ImageDraw.Draw(board)
    for n,(label,source) in enumerate([('Original water pose',old),('Revised candidate',candidate),('Actual adjacent gait '+str(p['actualGaitPhase']),gait)]):
        x=20+n*380; d.text((x,15),key+' | '+label,fill='white');panel(board,source,(x,45))
        d.text((x,375),'Fixed head/collar window x4',fill='white');panel(board,source.crop((125,55,195,125)),(x,400),4)
    base=json.loads((OUT/f'generation-job-{key}-v1.json').read_text(encoding='utf-8'))
    assert sha(Path(base['references'][2]['path']))==base['references'][2]['sha256']
    master=Image.open(base['references'][2]['path']).convert('RGBA')
    master=master.resize((int(master.width*148/956),int(master.height*148/956)),Image.Resampling.LANCZOS)
    d.text((1170,15),'Original West master | H148 ruler',fill='white');panel(board,master,(1230,65),2)
    d.text((20,720),'Whole canvases share H148 calibration. Fixed windows are diagnostics; no head/part fitting. Source candidate only.',fill='white')
    board.save(OUT/f'{key}-review.png');records.append(rec)
(OUT/'review.json').write_text(json.dumps({'poses':records,'fullVisualAcceptance':False,'normalAdmission':False},indent=2)+'\n',encoding='utf-8')
print(json.dumps(records))
