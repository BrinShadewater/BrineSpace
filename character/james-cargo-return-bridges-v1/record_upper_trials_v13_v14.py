from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
def atomic(path,old,new):
    assert path.read_bytes()==old
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(temp,path)
audit=json.loads((p/'selected-join-audit-v9/audit.json').read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in audit['inputs'].items())
verdicts={
    'v13':'Rejected: generated upper-body crown151 against outgoing148/incoming149. Head raised, badge enlarged/redesigned, face material/identity drift. Whole lower body exact does not justify admitting upper-body anatomy drift.',
    'v14':'Rejected: numerical crown148 agrees with outgoing reference, but face shifts/changes and badge emblem/shape and shoulder breadth drift. Correct crown alone does not establish identity, scale, articulation or material continuity.'}
for version in ['v13','v14']:
    guard=json.loads((p/('package-upper-'+version+'-validation.json')).read_bytes())
    assert guard['exitCode']==0 and guard['realProfileUnchanged'] and not guard['timedOut']
    package=json.loads((p/('upper-'+version+'-package.json')).read_bytes())
    assert package['protectedOriginalPixels']==61476 and package['translation']==[0,0] and package['grade']=='none'
    assert (p/('package-upper-'+version+'.gd.uid')).exists()
    path=p/('upper-'+version+'-source-review.json');old=path.read_bytes();review=json.loads(old)
    assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in review['inputSha256'].items())
    review.update(visualReviewPending=False,selected=False,verdict=verdicts[version],nativeActorMotionRun=False,
        reviewed='Generated raw, four registered full-body source presentations and four enlarged upper-body crops inspected. Source fidelity fails before actor-motion admission; current selected normal V9 unchanged.')
    atomic(path,old,(json.dumps(review,indent=2)+'\n').encode())
verdict={'selected':False,'preferredNormalSelectionChanged':False,'method':'Built-in image_gen edits, two separate calls; native Godot uniform256/1254scale, original registration, no grade/translation; generated upper104/64/58/70 region admitted for source trial only.',
    'trials':verdicts,'normalSelectedSourceHashesUnchanged':True,'nativeActorMotionRun':False,
    'protectedOriginalPixelsEach':61476,'sourceReviewScope':'Eight full-body comparisons/eight upper-body crops plus both raw outputs; not paired helmet/full motion/master acceptance.',
    'prompts':['upper-body-intermediate-v13-prompt.txt','upper-body-intermediate-v14-prompt.txt'],
    'raw':['upper-body-intermediate-v13-raw.png','upper-body-intermediate-v14-raw.png']}
(p/'upper-v13-v14-verdict.json').write_text(json.dumps(verdict,indent=2)+'\n')
section='''### James coherent upper-body trials V13/V14 — October 2, 2026

Two separate built-in image_gen edits preserve exact prompts and1254square raws.
First requests halfway head/collar/shoulder orientation between selected neighbor
poses; second adds explicit crown75/76, chin/badge position and emblem constraints.
Native Godot uniform256/1254 scale, no translation/grade, upper104/64/58/70 region;
61476original pixels outside it exact per trial, including lower body/case/feet.
Both package intervals engine0/scratch APPDATA/owner profile unchanged; paired UIDs.
Raws/eight full-body comparisons/eight enlarged crops inspected; sources FAIL.

V13 crown distance151 against outgoing148/incoming149; raises head and changes
badge/face. V14 crown148 matches outgoing but face position/features and shoulder
badge emblem/shape/breadth drift. Both rejected, original normal V9 paired sources
hash-exact unchanged. No helmet counterpart, actor-motion run or new admission.
Do not spend full native-motion validation on a source already failing identity.

Lesson: numeric crown constraints can fix crown drift while anatomy/emblem still
fail. An enlarged raw or protected lower-body pixels is not fidelity proof; compare
registered face, shoulder breadth, emblem and matte grade against BOTH neighbors
before paired motion. Keep coherent upper articulation scope, original physical
registration/endpoints and canonical identity; do not force a whole-body height
normalization or hide redesigned insignia behind a passing pixel-count report.
Next source repair must resolve intermediate upper articulation with face/badge
identity intact, then matched helmet and full native return/Continue validation.
Full directional/master/context/cross-family goal active/incomplete.
Evidence: character/james-cargo-return-bridges-v1/upper-v13-v14-verdict.json,
upper-v13-source-review.json, upper-v14-source-review.json and exact prompt files.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        marker=b'### James selected West join isolated';at=old.index(marker)
        new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,old,new)
path=r/'character/james-floor-case-west-v1/HANDOFF.md';old=path.read_bytes()
addition=b'\nV13/V14 coherent upper-body raw/prompt/package/source reviews retained; both\nrejected. V13 raises crown3px from outgoing; V14 crown agrees but face/badge\nidentity drifts.61476lower/outside pixels exact each, normal V9 source hashes\nunchanged. No actor-motion run for failing sources. Next preserve face/badge\nidentity through coherent intermediate upper articulation, then paired helmet.\nVerdict: character/james-cargo-return-bridges-v1/upper-v13-v14-verdict.json.\n'
if b'V13/V14 coherent upper-body raw/prompt' not in old:atomic(path,old,old+addition)
print('Both source failures recorded in five guides/handoff; preferred normal sources unchanged; no full-goal completion claimed.')
