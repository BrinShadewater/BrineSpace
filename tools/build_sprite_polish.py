"""Package revised authored Marsh sheets and a shared palette per companion.

No painting or synthetic in-betweens: only key removal, registration, area
downsampling, palette quantization and reuse of authored transition endpoints.
Original packs remain intact. Run from any directory with the project Python.
"""
from pathlib import Path
import copy, hashlib, json
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'character/sprite-polish-v2'
DIRS = ['south', 'north', 'east', 'west']
REPORT = {}

def read_pack(path):
    manifest = json.loads(path.read_text())
    clips = {s['id']: [Image.open(path.parent / f).convert('RGBA') for f in s['frameFiles']] for s in manifest['states']}
    return manifest, clips

def quantize(clips):
    samples = np.concatenate([np.asarray(im)[np.asarray(im)[:,:,3] > 0,:3] for row in clips.values() for im in row])
    palette = Image.fromarray(samples.reshape(1,-1,3)).quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    for row in clips.values():
        for i, im in enumerate(row):
            alpha = im.getchannel('A')
            row[i] = im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA')
            row[i].putalpha(alpha.point(lambda a: 255 if a >=128 else 0))

def save_pack(name, manifest, clips):
    dest = OUT / name
    dest.mkdir(parents=True, exist_ok=True)
    colors = set(); count = 0
    for s in manifest['states']:
        s['frameFiles'] = []
        for i, im in enumerate(clips[s['id']]):
            assert im.size == (92,92)
            b = im.getbbox(); assert b and b[0]>0 and b[1]>0 and b[2]<92 and b[3]<92,(name,s['id'],b)
            a = np.asarray(im); assert set(np.unique(a[:,:,3])) <= {0,255}
            colors.update(map(tuple,a[a[:,:,3]>0,:3].tolist()))
            p = dest / 'frames' / s['id'] / f'{i:03}.png'; p.parent.mkdir(parents=True,exist_ok=True); im.save(p)
            s['frameFiles'].append(p.relative_to(dest).as_posix()); count+=1
        assert len(s['frameFiles'])==len(s['frameDurationsMs'])
    manifest.update(frameWidth=92,frameHeight=92,pivot=[46,86],paletteColors=64,mirrored=False)
    (dest/'manifest.json').write_text(json.dumps(manifest,indent=2))
    REPORT[name] = dict(clips=len(clips),frameReferences=count,opaqueColors=len(colors))
    assert len(colors)<=64

def slice_marsh(name, cols):
    src = OUT/'sources'/f'marsh-{name}.png'; im = Image.open(src).convert('RGBA')
    rows = {}
    for row, direction in enumerate(DIRS):
        strip=im.crop((0,round(row*im.height/4),im.width,round((row+1)*im.height/4)))
        ink=np.asarray(strip); rgb=ink[:,:,:3].astype(int)
        mask=(ink[:,:,3]>=128)&~((rgb[:,:,0]>rgb[:,:,1]+55)&(rgb[:,:,2]>rgb[:,:,1]+55))
        edges=[0]
        for col in range(1,cols):
            start=round(col*im.width/cols)-85; counts=mask.sum(axis=0)[start:start+170]
            edges.append(start+int(np.median(np.where(counts==counts.min())[0])))
        edges.append(im.width)
        tiles=[]
        for col in range(cols):
            tile=strip.crop((edges[col],0,edges[col+1],strip.height))
            a=np.asarray(tile).copy(); rgb=a[:,:,:3].astype(int)
            a[a[:,:,3]<128,:]=0
            a[(rgb[:,:,0]>rgb[:,:,1]+55)&(rgb[:,:,2]>rgb[:,:,1]+55),:]=0
            tile=Image.fromarray(a); b=tile.getbbox()
            assert b and b[0]>0 and b[1]>0 and b[2]<tile.width and b[3]<tile.height,(name,row,col,b)
            tiles.append((tile,b))
        baseline=max(b[3] for _,b in tiles); top=min(b[1] for _,b in tiles)
        scale=min(74/(baseline-top),88/max(b[2]-b[0] for _,b in tiles))
        frames=[]
        for tile,b in tiles:
            body=tile.crop(b).resize((round((b[2]-b[0])*scale),round((b[3]-b[1])*scale)),Image.Resampling.BOX)
            body.putalpha(body.getchannel('A').point(lambda a:255 if a>=128 else 0))
            frame=Image.new('RGBA',(92,92)); x=46-body.width//2; y=86-round((baseline-b[1])*scale)
            assert x>0 and y>0 and x+body.width<92 and y+body.height<92,(name,direction,body.size)
            frame.alpha_composite(body,(x,y)); frames.append(frame)
        rows[direction]=frames
    return rows

