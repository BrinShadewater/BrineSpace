from pathlib import Path
import json, os, hashlib, shutil
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parent;ROOT=P.parents[1];OLD=P.parent/'james-meal-pickup-south-v1'
def atomic(path, transform):
    old=path.read_bytes();temp=path.with_name(path.name+'.james-south-open.tmp');temp.write_bytes(transform(old))
    assert path.read_bytes()==old,f'Concurrent modification: {path}';os.replace(temp,path)
def dump(path,value):path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
r=json.loads((P/'native-contact-evidence.json').read_text());v=json.loads((P/'native-contact-validation.json').read_text())
n=json.loads((OLD/'native-service-sides-evidence.json').read_text());nv=json.loads((OLD/'native-service-sides-validation.json').read_text())
assert (r['checks'],r['failures'])==(235,0) and (n['checks'],n['failures'])==(51,0)
assert v['exitCode']==nv['exitCode']==0 and not v['timedOut'] and not nv['timedOut']
assert 'ERROR:' not in (P/'native-contact.log').read_text() and 'ERROR:' not in (OLD/'native-service-sides.log').read_text()
for suffix in ['-evidence.json','-validation.json','.log']:
    shutil.copy2(OLD/('native-service-sides'+suffix),P/('native-north-regression'+suffix))
