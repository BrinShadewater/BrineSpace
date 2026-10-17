from pathlib import Path
import json,hashlib,uuid,os
P=Path(__file__).resolve().parent;R=P.parents[1]
frozen=json.loads((P/'east-turn-join-inputs.json').read_bytes())
changed=[p for p,h in frozen.items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
assert not changed,changed
review=json.loads((P/'east-turn-join-review.json').read_bytes());assert review['slots']==92
record={'selected':False,'visualReview':{'slots':92,'boards':16,'reviewedAllBoards':True,'scope':review['scope'],'finding':'East bare head proportion differs from staged smaller head at carry/turn joins; current helmet shell remains coherent in reviewed source poses.'},'generation':{'source':'turn-head-generated-v1.png','providerSource':'C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-279198d6-d91f-4e12-a08a-d2c239b6796b.png','size':[1536,1024],'alphaExtrema':[0,254],'alphaZeroPixels':950461,'accepted':False,'reason':'Visible halo around head/collar and oversized goggles. Upper suit is also redrawn; raw sheet cannot replace whole bodies. No bounded source extraction or native admission performed.'},'hashes':{name:hashlib.sha256((P/name).read_bytes()).hexdigest() for name in ['turn-head-target.png','turn-head-masters.png','turn-head-revised-anchor.png','turn-head-prompt.txt','turn-head-layout.json','turn-head-generated-v1.png']},'frozenTurnInputs':len(frozen),'changedTurnInputs':changed,'nativeTaskAcceptance':False,'fullGoalComplete':False}
(P/'east-turn-visual-findings.json').write_text(json.dumps(record,indent=2))
section='''## James East-connected cargo turn source review — October 2, 2026

Current ordered catalog/loader resolves six East-connected dry carrying turns in
both gears,92source slots across16registered master/carry/turn/head boards; all
reviewed. East/West half turns are included alongside East/North and East/South
quarter turns and their returns. Current14side banks retain recorded selection.
Bare East and near-East turn heads still differ from staged smaller cargo head;
family admission remains open. Helmet shell remains coherent in reviewed poses.
Source review does not establish continuous motion or actual task/Continue joins.

Six distinct head closeups, three directional master references, revised East
anchor and exact prompt retained. Built-in1536x1024 transparent result retained
as turn-head-generated-v1.png, UNSELECTED: visible surrounding halo and oversized
goggles need correction; generated upper suit redraw cannot replace original
bodies. No extraction, native test, normal loader or raster selection change.
All frozen turn inputs unchanged after review. No owner profile or gameplay run.

Lesson: head repair must reconcile quarter turns, half turns, reverse aliases and
directional gaze before selection. A transparent request can still return a visible
halo; inspect source background and goggles at native source scale. Do not accept
a generation from cell count or alpha presence alone. Keep raw source/prompt and
record its quality failure before trying another source or bounded extraction.
Next master-matched turn head sources without halo/oversized goggles, shared-pose
repair, then paired native joins and actual task/Continue. Full James goal remains
active/incomplete; West hand-edge cleanup and cross-family context/polish remain.
'''
def atomic(path,data):
    before=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(data);assert path.read_bytes()==before;os.replace(tmp,path)
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    before=path.read_bytes();assert section.splitlines()[0].encode() not in before
    atomic(path,section.encode()+b'\n'+before if path.name=='CURRENT_STATUS.md' else before+b'\n\n'+section.encode())
path=P/'HEAD_CANDIDATE_HANDOFF.md';atomic(path,path.read_bytes()+b'\n\n'+section.encode())
print(json.dumps({'reviewedSourceSlots':92,'reviewedBoards':16,'frozenInputs':len(frozen),'changedInputs':0,'generationSelected':False,'guidesUpdated':5}))
