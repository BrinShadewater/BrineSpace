from pathlib import Path
import json, hashlib, shutil
import imageio.v2 as iio
from PIL import Image, ImageDraw

P=Path(__file__).resolve().parent
C=P.parent
src=C/'branforth-video-north-v2/source.mp4'
r=iio.get_reader(src)
frames=[r.get_data(i) for i in range(36,72)]
fps=r.get_meta_data()['fps'];r.close()
assert fps==24 and len(frames)==36
# Two repetitions of the owner's accepted complete stride. No interpolation.
with iio.get_writer(P/'driving-walk.mp4',fps=fps,codec='libx264',quality=9,macro_block_size=1) as w:
    for a in frames*2:w.append_data(a)
shutil.copy2(C/'bill-video-north-v2/master-input.png',P/'bill-master.png')
prompt='Use the reference image for Bill\'s appearance and the driving video for his walking motion. Viewed directly from behind, Bill walks in place with the same alternating leg action and restrained arm swing as the driving character. Preserve Bill\'s body proportions, dark brown hair, deep charcoal suit, silver hardware, burgundy shoulder patches and his own backpack and equipment. Keep the camera fixed, character centered, consistent scale and lighting, and the plain green background.'
(P/'prompt.txt').write_text(prompt)
meta=dict(status='prepared_pending_explicit_free_generation_request',model='hf_mult_motion_control',resolution='720p',count=1,use_free_gens=True,sourceVideo=str(src.relative_to(C)),sourceSha256=hashlib.sha256(src.read_bytes()).hexdigest(),sourceFrames=list(range(36,72))*2,sourceFps=fps,durationSeconds=3,derivation='Two repetitions of the accepted 36-frame cycle at original cadence. No new poses or retiming.',appearance='bill-video-north-v2/master-input.png',prompt=prompt,creditFallbackAllowed=False)
(P/'request.json').write_text(json.dumps(meta,indent=2)+'\n')
sheet=Image.new('RGB',(1152,640),'#263139');d=ImageDraw.Draw(sheet)
bill=Image.open(P/'bill-master.png').convert('RGB').resize((384,384))
sheet.paste(bill,(0,40));d.text((12,12),'BILL / APPEARANCE REFERENCE',fill='white')
for j,n in enumerate([0,6,12,18,24,30]):
    im=Image.fromarray(frames[n]).resize((256,256));x=384+(j%3)*256;y=40+(j//3)*288
    sheet.paste(im,(x,y));d.text((x+8,y+260),f'Driving source frame {36+n}',fill='white')
d.text((12,600),'Accepted Branforth stride, repeated twice. Bill keeps his own uniform and equipment.',fill='white')
sheet.save(P/'input-review.png')
rr=iio.get_reader(P/'driving-walk.mp4');assert rr.count_frames()==72;rr.close()
print('Prepared 72-frame / 3-second driving clip and Bill appearance reference. No generation submitted.')
