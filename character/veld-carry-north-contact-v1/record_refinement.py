from pathlib import Path
import hashlib,json,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[1];V=R/'character/veld-carry-north-contact-video-v1'
review=json.loads((V/'raw-review/review.json').read_text());assert review['frameCount']==141 and len(review['boards'])==6
review['visualReview']={'date':'2026-10-02','framesReviewed':141,'boardsReviewed':review['boards'],'verdict':'rejected','finding':'Awkward crossing/merging legs and unclear support contacts; visible colour flash81–82. Stable head width does not certify anatomy or footplant. No source segment selected.'}
(V/'raw-review/review.json').write_text(json.dumps(review,indent=2)+'\n')
assert hashlib.sha256((V/'master-input.png').read_bytes()).hexdigest()==json.loads((V/'generation.json').read_text())['imageSha256']
counts=[]
for folder in ['veld-carry-north-original-master-v1','veld-north-original-motion-v1']:
    inputs=json.loads((R/'output'/folder/'inputs-before.json').read_text())
    for ref,digest in inputs.items():assert hashlib.sha256((R/ref).read_bytes()).hexdigest()==digest,ref
    counts.append(len(inputs))
note='''## Veld North contact refinements and continuous source rejection — October 2, 2026

Whole-source contactV3 improves upper-body width62–63 but support span regresses
24→13px and neutral upper-leg median65.7–67.7 is darker than original-held77.
V4 widens too far65–66/hips46–48, support span19, median86.7–88.3 too light.
Both rejected; exact builtin prompts/raw/registered whole figures retained in
character/veld-carry-north-contact-v1. PreviousV2median75–76 was already close;
compare corresponding held action landmarks (upper width61/hips42), not total
resting silhouette63 that includes straight arms/gloves. No candidate installed.

One authorized direct HailuoFast2.3/768P6s whole-motion study from unchanged first
original-guided held source completed task448304417616434; estimatedUS$0.19, actual
billing unknown. character/veld-carry-north-contact-video-v1 retains frozen input,
prompt, source, receipt and all141frames/six chronology boards. All141frames viewed;
REJECTED before loop/extraction/native: feet cross/merge, support contacts unclear,
colour flash81–82. Head width84–88 mostly stable versus initial86; moving height
584–639alone does not establish scale drift. No normal selectors/controller changes.
Two earlier193/193frozen source catalogues still byte-identical; owner preservation
2931belongs to prior scratch-native interval, no new Godot/profile run this turn.

Lessons: colour diagnostics can show an apparently light reference already matches
the master; avoid speculative darkening. Compare homologous regions under the
same action/physical ruler. A successful request does not preserve stated geometry
or material; measure every refinement again. After equivalent source failures,
change authoring strategy, retain all-frame verdict, and avoid uncontrolled retries.
Continuous source can preserve identity yet fail contact/grade. Never hide a colour
flash or half-stride by cherry-picking a convenient loop. FFmpeg fps_mode passthrough
replaces removed-vsync option; decode actual frames without padding/interpolation.

Next faithful whole-source support extrema and full alternating gait/contact review;
original North turn endpoints, other cardinal fidelity, remaining actions, normal
integration and cross-library polish remain. Full goal active/incomplete. Handoffs
in both contact study folders; previous technical clock pass never footplant pass.

'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    with target.open('rb') as src:
        if src.read(120).startswith(note[:100].encode()):continue
        src.seek(0);before=target.stat();tmp=target.with_name(target.name+'.veld-north-contact-refinement.tmp')
        with tmp.open('wb') as dst:dst.write(note.encode());shutil.copyfileobj(src,dst,1024*1024)
    for attempt in range(20):
        now=target.stat();assert(now.st_size,now.st_mtime_ns)==(before.st_size,before.st_mtime_ns),str(target)
        try:os.replace(tmp,target);break
        except PermissionError:
            if attempt==19:raise
            time.sleep(.5)
print(f'All141raw-frame rejection recorded;five references updated;frozen catalogues{counts}unchanged.')
