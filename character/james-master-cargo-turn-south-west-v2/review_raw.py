from pathlib import Path
from PIL import Image,ImageDraw
import imageio.v2 as iio
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
inputs=json.loads((p/'inputs.json').read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in inputs['preCallSha256'].items())
reader=iio.get_reader(str(p/'source.mp4'));meta=reader.get_meta_data();frames=[Image.fromarray(x[:,:,:3]) for x in reader];reader.close();assert meta['size']==(768,768)
out=p/'raw-review';out.mkdir(exist_ok=True);pages=[]
for start in range(0,len(frames),24):
    board=Image.new('RGB',(1440,1370),'#303b40');draw=ImageDraw.Draw(board)
    for j,name in enumerate(['first','last']):
        im=Image.open(p/(name+'-input.png')).convert('RGB').resize((240,240),Image.Resampling.LANCZOS)
        board.paste(im,(j*240,24));draw.text((j*240+4,4),name+' supplied canonical endpoint',fill='white')
    for j,frame in enumerate(frames[start:start+24]):
        x=j%6*240;y=274+j//6*274;board.paste(frame.resize((240,240),Image.Resampling.LANCZOS),(x,y+24));draw.text((x+4,y+4),str(start+j),fill='white')
    name=f'raw-{start:03d}.png';board.save(out/name);pages.append(name)
indices=[0,round((len(frames)-1)/4),round((len(frames)-1)/2),round(3*(len(frames)-1)/4),len(frames)-1]
board=Image.new('RGB',(1792,590),'#303b40');draw=ImageDraw.Draw(board)
samples=[('supplied South',Image.open(p/'first-input.png').convert('RGB')),('supplied West',Image.open(p/'last-input.png').convert('RGB'))]+[(str(i),frames[i]) for i in indices]
for j,(label,im) in enumerate(samples):
    small=im.resize((256,256),Image.Resampling.LANCZOS);board.paste(small,(j*256,24));draw.text((j*256+4,4),label,fill='white')
    crop=small.crop((96,56,176,136)).resize((256,256),Image.Resampling.NEAREST);board.paste(crop,(j*256,300))
board.save(out/'endpoint-samples.png')
for i in [0,len(frames)-1]:frames[i].save(out/('full-%03d.png'%i))
report={'decodedFrames':len(frames),'fps':meta['fps'],'size':list(meta['size']),'sourceSha256':hashlib.sha256((p/'source.mp4').read_bytes()).hexdigest(),'pages':pages,'sampleIndices':indices,'visualReviewPending':True,'selected':False,'scope':'All raw wholebody frames beside supplied canonical endpoints, common uniform256 display only. No alpha extraction/gear/native/normal source admission or continuous watched-motion acceptance.'}
(out/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:report[k] for k in ['decodedFrames','fps','size','pages','sampleIndices']}))
