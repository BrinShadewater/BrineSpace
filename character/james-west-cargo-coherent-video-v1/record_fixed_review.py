from pathlib import Path
import json,hashlib,os,uuid
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'fixed-review'
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    tmp.write_bytes(new);assert path.read_bytes()==old;os.replace(tmp,path)
review=json.loads((out/'review.json').read_bytes())
assert review['frames']==141 and review['canvas']==[256,256]
assert review['sourceSha256']==hashlib.sha256((p/'source.mp4').read_bytes()).hexdigest()
finding='All141 fixed-scale extracted poses/six chronological boards plus seven enlarged foot/head samples reviewed beside original unload endpoint. Boot toe/ankle/heel silhouette shifts through profile rotation, late head tilts down and last pose does not restore original unload-ready gaze/case pose. Source begins unload0, not required outgoing carry-turn010: it cannot replace carry-to-unload bridge. One-pixel white-key recipe leaves pale halo, an extraction failure separate from source motion. Rejected for current bridge replacement; no native or helmet expansion. Foot union bounds are diagnostics, not segmented individual contacts.'
review.update(visualReviewPending=False,sourceAcceptance=False,selected=False,finding=finding,continuousPlaybackWatched=False)
atomic(out/'review.json',(json.dumps(review,indent=2)+'\n').encode())
v=json.loads((p/'VERDICT.json').read_bytes());v.update(fixedReview='fixed-review/review.json',finding=finding,
 next='Author coherent carry-to-unload source using actual carry-turn010 and unload0 endpoint pair, camera/foot/root/master constraints. Preserve normal selection; do not crop-paste independent heads or translate away foot motion. New white-key extraction needs halo treatment before any alpha acceptance.')
atomic(p/'VERDICT.json',(json.dumps(v,indent=2)+'\n').encode())
incoming=r/'character/james-east-cargo-heads-v3/frames/bare/carry-turn-east-west/010.png'
ending=r/'character/james-cargo-material-joined-v1/frames/bare/unload-west/000.png'
board=Image.new('RGB',(1024,288),'#303b40');d=ImageDraw.Draw(board)
for k,(label,path) in enumerate([('required carry entry',incoming),('video first',out/'frames/000.png'),('video last',out/'frames/140.png'),('required unload exit',ending)]):
    im=Image.open(path).convert('RGBA');assert im.size==(256,256)
    bg=Image.new('RGBA',im.size,'#303b40');bg.alpha_composite(im)
    board.paste(bg.convert('RGB'),(k*256,24));d.text((k*256+4,4),label,fill='white')
board.save(out/'endpoints.png')
section='''### James coherent cargo fixed-scale rejection — October 2, 2026

Extracted141decoded768square frames at ONE whole-canvas1/3 scale into256square,
p128224/H148 reference; no translations/bounds fitting/grade or anatomy painting.
Border-connected white key plus one-pixel fringe unmix leaves pale outline: alpha
recipe not accepted. All six chronological boards/141poses and seven enlarged
foot/head samples inspected. Boots shift silhouette/ankle/heel through profile
rotation; late downward gaze and last pose do not restore original unload pose.
Study starts unload0, not required carry-turn010, so REJECTED as bridge replacement.
No native/helmet expansion. Diagnostic foot union bounds are not individual contact
measurements; no continuous watched/master/full-set acceptance. Normal selection
unchanged, no new generation/spend or owner profile access.

Lesson: coherent video preserves adjacent identity better but a settle cycle from
the exit pose cannot supply missing carry-entry articulation. Establish BOTH actual
whole endpoint poses before generating; reject semantic/foot failures before native
expansion. Treat white-key halos separately from motion defects; never hide drift
with per-frame translation/height fitting or blanket recolouring. Next endpoint-
constrained coherent carry-to-unload source, paired helmet/native admission if sound.
Five guides updated; goal active/incomplete. Evidence: character/james-west-cargo-
coherent-video-v1/fixed-review/review.json, endpoints.png, extract_fixed.py/VERDICT.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James coherent cargo video raw review');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,new)
handoff=r/'character/james-floor-case-west-v1/HANDOFF.md'
atomic(handoff,('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James cargo polish

## Objective and acceptance
Complete James set matching masters/style/perspective/height/proportions/matte
grade, followed by cross-family polish. Goal incomplete.

## Accepted decisions and constraints
Normal V9/riseV6/caseV7 unchanged. Preserve owner profile/concurrent crew work.
No per-frame scale/translation to conceal drift; no commit/export.

## Current state
Coherent-video-v1/extract_fixed.py makes141fixed256 exports and review boards.
fixed-review/review.json and VERDICT record rejection for bridge replacement.
Both endpoint comparison and extraction halo failure retained. Five guides updated.

## Verification
All141 extracted poses/six boards and seven enlarged foot/head samples inspected.
Foot silhouettes shift, late gaze and case pose fail exit. Video begins unload0,
not actual carry-turn010. White-key alpha leaves halo. Source hashes checked.
No native/helmet expansion or full-set acceptance; no owner profile access/spend.
Normal integration checks retain their earlier revisions. No live provider job.

## Next action
Review required carry/unload endpoint board, then author coherent bridge from
actual entry with exit constraint. Reject source defects before helmet/native
expansion. Other cardinals, natural contexts and full master/cross-family polish
remain. Goal active/incomplete; no blocker.
''').encode())
print('141 fixed exports reviewed; study rejected for bridge replacement; five guides/handoff updated.')
