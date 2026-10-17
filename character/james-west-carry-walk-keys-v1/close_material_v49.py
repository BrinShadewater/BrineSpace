from pathlib import Path
import json,hashlib,os,uuid,time
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'master-material-v49'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((out/'package-review.json').read_bytes())
d.update(visualReviewPending=False,reviewedBoards=['native-material-comparison.png','enlarged-material-comparison.png','paired-protected-review.png'],disposition='retain_head_protected_representative_for_motion_expansion',sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,guardedHeadRows=104,protectedBarePixels=26624,helmetCap=[102,62,155,110],pairedBodyBelow110Exact=True,findings=['Material materially closer to original neutral/warm charcoal master, with subdued seams and dull silver hardware.','Whole raw changes face/crown by1px; unguarded source not acceptable. Original target top104rows restored exactly; established helmet cap reused.','One fixed walking-entry pose only. Sole exclusive row223 remains target223 versus standing master224; no per-pose height fitting.','Case geometry/interior suit detail and entire gait/pickup connection still require review. No continuous motion, runtime or full-set acceptance.'])
d['artifactSha256']={f.name:sha(f) for f in out.glob('*.png')}
(out/'package-review.json').write_text(json.dumps(d,indent=2)+'\n')
(out/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='8a887481-a865-45f1-9796-1ed666ede565',source='C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-8a887481-a865-45f1-9796-1ed666ede565.png',rawSha256=sha(out/'raw.png'),promptFile='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
section='''### James West representative carrying material repair — October 2, 2026

V49 builtin material edit uses V16walking-entry as target, registered original West
master as material/identity reference and provisional local3case as supporting
design reference. Exact prompt/input hashes and terminal raw retained. Full1254
square normalized once to256, no bbox fitting or RGB grading. Native and enlarged
four-source comparisons plus paired protected-source board actually reviewed.
Matte charcoal fabric and subdued seams/hardware are closer to original master.

Whole output changed face/crown; unguarded source is not admitted. Preserve exact
target top104rows (26624pixels), then reuse established helmet cap102,62..155,110;
paired bodies below110 exact. Source remains a representative expansion candidate,
not final acceptance or normal selection. Target/candidate sole exclusive223 vs
standing master224 retained without fitting. Original source head/material evidence
does not certify case/body geometry, all gait interiors, runtime or continuous motion.

Lesson: material-only edits can change identity. Separate raw evaluation from
protected-source composition, review both at native size, and compare authored
fabric against actual original master before expanding an entire family. V48normal
pickup/walk endpoint remains exact; new body must reconcile with that predecessor.
Next distributed walking material repairs, native motion/joins and full-set polish.
Evidence:character/james-west-carry-walk-keys-v1/master-material-v49/package-review.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':
        at=old.index('### James actual pickup-to-carry source join checked'.encode());new=old[:at]+entry+b'\n'+old[at:]
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
(out/'HANDOFF.md').write_text('# Project handoff\n\nObjective: full James master-matched library and polish; incomplete.\n\n'+section+'\nChanged: V49raw/prompt/references/protected pair/review/helpers and five guides. Existing normal artwork/controller unchanged. No commit/PR/export. Generation terminal/copied; no active job.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
print(json.dumps(dict(reviewedBoards=3,protectedBarePixels=26624,guides=5,normalChanged=False,fullGoalComplete=False)))
