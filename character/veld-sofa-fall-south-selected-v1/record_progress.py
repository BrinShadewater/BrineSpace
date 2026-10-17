"""Record normal paired world/Continue admission at the actual verified scope."""
from pathlib import Path
import json,re,hashlib,subprocess,sys
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-sofa-selected-continue-v1';M=R/'output/veld-sofa-normal-motion-v1'
world=json.loads((O/'validation.json').read_text());motion=json.loads((M/'validation.json').read_text());assert world['passed'] and motion['passed']
view=json.loads((P/'world-review-evidence.json').read_text());assert view['visualReview']=='all20boards-reviewed'
mv=json.loads((P/'motion-review-evidence.json').read_text());assert mv['visualReview']=='all4contact-sheets/all196native-presentations-reviewed'
count=int(re.search(r'VELD SOFA WORLD CONTINUE: (\d+) checks,0 failures',(O/'native.log').read_text()).group(1))
assert 'status' not in (R/'scripts/crew_sprite_player.gd').read_text(), 'Promotion requires ignored descriptive metadata only'
promotion={}
for gear in ['bare','helmet']:
    path=P/f'{gear}-manifest.json';before=path.read_bytes();old=json.loads(before);new=dict(old);new['status']='selected'
    snapshot=P/f'{gear}-manifest-before-status.json';snapshot.write_bytes(before)
    assert {k:v for k,v in old.items() if k!='status'}=={k:v for k,v in new.items() if k!='status'}
    path.write_text(json.dumps(new,indent=2)+'\n',encoding='utf-8')
    promotion[gear]={'oldSHA256':hashlib.sha256(before).hexdigest(),'newSHA256':hashlib.sha256(path.read_bytes()).hexdigest(),'onlyChange':'descriptive status field; parser never reads it; all states/profile/paths/durations byte-equivalent as parsed JSON'}
(P/'status-promotion.json').write_text(json.dumps(promotion,indent=2)+'\n',encoding='utf-8')
run=subprocess.run([sys.executable,str(P/'verify_selected.py')],capture_output=True,text=True);assert run.returncode==0,run.stderr
text=f'''## Veld South sofa falls normally selected - October 2, 2026

Normal grid loader/ACTIVE_ASSETS now select paired tablet and empty-handed sofa
falls in character/veld-sofa-fall-south-selected-v1. Two finite states/six slots
each per gear,18unique retained source PNG; reviewed H148/256x272/p128224/matte
grade/shared shell unchanged.50source/registry/literal-loader checks pass.
Final metadata promotion changes descriptive status only; parser ignores it,
all runtime states/profile/paths/durations unchanged. Before/after JSON retained.

Normal-only world mortality and ordinary disk/fresh-main Continue:
{count}checks0fail/20world deaths/20fresh disk restores/6000future actor updates,
engine0/{world['seconds']}s/clean log. Fourteen live reader entrances include both
neutral endpoints; six actual power/suspension read-exit contexts. Real mortality
roster accounting and paid Bill survivor preserve ordinary save eligibility.
Independent six-source clock, sofa support/floor depth, fixed navigation foot,
exact paused source/contact, reference/resumed future and canonical terminal
checked. All20boards/{view['nativeSourcePairs']}source-native pairs visually reviewed.
Final66targeted inputs/all2931owner non-log files unchanged under scratch APPDATA.
Prescribed default South sofa, paused world/actor stepping; not natural hazards,
chooser/traffic, title/new-process Continue or final owner motion acceptance.

Native30fps finite review:942checks0fail/196source-native pairs, engine0/
{motion['seconds']}s;66inputs/whole owner profile unchanged in separate scratch.
All4contact sheets/all196native presentations inspected. Four lossless APNG
previews retain exact decoded native room colours:200checks0fail.1.6s sampled
motion,800ms viewer terminal hold, repeat resets preview only; authored fall finite.
No GIF palette reduction; original source/native PNG and hashes retained.

Initial world interval remains FAILED after7live contexts: interrupted exit
submitted an equal-pixel different texture object. Separate real-state probe
proved samePixels=true/sameTexture=false,centerDistance0.19764. Resample actual
post-transition texture for strict capture; no production animation/assertion
weakening. Original interval/probe retained, final complete run passes.

Lesson: preserve prop state and exact whole entrance, then validate normal world
roster, ordinary disk/future playback and native furniture contact separately.
Pixel-identical aliases are distinct loaded textures: refresh the source after
real stage changes before checking submitted identity. Use lossless native motion
previews when judging matte skin/hair/suit instead of introducing palette drift.
Next partial South sit/rise falls, remaining readers/directional furniture
contexts and full-library master/transition polish. Full Veld goal active/incomplete.
Reviews: character/veld-sofa-fall-south-selected-v1/review.html and motion-review.html.
'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    original=target.read_bytes();old=original.decode('utf-8');assert text.splitlines()[0] not in old
    updated=text+'\n'+old if target.name=='CURRENT_STATUS.md' else old.rstrip()+'\n\n'+text
    temp=target.with_name(target.name+'.veld-sofa.tmp');temp.write_text(updated,encoding='utf-8');assert target.read_bytes()==original;temp.replace(target)
handoff=f'''# Project handoff

Updated: 2026-10-02 - Project: BrineSpace - Task: Veld normally selected sofa falls

## Objective and acceptance
Full master-matched Veld set and cross-family polish active/incomplete. This pair
normally selected after world/ordinary Continue and sampled native motion checks.

## Accepted decisions and constraints
Both prop states, exact whole incoming pose/contact, fixed H148/master grade/shell.
Preserve owner geometry/navigation/save eligibility and unrelated actor selections.

## Current state
Paired selected manifests, literal grid loader and ACTIVE_ASSETS entries.18unique
PNG aliases to retained original/neutral sources; status-only promotion retained.
Normal-only world Continue and30fps motion fixtures/runners; review/evidence/APNG.
Source builder remains staged/raw reproducible; selected bundle is separate.

## Verification
50source admission;{count}world checks0fail/20deaths/20fresh disk/6000future steps.
20boards/{view['nativeSourcePairs']}pairs reviewed.942motion checks/196pairs0fail,
all196native frames reviewed;200decoded APNG colour checks.66inputs and2931owner
files unchanged in both scratch intervals. Original alias-identity fixture failure
and real-state probe preserved; assertions/controller art unchanged.
Scope: prescribed default South sofa, actual world mortality API/roster, normal
disk/fresh-main restoration and paused-world actor stepping. Natural chooser,
hazard/traffic/title/new-process and final owner visual acceptance remain open.

## Next action
Authored partial South sit/rise falls, remaining reader/directional furniture
contexts; full-library master/proportion/material/motion joins and final polish.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
prior=R/'character/veld-sofa-fall-south-v1/HANDOFF.md';old=prior.read_text(encoding='utf-8');prior.write_text(old+'\n## Later normal admission\nBoth prop states now selected. Current handoff: ../veld-sofa-fall-south-selected-v1/HANDOFF.md.\n',encoding='utf-8')
print(json.dumps({'worldChecks':count,'updatedDocs':5,'normallySelected':True,'fullGoal':'active/incomplete'}))
