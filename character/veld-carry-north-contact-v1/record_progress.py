from pathlib import Path
import json,hashlib,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[1]
D=R/'character/veld-carry-north-original-master-v1/motion-review-v1'
counts=[]
for folder in ['veld-carry-north-original-master-v1','veld-north-original-motion-v1']:
    inputs=json.loads((R/'output'/folder/'inputs-before.json').read_text())
    for ref,digest in inputs.items():assert hashlib.sha256((R/ref).read_bytes()).hexdigest()==digest,ref
    counts.append(len(inputs))
e=json.loads((D/'review-evidence.json').read_text());assert e['decodedNativeFramesExact']==180
e['contactConsistency']='failed';e['contactFinding']='Support boots move with body; distance-clock success does not certify world foot planting.'
e['sourceRepair']='character/veld-carry-north-contact-v1; candidates remain unselected'
e['visualReview']={'date':'2026-10-02','distinctSourcePoses':28,'boards':['bare-all-movement-source-poses.png','helmet-all-movement-source-poses.png'],'sizes':[47,93],'finding':'Whole body and shared helmet source registration stable; moving support boot slides. Native continuous contact audit failed.'}
(D/'review-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
note='''## Veld North contact repair studies — October 2, 2026

The original-guided North carry family passes prescribed continuous start/carry/
stop clock and travel checks, but FOOT CONTACT FAILS.180native presentations over
three distance-driven cycles per gear;1093checks0,8.0s.193frozen inputs unchanged;
2931owner non-log files unchanged under scratch APPDATA. Native trace uses actual
sprite distance phase and prescribed speed/position, not VeldNpc/station physics.
Sole-bottom proxy finds12support runs, max9.2world-unit drift (~13.1px at93view).
Existing source puts supporting feet on one relative floor; body travel carries
the grounded boot along. Source joins and clock checks never establish footplant.

character/veld-carry-north-contact-v1 retains builtin twelve-pose candidateV1,
exact prompt/raw/source audit and twelve diagnostic whole-source registrations.
V1 rejected: support LEFT toe218–219 and RIGHT219–221 hardly move through halves;
head ruler22–23 but silhouette142–145 versus original standing148, smaller body.
Do not promote this or change stride to hide slip. BuiltinV2 two-pose support pair
does change LEFT contact198→222 (24native pixels) with registered skull, but falls
short of36target and narrows body58 versus original63; heads22. Moving silhouettes
134/146 are measured, not forced148. V2 is a diagnostic concept, not accepted gait.
Original proportion/material fidelity and coherent swing boot still need correction.
No normal selectors changed, no anatomy strips/RGB edits. Existing source packages
remain frozen. Complete goal active/incomplete; staged gait is not contact accepted.

Lesson: register a moving source to head/body physical ruler, then measure support
contact relative pelvis and world travel. Never force all moving bounding heights
or toe positions to equal standing height/floor. More generated frames alone do
not solve a repeated pose. Establish a convincing planted-foot forward/backward
pair before expanding a loop; dense sampling still needs actual continuous review.
Next whole-source contact pair/cycle, original North turn endpoints, other cardinal
master fidelity, remaining action matrix, normal integration and library polish.

'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    with target.open('rb') as src:
        if src.read(120).startswith(note[:100].encode()):continue
        src.seek(0);before=target.stat();tmp=target.with_name(target.name+'.veld-north-contact-v1.tmp')
        with tmp.open('wb') as dst:dst.write(note.encode());shutil.copyfileobj(src,dst,1024*1024)
    for attempt in range(20):
        now=target.stat();assert(now.st_size,now.st_mtime_ns)==(before.st_size,before.st_mtime_ns),str(target)
        try:os.replace(tmp,target);break
        except PermissionError:
            if attempt==19:raise
            time.sleep(.5)
print(f'Five maintained references updated; frozen catalogues unchanged:{counts}')
