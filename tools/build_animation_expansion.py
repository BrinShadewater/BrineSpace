"""Package authored v5 poses; deterministic extraction, registration and palettes only."""
from pathlib import Path
import json, hashlib, copy, sys
from PIL import Image, ImageDraw
import build_sprite_polish as pack
import build_companion_cleanup as clean
ROOT=pack.ROOT
OUT=ROOT/'character/animation-expansion-v5'
pack.OUT=OUT
DIRS=['south','west','north','east']
NEW={}

def load(folder):return pack.read_pack(ROOT/'character'/folder/'manifest.json')
def add(m,clips,key,frames,ms=180,loop=False):
    frames=[im.copy() for im in frames]
    clips[key]=frames
    state=next((s for s in m['states'] if s['id']==key),None)
    if state is None:state={'id':key};m['states'].append(state)
    state.update(frameDurationsMs=[ms]*len(frames),loop=loop)
    for prop in ['facings','depthOffsets']:state.pop(prop,None)
    NEW.setdefault(m['character'],set()).add(key)

def sheet(name,cols=8,dirs=DIRS,height=74,reference=0):
    rows=clean.rows(OUT/'sources'/f'{name}.png',4,cols,gutter_fraction=.4)
    result={}
    for d,tiles in zip(dirs,rows):
        h=height if isinstance(height,int) else height[d]
        refheight=max(t.height for t in tiles) if reference is None else tiles[reference].height
        scale=min(h/refheight,87/max(t.width for t in tiles),83/max(t.height for t in tiles))
        result[d]=[clean.frame(t,scale) for t in tiles]
    return result

def marsh():
    m,c=load('sprite-polish-v2/marsh');m['character']='marsh'
    sit=sheet('marsh-sit',dirs=['south','east','north','west'])
    rest=sheet('marsh-rest',dirs=['south','east','north','west'])
    cargo=sheet('marsh-cargo')
    image=Image.open(OUT/'sources/marsh-water-spaced.png').convert('RGBA')
    ys=[0,131,248,370,475,621,761,892,1024];raw=[]
    for r in range(8):
        row=[]
        for col in range(4):
            tile=clean.clean(image.crop((col*384,ys[r],(col+1)*384,ys[r+1])))
            b=tile.getbbox();assert b and b[0]>0 and b[1]>0 and b[2]<tile.width and b[3]<tile.height,(r,col,b)
            row.append(tile.crop(b))
        raw.append(row)
    # Two side-tread cells face the opposite direction. Reassign those authored
    # cells; no raster mirroring or invented in-between frames.
    west=[raw[5][0],raw[5][1],raw[7][2],raw[5][1]]
    east=[raw[7][0],raw[7][1],raw[5][2],raw[5][3]]
    raw[5]=west;raw[7]=east
    water={}
    # Shared anatomical scale across front/rear foreshortening and side strokes.
    # Upright treading has bent legs, so its bounding height is not standing height.
    water_scale=87/max(t.width for row in raw for t in row)
    for i,d in enumerate(DIRS):
        tiles=raw[i]+raw[i+4]
        water[d]=[clean.frame(t,water_scale) for t in tiles]
    for d in DIRS:
        s,r,g,w=sit[d],rest[d],cargo[d],water[d];idle=c['idle-'+d][0]
        entry=[idle,s[1],s[2],s[3]]
        lie=[idle,r[2],r[3],r[4]] # Omit wrongly facing west-row column 1.
        for action,frames,ms,loop in [
            ('sit-down',entry,200,False),('sit-rise',entry[::-1],200,False),
            ('sit-idle',s[3:5],650,True),('read-seated',s[5:8],450,True),
            ('lie-down',lie,200,False),('get-up',[r[5],r[6],r[7],idle],200,False),
            ('sleep',r[4:6],900,True),('pickup',[idle,g[1],g[2],g[3]],130,False),
            ('carry',g[4:8],180,True),('cargo-unload',[g[3],g[2],g[1],idle],130,False),
            ('unload',[g[3],g[2],g[1],idle],130,False),
            ('swim',w[:4],180,True),('tread',w[4:],240,True)]:add(m,c,action+'-'+d,frames,ms,loop)
    pack.quantize(c);pack.save_pack('marsh',m,c)
    envelope=json.loads((ROOT/'character/sprite-polish-v2/marsh/clearance.json').read_text())
    for mode in envelope:
        for d in DIRS:
            boxes=[im.getbbox() for key,row in c.items() if key.endswith('-'+d) for im in row]
            b=[min(x[0]-46 for x in boxes),min(x[1]-86 for x in boxes),max(x[2]-46 for x in boxes),max(x[3]-86 for x in boxes)]
            b=[v*.8821621622 for v in b];old=envelope[mode][d]
            envelope[mode][d]=[min(old[0],b[0]),min(old[1],b[1]),max(old[2],b[2]),max(old[3],b[3])]
    (OUT/'marsh/clearance.json').write_text(json.dumps(envelope,indent=2))

