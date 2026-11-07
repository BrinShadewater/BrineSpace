"""Package three authored transfer/closure figures with one neutral ruler."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]; BASE=ROOT/'character/marsh-north-step-v1'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    rawpath=BASE/'sources/north-step-09.png'; raw=Image.open(rawpath).convert('RGBA'); cells=[]
    cuts=[round(i*raw.width/3) for i in range(4)]
    for i in range(3):
        a=np.array(raw.crop((cuts[i],0,cuts[i+1],raw.height))); a[:,:,3]=np.where(a[:,:,3]>=128,255,0); a[a[:,:,3]==0]=0; cells.append(Image.fromarray(a))
    idle=Image.open(ROOT/'character/marsh-v2/frames/bare/idle-north/000.png').convert('RGBA')
    neutral=cells[2].getbbox(); scale=(idle.getbbox()[3]-idle.getbbox()[1])/(neutral[3]-neutral[1])
    def contact(im):
        a=np.array(im); yy,xx=np.indices(a[:,:,3].shape); box=im.getbbox(); split=(box[0]+box[2])/2
        mask=(a[:,:,3]>0)&(yy>box[1]+.65*(box[3]-box[1]))&(xx<split)
        bottom=int(np.where(mask)[0].max()); return [float(np.median(np.where(mask & (yy>=bottom-2))[1])),bottom]
    target=contact(idle); output=BASE/'candidate-09'; output.mkdir(exist_ok=True); frames=[]; extraction=[]
    for i,im in enumerate(cells):
        sized=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.BOX)
        a=np.array(sized); a[:,:,3]=np.where(a[:,:,3]>=128,255,0); a[a[:,:,3]==0]=0; sized=Image.fromarray(a)
        anchor=contact(sized); offset=[round(target[k]-anchor[k]) for k in range(2)]
        frame=Image.new('RGBA',(184,184)); frame.alpha_composite(sized,offset); box=frame.getbbox()
        assert box[0]>0 and box[1]>0 and box[2]<184 and box[3]<184 and contact(frame)[1]==target[1]
        frame.save(output/('%03d.png'%i)); frames.append(frame); extraction.append({'cell':i,'resizedSupport':anchor,'offset':offset,'bounds':box,'supportContact':contact(frame),'width':box[2]-box[0]})
    recipe={'status':'unselected whole transfer/closing source study; motion/contact/native joins pending','rawSha256':sha(rawpath),'promptSha256':sha(BASE/'sources/north-step-09.prompt.txt'),'sourceCellBoundaries':cuts,'neutralRulerCell':2,'standingScale':scale,'supportSide':'left','extraction':extraction,'grade':'none','alpha':'128 then BOX then128; invisible RGB zero','frameHashes':{('%03d.png'%i):sha(output/('%03d.png'%i)) for i in range(3)},'limits':'Left support registered to selected neutral floor for source inspection only. Full-step/root-dependent registration, actual travel and Continue not yet implemented.'}
    (output/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    board=Image.new('RGB',(184*5,230),'#293b40'); draw=ImageDraw.Draw(board)
    for i,(im,label) in enumerate([(idle,'Selected idle'),(frames[0],'Weight transfer'),(frames[1],'Right closes'),(frames[2],'Source neutral'),(idle,'Selected idle')]):
        board.paste(im,(184*i,25),im); draw.text((184*i+4,6),label,fill='white')
    board.save(output/'comparison.png'); print('Transfer widths',[e['width'] for e in extraction],'single scale',round(scale,5))
if __name__=='__main__': main()
