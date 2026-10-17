from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
pack=json.loads((R/'character/james-torch-material-residue-v2/bare-manifest.json').read_text())
states={s['id']:s for s in pack['states']}
native=json.loads((P/'validate-evidence.json').read_text())
bindings=[]; output=[];checks=0
def load(path):return Image.open(R/path.removeprefix('res://')).convert('RGBA')
def source_hash(im):return hashlib.sha256(im.tobytes().hex().encode()).hexdigest()
def row(key,index):
    state=states[key]
    return {'key':key,'index':index,'file':state['frameFiles'][index],'ms':state['frameDurationsMs'][index]}
def plane(item):
    im=load(item['file']);out=Image.new('RGBA',(184,196));out.alpha_composite(im,(92-pack['pivot'][0],172-pack['pivot'][1]));return out
for direction in ['north','east','south','west']:
    gif=[];clock=[];board=Image.new('RGB',(8*184,3*220),'#303b40');draw=ImageDraw.Draw(board)
    for phase_row,phase in enumerate(['torch-draw','weld','torch-stow']):
        record=next(r for r in native['records'] if r['label']==f'{direction}-{phase}-power-before')
        key=phase+'-'+direction
        images=[load(f) for f in states[key]['frameFiles']]
        indices=[i for i,im in enumerate(images) if source_hash(im)==record['sourceHash']]
        assert indices,(key,indices);checks+=1
        index=indices[0];current=row(key,index)
        if phase=='torch-draw':exit_path=[row(key,i) for i in range(index,-1,-1)]
        elif phase=='torch-stow':exit_path=[row(key,i) for i in range(index,len(images))]
        else:
            exit_path=[{**current,'ms':50}]+[row('torch-stow-'+direction,i) for i in range(len(states['torch-stow-'+direction]['frameFiles']))]
        return_path=list(reversed(exit_path))
        assert load(exit_path[0]['file']).tobytes()==images[index].tobytes();checks+=1
        neutral=load(states['torch-draw-'+direction]['frameFiles'][0]).tobytes()
        assert load(exit_path[-1]['file']).tobytes()==neutral;checks+=1
        assert load(return_path[0]['file']).tobytes()==neutral;checks+=1
        assert load(return_path[-1]['file']).tobytes()==images[index].tobytes();checks+=1
        for name,sequence in [('exit',exit_path),('return',return_path)]:
            id=f'construction-{name}-{phase}-{direction}'
            output.append({'id':id,'name':id,'frameFiles':[r['file'] for r in sequence],'frameDurationsMs':[r['ms'] for r in sequence],'loop':False})
        bindings.append({'direction':direction,'phase':phase,'nativeLabel':record['label'],'nativeSourceHash':record['sourceHash'],'startIndex':index,'pixelEquivalentIndices':indices,'exit':exit_path,'return':return_path})
        sampled=[current]+[exit_path[round((len(exit_path)-1)*t)] for t in [0,.5,1]]+[return_path[round((len(return_path)-1)*t)] for t in [0,.5,1]]+[current]
        for j,item in enumerate(sampled):
            im=plane(item);x=j*184;y=phase_row*220;board.paste(im,(x,y+24),im);draw.text((x+3,y+3),phase+' '+['before','exit start','exit middle','idle','return start','return middle','resumed','join'][j],fill='white')
        sequence=[{**current,'ms':350}]+exit_path+[{**exit_path[-1],'ms':600}]+return_path+[{**current,'ms':500}]
        for item in sequence:
            im=Image.new('RGB',(368,416),'#303b40');sprite=plane(item).resize((368,392),Image.Resampling.NEAREST);im.paste(sprite,(0,24),sprite)
            ImageDraw.Draw(im).text((5,5),direction+' / '+phase+' / staged interruption',fill='white')
            gif.append(im);clock.append(item['ms'])
    board.save(P/(direction+'-candidate.png'))
    gif[0].save(P/(direction+'-candidate.gif'),save_all=True,append_images=gif[1:],duration=clock,loop=0,disposal=2)
manifest={k:v for k,v in pack.items() if k!='states'};manifest['states']=output;manifest['status']='staged_whole_source_interruption_not_installed'
(P/'candidate-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
hashes={r['file']:hashlib.sha256((R/r['file'].removeprefix('res://')).read_bytes()).hexdigest() for b in bindings for r in b['exit']}
(P/'candidate-bindings.json').write_text(json.dumps({'bindings':bindings,'sourceFileHashes':hashes},indent=2)+'\n')
(P/'candidate-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'states':len(output),'refs':sum(len(s['frameFiles']) for s in output),'uniqueSourceFiles':len(hashes),'newArtwork':0,'runtimeInstalled':False,'scope':'Twelve actual observed bare interruption entry poses. Exact retained first source, reverse partial draw, remaining stow, held source followed by authored stow, exact neutral and reverse return to exact retained source. Fixed148 ruler/pivot and source RGB/alpha unchanged. Candidate not yet controller-driven; all arbitrary source phases, repeated interruption, safety and fresh Continue of candidate remain.'},indent=2)+'\n')
print(json.dumps({'checks':checks,'states':len(output),'refs':sum(len(s['frameFiles']) for s in output),'installed':False}))
