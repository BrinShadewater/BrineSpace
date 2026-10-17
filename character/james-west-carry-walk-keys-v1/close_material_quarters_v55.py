from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,os,uuid,time,subprocess
p=Path(__file__).resolve().parent;r=p.parents[1];review=p/'material-quarter-review-v54'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
new=[(24,52,'e935c9a1-faf6-4ab0-9e9e-9fdc7ca3fee9'),(36,53,'9d2a4e3a-18bb-4517-ba1a-1f3831f65340'),(48,55,'cef7b672-fc26-44ff-99de-12b0ca3327f1')]
for phase,version,execution in new:
    out=p/f'master-material-phase{phase}-v{version}';inputs=json.loads((out/'inputs.json').read_bytes())
    for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in inputs[group].items())
    assert sha(out/'prompt.txt')==inputs['promptSha256']
    original=np.asarray(Image.open(p/'master-head-review-v16'/f'bare-{phase:03d}.png').convert('RGBA'))
    bare=np.asarray(Image.open(out/'bare-head-protected.png').convert('RGBA'));helmet=np.asarray(Image.open(out/'helmet-head-protected.png').convert('RGBA'))
    assert np.array_equal(bare[:104],original[:104]) and np.array_equal(bare[110:],helmet[110:])
    d=json.loads((out/'package-review.json').read_bytes());d.update(visualReviewPending=False,reviewedBoards=3,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,disposition='material_direction_retained_geometry_polish_required',protectedHeadRows=104,pairedBodyBelow110Exact=True,findings=['Muted matte suit/hardware closer to original and repaired entry; no full visual acceptance.','Whole source edit changes internal case/body details and small silhouette regions. Restored head/cap alone does not prove anatomy/gear/grip fidelity.','Phase24 sole exclusive225 versus input226; phase36/48 sole223 retained. No per-pose fitting used.','Sparse source study, not completed49-frame motion or normal runtime admission.']);d['artifactSha256']={f.name:sha(f) for f in out.glob('*.png')};(out/'package-review.json').write_text(json.dumps(d,indent=2)+'\n')
    (out/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(out/'raw.png'),promptFile='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
sources=[(0,p/'master-material-v49'),(12,p/'master-material-phase12-v51')]+[(phase,p/f'master-material-phase{phase}-v{version}') for phase,version,_ in new]
board=Image.new('RGBA',(1536,560),(47,58,63,255));draw=ImageDraw.Draw(board);records=[]
for row,mode in enumerate(['bare','helmet']):
    for col,(phase,folder) in enumerate(sources):
        f=folder/(mode+'-head-protected.png');im=Image.open(f).convert('RGBA');board.alpha_composite(im,(col*256,row*280+24));draw.text((col*256+5,row*280+5),mode+' phase'+str(phase),fill='white');records.append(dict(phase=phase,mode=mode,file=f.relative_to(r).as_posix(),sha256=sha(f)))
    board.alpha_composite(Image.open(r/'character/james-west-master-carry-v1/registered-original-master.png').convert('RGBA'),(1280,row*280+24));draw.text((1285,row*280+5),'original bare master',fill='white')
board.save(review/'paired-five-key-review.png')
(review/'five-key-inputs.json').write_text(json.dumps(dict(sourceRecords=records,normalChanged=False,fullGoalComplete=False,scope='Five sparse phase sources per gear, not full49 source coverage or continuous motion.'),indent=2)+'\n')
section='''### James West carrying quarter-stride material studies — October 2, 2026

V52phase24, V53phase36 and V55phase48 builtin single-source material edits copied
with exact prompts/precall input hashes. Each full1254square normalized once256,
without bbox fitting or RGB grading. All nine native/enlarged/paired source boards
reviewed, plus V54four-key consistency board. Top104bare rows restored exactly,
established helmet cap reused, paired body below110 exact. Original master checked.
Finish closer to subdued matte suit/hardware; retained material-direction studies,
not full source acceptance. Case/body interiors and tool/grip geometry still change.

V54body silhouette diagnostic below110: alpha128IoU93.3..94.1percent over phases
0/12/24/36,219..311changedmask pixels per pose. Metrics do not certify anatomy or
internal gear fidelity. Phase24sole225 vs original226; phase36/48sole223 retained.
Five sparse phases0/12/24/36/48 per gear are not all49walking sources. No mixed old/
new runtime bank installed, no cadence/continuous motion or normal selection claim.

Lesson: keeping head and pivot is insufficient for material-only acceptance.
Cross-reference body silhouettes AND internal case grip/tools/proportions against
the actual predecessor and original master. Keep finish improvement separate from
geometry acceptance. Next tighter fabric/contact repairs where geometry changed,
remaining gait poses, complete motion/context review and full-set consistency polish.
Evidence:character/james-west-carry-walk-keys-v1/material-quarter-review-v54/five-key-inputs.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':
        at=old.index('### James West carrying distributed material trial'.encode());data=old[:at]+entry+b'\n'+old[at:]
    else:data=old+b'\n'+entry
    tmp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(data)
    try:
        for attempt in range(5):
            assert f.read_bytes()==old
            try:os.replace(tmp,f);break
            except PermissionError:
                if attempt==4:raise
                time.sleep(1)
    finally:
        if tmp.exists():tmp.unlink()
for out in [review]+[p/f'master-material-phase{phase}-v{version}' for phase,version,_ in new]:
    (out/'HANDOFF.md').write_text('# Project handoff\n\nObjective: full James master-matched library then polish; incomplete.\n\n'+section+'\nChanged: source studies, protected pairs, deterministic packing/review helpers and five guides. No normal art/runtime changes or commit/PR/export. Generations terminal/copied; no active handles.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in [review]+[p/f'master-material-phase{phase}-v{version}' for phase,version,_ in new] for f in folder.glob('*.png')]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0');assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(dict(newPairedSourceStudies=3,reviewedSourceBoards=9,guides=5,lfsRasters=len(rasters),normalChanged=False)))