def marsh():
    m, old = read_pack(ROOT/'character/marsh-v1/final/manifest.json')
    m['sourceManifest']='../../marsh-v1/final/manifest.json'
    m['sourceSheets']=['../sources/marsh-'+n+'.png' for n in ['locomotion','work','swim','death']]
    sheets={n:slice_marsh(n,c) for n,c in [('locomotion',8),('work',8),('swim',8),('death',6)]}
    clips={}
    for s in m['states']:
        state,d = s['id'].rsplit('-',1)
        if state=='idle': frames=sheets['locomotion'][d][:2]; s['frameDurationsMs']=[650,650]
        elif state in ['walk','run']: frames=sheets['locomotion'][d][2:]
        else:
            # Existing state aliases remain explicit; this pass repairs anatomy,
            # not the semantics of every secondary crew activity.
            frames=[]
            for p in s['frameFiles']:
                source=Path(p).parent.name.rsplit('-',1)[0]; i=int(Path(p).stem.split('_')[-1])
                selected = source
                indices=[1,2,3,4,5,6] if source=='swim' else [0,1,2,3,4,7] if source=='work' else list(range(6))
                frames.append(sheets[selected][d][indices[i]].copy())
            if state in ['death-ground','death-water','kneel','sit-down','lie-down']:frames[0]=sheets['locomotion'][d][0].copy()
            if state in ['stand','sit-rise','get-up']:frames[-1]=sheets['locomotion'][d][0].copy()
        clips[s['id']]=[f.copy() for f in frames]
    quantize(clips); save_pack('marsh',m,clips)
    # Conservative envelope union prevents animation changes reducing clearance.
    envelope=json.loads((ROOT/'character/marsh-v1/clearance.json').read_text())
    for mode in envelope:
        for d in DIRS:
            boxes=[im.getbbox() for key,row in clips.items() if key.endswith('-'+d) for im in row]
            new=[min(b[0]-46 for b in boxes),min(b[1]-86 for b in boxes),max(b[2]-46 for b in boxes),max(b[3]-86 for b in boxes)]
            new=[v*.8821621622 for v in new]; oldbox=envelope[mode][d]
            envelope[mode][d]=[min(oldbox[0],new[0]),min(oldbox[1],new[1]),max(oldbox[2],new[2]),max(oldbox[3],new[3])]
    (OUT/'marsh/clearance.json').write_text(json.dumps(envelope,indent=2))

def companions():
    for name in ['river','josh','margot']:
        base, locomotion=read_pack(ROOT/f'character/{name}-v1/manifest.json')
        actions, poses=read_pack(ROOT/f'character/companion-personality-v1/{name}/manifest.json')
        base['sourceManifest']=f'../../{name}-v1/manifest.json'
        base.pop('source',None)
        actions['sourceManifest']=f'../../companion-personality-v1/{name}/manifest.json'
        actions['source']=f'../../companion-personality-v1/sources/{name}.png'
        if name!='margot':
            for s in list(actions['states']):
                action,d=s['id'].rsplit('-',1)
                for phase, frames in [('enter',[locomotion['idle-'+d][0],poses[s['id']][0]]),('exit',[poses[s['id']][-1],locomotion['idle-'+d][0]])]:
                    key=f'{action}-{phase}-{d}'; poses[key]=[f.copy() for f in frames]
                    actions['states'].append(dict(id=key,frameDurationsMs=[150,150],loop=False))
        allclips={**locomotion,**poses}; quantize(allclips)
        save_pack(name,base,{k:allclips[k] for k in locomotion})
        save_pack(name+'-actions',actions,{k:allclips[k] for k in poses})