def companion(identity):
    folder='josh-repair-v4' if identity=='josh' else 'companion-cleanup-v3'
    m,c=load(folder+'/'+identity);a,p=load(folder+'/'+identity+'-actions')
    m['character']=identity;a['character']=identity+'-actions'
    if identity=='margot':
        heights={d:34 if d=='south' else 28 for d in DIRS}
        sit=sheet('margot-sit',height=heights)
        for action in ['sit','groom','nap']:
            rows=sit if action=='sit' else sheet('margot-'+action,dirs=['south','east','north','west'] if action=='nap' else DIRS,height=heights)
            for d,t in rows.items():
                idle=c['idle-'+d][0]
                enter=[idle,t[0],t[1],t[2]]
                # Groom source's final side poses face the wrong way; use the
                # authored standing endpoint from the matching sit direction.
                leave=[t[5],t[6],sit[d][6] if action=='groom' else t[7],idle]
                add(a,p,action+'-enter-'+d,enter,200)
                add(a,p,action+'-'+d,t[2:6],450 if action!='nap' else 900,True)
                add(a,p,action+'-exit-'+d,leave,200)
        extras=sheet('margot-extras',height=heights)
        for d,t in extras.items():
            add(a,p,'stretch-'+d,t[:4],600)
            add(a,p,'yawn-enter-'+d,[c['idle-'+d][0],sit[d][1]],200)
            add(a,p,'yawn-'+d,t[4:8],600)
            add(a,p,'yawn-exit-'+d,[sit[d][6],c['idle-'+d][0]],200)
    else:
        height=44 if identity=='river' else 70
        # Generator delivered six columns for locomotion, despite eight requested.
        rows=sheet(identity+'-locomotion',cols=6,height=height)
        turns=sheet(identity+'-turns',cols=6,height=height)
        for d,t in rows.items():
            add(m,c,'move-start-'+d,[c['idle-'+d][0],t[1],c['walk-'+d][0]],150)
            add(m,c,'move-stop-'+d,[c['walk-'+d][-1],t[4],c['idle-'+d][0]],150)
        quarters={}
        for i,d in enumerate(DIRS):
            to=DIRS[(i+1)%4];t=turns[d]
            quarters[d,to]=[c['idle-'+d][0],*t[1:5],c['idle-'+to][0]]
            quarters[to,d]=quarters[d,to][::-1]
        for d in DIRS:
            for to in DIRS:
                if d==to:continue
                frames=quarters.get((d,to))
                if frames is None:
                    mid=DIRS[(DIRS.index(d)+1)%4];frames=quarters[d,mid]+quarters[mid,to][1:]
                add(m,c,'turn-'+d+'-'+to,frames,75)
            if identity=='josh':
                to=DIRS[(DIRS.index(d)+1)%4];q=quarters[d,to]
                add(a,p,'turn-enter-'+d,q[:2],150)
                add(a,p,'turn-'+d,[q[2],q[3],q[4],q[3],q[2]],360)
                add(a,p,'turn-exit-'+d,q[1::-1],150)
        power=sheet(identity+'-power'+('-keyed' if identity=='josh' else ''),cols=6,height=height,reference=None)
        for d,t in power.items():
            idle=c['idle-'+d][0]
            if identity=='river':
                add(a,p,'boot-'+d,t,350)
                add(a,p,'boot-exit-'+d,[t[-1],idle],150)
            else:
                add(a,p,'powerdown-enter-'+d,[idle,*t[1:]],150)
                add(a,p,'powerdown-'+d,t[4:],600,True)
                add(a,p,'powerdown-exit-'+d,[*t[4::-1],idle],150)
    both={**c,**p};pack.quantize(both)
    for manifest in [m,a]:
        manifest['sourceManifest']='../../'+folder+'/'+(identity if manifest is m else identity+'-actions')+'/manifest.json'
        manifest['expansionSources']='../sources/'
    pack.save_pack(identity,m,{k:both[k] for k in c})
    pack.save_pack(identity+'-actions',a,{k:both[k] for k in p})

def review():
    html=['<!doctype html><meta charset="utf-8"><title>Animation expansion v5</title><style>body{background:#18242a;color:#ddd;font:16px system-ui;padding:24px}.grid{display:flex;flex-wrap:wrap}figure{margin:8px}img{image-rendering:pixelated}figcaption{max-width:276px}</style><h1>Animation expansion v5</h1><p>Authored poses. Each preview shows native frames enlarged 3×. Source sheets and prior packs preserved.</p>']
    contact=[]
    for identity,keys in NEW.items():
        m,c=pack.read_pack(OUT/identity/'manifest.json');html.append('<h2>'+identity+'</h2><div class="grid">')
        for key in sorted(keys):
            state=next(s for s in m['states'] if s['id']==key);frames=[]
            for im in c[key]:
                bg=Image.new('RGBA',(92,92),'#18242a');bg.alpha_composite(im)
                frames.append(bg.resize((276,276),Image.Resampling.NEAREST).convert('RGB'))
            filename=identity+'--'+key+'.gif'
            frames[0].save(OUT/filename,save_all=True,append_images=frames[1:],duration=state['frameDurationsMs'],loop=0,disposal=2)
            html.append(f'<figure><img src="{filename}" width="276"><figcaption>{key}</figcaption></figure>')
            if key.endswith('-south') and '-turn-' not in key:contact.append((identity+' '+key,c[key][len(c[key])//2]))
        html.append('</div>')
    (OUT/'review.html').write_text(''.join(html))
    board=Image.new('RGB',(800,((len(contact)+3)//4)*125),'#18242a');draw=ImageDraw.Draw(board)
    for i,(label,im) in enumerate(contact):
        x=i%4*200;y=i//4*125;board.paste(im,(x+40,y),im);draw.text((x+3,y+100),label,fill='white')
    board.save(OUT/'contact.png')

if __name__=='__main__':
    if '--companions-only' not in sys.argv:marsh()
    for identity in ['margot','river','josh']:companion(identity)
    review()
    (OUT/'build-report.json').write_text(json.dumps({'packs':pack.REPORT,'newClips':{k:sorted(v) for k,v in NEW.items()},'sources':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (OUT/'sources').glob('*.png')}},indent=2))
    print(json.dumps(pack.REPORT))
