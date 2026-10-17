from pathlib import Path
import json,hashlib,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-north-gather-original-v1';report=json.loads((O/'validation.json').read_text());assert report['passed'];counts=[]
for folder in ['veld-north-gather-original-v1','veld-carry-north-original-master-v1','veld-north-original-motion-v1']:
    inputs=json.loads((R/'output'/folder/'inputs-before.json').read_text())
    for ref,digest in inputs.items():assert hashlib.sha256((R/ref).read_bytes()).hexdigest()==digest,ref
    counts.append(len(inputs))
(P/'visual-review.json').write_text(json.dumps({'date':'2026-10-02','reviewed':['gather-master-comparison-v2.png','output/veld-north-gather-original-v1/bare-000-native.png','output/veld-north-gather-original-v1/helmet-000-native.png'],'sizes':[47,93,148],'verdict':'staged source foundation reviewed; animation incomplete','finding':'Head22/upper62/standing148/boot224 close to original held22/61/148/224. Boots37combined gathered, original source boot breadth restored from undersizedV1. Matte material close, slight quilt/pattern differences remain. Whole shared shell stable. No gather/turn chronology or gait acceptance.','native':report,'frozenCataloguesUnchanged':counts},indent=2)+'\n')
note='''## Veld North original-master gathered source — October 2, 2026

character/veld-turn-north-east-original-master-v1 now retains a reviewed paired
gathered North SOURCE FOUNDATION for feet-together pivots. RawturnV1 rejected:
old guide dominated anatomy, rear body53/head20 versus held61/22. Direct whole
master edit gatherV1 preserves torso but boots31combined too narrow; focusedV2
restores boots37, head22/body62/H148/boot224, cloth median81versus originalheld78.
Same camera/connected anatomy/matte detail close at actual size; quilt/pattern
polish remains. Raw/prompts/rejections/provenance preserved. No RGB grading or
limb strips. Whole original34x36North shell at112,68, protected body outside head.

4package checks0;33native checks0/6presentations/5.21s. Actual sprite player held/
gathered comparison both gears47/93/148; both full native boards visually reviewed.
53frozen inputs stable;2931owner non-log files unchanged under scratch APPDATA.
Earlier193/193North family/motion catalogues also stable. SOURCE POSE ONLY, no
gather animation, turn chronology/angles, natural gait/contact, controller/world,
case lifetime/save acceptance or normal selectors. Full goal active/incomplete.

Lesson: an old pose guide can override canonical anatomy even with explicit master
instructions. Use direct whole-master stance edit, check physical head/torso AND
individual boot breadth; feet-together must not mean smaller boots. Register global
floor from actual isolated/resampled source ruler, not rounded raw bounding point;
the latter was2px off. One common turn ruler retained, never per-pose floor fitting.
Current held stance is wider than requested pivot stance: author gather movement
before the pivot, do not snap endpoints or distort the whole library to one stance.
Keep frozen source audits unchanged after native review; dated verdict is separate.

Next original-faithful gather interiors and angular turn source from new gathered
foundation; original East face/hair/material, shared helmet yaw, native chronology.
North gait contact stillFAILED separately. Other cardinal master fidelity, remaining
actions, normal integration and cross-library polish remain. HANDOFF.md records scope.

'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    with target.open('rb') as src:
        if src.read(120).startswith(note[:100].encode()):continue
        src.seek(0);before=target.stat();tmp=target.with_name(target.name+'.veld-original-gather.tmp')
        with tmp.open('wb') as dst:dst.write(note.encode());shutil.copyfileobj(src,dst,1024*1024)
    for attempt in range(20):
        now=target.stat();assert(now.st_size,now.st_mtime_ns)==(before.st_size,before.st_mtime_ns),str(target)
        try:os.replace(tmp,target);break
        except PermissionError:
            if attempt==19:raise
            time.sleep(.5)
print(f'Gathered source review/handoff recorded; frozen catalogues{counts}stable;five maintained references updated.')
