"""Reproduce the reviewed north tread registration from frozen current sources."""
from pathlib import Path
import json, hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-quality-pass-v2'
def main():
    s=json.loads((BASE/'baseline-contract.json').read_text())['states']['tread-north']
    files=[];records={}
    for i,(f,h,dy) in enumerate(zip(s['files'],s['hashes'],[0,0,-15,-13])):
        assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h
        im=Image.open(ROOT/f).convert('RGBA');out=Image.new('RGBA',im.size);out.paste(im,(0,dy))
        assert out.crop(out.getbbox()).tobytes()==im.crop(im.getbbox()).tobytes()
        p=BASE/f'frames/tread-north/{i:03}.png';p.parent.mkdir(parents=True,exist_ok=True);out.save(p);files.append(p.relative_to(BASE).as_posix())
        records[p.relative_to(ROOT).as_posix()]={'source':f,'sourceSha256':h,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'translation':[0,dy],'actor':'marsh'}
    manifest={'revision':'marsh-quality-pass-v2','canvas':[184,184],'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','gaitPhaseGroups':{'walk':'marsh-dry','run':'marsh-dry'},'states':[{'id':'tread-north','frameFiles':files,'frameDurationsMs':s['durations'],'loop':True}]}
    (BASE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (BASE/'installation.json').write_text(json.dumps({'frames':records,'reason':'North floating loop was registered to changing boot height; stabilize head/torso with 2px natural bob, preserving authored leg motion and every visible pixel.'},indent=2)+'\n')
    print('Four north tread slots reproduce; all cropped artwork pixels preserved')
if __name__=='__main__':main()
