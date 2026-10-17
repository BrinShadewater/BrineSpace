from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
prompt='''Use case: background-extraction. Remove ONLY the plain white background from this exact2x2 atlas, make it genuinely transparent. Preserve the EXACT1254square canvas, equal627square cells, all four source poses at exactly their existing coordinates/scale/margins. No cropping, moving, zooming, reposing, redrawing faces, sharpening, colour changes or new details. Keep mature grey-brown hair/goggles/moustache, matte graphite suit and muted yellow patches as supplied. Clean white background contamination from silhouette edges so there is NO white/pale outline when displayed on dark grey. Preserve genuine grey hair and silver clothing highlights; do not erase them as background. Subject pixels should retain their supplied colour and anatomy; edit only alpha/background-edge contamination. Four different original poses, same grid, no labels or extra artwork.'''
(p/'alpha-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
(p/'alpha-inputs.json').write_text(json.dumps({n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in ['grade-raw.png','alpha-prompt.txt']},indent=2)+'\n')
print('Background-only alpha edit prompt/source hashes frozen.')
