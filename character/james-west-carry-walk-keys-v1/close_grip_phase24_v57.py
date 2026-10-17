from pathlib import Path
import json,hashlib,os,uuid,time
p=Path(__file__).resolve().parent;r=p.parents[1];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
spec=[('case-grip-phase24-v56','f93b2105-bf50-4aad-b118-363a204fd760','rejected_brighter_fittings_insufficient_grip_improvement'),('case-grip-material-phase24-v57','7f2451ce-8200-4324-b0f2-2ca46f827d38','retain_local_matte_original_grip_candidate')]
for name,execution,disposition in spec:
    out=p/name;inputs=json.loads((out/'inputs.json').read_bytes())
    for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in inputs[group].items())
    assert sha(out/'prompt.txt')==inputs['promptSha256']
    d=json.loads((out/'review.json').read_bytes());d.update(visualReviewPending=False,reviewedBoards=2,disposition=disposition,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False)
    d['findings']=(['Native contact/whole boards reviewed. Brighter fittings without clear grip improvement; rejected, no native rerun or selection.'] if 'v56' in name else ['Native contact/whole boards reviewed. Original-pose crop as edit target yields subdued hardware and contact closer to original than V52full-body material edit.','63464outside pixels exact to V52preceding candidate, including head/legs; does not certify original-master anatomy outside patch.','Case projected outline/gloves/arm seam still require full motion and neighbour comparisons; retained candidate only. V52sole225vsoriginal226 unresolved.'])
    d['artifactSha256']={f.name:sha(f) for f in out.glob('*.png')};(out/'review.json').write_text(json.dumps(d,indent=2)+'\n')
    (out/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(out/'raw.png'),prompt='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
section='''### James middle carrying grip local material study — October 2, 2026

V56local80square edit targets V52material pose with original stride24grip guide;
contact and paired whole-source boards reviewed, rejected: brighter fittings with
no clear native grip improvement. V57instead uses original V16stride24crop as edit
target, V49entry as matte finish reference and original West master as authority.
Native contact/whole boards reviewed: subdued case hardware and grip closer to
original pose; retained local candidate, not source/motion/normal acceptance.

Full generated square normalized once80; admit only90,118..146,155 into preceding
V52material pair.63464outside pixels exact per gear, head/legs protected, paired
body below110 exact. This protection is relative to V52candidate, not untouched
original master. V52sole225vsoriginal226 and whole-body/case geometry concerns
remain. No hand-painted pixels, bbox fitting, RGB grading, runtime or selection
changes. Exact prompts/precall inputs/terminal raws and rejected source retained.

Lesson: use the correct existing grip as edit target when only material needs
repair; asking a changed full-body source to recover original geometry is weaker.
Inspect local patch joins at native size, distinguish protected candidate pixels
from original-master fidelity, then review adjacent frames and full motion.
Next cross-reference this contact with five staged keys, repair remaining sources
and cadence/context before normal admission; full-set consistency goal incomplete.
Evidence:character/james-west-carry-walk-keys-v1/case-grip-material-phase24-v57/review.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':
        at=old.index('### James West carrying quarter-stride material studies'.encode());new=old[:at]+entry+b'\n'+old[at:]
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
for name,_,_ in spec:(p/name/'HANDOFF.md').write_text('# Project handoff\n\nObjective: full James master-matched library and polish; incomplete.\n\n'+section+'\nChanged: V56/V57local source studies, protected candidate pair/reviews/helpers and five guides. No normal code/art changes, commit/PR/export. Both generations terminal/copied; no live handles.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
print(json.dumps(dict(rejected=56,retainedLocalCandidate=57,outsidePixelsExact=63464,guides=5,normalChanged=False)))
