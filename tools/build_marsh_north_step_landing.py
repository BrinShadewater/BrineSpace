"""Package a whole forward-planted North stance and its shared neutral ruler."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-north-step-v1'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    rawpath=BASE/'sources/north-step-08.png'; raw=Image.open(rawpath).convert('RGBA'); cells=[]
    cuts=[0,round(raw.width/2),raw.width]
    for i in range(2):
        a=np.array(raw.crop((cuts[i],0,cuts[i+1],raw.height)))
        a[:,:,3]=np.where(a[:,:,3]>=128,255,0); a[a[:,:,3]==0]=0; cells.append(Image.fromarray(a))
    idlepath=ROOT/'character/marsh-v2/frames/bare/idle-north/000.png'; idle=Image.open(idlepath).convert('RGBA')
    box=cells[1].getbbox(); scale=(idle.getbbox()[3]-idle.getbbox()[1])/(box[3]-box[1])
    def sole(im,left):
        a=np.array(im); yy,xx=np.indices(a[:,:,3].shape); box=im.getbbox(); split=(box[0]+box[2])/2
        # This two-pose stance has distinct shoes, visually checked. Measure the
        # full actual sole rather than dropping its rounded inner tip.
        mask=(a[:,:,3]>0)&(yy>=box[1]+.65*(box[3]-box[1]))&((xx<split) if left else (xx>=split))
        bottom=int(np.where(mask)[0].max()); return [float(np.median(np.where(mask & (yy>=bottom-2))[1])),bottom]
    target=sole(idle,False); output=BASE/'candidate-08'; output.mkdir(exist_ok=True); rendered=[]; extraction=[]
    for i,im in enumerate(cells):
        support=sole(im,False)
        sized=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.BOX)
        a=np.array(sized); a[:,:,3]=np.where(a[:,:,3]>=128,255,0); a[a[:,:,3]==0]=0
        sized=Image.fromarray(a); resized_support=sole(sized,False)
        offset=[round(target[k]-resized_support[k]) for k in range(2)]
        frame=Image.new('RGBA',(184,184)); frame.alpha_composite(sized,offset)
        box=frame.getbbox(); assert box[0]>0 and box[1]>0 and box[2]<184 and box[3]<184
        assert sole(frame,False)[1]==target[1]
        rendered.append(frame); extraction.append({'cell':i,'sourceSupport':support,'resizedSupport':resized_support,'targetSupport':target,'offset':offset,'bounds':box,'width':box[2]-box[0],'leftContact':sole(frame,True),'rightContact':sole(frame,False)})
    rendered[0].save(output/'landing.png'); rendered[1].save(output/'neutral-ruler.png')
    frames=[idle,rendered[0],idle]
    for i,im in enumerate(frames): im.save(output/('%03d.png'%i))
    manifest={'frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'states':[{'id':'north-step-landing-study','frameFiles':['000.png','001.png','002.png'],'frameDurationsMs':[120]*3,'loop':False,'facings':['north']*3,'waterKinds':['walk']*3,'waterPoses':[False]*3,'depthOffsets':[0.0]*3}]}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    gap=extraction[0]['rightContact'][1]-extraction[0]['leftContact'][1]
    recipe={'status':'unselected isolated landing study; no complete motion/contact acceptance','rawSha256':sha(rawpath),'promptSha256':sha(BASE/'sources/north-step-08.prompt.txt'),'sourceCellBoundaries':cuts,'neutralRulerCell':1,'standingScale':scale,'extraction':extraction,'landingDepthPixels':gap,'impliedNorthLength':gap*65.28/148,'alpha':'128 then BOX then128; invisible RGB zero; original partial-alpha halo retained in raw','grade':'none','frameHashes':{('%03d.png'%i):sha(output/('%03d.png'%i)) for i in range(3)},'limits':'Isolated grounded-forward stance plus exact idle comparison. Three presentation holds are an audition, not a short-step animation. No root travel/controller/contact/safety/Continue/normal selection.'}
    (output/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    board=Image.new('RGB',(184*4,230),'#293b40'); draw=ImageDraw.Draw(board)
    for i,(im,label) in enumerate([(idle,'Selected idle'),(rendered[0],'New landing'),(rendered[1],'Source neutral'),(idle,'Selected idle')]):
        board.paste(im,(184*i,25),im); draw.text((184*i+4,6),label,fill='white')
    board.save(output/'comparison.png')
    print('Landing depth',gap,'dense pixels;',round(recipe['impliedNorthLength'],3),'world units; widths',[e['width'] for e in extraction])
if __name__=='__main__': main()
