from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[1]
C=json.loads((P/'source-bindings.json').read_text())['coverage']
for mode in ['body','equipment']:
    for key in C[mode]:
        if not key.startswith('idle-'):C[mode][key]['path']='character/james-torch-material-residue-v2/'+('bare' if mode=='body' else 'helmet')+'-manifest.json'
cache={};records=[];boards=[]
def load(mode,key):
    path=R/C['body' if mode=='bare' else 'equipment'][key]['path']
    if path not in cache:cache[path]=json.loads(path.read_text())
    m=cache[path];s=next(s for s in m['states'] if s['id']==key)
    assert m['standingHeight']==148
    files=[R/f.removeprefix('res://') if f.startswith('res://') else (path.parent/f).resolve() for f in s['frameFiles']]
    return m,s,files
def plane(file,m):
    im=Image.open(file).convert('RGBA');out=Image.new('RGBA',(224,224));out.alpha_composite(im,(112-int(m['pivot'][0]),204-int(m['pivot'][1])));return out
for direction in ['east','north','south','west']:
    poses=[]
    for key in ['torch-draw-'+direction,'weld-'+direction,'torch-stow-'+direction]:
        m,s,files=load('bare',key)
        for i,file in enumerate(files):poses.append((key,i))
    masters={mode:plane(load(mode,'idle-'+direction)[2][0],load(mode,'idle-'+direction)[0]) for mode in ['bare','helmet']}
    master_board=Image.new('RGB',(448,250),'#303b40');d=ImageDraw.Draw(master_board)
    for j,mode in enumerate(['bare','helmet']):master_board.paste(masters[mode],(j*224,26),masters[mode]);d.text((j*224+4,4),mode+' '+direction+' master',fill='white')
    master_board.save(P/f'{direction}-masters.png')
    gif=[];durations=[]
    for page in range((len(poses)+23)//24):
        chunk=poses[page*24:(page+1)*24];board=Image.new('RGB',(12*224,4*250),'#303b40');d=ImageDraw.Draw(board)
        for j,(key,index) in enumerate(chunk):
            pair=Image.new('RGB',(672,250),'#303b40');pd=ImageDraw.Draw(pair);pd.text((4,4),key+' '+str(index),fill='white')
            pair.paste(masters['bare'],(0,26),masters['bare'])
            for mode_row,mode in enumerate(['bare','helmet']):
                m,s,files=load(mode,key);file=files[index];im=plane(file,m);a=np.array(im);yy,xx=np.where(a[:,:,3]>192)
                x=j%12*224;y=(j//12*2+mode_row)*250
                board.paste(im,(x,y+26),im);d.text((x+3,y+3),mode+' '+key.removesuffix('-'+direction)+' '+str(index),fill='white')
                master_a=np.array(masters[mode]);my,mx=np.where(master_a[:,:,3]>192)
                d.line((x,y+26+int(my.min()),x+223,y+26+int(my.min())),fill='#62747b');d.line((x,y+26+int(my.max()),x+223,y+26+int(my.max())),fill='#62747b')
                records.append({'mode':mode,'key':key,'index':index,'path':file.relative_to(R).as_posix(),'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'pivot':m['pivot'],'standingHeight':m['standingHeight'],'boundsAlpha192':[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())],'masterBoundsAlpha192':[int(mx.min()),int(my.min()),int(mx.max()),int(my.max())],'durationMs':s['frameDurationsMs'][index]})
                pair.paste(im,((mode_row+1)*224,26),im)
            gif.append(pair);durations.append(s['frameDurationsMs'][index])
        name=f'{direction}-page{page}.png';board.save(P/name);boards.append(name)
    gif[0].save(P/f'{direction}-paired-controller-source.gif',save_all=True,append_images=gif[1:],duration=durations,loop=0,disposal=2)
(P/'review-evidence.json').write_text(json.dumps({'sourceReferences':len(records),'boards':boards,'records':records,'scope':'All selected paired dry torch draw/weld/stow source references, fixed manifest pivot/148 standing ruler, master crown/sole guides. Bounds include torch/flame and do not measure anatomy. No per-pose scale/grade/translation edits. Source GIF is one authored draw/weld/stow pass, not the actual longer runtime work timer.'},indent=2))
print(json.dumps({'sourceReferences':len(records),'boards':boards}))
