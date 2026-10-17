from pathlib import Path
from PIL import Image,ImageDraw
import json,re,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];grid=r/'scripts/grid_canvas.gd';text=grid.read_text(encoding='utf-8').split('elif actor == "branforth":',1)[1].split('\n\t\tset(actor+',1)[0];selected=None
for match in re.finditer(r'player\.load_manifest\("(res://character/[^"]+\.json)"',text):
    manifest=r/match[1].removeprefix('res://');data=json.loads(manifest.read_bytes())
    for state in data.get('states',[]):
        if state['id']=='walk-west':selected=(manifest,data,state)
assert selected
manifest,data,state=selected;frames=[];files=[grid,manifest];pivot=data['pivot'];scale=148/data['standingHeight']
assert scale==1,(manifest,data['standingHeight'])
for ref in state['frameFiles']:
    f=r/ref.removeprefix('res://') if ref.startswith('res://') else manifest.parent/ref;files.append(f);im=Image.open(f).convert('RGBA');out=Image.new('RGBA',(256,256));out.alpha_composite(im,(round(128-pivot[0]),round(224-pivot[1])));frames.append(out)
cols=8;rows=(len(frames)+cols-1)//cols;board=Image.new('RGBA',(cols*192,rows*215),(48,59,63,255));d=ImageDraw.Draw(board)
for i,im in enumerate(frames):
    x=(i%cols)*192;y=(i//cols)*215;board.alpha_composite(im.crop((64,48,256,240)),(x,y+23));d.text((x+5,y+5),f'normal walk-west {i}',fill='white')
board.convert('RGB').save(p/'normal-walk-west-chronology.png')
# Representative full, head and leg comparisons use actual sources, no bbox fitting.
indices=sorted(set([0,len(frames)//4,len(frames)//2,3*len(frames)//4,len(frames)-1]));base=Image.open(p/'base.png').convert('RGBA');compare=Image.new('RGBA',(256*(len(indices)+1),282),(48,59,63,255));d=ImageDraw.Draw(compare)
for col,(im,label) in enumerate([(base,'new carry master pose')]+[(frames[i],'selected walk '+str(i)) for i in indices]):compare.alpha_composite(im,(col*256,26));d.text((col*256+5,7),label,fill='white')
compare.convert('RGB').save(p/'walk-master-carry-comparison.png')
(p/'walk-donor-inputs.json').write_text(json.dumps({'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'manifest':manifest.relative_to(r).as_posix(),'frameCount':len(frames),'pivot':pivot,'standingHeight':data['standingHeight'],'frameDurationsMs':state.get('frameDurationsMs',[]),'representativeIndices':indices,'visualReviewPending':True,'scope':'Offline ordered literal walk-west selection and complete source chronology; no cargo donor acceptance, authored rig, native cadence or active normal change.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'manifest':manifest.relative_to(r).as_posix(),'frames':len(frames),'indices':indices}))
