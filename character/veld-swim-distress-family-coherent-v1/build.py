"""Consolidate independently authored cardinal candidates without regrading pixels."""
from pathlib import Path
import copy,json,hashlib,shutil
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];DIRECTIONS=['east','west','north','south']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks=0;bindings=[];images={};manifests={}
 for gear in ['bare','helmet']:
  states=[];template=None
  for direction in DIRECTIONS:
   source=R/f'character/veld-swim-distress-{direction}-coherent-v1';path=source/f'{gear}-manifest.json';m=json.loads(path.read_text());s=copy.deepcopy(m['states'][0]);key='swim-distress-'+direction
   assert s['id']==key and m['pivot']==[128,128] and m['standingHeight']==148;checks+=1
   assert s['frameDurationsMs']==[160]*6 and s['loop'] and s['waterPoses']==[True]*6;checks+=1
   inputs=[];files=[];row=[]
   master=R/f"character/veld-water-{direction}-coherent-v1/frames/{gear}/swim-{direction}/000.png"
   for i,f in enumerate(s['frameFiles']):
    authored=source/f;src=master if i in [0,5] else authored;out=P/f'frames/{gear}/{key}/{i:03}.png';out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,out)
    assert sha(src)==sha(out);checks+=1
    files.append(out.relative_to(P).as_posix());inputs.append({'file':src.relative_to(R).as_posix(),'sha256':sha(src),'slot':i,'role':'selected_swim_exact_join' if i in [0,5] else 'authored_gesture','authoredInput':authored.relative_to(R).as_posix(),'authoredSha256':sha(authored)});row.append(Image.open(out).convert('RGBA'))
   assert sha(P/files[0])==sha(master) and sha(P/files[5])==sha(master);checks+=2
   s['frameFiles']=files;states.append(s);template=m;images[(gear,direction)]=row
   bg=[]
   for im in row:
    canvas=Image.new('RGBA',im.size,'#202a30');canvas.alpha_composite(im);bg.append(canvas.convert('RGB'))
   bg[0].save(P/f'{gear}-{direction}-distress.gif',save_all=True,append_images=bg[1:],duration=[160]*6,loop=0,disposal=2)
   bindings.append({'gear':gear,'direction':direction,'manifest':path.relative_to(R).as_posix(),'manifestSha256':sha(path),'frames':inputs})
  manifest={**template,'name':'Veld coherent cardinal swimming distress '+gear,'states':states,'status':'selected_local_family_continuous_motion_polish_pending'}
  (P/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');manifests[gear]=manifest
 board=Image.new('RGBA',(7*142,8*165),'#202a30');draw=ImageDraw.Draw(board)
 for d,direction in enumerate(DIRECTIONS):
  for g,gear in enumerate(['bare','helmet']):
   row=d*2+g;reference=Image.open(R/f'character/veld-water-{direction}-coherent-v1/frames/{gear}/swim-{direction}/000.png').convert('RGBA')
   for i,image in enumerate([reference]+images[(gear,direction)]):
    board.alpha_composite(image.resize((142,142),Image.Resampling.LANCZOS),(i*142,row*165+20));draw.text((i*142+3,row*165+2),direction+' '+gear+(' master' if i==0 else ' '+str(i-1)),fill='white')
 board.save(P/'station-scale-family-contact.png')
 (P/'source-bindings.json').write_text(json.dumps({'checks':checks,'failures':0,'states':8,'references':48,'sourceBindings':bindings,'scope':'32 exact authored interiors plus16 exact selected-swim entry/closure donors; not normal-loader selection or whole-world motion acceptance'},indent=2)+'\n')
 (P/'index.html').write_text('<meta charset="utf-8"><title>Veld cardinal swimming distress candidates</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:24px}img{max-width:100%}</style><h1>Veld cardinal swimming distress — selected family</h1><p>Four independently authored directions, paired bare/native helmets, selected prone cameras and material grade. Eight states/48refs. Selected swim pose joins slots0/5 exactly; authored gesture interiors retained byte-exact. Source provenance distinguishes both donors. Normal loader now selects this family. Lifecycle, all-phase reset, furnished/disk and physical escape evidence are recorded separately. Continuous motion and cross-family polish remain. <a href="motion.html">Play beside selected swim masters</a>.</p><img src="station-scale-family-contact.png">'+''.join(f'<h2>{d}</h2><img src="bare-{d}-distress.gif"><img src="helmet-{d}-distress.gif">' for d in DIRECTIONS))
 print(f'{checks} source-consolidation/registration/timing checks PASS;8states/48refs;32 authored interiors unchanged,16 exact selected master joins')
if __name__=='__main__':main()
