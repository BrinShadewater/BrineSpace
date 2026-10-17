from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
assert json.loads((P/'package-checks.json').read_text())['failures']==0
note='''## Veld East lounge fall source - October 1, 2026

Staged character/veld-lounge-fall-east-v1 adds six finite seated-to-floor poses
in both gears,12RGBA exports. Two newly authored whole-body interiors provide
forward seated slump and slide toward knee/hand support. Initial source is exact
master-aligned staged East seated frame5, with only16transparent bottom rows
added. Last three sources exactly reuse established early floor-fall brace,
roll and resting endpoints. That East seated foundation remains staged too;
normal selected library is unchanged. No production/gameplay/room/save changes.

Built-in imagegen exec-01e860c7-d9b9-4e46-afbd-e79c90e5c088 retained raw fall-v1.png
and exact prompt. Reference1 selected East idle is identity/physique/matte material
authority; reference2 staged coherent East seated is entry gesture; reference3
early fall source supplies floor choreography/uniform detail. Actual raw1280square
has upright opaque height649, so one148/649 anatomical ruler applies to both new
interiors. No per-pose box fitting. Pooled skin/hair/science/neutral master grade
before resampling, body component isolation/transparent edges.256x272/p128,224/H148.
Unscaled canonical35x39 East helmet uses rigid rotations/collar registration;
body outside bounded head insert exactly equal bare. First seated equipped head
and last three equipped floor frames remain their exact established sources.

22builder and56independent package/alpha/finite timing/exact entry-floor joins/
paired helmet-body checks0fail. Six slots1440ms finite, two source GIFs at3xslower
with pooled palettes. Paired complete-body board reviewed beside original-scale
standing master: attached hips/limbs, warm skin/brown bun, charcoal matte suit,
blue insignia and scientific hardware retained. Source/artwork evidence only;
no native furniture contact, mortality selector, source-clock API, full Continue
or new gameplay cadence proof. No Godot test this source-only interval, so no
owner profile reads/writes. Source/raw/prompt/builders/evidence retained.

Lesson: a chair fall needs an authored slump and slide before the established
knee/hand floor brace; a generic standing fall skips those anatomical contacts.
Keep exact seated entrance and canonical resting endpoint, one anatomical ruler
and semantic grade, and reuse proven whole-body landing sources. Mark the entry
foundation's staged status explicitly; artwork extraction/PNG checks do not prove
live chair root/depth or natural world mortality. Next native seat-root registration,
strict seated/partial source selection and full save/future continuation; remaining
cardinal lounge coverage, whole-world hazards, normal paired installation and
full-set Veld master/cross-family polish remain open. Full goal active/incomplete.
'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for i,path in enumerate(targets):
 old=path.read_bytes();payload=note.replace('\n','\r\n').encode()
 if note.splitlines()[0].encode() not in old:path.write_bytes(payload+b'\r\n'+old if i==0 else old+b'\r\n'+payload)
handoff='''# Project handoff

Updated:2026-10-01 - Project:BrineSpace - Task:Veld East lounge fall source

## Objective and acceptance
Full Veld master-matching set, then cross-family consistency/polish.
Goal active/incomplete; East lounge fall artwork staged. Owner acceptance open.

## Accepted decisions and constraints
Selected East idle identity/physique/matte authority. Exact staged East seated
entry5; exact early floor brace/roll/rest endpoints. One148/649 anatomical ruler,
pooled semantic master grade.256x272/p128,224/H148. Native canonical helmet,
unchanged body outside head. Preserve old sources/owner geometry/normal library.

## Current state
Raw built-in source and exact prompt in sources/, build.py exports12paired PNGs.
Six finite slots1440ms with two generated interiors and four exact reused sources.
validate.py/review.py, paired original-scale master board and two source GIFs.
No production selectors or normal manifest installation this source milestone.

## Verification
22builder/56independent package checks0fail. Whole-source board reviewed against
standing master. Exact incoming/floor joints, native helmet-body protection,
finite timing, alpha and source ruler checked. candidate-evidence.json binds
source/artwork metadata and references. No native room/mortality/Continue proof
from these source checks; no Godot run/owner save writes this interval.
Prior eight early bunk floor deaths/full Continue21094native checks and scoped
bunk/held/water regressions pass separately in veld-bunk-early-fall-v1.

## Next action
Native chair root/depth registration, strict seated/partial mortality selection
and full disk/fresh-scene future Continue for East. Remaining cardinal lounge
falls, whole-world hazard cadence, normal paired body installation and full-set
Veld master/cross-family polish. No commit/export requested.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
files=[P/n for n in ['sources/fall-v1.png','sources/prompt-v1.txt','build.py','validate.py','review.py','record.py','bare-manifest.json','helmet-manifest.json','registration.json','material-grade.json','package-checks.json','paired-source-review.png','index.html','HANDOFF.md']]+list((P/'frames').rglob('*.png'))+list(P.glob('*.gif'))+[R/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png',R/'character/veld-seated-east-coherent-v1/frames/bare/sit-down-east/005.png',R/'character/veld-seated-east-coherent-v1/frames/helmet/sit-down-east/005.png',R/'character/veld-bunk-early-fall-v1/sources/fall-v1.png']
(P/'candidate-evidence.json').write_text(json.dumps({'generation':'built-in imagegen exec-01e860c7-d9b9-4e46-afbd-e79c90e5c088','builderChecks':22,'packageChecks':56,'exports':12,'newInteriorPosesPerGear':2,'normalSelection':False,'nativeChairContactProven':False,'visualReview':'Paired complete-body board against original-scale selected East standing master','scope':'Staged East lounge artwork with staged coherent seated entry; not live room/mortality/Continue evidence','bindings':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
h=R/'character/veld-bunk-early-fall-v1/HANDOFF.md';s=h.read_text(encoding='utf-8')
s=s.replace('Lounge fall sources/transition coverage, then whole-world hazard cadence and','East lounge source now staged in character/veld-lounge-fall-east-v1; native\nchair registration/selection/Continue and other cardinal sources next. Then\nwhole-world hazard cadence and')
h.write_text(s,encoding='utf-8')
print('22builder/56package checks;12exports;five lessons and concise handoffs saved')
