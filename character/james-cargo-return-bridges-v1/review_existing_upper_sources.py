from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'existing-upper-source-review';out.mkdir(exist_ok=True)
rows=[]
def add(path,label,gear,pivot=(128,224)):
    im=Image.open(path).convert('RGBA');canvas=Image.new('RGBA',(256,256))
    canvas.alpha_composite(im,(round(128-pivot[0]),round(224-pivot[1])))
    rows.append((gear,label,canvas,path))
for gear in ['bare','helmet']:
    for index in [1,2]:add(p/f'frames-v9/{gear}/{index:03d}.png',f'V9 interior{index}',gear)
    mp=r/'character/james-east-cargo-heads-v3'/f'{gear}-manifest.json';m=json.loads(mp.read_bytes())
    for key,indices in [('carry-turn-east-west',[7,8,9,10]),('carry-turn-west-east',[0,1,2,3])]:
        s=next(x for x in m['states'] if x['id']==key)
        for i in indices:
            ref=s['frameFiles'][i];path=r/ref[6:] if ref.startswith('res://') else mp.parent/ref
            add(path,key+' '+str(i),gear,m['pivot'])
    mp=r/'character/james-cargo-turn-south-west-v1'/f'{gear}-manifest.json';m=json.loads(mp.read_bytes())
    s=next(x for x in m['states'] if x['id']=='carry-turn-south-west')
    for i in range(max(0,len(s['frameFiles'])-4),len(s['frameFiles'])):
        ref=s['frameFiles'][i];path=r/ref[6:] if ref.startswith('res://') else mp.parent/ref
        add(path,'south-west '+str(i),gear,m['pivot'])
    refs=json.loads((p/'reference-evidence.json').read_bytes())['sources']
    idle=next(x for x in refs if x['mode']==gear and x['key']=='idle-west')
    add(r/idle['path'],'selected idle reference',gear,idle['pivot'])
pages=[];report=[]
for gear in ['bare','helmet']:
    selected=[x for x in rows if x[0]==gear]
    for page in range((len(selected)+4)//5):
        board=Image.new('RGB',(5*320,590),'#303b40');draw=ImageDraw.Draw(board)
        for col,item in enumerate(selected[page*5:page*5+5]):
            _,label,im,path=item;x=col*320
            draw.text((x+5,5),gear+' '+label,fill='white');board.paste(im,(x+32,25),im)
            bg=Image.new('RGBA',(256,256),'#303b40');bg.alpha_composite(im)
            board.paste(bg.crop((100,60,166,133)).convert('RGB').resize((264,292),Image.Resampling.NEAREST),(x+28,288))
            report.append({'gear':gear,'label':label,'source':str(path.relative_to(r)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        file=f'{gear}-{page}.png';board.save(out/file);pages.append(file)
(out/'review.json').write_text(json.dumps({'visualReviewPending':True,'sources':report,'pages':pages,'scope':'Existing whole sources and diagnostic upper crops, source reuse feasibility only; no new raster painting, source selection, native motion or master acceptance.'},indent=2)+'\n')
print(f'{len(rows)} registered source presentations, {len(pages)} boards.')
