"""Freeze whole North bodies and reusable authored effect sources for review."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-north-injury-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sources=BASE/'sources';sources.mkdir(parents=True,exist_ok=True)
    catalog=ROOT/'character/marsh-v2/catalog.json';states={}
    for name in json.loads(catalog.read_text())['body']:
        manifest=ROOT/name.removeprefix('res://') if name.startswith('res://') else catalog.parent/name
        for state in json.loads(manifest.read_text())['states']:
            states[state['id']]=[ROOT/p.removeprefix('res://') if p.startswith('res://') else manifest.parent/p for p in state['frameFiles']]
    body=ROOT/'character/marsh-north-collapse-material-v1/candidate-02'
    rows=[('Complete new dry body',[body/f'{i:03d}.png' for i in range(6)]),('Old North white-fluid guide',states['injury-ground-north']),('Old North recovery guide',states['injury-rise-north'])]
    board=Image.new('RGB',(1104,660),'#293b40');draw=ImageDraw.Draw(board);records=[]
    for row,(label,paths) in enumerate(rows):
        for i,path in enumerate(paths):
            im=Image.open(path).convert('RGBA');board.paste(im,(i*184,row*220+30),im)
            draw.text((i*184+3,row*220+5),label+' '+str(i),fill='white')
            records.append({'path':path.resolve().relative_to(ROOT).as_posix(),'sha256':sha(path)})
    board.save(sources/'body-fluid-guide.png')
    effects=ROOT/'character/marsh-south-injury-material-v1/candidate-01'
    reusable=[ROOT/'character/marsh-south-injury-material-v1/sources/fluid-01.raw.png',ROOT/'character/marsh-south-injury-material-v1/sources/fluid-01.request.json',ROOT/'character/marsh-south-injury-material-v1/sources/fluid-01.prompt.txt']+[effects/f'effect-{i:02d}.png' for i in range(4)]
    recipe={'normalAdmission':False,'status':'frozen before effect placement; inspect rear-view guide first','bodyGuideFrames':records,'reusedAuthoredEffects':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in reusable],'operations':'Reuse complete independent white-fluid swatches at same standingHeight148 density. Exact whole North body figures; whole translations of effects behind body, fixed floor puddle. No generated body edits or old-guide subtraction.','pending':'Determine right-screen glove anchor and floor puddle from complete new bodies; material/native review.'}
    (sources/'reuse-request.json').write_text(json.dumps(recipe,indent=2)+'\n')
    print('Frozen18 complete body/guide frames and7 independent effect provenance inputs.')
if __name__=='__main__':main()
