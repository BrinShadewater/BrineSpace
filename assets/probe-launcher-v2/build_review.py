"""Package native mechanics captures for the existing local review server."""
from pathlib import Path
from PIL import Image,ImageDraw
import shutil

PACK=Path(__file__).resolve().parent
OUT=PACK.parent/'room-risers-expansion-v1/special-north/launcher'
frames=[Image.open(f).convert('RGB') for f in sorted((PACK/'review').glob('frame-*.png'))]
assert len(frames)==265
frames[0].save(PACK/'launch-recovery.webp',save_all=True,append_images=frames[1:],duration=42,loop=0,lossless=True)
sheet=Image.new('RGB',(1536,1060),(25,34,40));draw=ImageDraw.Draw(sheet)
for i,n in enumerate([0,100,120,144,190,264]):
    x=(i%3)*512;y=(i//3)*530
    sheet.paste(frames[n],(x,y+18));draw.text((x+8,y+2),f'Frame {n}',fill='white')
sheet.save(PACK/'motion-sheet.png')
for name in ['launch-recovery.webp','motion-sheet.png']:shutil.copy2(PACK/name,OUT/name)
page=OUT/'index.html'
html=page.read_text(encoding='utf8')
html=html.replace('A new rail base seats inside the wall portal. Hydraulic jaws release, the cradle advances during launch, then draws back and clamps after recovery.', 'The shortened platform meets the bottom edge of the riser wall. The probe enters the dark tunnel and passes behind its steel surround, then emerges during recovery. Hydraulic jaws and cradle follow the existing launch clock.')
html=html.replace('src="launch-recovery.webp"','src="launch-recovery.webp?v=short-tunnel"')
page.write_text(html,encoding='utf8')
for suffix in ['summary.json','review.log']:
    shutil.copy2(PACK.parent/'room-risers-expansion-v1/evidence'/('native-survey_probe_bay-'+suffix),PACK/('native-'+suffix))
print('265-frame shortened-platform/tunnel preview refreshed.')
