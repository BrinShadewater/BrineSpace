from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;P=R/'character/krusher-water-cargo-turns-v3';read=lambda p:json.loads(p.read_text())
ind=read(P/'independent-validation.json');val=read(P/'validation.json');native=read(P/'review/native/report.json');run=read(P/'review/native/run-verification.json');media=read(P/'review/media.json')
assert not ind['errors'] and not val['errors'] and not native['errors'] and not run['loggedErrors'] and not run['ownerFilesChanged'] and run['engineExit']==0
f=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),22);board=Image.new('RGBA',(1000,880),'#252b2e');draw=ImageDraw.Draw(board);draw.text((20,15),'KRUSHER DOM / UNDERWATER HEAD FIT',font=f,fill='white');draw.text((20,45),'Original James motion / complete head and neck / muted cyan',font=f,fill='#bed2d3')
for row,g in enumerate(['bare','helmet']):
 for col,(family,key,i) in enumerate([('cargo','swim-carry-east',0),('turn','swim-turn-north-south',2),('cargo-turn','swim-carry-turn-south-west',2)]):
  m=read(P/f'{family}-{g}-manifest.json');s=next(s for s in m['states'] if s['id']==key);im=Image.open(P/s['frameFiles'][i]).convert('RGBA');x0,y0,x1,y1=im.getbbox();im=im.crop((x0-4,y0-4,x1+4,y1+4));im=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST);x=col*333+(333-im.width)//2;y=115+row*370;board.alpha_composite(im,(x,y));draw.text((col*333+18,y-27),g+' / '+['carry','swim turn','carry turn'][col],font=f,fill='white')
