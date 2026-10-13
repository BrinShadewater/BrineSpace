"""Freeze South selected identity and complete existing run cycle for direct review."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-run-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sources=BASE/'sources';sources.mkdir(parents=True,exist_ok=True);catalog=ROOT/'character/marsh-v2/catalog.json';states={}
    for name in json.loads(catalog.read_text())['body']:
        manifest=ROOT/name.removeprefix('res://') if name.startswith('res://') else (catalog.parent/name).resolve()
        for s in json.loads(manifest.read_text())['states']:
            states[s['id']]=([ROOT/p.removeprefix('res://') if p.startswith('res://') else (manifest.parent/p).resolve() for p in s['frameFiles']],s)
    primary=[states['idle-south'][0][0],states['idle-south'][0][1],states['walk-south'][0][0],states['walk-south'][0][3]]
    board=Image.new('RGB',(4*552,620),'#293b40');draw=ImageDraw.Draw(board)
    for i,path in enumerate(primary):
        im=Image.open(path).convert('RGBA');assert im.size==(184,184);im=im.resize((552,552),Image.Resampling.NEAREST);board.paste(im,(i*552,50),im)
        draw.text((i*552+8,8),['SELECTED South idle0','SELECTED South idle1','SELECTED South gait0','SELECTED South gait3'][i],fill='white')
        draw.text((i*552+8,28),'PRIMARY body/identity/camera/material density',fill='#a4d4c3')
    board.save(sources/'selected-south-idle-gait.png')
    run=states['run-south'][0];board=Image.new('RGB',(6*368,440),'#293b40');draw=ImageDraw.Draw(board)
    for i,path in enumerate(run):
        im=Image.open(path).convert('RGBA').resize((368,368),Image.Resampling.NEAREST);board.paste(im,(i*368,50),im)
        draw.text((i*368+8,8),'Existing run phase'+str(i)+' /100ms',fill='white');draw.text((i*368+8,28),'MOTION ONLY; not proportions master',fill='#a4d4c3')
    board.save(sources/'run-pose-guide.png');b=Image.open(primary[0]).getbbox()
    provenance={'normalAdmission':False,'primarySourceFrames':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in primary],'guideSourceFrames':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in run],'selectedIdleOccupiedSize':[b[2]-b[0],b[3]-b[1]],'runTiming':states['run-south'][1]['frameDurationsMs'],'runLoop':states['run-south'][1]['loop']}
    (sources/'guide-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n');print('Frozen South selected identity and six complete run phases before authoring.')
if __name__=='__main__':main()
