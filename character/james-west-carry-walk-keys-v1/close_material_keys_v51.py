from pathlib import Path
import json,hashlib,subprocess,os,uuid,time
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1];v50=p/'master-material-keys-v50';v51=p/'master-material-phase12-v51'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for out,execution in [(v50,'13b55b6f-502e-4732-88f4-751b1ead8fd3'),(v51,'4207f445-70c4-4053-923f-249aead94131')]:
    inputs=json.loads((out/'inputs.json').read_bytes())
    for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in inputs[group].items())
    assert sha(out/'prompt.txt')==inputs['promptSha256']
    (out/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(out/'raw.png'),promptFile='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
d=json.loads((v50/'review.json').read_bytes());d.update(visualReviewPending=False,reviewedBoards=3,findings=['All9sprites enlarged from roughly147..150 to190..194opaque pixels and shifted crown from76 to30..54.','Material improvement cannot justify anatomy/registration drift; rejected without per-cell fitting or runtime testing.']);(v50/'review.json').write_text(json.dumps(d,indent=2)+'\n')
d=json.loads((v51/'package-review.json').read_bytes());d.update(visualReviewPending=False,reviewedBoards=3,disposition='retain_head_protected_stride_representative',sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,protectedHeadRows=104,pairedBodyBelow110Exact=True,findings=['Single stride material closer to original master and V49entry, with restrained seams/hardware.','Raw crown75 versus target76; preserve exact targettop104rows and established helmetcap.','Target sole225 retained; candidate horizontal bounds shift1px. Whole-case contour/interior proportions and full gait still require review.','Only stages0/12 repaired; not full49source motion/runtime acceptance.']);(v51/'package-review.json').write_text(json.dumps(d,indent=2)+'\n')
board=Image.new('RGBA',(768,560),(47,58,63,255));draw=ImageDraw.Draw(board)
for row,mode in enumerate(['bare','helmet']):
    for col,(label,f) in enumerate([('repaired entry',p/'master-material-v49'/(mode+'-head-protected.png')),('repaired stride12',v51/(mode+'-head-protected.png')),('original master',r/'character/james-west-master-carry-v1/registered-original-master.png')]):
        board.alpha_composite(Image.open(f).convert('RGBA'),(col*256,row*280+24));draw.text((col*256+5,row*280+5),mode+' '+label,fill='white')
board.save(v51/'paired-key-consistency.png')
section='''### James West carrying distributed material trial — October 2, 2026

V50nine-key3x3material atlas rejected. All three native review boards inspected:
poses0/6/12/18/24/30/36/42/48 enlarged from147..150 to190..194opaque pixels,
crown shifted from76 to30..54. Full1254square normalization to768 retained the
drift; no per-cell fitting, head rescue, runtime testing or adoption warranted.
Material improvement never justifies altered physical scale or source registration.

V51individual stride12 builtin edit uses actual stride target, original master
material reference and protected V49entry finish. Terminal raw/prompt/input hashes
retained. Three native/enlarged/paired review boards inspected. Better matte fabric,
subdued silver and seams. Raw crown shifts1px; restore exact target top104rows and
established helmet cap. Paired body below110 exact, target sole225 retained, whole
horizontal bounds shift1px. Retained representative; source/case/body geometry and
full gait acceptance remain open. V49entry/V51stride0/12 do not cover all49sources.

Lesson: multi-pose edits can preserve chronology while losing grid scale/margins.
Check actual cell crown/sole bounds against input before accepting any atlas.
Reject resized anatomy rather than fit it away. Individual material edits have
better registration here; continue existing full-family repair scope, cross-reference
normal pickup/carry and original masters, then native motion and full-set polish.
Five maintained guides updated; no normal artwork/controller changes.
Evidence:character/james-west-carry-walk-keys-v1/master-material-phase12-v51/package-review.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':
        at=old.index('### James West representative carrying material repair'.encode());new=old[:at]+entry+b'\n'+old[at:]
    else:new=old+b'\n'+entry
    tmp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    try:
        for attempt in range(5):
            assert f.read_bytes()==old
            try:os.replace(tmp,f);break
            except PermissionError:
                if attempt==4:raise
                time.sleep(1)
    finally:
        if tmp.exists():tmp.unlink()
for out in [v50,v51]:(out/'HANDOFF.md').write_text('# Project handoff\n\nObjective: full James master-matched set and polish; incomplete.\n\n'+section+'\nChanged: V50/V51source studies, packaging/review and five guides. Native gameplay unchanged; no commit/PR/export. Generations terminal/copied; no active handles.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in [v50,v51] for f in folder.glob('*.png')]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0');assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(dict(atlasRejected=True,strideRepresentative=12,guides=5,lfsRasters=len(rasters),normalChanged=False)))
