from pathlib import Path
import hashlib,json,os,shutil,time
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-north-gather-boot-master-v1';counts=[]
for folder in ['veld-north-gather-boot-master-v1','veld-north-east-helmet-aligned-v3','veld-north-east-helmet-aligned-v2','veld-north-east-helmet-aligned-v1','veld-north-east-original-turn-v2','veld-north-gather-original-v1','veld-carry-north-original-master-v1','veld-north-original-motion-v1']:
    refs=json.loads((R/'output'/folder/'inputs-before.json').read_text())
    for ref,digest in refs.items():assert hashlib.sha256((R/ref).read_bytes()).hexdigest()==digest,ref
    counts.append(len(refs))
report=json.loads((O/'validation.json').read_text());assert report['passed']
audit=json.loads((P/'corrected-gather-audit-v5.json').read_text());original,old,current=audit['rows'];assert [f['width'] for f in current['feet']]==[22,23]
assert current['height']==148 and current['upperBodyWidth']==61
for gear in ['bare','helmet']:
    Image.open(O/f'{gear}-000-native.png').save(P/f'{gear}-native-master-review.png')
review={'date':'2026-10-02','verdict':'boot-corrected whole source foundation, paired native poses reviewed; transition motion incomplete','nativeSizes':[47,93,148],'boards':['bare-native-master-review.png','helmet-native-master-review.png'],'sourceMeasurements':current,'previousGatheredBootWidths':[19,19],'originalBootWidths':[22,23],'motionDraft':'Rejected: planted left-foot center moves113.5to118before its intended lift, torso58-59vs61; boots shrink and cloth brightens. No selected gather sequence.','validation':report,'frozenCataloguesUnchanged':counts}
(P/'visual-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
with (P/'EXECUTIONS.md').open('a',encoding='utf-8') as f:f.write('''
- ebb8d200-d578-4e1e-a1c8-a09e7104a666: raw-corrected-gather-v5.png, prompt-corrected-gather-v5.txt. Whole v2 breadth target plus unchanged original cloth detail reference ONLY. Selected SOURCE FOUNDATION: boots22/23, torso61/head23/H148/sole224, neutral cloth quartiles63/77.33/87 versus original61/78/92.67. No deterministic body RGB edits. Paired whole original rear shell; transition not authored/accepted.
''')
(P/'HANDOFF.md').write_text('''# Veld original boot-breadth gathered foundation

Updated: October 2, 2026 · Project: BrineSpace

## Objective and acceptance
Full Veld animation set faithful to original identity/style/camera/physical size,
height/proportions/grade; continually maintain pipeline/skills/bible, then broad
cross-library consistency/polish. Current work is held-to-gather stance movement.

## Accepted decisions and constraints
Whole builtin art sources; preserve physical boot size while closing space. No
anatomical strips, body RGB grading, per-pose scale/floor fitting or normal adoption.
Keep old source/native evidence frozen and isolate owner profile for Godot work.

## Current state
Homologous toe/sole audit finds original held boots22/23px, prior gathered19/19 at
same148 ruler. Combined span alone hid the footwear shrinking. New v5 whole source
restores22/23, torso61/head23/H148/sole224. Neutral upper-leg quartiles63/77.33/87
vs original61/78/92.67: matte cloth close, original head22 vs new23 remains1px
contour/detail polish. Same direct North/back camera, connected body and hardware.
Four interior v1 source poses retained DIAGNOSTIC ONLY: first planted LEFT sole
center moves113.5to118 before left lift; torso58-59 vs61; boots shrink, cloth bright.
Endpoint v1 stillsmall boots; v2 breadth correct but cloth88, v3 dark65/v4bright92.
v5 direct original cloth crop reference recovers material without output RGB edits.
Raw/prompts/EXECUTIONS, inspect_interiors/inspect_endpoint and source review boards
retained. Paired v5 gather-frames/manifests and package_endpoint, protected body
under whole original rear34x36helmet shell. Source pose only, no motion adoption.
tests/test_veld_north_gather_boot_master_v1.gd and UID; tools isolated runner;
output/veld-north-gather-boot-master-v1. Previous turns retain old narrower endpoint.

## Verification
4source/protection/clipping checks0;33native checks0/6presentations5.05s.
Both bare/helmet full boards47/93/148 visually reviewed; actual source/root metadata.
59frozen inputs unchanged;2931owner non-log files unchanged scratchAPPDATA.
Prior32/30/41/71/53/193/193catalogues unchanged. No native motion/contact acceptance,
normal controller/world/case/save or owner acceptance. Full goal active/incomplete.

## Next action
Author four whole transition interiors from exact original held and NEW v5 gathered
source, not old narrower endpoint. Keep LEFT planted at113.5 through RIGHT inward
step, then RIGHT planted139 while LEFT gathers toward116.5. Recheck sole/contact,
individual boot breadth, torso/head/material at common ruler before native sequence.
Rebase staged North turn entrance onto corrected gather endpoint only after joins
reviewed. Failed North gait contact, new East family joins, other cardinal fidelity,
remaining actions, normal integration and full-library polish remain.
''',encoding='utf-8')
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Veld gathered stance</title><style>body{background:#182229;color:#e5e9e8;font:18px system-ui;max-width:1100px;margin:30px auto;padding:20px}p{line-height:1.5}img{display:block;max-width:100%;height:auto}details{margin:25px 0}</style><h1>Veld gathered stance</h1><p>Feet together now retain the original boot size. The suit finish also follows the original matte cloth more closely. Original held pose above, corrected gathered pose below, at three game sizes.</p><p>This is the corrected destination pose. The movement between the poses is still being authored.</p><h2>Bare head</h2><img src="bare-native-master-review.png" alt="Original held and corrected gathered bare poses"><h2>Helmet</h2><img src="helmet-native-master-review.png" alt="Original held and corrected gathered helmet poses"><details><summary>Boot comparison with the previous gathered pose</summary><img src="corrected-gather-master-review-v5.png" alt="Original, previous and corrected boot proportions"></details></html>'''
(P/'index.html').write_text(html,encoding='utf-8')
note='''## Veld original boot-breadth gathered foundation — October 2, 2026

character/veld-gather-north-original-master-v1 reaudits held-to-gather endpoints:
original held toe/sole widths22/23px; earlier gathered19/19at same148 body ruler.
Closing the combined stance had hidden smaller individual boots. New whole builtin
v5 gathered source restores22/23, torso61/head23/H148/sole224. Neutral upper-leg
quartiles63/77.33/87 vs original61/78/92.67; matte original cloth closely retained.
Original head22 vs new23 remains1px contour/detail polish, not blanket identity pass.
No output RGB/body strips/per-pose scale edits. Paired original rear34x36shell with
protected body, raw/prompts/provenance/rejections/audits and native boards preserved.

4package checks0;33native checks0/6captures5.05s;59inputs frozen stable;2931owner
non-log files unchanged scratchAPPDATA. Both full native boards47/93/148 reviewed.
Prior32/30/41/71/53/193/193catalogues unchanged. Corrected SOURCE FOUNDATION only:
four new interior poses remain rejected diagnostic because first planted LEFT foot
moves113.5to118before its lift, torso58-59vs61, boots shrink and cloth brightens.
Current staged turns still reference the previous narrower gathered entry; rebase
after genuine transition/join review. No natural gait/controller/world/save proof.

Lessons: audit individual footwear breadth separately from total stance span and
head/torso dimensions. Common full-cell registration retains true authored shifts;
separate per-frame centering would conceal misplaced support feet. Generation
can follow small-foot endpoint guide and carry anatomy drift through intermediates.
Fix canonical endpoints before authoring motion. Requested percentage colour edits
are not predictable: inspected v2cloth88→v3dark65→v4bright92, not proportional to
prompt. Unchanged original cloth-detail reference recovered v5median77.33 vs78.
Material crop is reference only, never output anatomy; preserve full-source review.

Next genuine RIGHT inward/LEFT inward whole gather interiors at fixed original
support contacts/boot breadth/body/material, finite reverse and actual motion/join
review. Then corrected North turn entrance/new East family, failed North ground
contacts, remaining full-set actions/integration and broad consistency/polish.
Full goal active/incomplete. Latest HANDOFF.md/EXECUTIONS.md retain evidence.

'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    with target.open('rb') as src:
        if src.read(120).startswith(note[:100].encode()):continue
        src.seek(0);before=target.stat();tmp=target.with_name(target.name+'.veld-gather-boot-foundation.tmp')
        with tmp.open('wb') as dst:dst.write(note.encode());shutil.copyfileobj(src,dst,1024*1024)
    for attempt in range(20):
        now=target.stat();assert(now.st_size,now.st_mtime_ns)==(before.st_size,before.st_mtime_ns),str(target)
        try:os.replace(tmp,target);break
        except PermissionError:
            if attempt==19:raise
            time.sleep(.5)
print(f'Boot-corrected foundation recorded;catalogues{counts}stable;five maintained references updated.')
