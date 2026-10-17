from pathlib import Path
import json

P = Path(__file__).resolve().parent
root = P.parents[1]
reason = 'Visual source review: both feet lift together for extended sections, producing hovering/hopping rather than a complete alternating walk. Automatic loop selection cannot repair this motion.'
g = json.loads((P / 'generation.json').read_text())
g.update(balanceAfter=68, actualCredits=4, resultUrl='https://d8j0ntlcm91z4.cloudfront.net/user_3DI8EyzxtV7c98Xbr9UTZQAAYSr/hf_20260928_050924_c5a75d97-b725-4167-b776-aea034cddbf5.mp4')
(P / 'generation.json').write_text(json.dumps(g, indent=2) + '\n')
rejection = dict(status='rejected_not_for_runtime', reason=reason, reviewed=['source-contact.png', 'gait-analysis.png'], automaticExportIsDiagnosticOnly=True, furtherPaidRetries=0)
(P / 'rejection.json').write_text(json.dumps(rejection, indent=2) + '\n')
m = json.loads((P / 'manifest.json').read_text())
m.update(status='rejected_not_for_runtime', rejectionReason=reason)
(P / 'manifest.json').write_text(json.dumps(m, indent=2) + '\n')
(P / 'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill rear trial — rejected</title><style>body{background:#263139;color:#eee;font:18px system-ui;max-width:1100px;margin:30px auto}img{max-width:100%}a{color:#9ce}</style><h1>Bill rear trial — rejected</h1><p>' + reason + '</p><p>4 credits used; 68 remaining. Not installed. The earlier rear walk remains on review hold.</p><video controls loop style="max-width:100%" src="source.mp4"></video><p><a href="../bill-video-south-v3/">Latest front walk</a></p><img src="source-contact.png" alt="Source poses showing simultaneous foot lifts">')
ledger = root / 'docs/CREW_ANIMATION_BUDGET_2026-09-27.md'
with ledger.open('a', encoding='utf-8') as f:
    f.write('\nBill north v2: one 4-credit darker-master trial, confirmed balance68; total paid since116 snapshot48. Rejected after visual source review: simultaneous foot lifts/hovering, not an alternating walk. No additional paid retry. Diagnostic export must not be promoted.\n')
status = root / 'docs/CURRENT_STATUS.md'
b = status.read_bytes(); i = b.index(b'\n') + 1
entry = '\n## Bill rear retry rejected — September 27, 2026\n\nContinued after owner review of south v3. North v2 preserves the darker reference but fails gait: both feet lift together/hover. Source and diagnostics saved; manifest explicitly rejected, not installed. Earlier north v1 remains on review hold. One 4-credit attempt; confirmed balance68. Next rear attempt needs a different motion approach rather than more restrictive small-step wording. [Handoff](BILL_NORTH_V2_REJECTION_2026-09-27.md).\n\n'
status.write_bytes(b[:i] + entry.encode() + b[i:])
assert json.loads((P / 'manifest.json').read_text())['status'] == 'rejected_not_for_runtime'
assert (P / 'source.mp4').stat().st_size > 100000
print('Rejection recorded; source preserved; balance 68; no runtime files changed.')
