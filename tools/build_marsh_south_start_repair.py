"""Pack the coherent South-start repair without changing historical candidate02."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary
from build_marsh_south_start import sole
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-south-start-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    second='--second-repair' in sys.argv
    path=BASE/('sources/start-03.raw.png' if second else 'sources/start-02.raw.png');raw=Image.open(path).convert('RGBA');w,h=raw.size
    cells=[binary(raw.crop((i*w//4,0,(i+1)*w//4,h))) for i in range(4)]
    ys,xs=np.where(np.array(cells[3])[:,:,3]>0);scale=148/(ys.max()-ys.min()+1)
    idlepath=ROOT/'character/marsh-v2/frames/bare/idle-south/000.png';gaitpath=ROOT/'character/marsh-v2/frames/bare/walk-south/004.png'
    idle=Image.open(idlepath).convert('RGBA');gait=Image.open(gaitpath).convert('RGBA')
    folder='candidate-04' if second else 'candidate-03'
    out=BASE/folder;out.mkdir(exist_ok=True);frames=[idle];records=[]
    for i,cell in enumerate(cells):
        dense=binary(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.BOX),True)
        contact=sole(dense,True if i==2 else None)
        target=(sole(gait,True)[0],sole(idle,True)[1]) if i==2 else sole(idle)
        shift=(round(target[0]-contact[0]),round(target[1]-contact[1]))
        frame=Image.new('RGBA',(184,184));frame.alpha_composite(dense,shift)
        assert np.count_nonzero(np.array(frame)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]),'whole figure clipped'
        frame.save(out/('ruler.png' if i==3 else '%03d.png'%(i+1)))
        if i<3:frames.append(frame)
        yy,xx=np.where(np.array(frame)[:,:,3]>0)
        head=np.array(frame)[:,:,3]>0;head[50:]=False;hy,hx=np.where(head)
        records.append({'cell':[i*w//4,0,(i+1)*w//4,h],'sharedScale':scale,'registration':shift,'supportTarget':target,'bounds':[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())],'headAlphaCentroid':[float(hx.mean()),float(hy.mean())],'role':'neutral ruler' if i==3 else 'interior','sha256':sha(out/('ruler.png' if i==3 else '%03d.png'%(i+1)))})
    frames.append(gait);idle.save(out/'000.png');gait.save(out/'004.png')
    manifest=json.loads((BASE/'candidate-02/manifest.json').read_text());(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    left=sole(frames[3],True);end=sole(gait,True)
    recipe={'status':'unselected repaired source; visual/native verification pending','rawSha256':sha(path),'sharedNeutralScale':float(scale),'cells':records,'idleSha256':sha(idlepath),'gaitSha256':sha(gaitpath),'grade':'none; generation requested reference finish','supportDepthAdvanceDense':left[1]-end[1],'supportDepthAdvanceWorld':(left[1]-end[1])*65.28/148,'supportLateralSeamDense':left[0]-end[0],'supportLateralSeamWorld':(left[0]-end[0])*65.28/148,'gaitJoin':'derive from loaded durations of first4poses plus80ms consumed hold; currently .68s','decision':'Whole coherent strip edit; common neutral scale; complete figures registered without anatomy edits. Pose3 viewer-left support registered to selected gait4 lateral centroid, at selected idle support depth. Root bridges depth; no root lateral motion. Inspect body/head alignment: matching sole alone is insufficient. Historical candidate02 untouched.'}
    (out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    board=Image.new('RGB',(1104,440),'#293b40');draw=ImageDraw.Draw(board)
    for row,folder in enumerate(['candidate-02',folder]):
        for i in range(6):
            file='ruler.png' if i==5 else '%03d.png'%i;im=Image.open(BASE/folder/file).convert('RGBA');x=i*184;y=row*220
            board.paste(im,(x,y+30),im);draw.text((x+4,y+5),folder+' '+['idle','ready','load','left leads','gait4','ruler'][i],fill='white')
    board.save(out/'comparison.png');print('Repaired five slots; common scale',round(float(scale),5),'bounds',[r['bounds'] for r in records],'depth advance',recipe['supportDepthAdvanceDense'],'lateral seam',recipe['supportLateralSeamDense'],'dense pixels')
if __name__=='__main__':main()
