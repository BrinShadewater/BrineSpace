"""Restore erased authored collar pixels and match video-walk cloth tone.

Uses existing source pixels and locked palettes. No generated or invented poses.
Stages before publication; refuses intervening edits. Run once per frozen revision.
"""
from pathlib import Path
import hashlib, json, sys, shutil, os
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/veld-consistency-v1'
sys.path.insert(0,str(ROOT/'character/palette-standard-v1'))
from standardize import read, write, remapper, group, WEIGHTS

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pixels(im):return hashlib.sha256(im.tobytes()).hexdigest()
def normalized(im,pivot):
    canvas=Image.new('RGBA',(512,512))
    canvas.alpha_composite(im,(256-int(pivot[0]),400-int(pivot[1])))
    return canvas
def selected(actor):
    folder={'veld':'dr-veld-v2','branforth':'chief-engineer-branforth-v2'}[actor]
    base=ROOT/'character'/folder;catalog=read(base/'catalog.json');rows={};files={}
    for variant in ['body','equipment']:
        for f in catalog[variant]:
            path=base/f;pack=read(path)
            for state in pack['states']:
                row=[]
                for f in state['frameFiles']:
                    p=(path.parent/f).resolve();rel=p.relative_to(ROOT).as_posix()
                    files[rel]={'pivot':pack['pivot'],'actor':actor};row.append(rel)
                rows[variant+'/'+state['id']]=row
    return rows,files
def cloth(im,actor,top):
    a=np.array(im);mask=a[:,:,3]>0;mask[:top]=False
    y,x=np.where(mask);mask[y,x]=group(a[y,x,:3],actor)==0
    return a,mask
def prepare():
    if (OUT/'mapping.json').exists():raise ValueError('Frozen revision exists; do not regrade installed frames')
    edits={};files={};curves={};rows_by_actor={}
    for actor in ['veld','branforth']:
        rows,actor_files=selected(actor);files.update(actor_files);rows_by_actor[actor]=rows
        pal=read(ROOT/'character/palette-standard-v1/palettes'/f'{actor}.json')
        apply=remapper(pal);ramp=np.array(pal['neutralRamp'],dtype=np.uint8)
        if actor=='veld':
            for p in (OUT/'before-east-chain').glob('*.png'):
                if p.name.startswith('helmet-'):continue
                old=normalized(apply(Image.open(p)),[128,224])
                new=normalized(apply(Image.open(ROOT/'character/veld-identity-correction-v1/review/east-chain-01'/p.name)),[128,224])
                a,b=np.array(old),np.array(new)
                assert np.array_equal(a[a[:,:,3]>0],b[a[:,:,3]>0]),'Existing visible pixels changed'
                edits[pixels(old)]=(new,'authored collar restoration')
        samples={}
        for action in ['idle','walk']:
            values=[]
            for direction in ['east','west','south','north']:
                for rel in rows['body/'+action+'-'+direction]:
                    im=Image.open(ROOT/rel).convert('RGBA');a,mask=cloth(im,actor,im.getbbox()[1]+30)
                    values.extend((a[mask,:3]@WEIGHTS).tolist())
            samples[action]=np.quantile(values,[.1,.5,.9]).tolist()
        curve={'input':[0]+samples['walk']+[255],'output':[0]+samples['idle']+[255],
               'scope':'One fixed four-direction walk-family curve, neutral cloth below collar only; heads, coloured markings and lights unchanged'}
        curves[actor]=curve
        for direction in ['east','west','south','north']:
            for i,rel in enumerate(rows['body/walk-'+direction]):
                body=Image.open(ROOT/rel).convert('RGBA');top=body.getbbox()[1]+30
                for variant in ['body','equipment']:
                    path=rows[variant+'/walk-'+direction][i];im=Image.open(ROOT/path).convert('RGBA')
                    a,mask=cloth(im,actor,top)
                    luminance=a[mask,:3]@WEIGHTS
                    levels=np.clip(np.rint(np.interp(luminance,curve['input'],curve['output'])),0,255).astype(int)
                    a[mask,:3]=ramp[levels]
                    changed=Image.fromarray(a);pivot=files[path]['pivot']
                    assert np.array_equal(np.array(im)[:top],a[:top])
                    assert np.array_equal(np.array(im)[:,:,3],a[:,:,3])
                    edits[pixels(normalized(im,pivot))]=(normalized(changed,pivot),actor+' shared walk cloth curve')
    results={}
    for rel,info in files.items():
        im=Image.open(ROOT/rel).convert('RGBA');key=pixels(normalized(im,info['pivot']))
        if key not in edits:continue
        new,reason=edits[key];x=256-int(info['pivot'][0]);y=400-int(info['pivot'][1])
        new=new.crop((x,y,x+im.width,y+im.height))
        before=OUT/'originals'/rel;after=OUT/'mapped'/rel
        before.parent.mkdir(parents=True,exist_ok=True);after.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/rel,before);new.save(after)
        results[rel]={'before':digest(before),'after':digest(after),'reason':reason}
    write(OUT/'curves.json',curves);write(OUT/'mapping.json',results)
    print('Staged',len(results),'files; original bank preserved')
def install():
    entries=read(OUT/'mapping.json')
    for rel,e in entries.items():
        assert digest(ROOT/rel) in [e['before'],e['after']], 'Intervening edit: '+rel
        assert digest(OUT/'mapped'/rel)==e['after']
    for rel,e in entries.items():
        p=ROOT/rel
        if digest(p)==e['after']:continue
        temporary=p.with_suffix('.consistency-tmp');shutil.copy2(OUT/'mapped'/rel,temporary);os.replace(temporary,p)
    print('Installed',len(entries),'guarded consistency corrections')
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['prepare','install']);args=parser.parse_args()
    prepare() if args.mode=='prepare' else install()