def review():
    names=['bill','veld','branforth','marsh','river','josh','margot']
    paths=['major-bill-v2/final','dr-veld-v1/final','chief-engineer-branforth-v1/final']
    packs=[read_pack(ROOT/'character'/p/'manifest.json') for p in paths]+[read_pack(OUT/n/'manifest.json') for n in names[3:]]
    still=Image.new('RGB',(184*7,230),(24,36,42));draw=ImageDraw.Draw(still)
    for i,(name,(_,clips)) in enumerate(zip(names,packs)):
        im=clips['idle-south'][0].resize((184,184),Image.Resampling.NEAREST)
        still.paste(im,(i*184,30),im);draw.text((i*184+12,8),name,fill='white')
    still.save(OUT/'lineup.png')
    items=[]
    for name in names[3:]:
        m,clips=read_pack(OUT/name/'manifest.json')
        keys=['idle','walk','weld','swim','death-ground'] if name=='marsh' else ['idle','walk']
        for state in keys:
            frames=[]
            timing=next(s for s in m['states'] if s['id']==state+'-south')['frameDurationsMs']
            for tick in range(len(clips[state+'-south'])):
                canvas=Image.new('RGB',(736,205),(24,36,42));dr=ImageDraw.Draw(canvas)
                for col,d in enumerate(DIRS):
                    row=clips[state+'-'+d];im=row[tick%len(row)].resize((184,184),Image.Resampling.NEAREST)
                    canvas.paste(im,(col*184,20),im);dr.text((col*184+8,3),d,fill='white')
                frames.append(canvas)
            rel=f'{name}-{state}.gif';frames[0].save(OUT/rel,save_all=True,append_images=frames[1:],duration=timing,loop=0)
            items.append(f'<h3>{name} / {state}</h3><img src="{rel}">')
    for name in ['river','josh','margot']:
        m,clips=read_pack(OUT/(name+'-actions')/'manifest.json')
        for s in m['states']:
            if '-enter-' in s['id'] or '-exit-' in s['id']:continue
            frames=[]
            for im in clips[s['id']]:
                bg=Image.new('RGBA',(92,92),(24,36,42));bg.alpha_composite(im)
                frames.append(bg.resize((184,184),Image.Resampling.NEAREST).convert('RGB'))
            rel=f'{name}-{s["id"]}.gif';frames[0].save(OUT/rel,save_all=True,append_images=frames[1:],duration=s['frameDurationsMs'],loop=0)
            items.append(f'<details><summary>{name} / {s["id"]}</summary><img src="{rel}"></details>')
    native='<h2>Native Godot playback</h2><p>Large copies: 2x source pixels. Small copies: canonical room scale. Other crew hold idle where their base pack has no matching action.</p>'
    for state in ['idle','walk','weld','swim','death-ground']:
        if (OUT/f'native-{state}.gif').exists():native+=f'<h3>{state}</h3><img src="native-{state}.gif">'
    (OUT/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>Sprite polish</title><style>body{background:#18242a;color:#ddd;font:16px system-ui;padding:24px}img{image-rendering:pixelated;max-width:100%}h3{margin-top:30px}</style><h1>Sprite polish — scale and motion</h1><p>Marsh anatomy revision; companions share one 64-color palette per identity across locomotion and personality. Original packs retained. Work/rest/swimming aliases remain a documented limitation.</p><h2>Same scale lineup (2× pixels)</h2><img src="lineup.png">'+''.join(items)+native)

if __name__=='__main__':
    marsh();companions();review()
    REPORT['sources']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (OUT/'sources').glob('*.png')}
    REPORT['limits']='Marsh secondary activities still reuse work/collapse/swimming poses. Robot transitions reuse authored endpoints, not new in-between drawings. Original V1 packs remain intact.'
    (OUT/'build-report.json').write_text(json.dumps(REPORT,indent=2))
    print(json.dumps({k:v for k,v in REPORT.items() if k not in ['sources','limits']}))