board.save(H/'water-cargo-head-fit-sheet.png')
review={'sourceContextsReviewed':138,'sourceBoards':['source/heads-00.png','source/heads-01.png','source/heads-02.png','source/heads-03.png'],'nativeFullAndSmallViewsReviewed':['bare-swim-turn-north-south-002.png','helmet-swim-carry-turn-north-east-001.png','helmet-swim-turn-south-west-001.png','bare-swim-pickup-south-002.png'],'scope':'All revised head/collar contexts reviewed; native captures and original-hold sprite replay are not continuous station gameplay or final owner acceptance. Yellow shoulder/hardware palette audit remains.'}
(P/'review/visual-review.json').write_text(json.dumps(review,indent=2)+'\n')
handoff=f'''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: Krusher underwater cargo head fit

## Objective and acceptance
Complete Krusher animations with attached head/neck, clean hair and fitted helmet identity. Goal active/incomplete. This family is reviewed and technically checked; actual station and owner acceptance remain.

## Accepted decisions and constraints
Krusher Dom / System Administrator / AI & Robotics, James utility suit, matte muted cyan #527C80. Original motion/clocks/pivots/density, case, hands, tools and helmet shell preserved. Station first; no normal roster or owner-save installation.

## Current state
Water-cargo-turns-v3:64states/464refs/160unique/138revised,22retained. Original v2 whole six manifests byte exact. Sixteen whole source poses reuse corrected water-v3 and recovery-salvage-v2 by original James full RGBA hash, preserving turn/gait and salvage/pickup endpoints. Remaining cardinal and quarter full H3 head/neck sources compose original bodies; no painted neck bridges. North-to-South bare intermediate2 registered down1pixel after detached initial fit. Overhead South pickup2 explicitly reviews back-collar/nape attachment rather than projected chin/chest contact.
Old rear/quarter face hulls included warm helmet hardware. Twelve quarter helmets restore original source shell outside observed face apertures; rear carry views with no visible face retain original shell rather than painted identity on hardware. Full source/manifest/revision provenance, independent validators, native review and original-hold media reproducible via head-fit-v3/build_water_cargo.py, review_water_cargo.py, record_water_cargo.py and pack scripts. All138changed contexts on4boards and targeted full/small native views inspected. Original yellow trim remains pending palette audit. Full selected bank/package unchanged.

## Verification
{val['checks']} original-source checks0:464slots, complete timing/water metadata, bodies/tools/hip hardware, exact turn/gait and pickup/carry joins and reversed choreographies. {ind['checks']} independent checks0:hashes/masks/whole manifests,16exact corrected shared poses,63bare complete source/body contacts and12restored-shell checks. Native{native['checks']}checks0/464prescribed captures/engine0/{run['seconds']:.2f}s,48automatic turns,1920distance-driven carry ticks. First minimal fixture lacked swimming gaits and logged nil textures; fixed by admitting corrected water-v3 and salvage-v2 into its own pack index, then all checks passed. Scratch APPDATA;{run['ownerFilesFingerprinted']}owner non-log files unchanged. Own .gd/.uid paired.
All232paired source slots replay{media['seconds']:.3f}s/encoded{media['encodedSeconds']:.6f}s within one frame. Source replay and sampled native controller checks are not continuous furnished-water station delivery/cancel contact. Raster/media LFS filters confirmed. No commits or live jobs.

## Next action
Migrate underwater interruptions using new shared endpoints, then death poses. Rear/quarter identity and muted cyan/yellow trim audit, coherent full bank/package, strict West cue retarget and service-loss diagnosis, then actual station/bare-water/full-library checks. No approval gate or blocker.
'''
for target in [P/'HANDOFF.md',H/'WATER_CARGO_HANDOFF.md']:target.write_text(handoff,encoding='utf-8')
p=R/'character/krusher-complete-animation-v1/progress.json';d=read(p);v=d['visualReview'];v['status']='head-construction-v3-water-cargo-partial';v['remaining']='Underwater interruptions/death migration; rear/quarter identity and muted cyan/yellow trim audit; coherent full bank/package; strict West cues/service-loss and actual station/bare-water/full-library review.';v['headConstructionV3']['waterCargo']={'pack':P.name,'states':64,'refs':464,'unique':160,'revised':138,'sourceChecks':val['checks'],'independentChecks':ind['checks'],'bareContacts':63,'nativeChecks':native['checks'],'nativeCaptures':464,'scope':'Partial H3 family migration; full selected bank unchanged; station acceptance pending.','handoff':'res://character/krusher-head-fit-v3/WATER_CARGO_HANDOFF.md'};p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
source=(H/'update_rest_recovery_status.ps1').read_text();start=source.index('    $krusherHeader = @'+chr(39));end=source.index('\n'+chr(39)+'@',start)+3;header=f'''## Krusher underwater cargo complete-head candidate - October 4, 2026

Goal active/incomplete. Water-cargo-turns-v3:64states/464refs/160unique,
138revised. Original whole manifests/body/case/tools/clocks/pivots retained;
16exact corrected water-v3/recovery-v2 shared poses. Complete cardinal/quarter
H3 heads and necks; rear helmet shell restored outside observed apertures.
{val['checks']}source +{ind['checks']}independent +{native['checks']}native checks0;63bare contacts,
12shell checks,464prescribed captures,48automatic turns/1920distance gait ticks.
Scratch APPDATA;{run['ownerFilesFingerprinted']}owner files unchanged; native{run['seconds']:.2f}s.
All138changed source contexts and targeted full/small native views reviewed.
232paired original-hold replay25.12s; not continuous station acceptance.
Full selected bank unchanged. Next interruptions/death, identity/cyan audit,
coherent bank/package, strict West and actual station/bare-water closeout.
Handoff:character/krusher-head-fit-v3/WATER_CARGO_HANDOFF.md.

''';(H/'update_water_cargo_status.ps1').write_text((source[:start]+'    $krusherHeader = @'+chr(39)+'\n'+header+chr(39)+'@'+source[end:]).replace('CURRENT_STATUS.krusher-head-construction-rest-recovery.tmp','CURRENT_STATUS.krusher-head-construction-water-cargo.tmp'),encoding='utf-8')
print(json.dumps({'states':64,'revised':138,'checks':val['checks']+ind['checks']+native['checks'],'goal':'active-incomplete'}))
