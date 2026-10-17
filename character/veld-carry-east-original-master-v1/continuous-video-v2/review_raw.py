from pathlib import Path
import hashlib,json,subprocess
from PIL import Image,ImageDraw
import numpy as np
from scipy import ndimage
P=Path(__file__).resolve().parent;D=P/'raw-review';D.mkdir(exist_ok=True)
g=json.loads((P/'generation.json').read_text(encoding='utf-8'));assert g['status'].lower()=='success'
assert hashlib.sha256((P/'master-input.png').read_bytes()).hexdigest()==g['imageSha256']
probe=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(P/'source.mp4')],capture_output=True,text=True,check=True)
info=json.loads(probe.stdout);(D/'probe.json').write_text(json.dumps(info,indent=2)+'\n',encoding='utf-8')
decode=subprocess.run(['ffmpeg','-y','-v','error','-i',str(P/'source.mp4'),'-fps_mode','passthrough','-threads','1',str(D/'raw-%03d.png')],capture_output=True,text=True)
(D/'decode.log').write_text(decode.stderr,encoding='utf-8')
assert decode.returncode==0,decode.stderr[-1800:]
files=sorted(D.glob('raw-*.png'));rows=[];boards=[]
for start in range(0,len(files),24):
    board=Image.new('RGB',(6*256,4*275),'#202a30');draw=ImageDraw.Draw(board)
    for j,file in enumerate(files[start:start+24]):
        im=Image.open(file).convert('RGB');a=np.array(im).astype(int);green=(a[:,:,1]>a[:,:,0]+40)&(a[:,:,1]>a[:,:,2]+40)&(a[:,:,1]>100)
        lab,n=ndimage.label(~green);sizes=np.bincount(lab.ravel());sizes[0]=0;body=lab==int(sizes.argmax());yy,xx=np.where(body)
        top=int(yy.min());height=int(yy.max()-yy.min()+1);head=body[top:top+round(height*16/148)];hx=np.where(head)[1]
        rec={'frame':start+j,'height':height,'width':int(xx.max()-xx.min()+1),'headWidth':int(hx.max()-hx.min()+1),'top':top,'bottom':int(yy.max()),'skullAxis':float((hx.max()+hx.min())/2)}
        rows.append(rec);thumb=im.copy();thumb.thumbnail((256,256),Image.Resampling.LANCZOS);col=j%6;rr=j//6;board.paste(thumb,(col*256+(256-thumb.width)//2,rr*275+19));draw.text((col*256+3,rr*275+3),f'{start+j} H{height} head{rec["headWidth"]}',fill='white')
    dest=D/f'chronology-{start//24:02}.png';board.save(dest);boards.append(dest.name)
(D/'review.json').write_text(json.dumps({'taskId':g['task_id'],'rawSHA256':hashlib.sha256((P/'source.mp4').read_bytes()).hexdigest(),'frameCount':len(files),'boards':boards,'rows':rows,'visualReview':'pending','scope':'Every raw video frame retained and plotted with original aspect ratio; green segmentation diagnostic only. No selected loop, alpha export, native or controller acceptance.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'frames':len(files),'boards':len(boards),'first':rows[0],'last':rows[-1],'heightRange':[min(r['height'] for r in rows),max(r['height'] for r in rows)]}))
