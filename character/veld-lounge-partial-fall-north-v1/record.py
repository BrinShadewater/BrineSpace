"""Record this source/contact milestone without claiming runtime admission."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
O=R/'output/veld-lounge-partial-fall-north-contact-v1'
native=json.loads((O/'validation.json').read_text());package=json.loads((P/'package-checks.json').read_text())
assert native['passed'] and native['realProfileChanges']==[] and package['failures']==0
heading='## Veld partial North lounge fall source and chair contact - October 2, 2026'
note='''
New staged character/veld-lounge-partial-fall-north-v1 supplies a partial lowering
pose2 entrance, two authored buckle/floor-brace interiors and exact established
North floor roll/rest3..5, both gears. Built-in source generation
exec-774892bf-42da-4a9b-adeb-1f1ced7eaeda and exact prompt retained. One148/592
anatomical ruler for both interiors; pooled master material grade uses explicit
rear ear windows, excluding brown hair from the skin authority. Original native
rear helmet depth views15/40degrees inserted; body outside head region unchanged.
12RGBA exports256x272/p128224/H148; finite1420ms, no mortality opt-in or loader edit.

18builder and70package checks pass. Native source/contact audition68checks0fail,
51.58s/engine0/cleanlog; actual default North lounge rotation0, all12 exact sources
submitted. Provisional partial chair root amounts .3125,.3125,.15625,0,0,0;
physical navigation foot fixed, first2 sources retain chair contact depth.
Paired full source/master and all12room/source presentations reviewed: attached
body, same matte materials/rear helmet, visible entry/buckle, clear floor landing.
Per-capture camera crops retained; discrete poses are not continuous native motion.
Scratch APPDATA and all2931owner non-log files unchanged. Bound original entry,
landing and helmet sources validated; broader production dependencies not frozen.

Lesson: exact partial entrance registration differs from fully seated contact.
Author buckle at a shared adult ruler; audition fractional chair-to-floor offsets
in actual room contact before connecting saved mortality. Keep depth-pitch helmet
construction rather than rotating a flat rear head; classify rear skin spatially
so pooled material matching cannot turn brown scalp into skin or gray hair.
Coverage currently source pose2 only; earlier/later partial entrances and rising
need actual selector/contact validation. No production death/save/Continue proof,
normal admission, natural hazards, all rotations or owner acceptance for this new
partial family. Next opt-in partial selector/root law, strict snapshot binding and
paired actual mortality/fresh disk future Continue; then remaining partial poses,
other actual furniture contexts and full cross-family consistency/polish.
Full goal active/incomplete. No commit/export requested.
'''
handoff='''# Project handoff

Updated:2026-10-02 - Project:BrineSpace - Task:Partial North lounge fall

## Objective and acceptance
Full master-matching Veld set and cross-family polish active/incomplete.
Partial North fall source/contact milestone; runtime and owner motion review open.

## Accepted decisions and constraints
Keep selected North seating and floor landing, real default chair geometry,
fixed148/592ruler, pooled anatomical matte grade and original rear helmet components.
No normal selection or production mortality changes in this milestone.

## Current state
New pack with raw/prompt, deterministic builder,12PNGs/paired manifests, validation,
source previews/master sheet, paired native contact boards/crops and evidence.
New isolated source-contact test/UID and runner; five lesson targets updated.

## Verification
18builder/70package/68native checks0fail. Native51.58s,engine0/cleanlog;
12actual room/source captures reviewed, fixed physical foot, provisional partial
chair root .3125 to0. Original sources/components bound; broader inputs not frozen.
Scratch APPDATA/all2931owner files unchanged. Rotation0 prescribed discrete poses,
not actual mortality, Continue, natural world cadence or all partial entrances.

## Next action
Bind eligible partial North displayed source and real registration to opt-in fall;
validate snapshot/root/depth and actual mortality/fresh disk future Continue.
Then remaining partial poses/actual furniture contexts, normal paired admission,
full cross-family master/style/camera/scale/proportion/material polish.
No blocker, commit/export or final owner acceptance claim.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
(P/'native-evidence.json').write_text(json.dumps({'native':native,'packageChecks':package['checks'],'sourceContactChecks':68,'reviewed':['paired-source-review.png','bare-native-contact.png','helmet-native-contact.png'],'normalSelection':False,'productionMortality':False,'freshContinue':False,'scope':'Rotation0 prescribed partial root/source audition only'},indent=2)+'\n',encoding='utf-8')
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in targets:
 text=path.read_text(encoding='utf-8')
 if heading in text:continue
 block=heading+'\n'+note+'\n'
 path.write_text(block+text if path.name=='CURRENT_STATUS.md' else text.rstrip()+'\n\n'+block,encoding='utf-8')
print('Source/contact handoff, native evidence and five lesson targets recorded')
