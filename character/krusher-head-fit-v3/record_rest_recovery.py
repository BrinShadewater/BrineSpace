from pathlib import Path
import json, subprocess
from PIL import Image, ImageDraw, ImageFont

R=Path(__file__).resolve().parents[2]; H=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text())
specs=[('rest','krusher-rest-family-v4',30,174,92,72,36,1290,'rest-preview.mp4'),('recovery','krusher-recovery-salvage-v2',16,96,86,65,29,764,'recovery-salvage-preview.mp4')]
entries={}
for key,folder,states,refs,unique,revised,contacts,nchecks,video in specs:
 p=R/'character'/folder; val=read(p/'independent-validation.json'); run=read(p/'review/native/run-verification.json'); native=read(p/'review/native/report.json'); media=read(p/'review/media.json')
 assert not val['errors'] and not native['errors'] and not run['ownerFilesChanged'] and not run['loggedErrors'] and run['engineExit']==0
 encoded=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(p/'review'/video)],text=True))
 assert abs(encoded-media['seconds'])<=1/60
 media.update(encodedSeconds=encoded,scope='Original paired source holds; not continuous station motion or owner acceptance.')
 (p/'review/media.json').write_text(json.dumps(media,indent=2)+'\n')
 views=['bare-bunk-enter-east-006.png','helmet-bunk-enter-east-006.png','bare-get-up-south-001.png','bare-get-up-west-002.png'] if key=='rest' else ['bare-salvage-south-002.png','helmet-salvage-south-002.png','bare-recover-air-east-000.png','helmet-salvage-west-004.png']
 (p/'review/visual-review.json').write_text(json.dumps({'changedSourceContextsReviewed':revised,'sourceBoards':['source/heads-00.png','source/heads-01.png'],'nativeFullAndSmallViewsReviewed':views,'scope':'Complete head/neck registration and visor fit on original James bodies reviewed. Original yellow shoulder trim remains pending cyan audit. Station acceptance pending.'},indent=2)+'\n')
 entries[key]={'pack':folder,'states':states,'refs':refs,'unique':unique,'revised':revised,'independentChecks':val['checks'],'bareHeadContactChecks':contacts,'nativeChecks':nchecks,'nativeCaptures':refs,'ownerFilesUnchanged':run['ownerFilesFingerprinted'],'encodedSeconds':encoded,'scope':'Partial full-library H3 candidate. Original bodies, clocks, root profiles, tools and helmet geometry retained. Existing selected full bank unchanged.','handoff':'res://character/krusher-head-fit-v3/REST_RECOVERY_HANDOFF.md'}

font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),22)
board=Image.new('RGBA',(1000,1080),'#252b2e'); d=ImageDraw.Draw(board)
d.text((20,15),'KRUSHER DOM / HEAD & NECK FIT',font=font,fill='white')
d.text((20,46),'James utility suit / matte muted cyan / animation candidates',font=font,fill='#bed2d3')
for row,(folder,manifest,key,i,label) in enumerate([
 ('krusher-james-canonical-v6','{gear}-manifest.json','idle-east',0,'Standing side'),
 ('krusher-rest-family-v4','{gear}-manifest.json','bunk-enter-east',6,'Reclined'),
 ('krusher-recovery-salvage-v2','salvage-{gear}-manifest.json','salvage-south',2,'Looking down')]):
 for col,gear in enumerate(['bare','helmet']):
  p=R/'character'/folder; m=read(p/manifest.format(gear=gear)); s=next(s for s in m['states'] if s['id']==key)
  im=Image.open(p/s['frameFiles'][i]).convert('RGBA'); box=im.getbbox(); crop=im.crop((max(0,box[0]-8),max(0,box[1]-8),min(im.width,box[2]+8),min(im.height,box[3]+8)))
  crop=crop.resize((crop.width*2,crop.height*2),Image.Resampling.NEAREST)
  x=col*500+(500-crop.width)//2; y=115+row*315
  board.alpha_composite(crop,(x,y)); d.text((col*500+25,y-28),label+' / '+gear,font=font,fill='white')
board.save(H/'rest-recovery-head-fit-sheet.png')

