from pathlib import Path
from PIL import Image
import hashlib,json,numpy as np,subprocess,os,uuid,time
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'leg-bridge-v20'
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def save(f,d):f.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
inputs=json.loads((out/'inputs.json').read_bytes())
assert all(sha(r/f)==v for f,v in inputs['preCallSha256'].items())
generation=json.loads((out/'generation.json').read_text(encoding='utf-8-sig'));assert generation['terminal']
base=np.array(Image.open(r/inputs['baseFile']).convert('RGBA'));candidate=np.array(Image.open(out/'candidate.png').convert('RGBA'))
mask=np.ones((256,256),bool);mask[140:228,88:166]=False
assert mask.sum()==58672 and np.array_equal(base[mask],candidate[mask])
solid=candidate[:,:,3]>=128;unvisited=set(zip(*np.where(solid)));sizes=[]
while unvisited:
    stack=[unvisited.pop()];n=0
    while stack:
        y,x=stack.pop();n+=1
        for dy,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
            v=(y+dy,x+dx)
            if v in unvisited:unvisited.remove(v);stack.append(v)
    sizes.append(n)
assert len(sizes)==1
review=json.loads((out/'review.json').read_bytes());assert review['rawSha256']==sha(out/'raw.png')
findings=[
    'Raw, native four-source comparison and paired whole/body three-pose boards reviewed.',
    'Lower-body trial provides a narrower near/far knee/shin/boot arrangement toward walk0, without the broad return stance seen in V19. Retained as a provisional lower-body source study.',
    'All standing master upper body/head/hands/case pixels above140 are exact;58672 outside lower-body region exact. One alpha128 connected silhouette.',
    'Upper-body/case/grip difference remains at the walk0 join; this source does not complete a smooth standing-to-walking bridge. Lower material/proportion and foot-contact progression need intermediate poses and motion review.',
    'No per-frame fitting, grading, mirroring, normal runtime adoption, native run or continuous visual acceptance.'
]
review.update(visualReviewPending=False,sourceAcceptance=False,selected=False,
    disposition='retained_provisional_lower_body_study',retainedForFurtherAuthoring=True,
    alpha128Components=len(sizes),alpha128Bounds=Image.fromarray((solid*255).astype('uint8')).getbbox(),findings=findings)
save(out/'review.json',review)
chain=json.loads((out/'chain-review.json').read_bytes());assert all(sha(r/f)==v for f,v in chain['sourceSha256'].items())
chain.update(visualReviewPending=False,reviewedBoards=['chain-whole.png','chain-body.png'],sourceAcceptance=False,selected=False,
    disposition='lower_body_study_only_upper_join_open',normalChanged=False,nativeRun=False,fullGoalComplete=False,findings=findings)
save(out/'chain-review.json',chain)
save(out/'generation-index.json',dict(generations=[dict(tool='builtin_image_gen',prompt='prompt.txt',raw='raw.png',rawSha256=sha(out/'raw.png'),
    terminal=True,disposition=review['disposition'],retainedForFurtherAuthoring=True,normalRuntimeUsed=False)],allTerminalAndCopied=True))
rasters=[f.relative_to(r).as_posix() for f in out.iterdir() if f.suffix=='.png']
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(attrs)==len(rasters)*3+1 and all(x==b'lfs' for x in attrs[2:-1:3])
section='''### James carrying lower-body source study — October 2, 2026

V20 one built-in generated lower-body edit terminal/copied; raw, native donor/
master comparison and paired whole/body source boards reviewed. Retained as a
provisional source study: narrower near/far knee/shin/boot arrangement approaches
walk0 without the V19 return to a broad stance. Original standing upper body,
head, gloves and case above140 exact;58672 outside lower-body pixels exact and
one alpha128 connected silhouette. No original-leg-exact claim, fit, grade or
mirror. Generation raw/prompt/input lineage retained and LFS verified.
The standing master torso/case/grip still changes at the walking endpoint; three
static source poses do not prove a smooth transition. Next establish earlier leg
intermediate and coherent torso/case chronology, then review finite motion and
native joins before adoption. Exact upper-body protection prevents equipment
drift during leg authoring but does not solve upper-body yaw or panel perspective.
V16 full49 walk remains provisional; normal bank/controllers/checkpoints untouched.
No native run or continuous visual acceptance this turn. Full cardinal/master
polish, actual room/equipment/cargo dispatch,interruptions/Continue remain open.
Evidence:character/james-west-carry-walk-keys-v1/leg-bridge-v20/review.json;
prompts:character/james-west-carry-walk-keys-v1/leg-bridge-v20/generation-index.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
    r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    for attempt in range(3):
        old=path.read_bytes();entry=section.encode()
        if entry.split(b'\n',1)[0] in old:break
        if path.name=='CURRENT_STATUS.md':
            at=old.index(b'### James actual-pose carrying bridge rejection');new=old[:at]+entry+b'\n'+old[at:]
        else:new=old+b'\n'+entry
        temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new)
        try:
            assert path.read_bytes()==old;os.replace(temp,path);break
        except PermissionError:
            temp.unlink()
            if attempt==2:raise
            time.sleep(2)
f=p/'HANDOFF.md';old=f.read_text(encoding='utf-8');marker='## V20 isolated lower-body study\n'
if marker not in old:
    at=old.index('## Next action\n')
    old=old[:at]+marker+'''One lower-body edit retained provisionally after raw/native comparison and two
paired boards reviewed. Narrower leg stance approaches walk0; master upper body,
head/gloves/case exact above140,58672 outside region exact,one alpha128 component.
Raw/prompt/frozen inputs stable,all terminal/copied,LFS checked,all five guides
updated. No finite/native/normal adoption. Torso/case/grip walking-endpoint join
still differs. Evidence:leg-bridge-v20/review.json and generation-index.json.
Next:earlier leg intermediate plus coherent upper-body/case transition, then
finite visual motion/native joins; do not infer smoothness from three source poses.

'''+old[at:]
    f.write_text(old,encoding='utf-8')
print(json.dumps(dict(retainedLowerBodyStudies=1,protectedPixels=58672,alpha128Components=1,
    reviewedRawImages=1,reviewedComparisonBoards=3,guides=5,lfsRasters=len(rasters),normalChanged=False,fullGoalComplete=False)))
