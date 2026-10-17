from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
paths=[]
for kind in ['salvage','pickup']:
 out=ROOT/'output'/f'bill-{kind}-west-candidate-native-v1'
 paths.extend([out/'validation.json',out/'native.log',ROOT/'tests'/f'test_bill_{kind}_west_candidates.gd'])
for folder in [P,P.parent/'bill-swim-pickup-helmet-west-coherent-v1',P.parent/'bill-salvage-west-coherent-v1',P.parent/'bill-salvage-helmet-west-coherent-v1']:
 m=json.loads((folder/'manifest.json').read_text(encoding='utf-8'));paths.append(folder/'manifest.json');paths.extend(folder/f for state in m['states'] for f in state['frameFiles'])
(P/'native-candidate-evidence.json').write_text(json.dumps({'files':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'scope':'102work+82pickup candidate checks;explicit injection,not installation'},indent=2)+'\n',encoding='utf-8')
handoff='''

## September30 West salvage/pickup pair staged
Objective: full master-consistent Bill set,then cross-set polish;active.
Accepted: independent West-specific left-facing work/cargo anatomy/control,
matte quilting/burgundy/plainring/cyan,compact two-bandcase. Working.28 ruler
from82px crown;pickup.255 from88–92px crowns,not common pixel scale across atlases.
Canonical40x40shell at87/95,crown102104,protectedforearm/body. Work840ms;pickup
520ms unchanged. Exact newwork000/currentcargo000padded42,40 endpoints.
Changed: four West bare/helmet work/pickup folders;immutable sources/prompts,
legrepairv2,builders/grade/registration/hashes/verify/browser/contact/movingGIFs;
two candidate fixtures+UIDs/runners;actual West live boundary fixture+runner;
bound evidence/README,skills/pipeline/bible/status. Runtime/registry unchanged.
Verification:62work+60pickup package PASS;102work native8.33sec;82pickup9.54sec;
1719actual live boundary39.22sec.2914realnon-logfiles unchanged each scratchrun.
Native82/enlarged148 darklight and moving browser reviewed. Actual controller/grid
nominal5.48work/520ms pickup and recall1.216sec,selected W/E carry/basic halfturns
finish/resume with80returnupdates;normaloneunit/recallzero,no early extraction.
Scopes: injected staged art and isolated direct work start. Additional loop-exit
phases,actualselected promotion,full outward/airlock journey remain unproven.
Next: independent North/South paired work/pickup;extra phase checks;family paired
promotion and selected proof;retainedlife/death,stationcargo motion,fullcross-set
consistency/polish. Fullgoal incomplete,no blocker.
'''
with (ROOT/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md').open('a',encoding='utf-8') as f:f.write(handoff)
lesson='''

### Independent West work/pickup ruler and late leg repair — September30,2026

Same character scale does not imply equal source pixel scale between atlases.
West work opaque crown82px needs.28;pickup88–92px needs.255 to project22–23px.
Use one frozen ruler/material curve per atlas,selected native endpoints/head,
and preserve West-specific chest hardware independently of East. Repair the
last interior's tucked knees in source toward the carry master;do not stretch
exported calves or force per-frame silhouette dimensions. Preserve case bands,
two connected hands,torso/head and complete atlas in the edit. Native helmet
40x40at87/95 remains fixed;protect suit/case/forward arm. West62+60package,
102+82candidate,1719actual boundary checks pass with2914profile files unchanged.
Actual work→pickup→cargo/recall→W/E half-turn finish/resume is separate from
selected-loader installation and full expedition journey. See staged West pair
README/live-review and Bill continuation. North/South and full-set polish remain.
'''
for p in [ROOT/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md'),ROOT/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md']:
 with p.open('a',encoding='utf-8') as f:f.write(lesson)
p=ROOT/'docs/CURRENT_STATUS.md'
intro='''## Bill West underwater work/pickup pair staged — September30,2026

Independent bare/helmet West working840ms loop and520ms pickup now match selected
matte/helmet/cargo art;case bands and lateleg extension retained. Fixed measured
work.28/pickup.255 rulers.122package+184candidate native+1719live controller/grid
checks PASS;2914realnon-logfiles unchanged each scratchrun. Native82/148darklight/
moving proofs saved. Runtime/registry unchanged. North/South,phasecoverage and
family promotion follow. [Handoff](BILL_ANIMATION_CONTINUATION_2026-09-29.md).
Full Bill goal active.

'''
p.write_bytes(intro.encode('utf-8')+p.read_bytes())
