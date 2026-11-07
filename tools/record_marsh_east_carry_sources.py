"""Record four whole East carry sources, rejected halves and the next correction."""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-carry-material-v1';S=BASE/'sources'
MARKER='## Marsh East carry source corrections and opposite stance — October 2, 2026'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    for name in ['carry-01','half-02','contact-03','contact-04']:
        r=json.loads((S/(name+'.request.json')).read_text());assert sha(S/(name+'.prompt.txt'))==r['promptSha256'] and sha(S/(name+'.raw.png'))==r['rawSha256']
        for q in r['orderedReferences']+r['sourceFrames']+r.get('guideToolDependencies',[]):assert sha(ROOT/q['path'])==q['sha256']
    pending=json.loads((S/'passing-05.request.json').read_text());assert pending['status']=='frozen before generation; not started' and sha(S/'passing-05.prompt.txt')==pending['promptSha256']
    for q in pending['orderedReferences']+pending['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
    diagnostics=[]
    for name in ['contact-03-unselected','contact-04-unselected']:
        f=Image.open(BASE/name/'far-contact.png').convert('RGBA');left=f.crop((0,150,85,184)).getbbox();right=f.crop((100,150,184,184)).getbbox();diagnostics.append({'source':name,'rearLeftLowerROI':[0,150,85,184],'frontRightLowerROI':[100,150,184,184],'rearAlphaBottom':150+left[3],'frontAlphaBottom':150+right[3]})
    assessment={'normalAdmission':False,'fullGoalComplete':False,'allFourRawSourcesInspected':True,'allFourPackedComparisonsInspected':True,'findings':'Source01 repeats near-leading/support in both halves. Half02 still repeats near support and changes crate front projection. Contact03 literal opposite thigh geometry succeeds but front far boot angled/projected above rear and crate differs. Contact04 keeps opposite thighs and flattens front boot; requested five-row clearance and original crate panel restoration not reached. No coherent complete cycle accepted.','bootDiagnostics':diagnostics,'limits':'Read-only lower-boot alpha envelopes only, not anatomical sole/physical contact certification. No Godot/native/full-save/Continue acceptance in this milestone.','next':'Generate frozen far-passing05 from contact04, then regenerate/review near half for consistent body/crate projection before cycle assembly/native validation; West carry and turns/held joins/full-set polish remain.'}
    (BASE/'source-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
    lesson=f'''
{MARKER}

Full Marsh master/style/camera/size/height/proportion/grade goal remains active and
incomplete. East carry sources are UNSELECTED. No normal catalog change, accepted
complete East carry cycle, Godot/native/full-save/Title Continue proof in this
milestone. Prior South/North carry523 checks each remain dated staged evidence
for those own sources only. Normal catalog77/228/1190 is coverage, not acceptance.

Selected East32x147 side idle is PRIMARY for adult body/small head/elevated camera/
quiet warm grade. Own original East master preserves visible temple implant,
swept blond hair, collar/chest plate/harness and authentic ankle buckles. Eight
unchanged selected guide frames/metadata/SHAs plus original master inspected.
Opposite walking guide uses whole walk0/walk3, no mirror or limb editing. Old
cargo guide provides crate/support/motion only; its body and crate projection vary.

Source01 exec-3a8c9230-d3ae-4fe6-b221-ab3ee9bcec81 uses selected idle first,
opposite two-stance guide second,old carry third,original master fourth. Five
complete figures,one neutral147 BOX scale .2727272727272727:82x144/65x145/
76x145/67x145,ruler38x147. All four still repeat near-leading/support. Slate crate
and hand support consistent within sheet; neutral profile broader than selected.
Candidate01 manifest retains184,p92/172,H148,four180ms and explicit carry stride
.0827027027027027, but is not an accepted alternating cycle. Four decoded APNG
frames pixel-exact; illustrative holds do not certify correct phases or motion.

Half02 exec-2557b186-1649-4014-be99-f397cd83811a places a single opposite stance
first, selected idle PRIMARY second, whole near-cargo figure third, original master
fourth. Three complete cells,one neutral147 scale .19367588932806323:88x147,
78x147,ruler36x148 (actual sample versus target147 recorded). Both requested far
poses remain near-leading/support; crate now shows a broader double-latch front
projection instead of source01 side view. Retained far-half-02-rejected, never
assembled as correct far phases. Numeric labels/ruler size are not phase proof.

Contact03 exec-1661ff9f-b710-4f30-ae90-3b6dc30c659a omits the conflicting whole
near-cargo reference. Literal geometric wording preserves LIGHT FOREGROUND thigh
downLEFT/back and DARKER FAR thigh downRIGHT/forward with correct occlusion.
Two complete cells,one neutral147 scale .1701388888888889:far contact77x144,
ruler34x147. This changes authoritative evidence: opposite leg identity finally
visible. Front far boot remains angled/projected above rear; crate has a broad
single-latch inset panel rather than source01 rounded divided side. Not a coherent
mixed cycle. Whole raw/packed/ruler comparison inspected; body/head/grade closer
to fitted master, supporting foot and cargo joins provisional.

Contact04 exec-ca634adf-5b2b-497b-a4c5-55523e79cbe1 uses complete contact03
first as whole edit guide,selected idle PRIMARY second,own original third. Two
complete cells,one neutral147 scale .17562724014336917:82x146,ruler37x147.
Opposite light/dark thighs retained; front far boot flatter. Requested five-row
lowest-far clearance and original rounded crate panel restoration still not reached.
Read-only lower-boot ROIs show rear/front alpha bottoms172/169 in03 and172/171
in04: projected separation reduces3 to1 rows, not anatomical sole/contact proof.
Walking heel/toe interaction and cargo variant remain provisional. Do not assemble
01 near half with04 far automatically and call crate/camera/grade consistent.

All four exact frozen prompts/ordered reference and source hashes/raw files/
original paths/generation IDs retained and revalidated. Whole alpha128 cells,one
unobstructed neutral BOX scale per sheet,whole translation to bbox172,zero clipped
opaque pixels. No mirror,limb/crate patches,recolour or pose/cargo-width fitting.
All raw/packed comparisons and used whole guides inspected. Contact03/04 raw
corner/middle gutter alpha0 confirmed; odd figure-count sheets have opaque center
figures, as expected. Pixel bbox/alpha envelopes diagnose registration, not motion.
Comparison caption corrected to East in reused helper; source PNG pixels unchanged.

Lessons: a near-leading cargo reference may compete with an opposite-leg stance
guide. Removing it and describing literal foreground/background thigh slopes
produced the needed opposite anatomy here; causality remains an inference. Support
identity, boot projection and crate perspective are independent checks. Solving
one does not solve all. Simplify whole-pose corrections sequentially, preserve
complete connected figures, inspect cargo design/hand support before combining
separately calibrated halves. Do not mirror asymmetric identity or use bbox bottoms
as proof of a planted boot. Keep sampled neutral/profile differences explicit.

Next far-passing05 request frozen and whole contact04 guide inspected. Generation
NOT STARTED, no job/tool handle live. Ask full far-support passing with same current
crate/hand support, far flat boot beneath pelvis,near thigh slightly back/left and
near rear boot raised. Then regenerate/review near half to match chosen full-body
cargo projection,assemble complete alternating loop and stage actual own East
movement. West carry,turn/held joins,normal full saves/visible Continues and full
consistency/polish remain. No owner save or gameplay files touched in this source
milestone; no native owner-fingerprint claim. Goal active/incomplete.
'''
    for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with p.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with p.open('a',encoding='utf-8') as stream:stream.write(lesson)
    installed.write_bytes(maintained.read_bytes())
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: East carry whole sources

## Objective and acceptance
Full master-matched set/consistency/polish active and incomplete. East carry01
near halves usable for comparison,02 correction rejected,03/04 opposite thigh
posture achieved but support/cargo projection provisional. No accepted complete
cycle/native/full-save/Continue or normal admission. No live process/job handle.

## Accepted decisions and constraints
Own32x147 selected East adult side body PRIMARY, original visible implant/hair/
hardware and elevated camera. Cargo extent is not body calibration. Complete
whole alpha128 cells,one neutral147 BOX scale per source,whole translation only,
zero clipped opaque pixels. No mirror/limb/crate patch/recolour/per-pose fit.
Keep current gameplay/cadence/normal selections and owner saves unchanged.

## Current state and changed files
New prepare/build carry01,half02,contact03/04 and prepare passing05 tools;
character/marsh-east-carry-material-v1/sources exact raw/IDs/original paths/
prompts/order/source/guide SHA provenance,opposite/whole correction guides.
Candidate01 four figures/ruler/manifest/recipe/comparisons/APNG,far-half02-rejected,
contact03/04-unselected with whole/ruler comparisons. source-assessment.json and
raw-alpha-diagnostics.json record actual observations. Pipeline,bible,current
status,maintained/installed master-repair skill appended. Passing05 frozen but
generation not started; its whole guide inspected. Concurrent other-actor notes
preserved, no normal catalog or runtime edits.

## Verification and scope
All four raw sources,packed comparisons/neutrals and used whole guides inspected.
Exact frozen prompts/references/source dependencies/raw SHAs revalidated. Five,
three,two,two complete cells;one neutral scale each,no clipping.01 APNG4 frames
decode exact180ms loop. Source01 repeats near support;02 repeats near and changes
crate front;03 has correct opposite thighs but angled far front boot;04 flattens
front boot without reaching requested clearance or original crate restoration.
Read-only boot alpha ROIs:03 rear/front172/169,04 172/171; not anatomical sole
proof. No Godot run or new native/profile interval, no transferred South/North
stage acceptance. No coherent mixed cycle certified.

## Remaining work and next action
Generate frozen passing05 using its three exact ordered local references from
request JSON; inspect complete support/raised boot/cargo/head/body/camera/grade.
Then regenerate/review near half matching chosen crate projection before assembly
and actual East actor validation. West carry/turn/held joins,independent normal
full saves/visible Title Continues and full-set consistency/polish remain.
Keep full goal active; do not declare full set from existing coverage counts.
'''
    (ROOT/'docs/MARSH_EAST_CARRY_SOURCES_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print('Recorded four East whole carry sources/opposite-stance lesson and frozen next correction; skill mirrors equal; goal incomplete.')
if __name__=='__main__':main()