handoff='''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: Krusher rest and recovery head fit

## Objective and acceptance
Complete Krusher animations with an attached full head/neck, clean brown hair and a face fitting the existing helmet. Goal active/incomplete; these are reviewed candidates, not owner or station acceptance.

## Accepted decisions and constraints
Krusher Dom / System Administrator / AI & Robotics. James utility suit and matte muted cyan #527C80. Preserve original body motion, density, timing, pivots, tools and helmet shell. Station test first; normal roster and owner saves unchanged.

## Current state
Rest-family-v4:30states/174refs/92unique/72changed,20rear retained. New closed-eye side and raised-chin front complete head/neck sources preserve raw builtin generation, exact prompt, native extraction and hashes. Whole sources rotate with nearest sampling and register to original neck landmarks; no painted bridges. Original rest-v2 full manifests exact, including depth and root profiles.
Recovery-salvage-v2:16states/96refs/86unique/65changed,21retained. Original full manifests, bodies and tools preserved. Full bowed South head registered up3pixels after initial gap rejection; rejected source review retained. Derived bowed visor records source crop/hash; original shell and alpha exact. Eight padded canonical-v6 recovery ends and eight closed salvage loops exact.
Build_rest.py, build_recovery.py, per-pack validators/native fixtures/review builders and record_rest_recovery.py reproduce outputs. All137changed source contexts and targeted native full/small views reviewed. Mobile overview and both original-hold MP4s delivered. Full-bank selection/package remains old until coherent migration; original yellow shoulders remain open for cyan audit.

## Verification
Rest:698independent checks,36full bare head contacts,20exact joins and10reversed choreographies;1290native checks/174captures/engine0/9.83s. Recovery:692independent checks,29bare contacts,8canonical ends/8closed loops;764native checks/96captures/engine0/9.12s. All errors0. Both used scratch APPDATA;2930owner non-log files unchanged. Original-hold replays25.48s and15.36s; encoded duration within one60Hz frame. Source/native prescribed captures do not establish continuous station contact. Existing generated .gd/.uid pairs retained; raster/media LFS attributes checked.

## Next action
Migrate underwater cargo from new water-v3 and recovery-v2 shared endpoints, then interruptions and death. Audit rear/quarter identity and remaining yellow shoulder trim, refresh coherent full bank/package, retarget strict West cues and diagnose service-loss, then actual station/bare-water/full-library review. No approval gate or live generation/native job.
'''
for target in [H/'REST_RECOVERY_HANDOFF.md',R/'character/krusher-rest-family-v4/HANDOFF.md',R/'character/krusher-recovery-salvage-v2/HANDOFF.md']:target.write_text(handoff,encoding='utf-8')
p=R/'character/krusher-complete-animation-v1/progress.json'; progress=read(p); v=progress['visualReview']; v['headConstructionV3'].update(entries); v['status']='head-construction-v3-rest-recovery-partial'; v['remaining']='Underwater cargo/interruption/death migration; rear/quarter identity and muted cyan shoulder audit; coherent full bank/package; strict West cues/service-loss and actual station/bare-water/full-library review.'; p.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
source=(H/'update_cargo_status.ps1').read_text(); start=source.index('    $krusherHeader = @'+chr(39)); end=source.index('\n'+chr(39)+'@',start)+3
header='''## Krusher rest and recovery complete-head candidates - October 4, 2026

Full goal active/incomplete. Rest-v4:30states/174refs/92unique/72revised;
recovery-salvage-v2:16states/96refs/86unique/65revised. Complete authored heads
and necks register to original body/collar poses; original helmets fit full visor
identity. Original whole manifests/clocks/pivots/tools/shell alpha retained.
Rest698independent/1290native; recovery692independent/764native; all errors0.
65full bare source/body contacts,137changed contexts and targeted native full/small
views reviewed.270prescribed captures; scratch APPDATA,2930owner files unchanged.
Original-hold videos25.48/15.36s within one frame; not continuous station acceptance.
Selected full bank remains old. Next underwater cargo/interruption/death,
rear/quarter/cyan shoulder audit, coherent bank/package, West and station review.
Handoff:character/krusher-head-fit-v3/REST_RECOVERY_HANDOFF.md.

'''
(H/'update_rest_recovery_status.ps1').write_text((source[:start]+'    $krusherHeader = @'+chr(39)+'\n'+header+chr(39)+'@'+source[end:]).replace('CURRENT_STATUS.krusher-head-construction-cargo.tmp','CURRENT_STATUS.krusher-head-construction-rest-recovery.tmp'),encoding='utf-8')
print(json.dumps(entries))
