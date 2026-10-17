from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
for name in ['middle-inputs.json','guided-middle-inputs.json']:
    inventory=json.loads((p/name).read_bytes())
    assert all(hashlib.sha256((p/k).read_bytes()).hexdigest()==v for k,v in inventory['preCallSha256'].items()),name
    if 'source' in inventory:assert hashlib.sha256((r/inventory['source']).read_bytes()).hexdigest()==inventory['sourceSha256']
for name,finding in [
 ('middle-review.json','Raw1254alpha and all whole/upper/original/station boards reviewed. Numeric halfway-angle prompt returns near-terminal orientation, larger shoulder patch and one-native-pixel crown rise; transition still switches at row2->3. REJECTED before gear/native admission.'),
 ('guided-middle-review.json','Existing SouthWest4 common80 crop used as pose target, actual outgoing as material/identity reference. Raw1254alpha and all whole/upper/original/station boards reviewed. Crown76 at all six rows, but broader face/head, enlarged goggles and badge reinterpretation remain; row2->3 family switch not resolved. REJECTED. Matching crown does not prove head proportions or master identity.')]:
    path=p/name;review=json.loads(path.read_bytes());review.update(visualReviewPending=False,selected=False,sourceAcceptance=False,finding=finding)
    atomic(path,(json.dumps(review,indent=2)+'\n').encode())
path=p/'endpoint-identity-review.json';identity=json.loads(path.read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in identity['inputSha256'].items())
identity.update(visualReviewPending=False,finding='All four registered whole/upper comparisons reviewed. Current selected idleWest is crew-runtime-matte-v1/branforth/frames/idle-west-breathing-v1/000.png, H148/pivot92,172 translated36,52 with no scale/face fitting. Static comparison exposes head/face/goggle/shoulder differences between selected standing, actual turn and actual cargo families; guided new middle broadens head further. Inference: this is not solely an absent yaw in-between. Selected standing is a current reference, not independent proof of original portrait-master acceptance.',next='Reconcile West endpoint-family identity/proportions with authoritative accepted masters before more interpolated poses; original endpoint protection was a trial constraint, not permission to preserve off-master identity. Prepare versioned source revision without normal admission until source/motion checks pass.')
atomic(path,(json.dumps(identity,indent=2)+'\n').encode())
section='''### James West middle-pose failures expose endpoint-family consistency work — October 2, 2026

Two new built-in transparent middle trials retained with exact prompts/hashes:
middle exec-e6dcf486-f427-4d2e-b155-afddaf12764e edits actual outgoing upper target
toward halfway input orientation; guided-middle exec-6cd838df-6a98-4b35-bb7d-63e791a1f1da
uses existing SouthWest4 crop as concrete pose target/outgoing material reference.
Both1254square wholecanvas->80 at original96/56, no per-pose fit or Python grade.
Only V9rows3/4 changed; original0/1/2/5 exact,61476outside pixels exact each edited
row. Six APNG RGB/80ms holds checked for each trial. Raw/full/upper/original and
82/54/27station-size boards inspected. Numeric angle returns near-final pose and
one-pixel crown rise; concrete guide retains crown76all6 but broadens face/head,
enlarges goggles and reinterprets badge. Both bridge trials REJECTED before helmet,
native or normal selection. No live generation, owner profile access or export.

New actual normal literal-loader West idle audit resolves selected
crew-runtime-matte-v1/branforth/frames/idle-west-breathing-v1/000.png,
H148/pivot92,172 translated36,52 to common256/p128224 only. Grid/manifests/selected
source and endpoints frozen/unchanged. Four whole/four enlarged upper comparisons
inspected: selected standing, actual turn endpoint, actual cargo endpoint, guided
trial differ in head/face/goggle/shoulder presentation. Inference: missing yaw
alone does not explain the family switch. Selected standing reference is NOT
independent original portrait-master acceptance; verify that lineage next.

Change of approach: reconcile West endpoint-family identity/proportions against
the authoritative accepted masters, then author matching connecting motion.
Do not keep unsuccessful original endpoints solely to satisfy a local byte
protection test, or repeat nominal degree prompts/retiming. Original endpoints
remain protected in THESE retained trials, not a universal owner constraint.
Same crown/H148 metadata does not certify head scale. Upscaling a final native
crop adds no detail; inspect preserved higher-resolution lineage before new art.
Any eventual admitted bank changes require revised strict source/checkpoint
bindings and fresh native evidence; prior green checks cannot transfer.

Normal cap/V9/riseV6/caseV7 unchanged. Goal active/incomplete; full action/cardinal/
context and cross-family master polish required. Five guides updated. Evidence:
character/james-west-upper-video-v1/{middle,guided-middle,endpoint-identity}-review.json
and HANDOFF.md. No blocking condition.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James upper-crop video, matte/alpha and late-angle source review');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,new)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West family consistency

## Objective and acceptance
Full James set matching accepted masters/style/perspective/size/height/proportions/
matte grade, then cross-family polish. Goal active/incomplete.

## Accepted decisions and constraints
Normal helmet-cap/V9/riseV6/caseV7 still selected. Temporary original-endpoint
protection is a trial constraint; do not preserve an off-master family solely for
compatibility. Source admissions require versioned strict bindings/fresh evidence.

## Current state
Here terminal upper video/raw142review, rejected grade/alpha bridge and retained
late terminal-side reference. New middle-raw.png/middle-prompt.txt and
guided-middle-raw.png/guided-middle-prompt.txt, two separate six-pose source trials,
actual selected West standing/endpoints comparison. Both middle trials rejected.
Five guides updated; no live job/native/profile/normal bank/commit/export write.

## Verification
Both1254alpha raws/full/upper/original/station boards inspected; twelve decoded
APNG RGB/80ms checks. Original rows0/1/2/5 exact,61476outside pixels per changed
row exact; no per-pose fitting/grade. Numeric middle crown76/76/76/75/76/76;
guided76all6 but broader face/goggles/badge drift. Three review records closed.
Current loader resolves idleWest crew-runtime-matte-v1/branforth; H148/p92,172
common256translation36,52, no scaling. Four whole/upper views inspected; normal
grid/manifests/source inventories stable. Static selected reference, not original
portrait-master lineage or continuous/native motion acceptance.

## Next action
Reconcile West endpoint-family head/face/equipment proportions against accepted
master lineage and preserved high-resolution sources before more transition art.
The source families differ beyond nominal yaw; crown equality is insufficient.
Actual West cargo source lineage begins james-cargo-west-v1/source-pose-guide-v2.png
and build.py; final unload0 aliases carry0. Do not run old builders over installed
banks; inspect sources/registration only. Then coherent revised endpoint/near-join
source family, paired equipment and native lifecycle/ordinary-turn evidence before
versioned normal admission. Other directions/contexts/full cross-family polish open.

Built-in middle generation exec-e6dcf486-f427-4d2e-b155-afddaf12764e;
guided exec-6cd838df-6a98-4b35-bb7d-63e791a1f1da. Saved raw/prompt paths above.
Prior grade/alpha/late prompt/raw lineage retained in separate review records.
''',encoding='utf-8')
print('Two middle source trials rejected; actual selected endpoint identity audit reviewed; hashes stable; five guides/handoff updated. Next master-family reconciliation.')
