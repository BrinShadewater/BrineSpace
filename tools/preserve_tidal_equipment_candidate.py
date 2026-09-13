"""Preserve the rejected first camera study without changing runtime selection."""
from pathlib import Path
import shutil,json,hashlib
from PIL import Image
root=Path(__file__).resolve().parents[1]
pack=root/'assets/tidal-owner-v2'
src=Path('C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-04b7b162-f9b1-4eae-8863-186b74a3fcec.png')
dst=pack/'equipment-source-v1.png'
shutil.copyfile(src,dst)
im=Image.open(dst).convert('RGBA')
(pack/'equipment-source-v1.review.json').write_text(json.dumps({'status':'rejected-not-selected','sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'size':im.size,'alpha_extrema':im.getchannel('A').getextrema(),'findings':['Filter retains a tall visible front face; camera is not overhead','Cartridge releases remain at rear/top','Exterior checker pattern must not be integrated'],'next':'Generate explicit plan-view geometry with circular filter lid, horizontal cartridge bodies and bottom service releases'},indent=2)+'\n')
