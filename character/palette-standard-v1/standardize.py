"""Deterministic, pose-preserving shared character colour ramps.

prepare freezes original exports and stages colour-only replacements. install
checks for intervening edits before publishing. Rebuilds always use the frozen
originals, never a previously mapped image. No geometry, alpha or metadata edits.
"""
from pathlib import Path
import argparse,hashlib,json,shutil,os
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.spatial import cKDTree
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
CAST={'bill':'major-bill-v3','veld':'dr-veld-v2','branforth':'chief-engineer-branforth-v2','marsh':'marsh-v2'}
DIRS=['south','east','west','north']
WEIGHTS=np.array([.2126,.7152,.0722])

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def write(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
def relative(path):return path.resolve().relative_to(REPO).as_posix()

def inventory():
    actors={};manifests={}
    for actor,folder in CAST.items():
        base=REPO/'character'/folder;cat=read(base/'catalog.json');states={};gear={};files=set()
        manifests[relative(base/'catalog.json')]=sha(base/'catalog.json')
        for variant in ['body','equipment']:
            for name in cat[variant]:
                path=base/name;pack=read(path);manifests[relative(path)]=sha(path)
                for s in pack['states']:
                    framepaths=[(path.parent/f).resolve() for f in s['frameFiles']];files.update(framepaths)
                    (states if variant=='body' else gear)[s['id']]={'files':[relative(p) for p in framepaths],'pivot':pack['pivot'],'height':pack['standingHeight']}
        refs=[states['idle-'+d]['files'][0] for d in DIRS]
        refs += [gear['idle-'+d]['files'][0] for d in DIRS if 'idle-'+d in gear]
        actors[actor]={'files':sorted(relative(p) for p in files),'references':refs,'states':states}
    for actor in ['margot','josh','river']:
        folder='margot-polish-v1' if actor=='margot' else 'robot-polish-v1'
        root=REPO/'character'/folder
        path=root/'manifest.json' if actor=='margot' else root/actor/'manifest.json'
        pack=read(path);states={};files=set();manifests[relative(path)]=sha(path)
        for s in pack['states']:
            framepaths=[(root/f).resolve() for f in s['frameFiles']];files.update(framepaths)
            states[s['id']]={'files':[relative(p) for p in framepaths],'pivot':pack['pivot'],'height':pack['standingHeight']}
        # Track actual runtime manifests too; aggregate exports alone are not bindings.
        packroot=root/'packs' if actor=='margot' else root/actor/'packs'
        for p in packroot.glob('*/manifest.json'):manifests[relative(p)]=sha(p)
        actors[actor]={'files':sorted(relative(p) for p in files),'references':[states['idle-'+d]['files'][0] for d in DIRS],'states':states}
    # Apply the same Veld palette to the existing candidate, without selecting it.
    for folder in ['veld-painted-v2','veld-painted-v2-helmet']:
        path=REPO/'character/crew-polish-v1'/folder/'manifest.json';pack=read(path);manifests[relative(path)]=sha(path)
        actors['veld']['files']+=sorted({relative(path.parent/f) for s in pack['states'] for f in s['frameFiles']})
    return {'actors':actors,'manifests':manifests}

def group(rgb,actor=""):
    r,g,b=rgb.astype(float).T
    result=np.zeros(len(rgb),dtype=np.uint8)
    result[(r-b>10)&(r>=g)]=1 # warm: skin, hair, red/orange paint, ivory
    result[(b-r>15)|((b-r>8)&(b-g>3))]=2 # blue/lavender paint and cool fittings
    result[(g-r>5)&(g-b>2)]=3 # sage paint, green bonnet/materials
    saturation=(np.maximum.reduce([r,g,b])-np.minimum.reduce([r,g,b]))/np.maximum(1,np.maximum.reduce([r,g,b]))
    # Desaturated blue/purple on cloth is a neutral cast, not a blue material.
    # Josh's lavender shells are deliberately less saturated than cobalt paint.
    result[(result==2)&(saturation<(.16 if actor=='josh' else .35))]=0
    # Bright cyan/status colours remain authored: these are light, not suit paint.
    result[(g-r>45)&(b-r>45)&(g>135)&(b>135)]=4
    return result

def palette(actor,info,baseline):
    pixels=[]
    for path in info['references']:
        im=np.array(Image.open(ROOT/'originals'/(baseline[path]['sha256']+'.png')).convert('RGBA'))
        pixels.append(im[:,:,:3][im[:,:,3]>0])
    rgb=np.concatenate(pixels);labels=group(rgb,actor);neutral=rgb[labels==0].astype(float);lum=neutral@WEIGHTS
    ramp=[]
    for value in range(256):
        near=np.abs(lum-value);sample=neutral[near<=max(4,float(np.partition(near,min(80,len(near)-1))[min(80,len(near)-1)]))]
        offsets=np.median(sample-(sample@WEIGHTS)[:,None],axis=0)
        offsets-=offsets@WEIGHTS
        ramp.append(np.clip(np.round(value+offsets),0,255).astype(int).tolist())
    groups={str(i):np.unique(rgb[labels==i],axis=0).tolist() for i in [1,2,3]}
    result={'actor':actor,'references':[{'path':p,'sha256':baseline[p]['sha256']} for p in info['references']],
        'policy':'One shared mapping for every pose and equipment frame. Neutral 256-step reference ramp; warm/blue/green use same-character idle chromaticity ramps at original luminance. Bright cyan light is retained. No per-frame exposure or adaptive recolouring.',
        'neutralRamp':ramp,'materialColours':groups}
    write(ROOT/'palettes'/f'{actor}.json',result)
    return result

def remapper(pal):
    ramp=np.array(pal['neutralRamp'],dtype=np.uint8)
    choices={int(k):np.array(v,dtype=float) for k,v in pal['materialColours'].items() if v}
    ratios={k:v/np.maximum(1,v@WEIGHTS)[:,None] for k,v in choices.items()}
    trees={k:cKDTree(v) for k,v in ratios.items()}
    lut=np.full(1<<24,0xffffffff,dtype=np.uint32)
    def apply(im):
        a=np.array(im.convert('RGBA'));mask=a[:,:,3]>0;rgb=a[:,:,:3][mask].astype(np.uint32)
        codes=(rgb[:,0]<<16)|(rgb[:,1]<<8)|rgb[:,2]
        unique=np.unique(codes[lut[codes]==0xffffffff])
        if len(unique):
            source=np.stack([unique>>16,(unique>>8)&255,unique&255],axis=1).astype(float)
            labels=group(source,pal['actor']);mapped=source.copy();lum=source@WEIGHTS
            idx=labels==0;mapped[idx]=ramp[np.clip(np.round(lum[idx]),0,255).astype(int)]
            for k,tree in trees.items():
                idx=labels==k
                if idx.any():
                    selected=tree.query(source[idx]/np.maximum(1,lum[idx])[:,None])[1]
                    mapped[idx]=ratios[k][selected]*lum[idx,None]
            mapped=np.clip(np.round(mapped),0,255).astype(np.uint32)
            lut[unique]=(mapped[:,0]<<16)|(mapped[:,1]<<8)|mapped[:,2]
        values=lut[codes]
        a[:,:,:3][mask]=np.stack([values>>16,(values>>8)&255,values&255],axis=1).astype(np.uint8)
        return Image.fromarray(a)
    return apply

def prepare():
    ROOT.mkdir(exist_ok=True);frozen=ROOT/'baseline.json'
    if not frozen.exists():
        inv=inventory();baseline={}
        for info in inv['actors'].values():
            for rel in info['files']:
                path=REPO/rel;digest=sha(path);dest=ROOT/'originals'/(digest+'.png');dest.parent.mkdir(exist_ok=True)
                if not dest.exists():shutil.copy2(path,dest)
                baseline[rel]={'sha256':digest}
        write(frozen,{'inventory':inv,'files':baseline})
    frozen=read(frozen);inv=frozen['inventory'];baseline=frozen['files'];results={};counts={}
    for actor,info in inv['actors'].items():
        pal=palette(actor,info,baseline);apply=remapper(pal);cache={};changed=0
        for rel in info['files']:
            digest=baseline[rel]['sha256'];key=actor+'-'+digest;dest=ROOT/'mapped'/(key+'.png')
            if key not in cache:
                src=ROOT/'originals'/(digest+'.png');assert sha(src)==digest, 'Frozen original changed: '+digest;original=Image.open(src).convert('RGBA');mapped=apply(original)
                a=np.array(original);b=np.array(mapped)
                assert np.array_equal(a[:,:,3],b[:,:,3]) and original.size==mapped.size and original.getbbox()==mapped.getbbox()
                assert np.array_equal(a[a[:,:,3]==0],b[b[:,:,3]==0])
                dest.parent.mkdir(exist_ok=True);mapped.save(dest,compress_level=3)
                cache[key]={'output':relative(dest),'sha256':sha(dest),'changedOpaquePixels':int(np.any(a[:,:,:3]!=b[:,:,:3],axis=2).sum())}
            results[rel]=dict(cache[key],actor=actor,originalSha256=digest);changed+=int(cache[key]['changedOpaquePixels']>0)
        counts[actor]={'files':len(info['files']),'changedFiles':changed,'uniqueOriginals':len(cache)}
        print(actor,counts[actor],flush=True)
    write(ROOT/'mapping.json',{'files':results,'counts':counts,'status':'prepared; not installed'})
    review(frozen,results)

def review(frozen,mapping):
    keys=['idle-south','walk-south','walk-east','repair-west','swim-east']
    board=Image.new('RGBA',(1500,7*290),'#242b2e');draw=ImageDraw.Draw(board)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    for row,(actor,info) in enumerate(frozen['inventory']['actors'].items()):
        chosen=keys if actor in CAST else (['idle-south','walk-south','groom-south','sit-south','swim-east'] if actor=='margot' else ['idle-south','walk-south','torch-south' if actor=='josh' else 'scan-south','powerdown-south' if actor=='josh' else 'boot-south','idle-east'])
        for col,key in enumerate(chosen):
            s=info['states'][key];rel=s['files'][0]
            draw.text((col*300+6,row*290+5),actor+' / '+key,fill='white',font=font)
            for side,path in enumerate([ROOT/'originals'/(frozen['files'][rel]['sha256']+'.png'),REPO/mapping[rel]['output']]):
                im=Image.open(path).convert('RGBA');pivot=s['pivot'];foot=(col*300+70+side*145,row*290+218)
                board.alpha_composite(im,(round(foot[0]-pivot[0]),round(foot[1]-pivot[1])))
                draw.text((col*300+16+side*145,row*290+245),'before' if side==0 else 'shared palette',fill='#b5c5c5',font=font)
    (ROOT/'review').mkdir(exist_ok=True);board.save(ROOT/'review/before-after.png')

def install():
    frozen=read(ROOT/'baseline.json');mapping=read(ROOT/'mapping.json')
    # Verify the entire write set before changing a single live file.
    for rel,digest in frozen['inventory']['manifests'].items():
        if sha(REPO/rel)!=digest:raise ValueError('Manifest changed during palette pass: '+rel)
    for rel,entry in mapping['files'].items():
        if sha(REPO/rel) not in [entry['originalSha256'],entry['sha256']]:raise ValueError('Intervening artwork edit: '+rel)
        if sha(REPO/entry['output'])!=entry['sha256']:raise ValueError('Staged artwork changed: '+rel)
    for rel,entry in mapping['files'].items():
        dest=REPO/rel
        if sha(dest)==entry['sha256']:continue
        temporary=dest.with_suffix('.palette-tmp');shutil.copyfile(REPO/entry['output'],temporary);os.replace(temporary,dest)
    mapping['status']='installed-source; executable exports not rebuilt';write(ROOT/'mapping.json',mapping)
    print('Installed',len(mapping['files']),'pose-preserving colour mappings.')

def map_file(actor, source, destination):
    source=Path(source).resolve();destination=Path(destination).resolve()
    if source==destination or destination.exists():
        raise ValueError('Use a separate, new destination; preserve the original source.')
    mapped=remapper(read(ROOT/'palettes'/f'{actor}.json'))(Image.open(source))
    destination.parent.mkdir(parents=True,exist_ok=True)
    mapped.save(destination)
    print('Mapped', actor, 'to', destination)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['prepare','install','map-file'])
    parser.add_argument('--actor',choices=['bill','veld','branforth','marsh','margot','josh','river'])
    parser.add_argument('--source');parser.add_argument('--destination');args=parser.parse_args()
    if args.mode=='map-file':
        if not all([args.actor,args.source,args.destination]):parser.error('map-file requires --actor, --source and --destination')
        map_file(args.actor,args.source,args.destination)
    elif args.mode=='prepare':prepare()
    else:install()