source=(OLD/'native-service-sides.gd').read_text().replace('const OUT := "res://character/james-meal-pickup-south-v1/"','const OUT := "res://character/james-meal-service-south-open-v1/"').replace('native-service-sides-evidence.json','native-north-regression-evidence.json')
(P/'native-north-regression.gd').write_text(source)
images=[Image.open(P/'captures'/f'source-{j:02d}.png').convert('RGB') for j in range(6)]
images[0].save(P/'supported-contact-diagnostic.gif',save_all=True,append_images=images[1:],duration=[350,150,200,200,150,500],loop=0,disposal=2)
board=Image.new('RGB',(3*432,2*456),'#303b40');d=ImageDraw.Draw(board)
for j,im in enumerate(images):
    at=((j%3)*432,(j//3)*456+24);board.paste(im,at);d.text((at[0]+8,at[1]-20),f'South source{j} / supported open counter / contact still pending',fill='white')
board.save(P/'contact-review.png')
dump(P/'selection.json',{'status':'supported_south_contact_art_unselected','ownerVisualAcceptance':False,'productionArtInstalled':False,'counter':'library/sp-generated-counter-galley-prep','fixturePosition':[0,126],'actualSouthLocalFoot':[48,128],'serviceContactFractions':{'north':[.5,1],'south':[.5,.45]},'counterFloorRect':[0,126,91.12,50.32],'checks':{'southChooserContact':235,'currentNorthRegression':51},'rejectedSource':{'path':'rejected-reach-source.png','original':'C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-a998860c-0a05-4cbc-a91d-eff5eb391118.png','prompt':'rejected-reach-prompt.txt','sha256':hashlib.sha256((P/'rejected-reach-source.png').read_bytes()).hexdigest(),'reason':'Maximum pose still keeps bowl/hands near waist, does not perform requested worktop reach; never extracted/selected/installed.'},'limitations':['235 checks prove supported chooser/route, source clocks and hull-bounded counter; visual hand/worktop contact FAILS.','South bowl uses temporary CandidateJames subclass/current older v3 sources; production art selection unchanged.','North51 geometry/idle/copy-side checks include four expected raw-UI-icon export warnings; not export or full journeys.','Both strict real-profile guards fail with last_session.json delta; attribution unproven, no owner restore.','Bowl/cup/returns/interrupts/Continue/current full-set polish remain.']})
handoff='''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: supported South open-counter meal contact

## Objective and acceptance
Full James animation/master/proportion/perspective/height/material goal stays active. Resolve a legitimate South meal context before further acquisition/cup/return art. This milestone establishes supported safe geometry; acquisition still fails visual worktop contact, is not selected or installed.

## Accepted decisions and constraints
Current sp-galley-2/4 remain North-only: raised backboards are not rear access. Use existing registered open prep counter, preserve owner layouts/source art/collision boxes/furniture scale. Standing master/slim legs/broad boots, permanent wrench image-left and torch image-right, one anatomical ruler/whole authored poses. No forced rear service, stretched arms, body splices or per-pose size fitting.

## Current state
rooms/station-props-v2/props.json adds galley_counter role, North/South service sides and explicit contact fractions to existing sp-generated-counter-galley-prep. scripts/crew_room_activity.gd resolves only explicit contact fractions before ordinary approach/clearance; older/default counters retain their original points. South uses registered footprint top .45; North uses1.0. Dedicated fixture prep at[0,126] has rect[0,126,91.12,50.32], fully inside ±184 hull band. Normal chooser reaches local[48,128], collision-safe South station with144service limit. No default furnishing or owner layout change. Candidate uses existing uninstalled v3 South bowl/temporary CandidateJames subclass, exact standing/held sources and900ms timer. New six-pose imagegen draft exec-a998860c-0a05-4cbc-a91d-eff5eb391118/prompt retained as rejected: still waist-level hands despite requested deep worktop lean; no extraction/package/normal art installation. Current scene captures/diagnostic GIF/board, isolated evidence and future North regression copy/UID helper retained.

## Verification
235native checks/0fail for actual normal hunger chooser/route, supported South facing, planted contact, all6candidate sources and exact held endpoint, counter hull bounds. Actual00/02/04 captures reviewed: hands still away from worktop, so source/contact visual acceptance FAILS. Do not claim green tests prove pickup. Current North regression51checks/0fail:4default rotations, blocked-front refusal, saved copies inherit North-only, unrestricted legacy fallback retained and native idle captures. Its log contains4expected raw UI icon export warnings, no engine errors; no export proof. Both engines0/no timeout/scratch APPDATA resolved. Strict full owner-profile guards FAILED,last_session.json only; cause unproven, no owner restore or clean-guard retry. First placement[0,175] was partly off-hull despite234green tests; retained prior-edge-placement. Correct in-hull image-edge contact[48,112] still unnecessarily far from actual floor contact; retained prior-image-edge-contact. Current[48,128] honors existing collision clearance rather than bypassing it.

## Next action
Author independently complete South reach interiors that bend forward from hips with head/shoulders changing projection, planted boots, unchanged arm/skull scale. Target actual worktop in current fixture; inspect depth ordering so gloves contacting the top are not hidden by the counter. Exact selected standing and held meal joins. Then cup, return, interruptions, production binding/Continue and remaining rest/life/mortality contexts/full cross-family polish. New draft and old v3 acquisition remain unselected. No commit/export, goal active.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
note='''\n## James supported South open-counter contact — October 1, 2026

Existing registered open prep counter now has galley_counter role, North/South service sides and explicit service_contact_fractions. Current raised-backboard sp-galley-2/4 stay North-only. crew_room_activity resolves explicit fractions with ordinary approach/collision checks; unchanged defaults otherwise. Dedicated prep fixture[0,126]/rect91.12x50.32 lies wholly inside hull; normal hunger chooser reaches safe South local[48,128]. South fraction .45 follows registered floor footprint, not misleading rear image edge. No default/owner furnishing/source art/collision/scale change.
235native checks/0fail prove chooser/route/6candidate source clocks/held join/hull bounds; actual worktop hand contact still FAILS. Temporary CandidateJames and old South v3 art remain uninstalled. New imagegen six-pose source exec-a998860c-0a05-4cbc-a91d-eff5eb391118 retained with exact prompt as rejected waist-level reach. North51checks/0fail confirm4defaults/blocked-front/copies/legacy fallback;4expected raw UI icon export warnings, no engine errors/export claim. Both engines0/scratch/no timeout; strict owner-profile guards FAILED,last_session.json delta, attribution unproven/no owner rollback. Prior off-hull and image-edge contact evidence archived.
Lesson: activity contact must follow the registered floor footprint of an elevated worktop; full image bounds can put the character too far away. Safe path/facing/source-clock tests do not prove visible hand contact or hull-safe furnishing. Do not compensate bad contact geometry with unnaturally long arms, body scaling, forced service through backboards or source art that still gestures at the waist. Next whole-pose South forward reach and tabletop occlusion, then cup/return/interrupt/production/Continue. Full James/rest/life/mortality/cross-family polish goal active. See character/james-meal-service-south-open-v1/HANDOFF.md.
'''.encode('utf-8')
paths=[ROOT/'docs/CURRENT_STATUS.md',ROOT/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    if b'James supported South open-counter contact' not in path.read_bytes():atomic(path,lambda old:note+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n'+note)
print(json.dumps({'southChecks':235,'northChecks':51,'geometrySupported':True,'visualHandContact':False,'artInstalled':False,'goalActive':True}))
