from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'close_lower_window_v203.py').read_text(encoding='utf-8').replace("out=p/'lower-window-v203'", "out=p/'lower-window-v208'").replace('import json,hashlib,subprocess','import json,hashlib,subprocess\nfrom PIL import Image\nimport numpy as np')
a=s.index('findings=');b=s.index('\nledger=',a)
s=s[:a]+"findings="+repr(['Four selected lower repairs retain readable overlapping feet/hardware in eight source repair boards, six-frame source board and all six paired native captures/four sizes. Source review preceded native launch.', 'Phase29upper-tail178.84to169.75/median69.14to67.20;30upper-tail181.69to170.68/median69.00to62.43;31upper-tail158.68to154.26/median58.93to59.71;32upper-tail159.62to156.56/median60.49to56.70.31/32were already darker before repair; different admitted masks and overlap prevent treating these as identical material samples. Full moving grade remains open;33original boots brighter.', 'Phase30uses knee-protectionV142as base, not earlier unprotectedV138. Rectangle108,157,127,183excluded and exact to V142 and original same-phase pixels in both gear variants. Original knee brightness retained; no master anatomy/grade acceptance.', 'Full original alpha/one-pixel rim/rows above181/paired body below110 exact. Six40ms sources240ms finite fixture verified. Not continuous full49motion/contact/no-flash/seam, normal lifecycle or all-family acceptance.'])+s[b:]
s=s.replace("[(25,199,'b46373c3-ba83-4872-b68b-49e8d60e4019'),(26,200,'91e035f9-90e6-4fc7-ad93-2c8287b9d67f'),(27,201,'946e8d50-4506-4577-8b25-61f24ac005bc'),(28,202,'9991e4fe-9746-44c3-9b9d-91731eb57678')]", "[(29,204,'f2d7762e-9315-4ad7-bf99-e809980511af'),(30,205,'a01d7643-c725-4bbf-a259-ad7fc350c00c'),(31,206,'185ca6ab-ac30-4426-898a-d0031893ee1d'),(32,207,'d2c5118f-ceae-4a9b-b9a9-90ed1ff8885a')]")
s=s.replace('+[25,26,27,28]','+[29,30,31,32]').replace('starting29','starting33').replace('sourceIndices=[24,25,26,27,28,29]','sourceIndices=[28,29,30,31,32,33]')
a=s.index('section=')
roi='''
roi=(108,157,127,183);x0,y0,x1,y1=roi;roi_sha={}
for mode in ['bare','helmet']:
 original=p/f'master-head-review-v16/{mode}-030.png';prior=p/f'knee-protection-phase30-v142/{mode}-head-protected.png';selected=p/f'lower-material-phase30-v205/{mode}-head-protected.png'
 arrays=[np.array(Image.open(f).convert('RGBA'))[y0:y1,x0:x1] for f in [original,prior,selected]]
 assert np.array_equal(arrays[0],arrays[1]) and np.array_equal(arrays[1],arrays[2])
 roi_sha.update({f.relative_to(r).as_posix():sha(f) for f in [original,prior,selected]})
(out/'knee-preservation.json').write_text(json.dumps(dict(rectangle=roi,exactToOriginalAndV142BothGear=True,sourceSha256=roi_sha,retainedOriginalBrightness=True,masterAnatomyAcceptance=False),indent=2)+'\\n',encoding='utf-8')
f=p/'lower-material-phase30-v205/package-review.json';d=json.loads(f.read_bytes());d.update(protectedRectangles=[list(roi)],protectedRectanglesExact=True,restoredKneeExactToOriginal=True);f.write_text(json.dumps(d,indent=2)+'\\n',encoding='utf-8')
'''
s=s[:a]+roi+s[a:]
a=s.index('section=');b=s.index('\nguides=',a)
section='''### James carrying lower finish phases29 to32 preserves restored knee - October3,2026

V204phase29/V205phase30/V206phase31/V207phase32 retained provisionally after
eight source repair boards reviewed BEFORE native launch; V208phase28..33source
board/all six paired native captures at four sizes visually reviewed. Overlapping
feet/hardware readable. Full alpha, one-pixel rim, rows above181 and paired body
below110 exact;763/631/765/932admitted,64773/64905/64771/64604outside-exact pixels.
Internal hardware remains visually assessed, not original-master anatomy proof.

V205uses V142knee-protected body as base, not unprotectedV138. Restored rectangle
108,157,127,183excluded from RGB admission, exact toV142AND original same-phase
pixels for both gears, independently verified/frozen in knee-preservation.json.
Original knee brightness retained; neither this nor fixed alpha establishes master
grade/proportions. Prep records explicit base folder/protected rectangles and
freezes both base gear files; packaging preserves/asserts each rectangle.
Lesson: carry earlier landmark repairs forward when expanding edit regions.
A general upper-row guard can cut through a restored fitting's buffer; exclude
its whole recorded ROI rather than accidentally repainting its lowest rows.

Local95thpercentiles29:178.84to169.75;30:181.69to170.68;31:158.68to154.26;
32:159.62to156.56. Medians69.14to67.20,69.00to62.43,58.93to59.71,60.49to56.70.
31/32already darker before repair; different masks/overlap are not equivalent
material samples. Full moving grade remains open. Original33boots brighter.
V20886checks/0failures/sixcaptures, original40ms each240msfinite window, engine
terminal; scratch APPDATA owner profile unchanged, frozen hashes stable. Ledger
29..32 nowV204/V205/V206/V207, priorV136/V142/V139/V140 preserved;49/49coverage
unchanged. Normal selection unchanged. V173full-cycle evidence remains specific
to earlier frozen sources. Continue finish33and beyond; moving grade/knee brightness,
full49master anatomy/contact/flash/seam, normal lifecycle and all-family polish.
No final source/full-goal acceptance. Evidence: lower-window-v208/review.json.
'''
s=s[:a]+"section="+repr(section)+s[b:]
s=s.replace("'### James carrying lower finish phases21 to24 with neighbour remake'", "'### James carrying lower finish phases25 to28 overlap review'")
a=s.index('handoff=');b=s.index('\nfor folder',a)
handoff='''# Project handoff

Updated: October3,2026. Goal: full James master-matched library, then all-family
consistency/polish. Active; candidate coverage does not establish final acceptance.

Constraints: master authority, matte charcoal/yellow/worn metal, original poses;
preserve prior landmark repairs, owner profile and normal runtime selection.

Changed: V204phase29/V205phase30/V206phase31/V207phase32 paired sources/raw/
frozen prompts/references; V208six-frame manifests/APNG/native probe/paired UID,
captures/review/independent knee preservation; helpers support explicit base and
protected ROIs/freeze both gears; ledger; status/pipeline/bible/crew references.

Checks:86native/0failures/sixcaptures,240ms,engine0/no timeout, scratch profile
owner unchanged, frozen hashes stable. Eight repair boards reviewed before native
launch; source window and all six paired captures/four sizes visually reviewed.
V205ROI108,157,127,183exact to original andV142bothgears; original knee brightness
retained. Full alpha/rim/upper rows exact; interior geometry visually assessed.

Remaining: lower finish33and beyond; moving grade/knee brightness, full49master
anatomy/contact/flash/seam; versioned normal carrying lifecycle and all-family
consistency. No normal change, continuous-motion or final master acceptance.
V173full-cycle evidence remains frozen to its earlier source versions.
'''
s=s[:a]+"handoff="+repr(handoff)+s[b:]
s=s.replace('retainedPhases=[25,26,27,28]','retainedPhases=[29,30,31,32]')
(p/'close_lower_window_v208.py').write_text(s,encoding='utf-8')
