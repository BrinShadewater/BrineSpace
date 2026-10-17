from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];N=R/'output/veld-death-ground-east-candidate-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    verification=json.loads((P/'verification.json').read_text());native=json.loads((N/'validation.json').read_text());log=(N/'native.log').read_text()
    assert verification['passed'] and '70 checks,0 failures' in log and 'ERROR:' not in log and native['returnCode']==0
    manifests={g:json.loads((P/f'{g}-manifest.json').read_text()) for g in ['bare','helmet']}
    files={g:[f+'?v='+sha(P/f)[:12] for f in m['states'][0]['frameFiles']] for g,m in manifests.items()}
    html='''<!doctype html><meta charset="utf-8"><title>Veld east dry collapse — master candidate</title><style>body{background:#202a30;color:#e1e8ed;font:16px sans-serif;margin:24px}a{color:#9bd1ef}.row{display:flex;gap:24px;flex-wrap:wrap}.panel{background:#25323b;padding:16px}.small{width:142px}input{width:300px}img{max-width:100%}</style><h1>Veld — east dry-collapse candidate</h1><p>Exact selected standing entry; one source-calibrated ruler and pooled master material grade. Canonical helmet follows neck and head tilt over the same body. Original1420ms finite clip; playback holds the corpse.</p><p>90 packaging/rebuild checks and70 actual player checks pass. Overall native runner profile guard FAILED: unattributed last_session.json changed. No clean-owner-profile claim for this interval. Scratch paths and all deltas retained. Candidate only; actual mortality/Continue/world behavior, remaining directions and full-set polish are open. Frames4/5 use a generated closed-eyelid patch confined to15native RGBpixels; all shell/visor/collar and alpha stay exact.</p><button id="play">Play once</button> <label>Frame <input id="slot" type="range" min="0" max="5" step="1" value="0"></label> <span id="label"></span><div class="row"><div class="panel"><h2>Selected master</h2><img id="master" width="256"></div><div class="panel"><h2>Bare</h2><img id="bare" width="256"><img id="smallbare" class="small"></div><div class="panel"><h2>Canonical helmet</h2><img id="helmet" width="256"><img id="smallhelmet" class="small"></div></div><p><a href="contact-sheet.png">All poses beside master</a> · <a href="../../output/veld-death-ground-east-candidate-v1/native-contact.png">Native148/82 board</a> · <a href="HANDOFF.md">Scope and next work</a></p><script>const files=FILES;const times=[180,160,180,180,220,500];let token=0;function show(i){document.querySelector('#slot').value=i;for(const g of ['bare','helmet'])for(const id of [g,'small'+g])document.getElementById(id).src=files[g][i];document.getElementById('label').textContent='Frame '+i+' / 5';}document.getElementById('master').src=files.bare[0];document.querySelector('#slot').oninput=e=>{token++;show(+e.target.value)};document.querySelector('#play').onclick=()=>{const current=++token;const start=performance.now();function tick(now){if(current!==token)return;let t=now-start,i=0;while(i<5&&t>=times[i]){t-=times[i];i++}show(i);if(now-start<1420)requestAnimationFrame(tick);}requestAnimationFrame(tick)};show(0);</script>'''.replace('FILES',json.dumps(files))
    (P/'index.html').write_text(html,encoding='utf-8')
    handoff='''# Project handoff

Updated:2026-10-01 · Project:BrineSpace · Task:Veld east closed-eyelid dry-collapse revision

## Objective and acceptance
Complete matching Veld animations, then whole-set consistency and motion polish. East dry death is now a paired candidate; normal selection remains unchanged.

## Accepted decisions and constraints
Exact selected bare/canonical-helmet idle entry, dry256plane/p128,224/H148, original1420ms timing, finite frame5. One148/494=.299595 isotropic source ruler for all interiors; natural lowering and physical boot/knee/forearm floor contacts. Pooled face/hair/science/neutral curves from the selected east idle. No opposite-view mirror or per-pose height normalization.

## Current state
Original exec-341162b9-d481-49a5-bb1f-c39735c3245c retained with exact prompt/reference binding. build.py exports12frames/2manifests/grade/contact registration/preview; canonical native head35x39 follows source neck and tilt, unchanged body outside local equipment region. Generated exec-3873a1fe-c231-4fb0-bc95-64cd2c548f92 supplies only a5x3eyelid RGBpatch in native region[24,17,29,20], applied before rotating frames4/5. Shell/visor/collar, face outline, every pose alpha, all bare and helmet0..3pixels remain exact. Original open-eye revision retained in revisions/open-eye-v1. verify.py, native test/UID, isolated runner and finite master comparison added. No production loader/registry mutation for this candidate.

## Verification
90 packaging/master/source/pixel/floor/metadata/native-head/expression/exact14file rebuild checks PASS.70 actual player checks pass with clean engine: exact loaded pixels, dry ruler/camera, original finite timing, arbitrary-clock entrance, in-memory player snapshot, negative phase clamp and held corpse. Native148/82 paired board reviewed after repairing its clipped fourth row. Overall runner FAILED profile guard: last_session.json changed; writer attribution unproven; all2,924 real non-log files fingerprinted, deltas/previous parse-error and clipped-board intervals retained. No unchanged-profile claim. Bare crowns76/91/129/162/179/185: final6px authored settlement retained for pacing review, not forced equal.

## Next action
Continue head/collar/foreground hand contact, pitch pacing, material and small-detail review in full-speed playback. Independent west raw6pose source exec-4ec1eb84-d058-4b02-8ba1-c9875c8d4bdf is saved; its atom badge must match the boxed master mark before fixed-ruler fitting/grade/helmet/native proof. Other dry directions and rest/life coverage, then actual mortality/live entrance/restore/furnished occlusion proof and complete cross-animation polish. Full goal active; no blocker/commit/export.
'''
    (P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
    heading='## Veld east dry-collapse closed-eye revision — October 1, 2026'
    note=f'''\n\n{heading}

Original6pose built-in source fitted into12bare/canonical-helmet frames. Exact selected east idle entries; one148/494=.299595 ruler, dry256plane/p128,224/H148, original1420ms finite terminal. Pooled head/face/science/neutral master curves, native35x39helmet follows source neck/tilt; paired body exact outside local head region.90 packaging/rebuild and70 actual-player checks pass, native148/82 reviewed. Overall runner FAILED profile guard: unattributed last_session.json changed;2,924 real non-log files fingerprinted/deltas retained, no clean-profile claim. Candidate only; no normal selection or mortality/Continue/world proof. Generated closed eyelid is restricted to15native RGBpixels and helmet frames4/5; canonical shell/visor/collar/face outline and all alpha remain exact. Earlier helmet and all bare pixels unchanged. Original open-eye revision archived.

Lesson: dry falls require floor-contact registration and a fixed anatomical ruler, not constant crown height. Source crown progression76/91/129/162/179/185 includes6px terminal settlement; retain authored geometry and review pacing instead of manufacturing equal-height passes. Include every native review row in viewport bounds; a successful save_png does not prove a whole-figure capture. Exact canonical shell/color does not certify a correct terminal expression. Author the semantic face change separately and bind its tiny compositing window; do not replace the wearable to fix an eyelid. Independent west raw6pose source saved; its atom badge differs from the boxed master mark and needs repair before fitting. Color grading cannot restore that missing symbol construction. Concurrent real-game PID371472 observed; its699s breadcrumb age differs from the6.9s fixture, consistent with the retained telemetry delta. No retrospective clean-profile claim. Other dry directions/rest/life/full-set matching and full cross-animation polish remain. Handoff:character/veld-death-ground-east-coherent-v1/HANDOFF.md. Full goal active.
'''
    for rel in ['docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
        p=R/rel
        if heading.encode() not in p.read_bytes():
            with p.open('ab') as f:f.write(note.encode())
    p=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
    if heading.encode() not in p.read_bytes():
        with p.open('ab') as f:f.write(note.encode())
    p=R/'docs/CURRENT_STATUS.md'
    if heading.encode() not in p.read_bytes():p.write_bytes((note.strip()+'\n\n').encode()+p.read_bytes())
    bound={}
    paths=[*P.glob('*.py'),P/'HANDOFF.md',P/'index.html',P/'contact-sheet.png',P/'verification.json',P/'registration.json',P/'material-grade.json',P/'frame-hashes.json',P/'sources/death-v1.png',P/'sources/prompt-v1.txt',P/'sources/reference-binding.json',P/'sources/canonical-head.png',P/'sources/canonical-head-closed.png',P/'sources/expression/closed-v1.png',P/'sources/expression/prompt-v1.txt',P/'sources/expression/closed-eye-native-comparison.png',R/'tests/test_veld_death_ground_east_candidate.gd',R/'tests/test_veld_death_ground_east_candidate.gd.uid',R/'tools/run_veld_death_ground_east_candidate.py',R/'tests/index.json']
    for g,m in manifests.items():paths.append(P/f'{g}-manifest.json');paths.extend(P/f for f in m['states'][0]['frameFiles'])
    paths.extend(N/f for f in ['native.log','validation.json','profile-before.json','profile-after.json','native-contact.png'])
    for p in paths:bound[p.relative_to(R).as_posix()]=sha(p)
    (P/'candidate-evidence.json').write_text(json.dumps({'candidateArtChecksPassed':True,'overallNativeRunnerPassed':native['passed'],'normalSelection':False,'nativeReport':native,'packagingChecks':verification['checks'],'playerChecks':70,'sha256':bound,'remaining':['all other dry directions','mortality/Continue/world proof','rest/life/full set','cross-family material/anatomy/detail/motion polish']},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'boundFiles':len(bound),'packaging':verification['checks'],'player':70,'runnerPassed':native['passed'],'normalSelection':False}))
if __name__=='__main__':main()
