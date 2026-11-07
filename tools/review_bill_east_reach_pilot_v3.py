"""Inspect complete authored pose against its unchanged detailed idle donor."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'character/bill-east-idle-interact-joined-v1'
PILOT = PACK / 'head-consistency-pilot-v3'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
receipt = json.loads((PILOT / 'provenance.json').read_text())
assert all(sha(Path(r['path'])) == r['sha256'] for r in receipt['references'])
assert sha(PILOT / 'raw-001.png') == receipt['rawSha256']

def common(path):
    return Image.open(path).convert('RGBA').resize((352, 352), Image.Resampling.LANCZOS)

def bounds(image):
    y, x = np.where(np.asarray(image)[:, :, 3] > 127)
    return [int(x.min()), int(y.min()), int(x.max()+1), int(y.max()+1)]

edited = common(PILOT / 'raw-001.png')
donor = common(PILOT / 'idle-edit-target.png')
guide = common(PILOT / 'reach-pose-guide.png')
master = common(PILOT / 'original-master.png')
prior = Image.new('RGBA', (352, 352))
prior.paste(Image.open(PACK / 'frames/interact-east/001.png').convert('RGBA'), (68, 52))
edited.crop((68, 52, 252, 236)).save(PILOT / 'candidate-001.png')
candidate_mask = np.asarray(edited)[:, :, 3] > 127
donor_mask = np.asarray(donor)[:, :, 3] > 127
outside = candidate_mask.copy()
outside[52:236, 68:252] = False
lower_a, lower_b = candidate_mask[140:], donor_mask[140:]
union = np.count_nonzero(lower_a | lower_b)
report = dict(status='pending_visual_review', donorBounds=bounds(donor), candidateBounds=bounds(edited),
              guideBounds=bounds(guide), lowerBodyIoU=float(np.count_nonzero(lower_a & lower_b)/union),
              opaqueOutsideCompatibilityCanvas=int(outside.sum()), normalAdmission=False,
              scope='Uniform whole352 canvas and184compatibility crop only. No local painting, anatomy fitting or head splice.')
if bounds(edited)[3] != bounds(donor)[3] or outside.any():
    report['status'] = 'geometry_failed_pending_decision'
(PILOT / 'review.json').write_text(json.dumps(report, indent=2)+'\n')
board = Image.new('RGB', (1500, 660), '#17252d')
draw = ImageDraw.Draw(board)
for i, (label, image) in enumerate([('Idle edit target', donor), ('First reach guide', guide), ('Prior candidate', prior), ('New whole pose', edited), ('Original master', master)]):
    view = image.crop((112, 50, 244, 238)).resize((264, 376), Image.Resampling.NEAREST)
    board.paste(view, (i*300+18, 40), view)
    head = image.crop((126, 67, 188, 120)).resize((248, 212), Image.Resampling.NEAREST)
    board.paste(head, (i*300+18, 430), head)
    draw.text((i*300+18, 16), label, fill='white')
board.save(PILOT / 'comparison.png')
print(json.dumps(report))
