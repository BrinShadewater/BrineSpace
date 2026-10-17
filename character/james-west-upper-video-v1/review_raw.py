from pathlib import Path
from PIL import Image,ImageDraw
import imageio.v2 as iio
import hashlib,json
p=Path(__file__).resolve().parent
reader=iio.get_reader(str(p/'source.mp4'));meta=reader.get_meta_data();frames=[Image.fromarray(x[:,:,:3]) for x in reader];reader.close()
out=p/'raw-review';out.mkdir(exist_ok=True)
pages=[]
for start in range(0,len(frames),24):
    board=Image.new('RGB',(1440,1370),'#303b40');draw=ImageDraw.Draw(board)
    for j,name in enumerate(['first','last']):
        im=Image.open(p/(name+'-input.png')).convert('RGB').resize((240,240),Image.Resampling.LANCZOS)
        board.paste(im,(j*240,24));draw.text((j*240+4,4),name+' exact endpoint',fill='white')
    for j,frame in enumerate(frames[start:start+24]):
        x=j%6*240;y=274+j//6*274
        board.paste(frame.resize((240,240),Image.Resampling.LANCZOS),(x,y+24));draw.text((x+4,y+4),str(start+j),fill='white')
    name=f'raw-{start:03d}.png';board.save(out/name);pages.append(name)
for i in [0,len(frames)//2,len(frames)-1]:frames[i].save(out/('full-%03d.png'%i))
report={'decodedFrames':len(frames),'fps':meta['fps'],'size':list(meta['size']),'sourceSha256':hashlib.sha256((p/'source.mp4').read_bytes()).hexdigest(),'pages':pages,'visualReviewPending':True,'selected':False,'scope':'All raw upper-crop frames beside actual upper endpoints. No alpha extraction, whole body assembly, native playback or owner acceptance.'}
(out/'review.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['decodedFrames','fps','size','pages']}))
