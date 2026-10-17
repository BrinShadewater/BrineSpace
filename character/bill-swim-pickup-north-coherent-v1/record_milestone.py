from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
paths=[]
for kind in ['salvage','pickup']:
 out=ROOT/'output'/f'bill-{kind}-north-candidate-native-v1'
 paths.extend([out/'validation.json',out/'native.log',ROOT/'tests'/f'test_bill_{kind}_north_candidates.gd'])
for folder in [P,P.parent/'bill-swim-pickup-helmet-north-coherent-v1',P.parent/'bill-salvage-north-coherent-v1',P.parent/'bill-salvage-helmet-north-coherent-v1']:
 m=json.loads((folder/'manifest.json').read_text(encoding='utf-8'));paths.append(folder/'manifest.json');paths.extend(folder/f for state in m['states'] for f in state['frameFiles'])
(P/'native-candidate-evidence.json').write_text(json.dumps({'files':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'scope':'102work+82pickup candidate checks;explicit injection,not installation'},indent=2)+'\n',encoding='utf-8')
handoff='''

## September30 North salvage/pickup pair staged
Objective: full master-consistent Bill set,then cross-set polish;active.
Accepted: independent rear prone North tool/case up,bootsdown,twin cylinders,
threecyanvents,Iclasp,mattequilting/straps/soles/burgundyinset/plainring. Bothatlases
fixed.27 ruler,sharedcrown128104. Narrow crown grade excludes adjacent warmcuffs.
Native40x34rear shell at10895;protectedbodyy129,outerarmsabove125,case/glovesabove
104 onpickup. Work840ms;pickup520ms,exact newwork000/cargo000pad24,56 endpoints.
Changed: four Northbare/helmetwork/pickup folders,sources/prompts/builders/grade/
registration/hashes/verify/contact/browser;two candidatefixtures+UIDs/runners,
Northactualcontroller/gridlivefixture/runners/GIFs/timeline/boundevidence/README;
skills/pipeline/bible/status. Runtime/registry unchanged.
Verification:62work+60pickup package PASS;102work native9.36sec;82pickup9.95sec;
1719live34.4sec,2914realnon-logfiles unchanged each scratchrun. Native82/148darklight,
pausedhelmet/casecontact and moving browser reviewed. Nominal5.48secwork/520ms
pickup,recall1.216sec;selected N/S carry/basic halfturns finish/resume through80
returnupdates;no earlyextract,normaloneunit/recallzero. Initialfixture signerror
put approachnorth instead ofsouth;8assertionsfailed,archived/superseded bycorrected
test. No animation/gameplaycode changes needed. Direct isolated workstart/injected
art,notselected promotion/full outward-airlock journey orall loop-exit phases.
Next: independentSouthpair,extra phasecoverage,family consistency/promotion and
actualselectedproof;retainedlife/death,stationcargo motion,fullcross-setpolish.
Fullgoal incomplete,no blocker.
'''
with (ROOT/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md').open('a',encoding='utf-8') as f:f.write(handoff)
lesson='''

### North work/pickup foreground and route axes — September30,2026

Rear prone work tools must pointTOP with bootsDOWN,retain twin cylinders/three
vents/Iclasp and narrow skull-crown grading so adjacent warm cuff glints are not
recolored. Fixed.27 atlas rulers and exact selected endpoints/native40x34shell
work together. Case/gloves above crown128104 must remain in front of the helmet;
protect outerforearms above125 and suitbelow129. Do not draw the new shell over
the liftedcase. North62+60package/102+82candidate/1719actualboundary checks pass;
2914realprofilefiles unchanged. Native82/148darklight/pausedcontact/moving review.
For Northreturn fixtures place the approach waypoint SOUTH(+y)of the workpoint;
a blindly rotated negative-x fixture became negative-y and kept Northheading,
failing the desired half-turn checks. Fix fixture geometry,keep assertions,
archive failed interval,rerun actual controller/renderer. Evidence is injected
isolatedworkstart,not wholeexpedition/selectedpromotion. See NorthpairREADME and
Billcontinuation;South,familypromotion,fullsetpolish remain.
'''
for p in [ROOT/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md'),ROOT/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md']:
 with p.open('a',encoding='utf-8') as f:f.write(lesson)
p=ROOT/'docs/CURRENT_STATUS.md'
intro='''## Bill North underwater work/pickup pair staged — September30,2026

Independent rear-view bare/helmetwork840ms andpickup520ms preserve twin cylinders,
threevents/Iclasp/quilt/soles and forwardtool/case orientation. Fixed.27 rulers,
canonicalrear helmet,protectedcase/arms,exactworking/cargo joins.122package+
184candidate native+1719livecontroller/grid checks PASS;2914realnon-logfiles
unchanged each scratchrun. Native82/148darklight/contact/moving proofs retained.
Runtime/registry unchanged. South,phasecoverage and familycomparison/promotion
follow. [Handoff](BILL_ANIMATION_CONTINUATION_2026-09-29.md). Full Bill goal active.

'''
p.write_bytes(intro.encode('utf-8')+p.read_bytes())
