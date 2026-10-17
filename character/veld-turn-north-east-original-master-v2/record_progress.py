from pathlib import Path
import hashlib,json,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-north-east-original-turn-v2';counts=[]
for folder in ['veld-north-east-original-turn-v2','veld-north-gather-original-v1','veld-carry-north-original-master-v1','veld-north-original-motion-v1']:
    inputs=json.loads((R/'output'/folder/'inputs-before.json').read_text())
    for ref,digest in inputs.items():assert hashlib.sha256((R/ref).read_bytes()).hexdigest()==digest,ref
    counts.append(len(inputs))
e=json.loads((P/'native-review-evidence.json').read_text());assert e['validation']['passed'] and e['exactDecodedNativeSamples']==108
e['visualReview']={'date':'2026-10-02','distinctPairedPosesReviewed':12,'nativeSizes':[47,93,148],'boards':['bare-native-source-poses.png','helmet-native-source-poses.png'],'verdict':'staged body study; helmet angular alignment failed','finding':'Broader original-guided North body and plain case; feet together/root registered, exact gathered alias. Original shell material/design reused but later helmet yaw lags bare face; final face opening pops. Source profile/material/East family joins and gathered transition remain open. Native chrono captures retained/decoded, not claimed as natural route acceptance.'}
e['frozenCataloguesUnchanged']=counts;(P/'native-review-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
note='''## Veld original-guided North–East pivot and helmet yaw defect — October 2, 2026

character/veld-turn-north-east-original-master-v2 builds whole body quarter from
reviewed gathered North source plus original East authored reference, without old
narrow body guide. V1 improves rear breadth/progressive turn but invents ornate
case; focusedV2 restores plain case/single latch. Rechecked anatomy/material after
generation. First slot exact gathered source alias both gears; other five new whole
poses at common ruler .20994475. Feet-together pivot registered to lower sole center,
not changing hair/nose bounding center; global first actual-resample floor retained.
Standing extent148–149, angular head bounds23–29; original profile/family polish open.

Paired finite NE/EN800ms original clocks/reverse metadata. Whole original angular
helmet shells/body protection reused. REVIEW FAILURE: helmet later yaw lags bare
face and face opening pops near final slot. Staged body study, not admitted helmet
or whole turn; align actual head yaw before adoption. Exact North gathered alias
does not close wider-held gather movement or new East cargo/action endpoint.

49source/protection/timing/APNGchecks0;565native checks0/108presentations6.91s.
Actual finite sprite player slots/dry metadata/physical128224pivot/standing148,
all slots forward/reversebothgears. All12distinct source poses viewed in two native
boards47/93/148;108actual native samples reconstruct exactly from four APNG holds.
Repeated identical capture holds legitimately merge, not108encoded unique frames.
71inputs stable;2931owner non-log files unchanged under scratchAPPDATA. Previous
53/193/193catalogues stable. No gather motion, gait contact, normal controller/
world, independent case or save acceptance; full goal remains active/incomplete.

Lessons: original material/spec reuse does not prove yaw correspondence to new
body/head chronology. Match equipment to actual pose, not presumed equal angular
steps in two separately authored atlases. Direct source request can invent props;
cross-reference case design and remeasure entire figure after focused prop edit.
Keep frame size/ruler/root and actual-angle view separate from bounding head width.
When native duplicate holds merge during APNG writing, verify expanded duration/
sample equivalence rather than inserting fake unique frames or assuming framecount.

Next whole helmet yaw correspondence/source correction and native chronology,
held-to-gather motion/new East family join/original profile/material check. North
gait contact stillFAILED separately; other cardinal fidelity, remaining actions,
normal integration and full-library consistency/polish remain. HANDOFF.md.

'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    with target.open('rb') as src:
        if src.read(120).startswith(note[:100].encode()):continue
        src.seek(0);before=target.stat();tmp=target.with_name(target.name+'.veld-original-ne-pivot.tmp')
        with tmp.open('wb') as dst:dst.write(note.encode());shutil.copyfileobj(src,dst,1024*1024)
    for attempt in range(20):
        now=target.stat();assert(now.st_size,now.st_mtime_ns)==(before.st_size,before.st_mtime_ns),str(target)
        try:os.replace(tmp,target);break
        except PermissionError:
            if attempt==19:raise
            time.sleep(.5)
print(f'NEbody study/helmet yaw defect recorded;catalogues{counts}unchanged;five maintained references updated.')
