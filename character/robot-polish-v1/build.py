"""Package authored robot sources at double legacy density, without palette reduction."""
from pathlib import Path
import json,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
from extract import ROOT,DIRS,extract
REPO=ROOT.parents[1]
PIVOT=(92,172)

# Source pixels per 65.28 world units. Josh and River are drawn at half the crew's height (owner, Sept 29).
STANDING = {'river': 296, 'josh': 296}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2))

def register(tile,scale,head=False):
    a=np.array(tile);mask=a[:,:,3]>0
    # Lower chassis anchors keep wide reaching arms from recentering the robot.
    y,x=np.where(mask & (np.indices(mask.shape)[0]>=tile.height*.85))
    ax=(x.min()+x.max()+1)/2;ay=y.max()+1
    if head:
        y,x=np.where(mask & (np.indices(mask.shape)[0]<tile.height*.18));ax=(x.min()+x.max()+1)/2
    body=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.LANCZOS)
    body.putalpha(body.getchannel('A').point(lambda v:255 if v>=128 else 0))
    # Register the final opaque contact after resize/alpha threshold. Rounding the
    # pre-resize bottom allowed a one-pixel vertical wobble between rolling frames.
    xy=(round(92-ax*scale),172-body.getbbox()[3])
    assert min(xy)>0 and xy[0]+body.width<184 and xy[1]+body.height<184,(tile.size,scale,xy)
    out=Image.new('RGBA',(184,184));out.alpha_composite(body,xy);return out

def main():
    catalog={};report={};calibration={}
    diagonals=extract('diagonals-v1',4,['josh','river'])
    for who,height in [('josh',140),('river',88)]:
        motion=extract(who+'-motion-v1',6);actions=extract(who+'-actions-v1',8)
        turns=extract(who+'-turns-v1',6)
        special=extract('josh-weld-v3' if who=='josh' else 'river-float-v1',6)
        if who=='josh':special['west'],special['east']=special['east'],special['west']
        power=extract('josh-power-v2' if who=='josh' else 'river-boot-v1',6)
        clips={};states=[];groups={'locomotion':[],'actions':[],'water':[]};calibration[who]={}
        def add(key,images,ms,group='actions',loop=True,note='authored'):
            files=[]
            for i,im in enumerate(images):
                rel=f'{who}/frames/{key}/{i:03}.png';p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True);im.save(p);files.append(rel)
            s=dict(id=key,frameFiles=files,frameDurationsMs=ms if isinstance(ms,list) else [ms]*len(images),loop=loop,provenance=note)
            states.append(s);groups[group].append(s);clips[key]=images
        m={};a={};t={};p={};sp={}
        for d in DIRS:
            scales={'motion':height/motion[d][0].height,'actions':height/actions[d][0].height,
                    'turns':height/turns[d][0].height,'power':height/power[d][0 if who=='josh' else 5].height,
                    'special':height/special[d][0].height}
            calibration[who][d]=scales
            m[d]=[register(im,scales['motion']) for im in motion[d]]
            a[d]=[register(im,scales['actions']) for im in actions[d]]
            t[d]=[register(im,scales['turns']) for im in turns[d]]
            p[d]=[register(im,scales['power']) for im in power[d]]
            sp[d]=[register(im,scales['special'],head=who=='josh') for im in special[d]]
            add('idle-'+d,[m[d][0],m[d][1],m[d][0]],[1800,350,650],'locomotion')
            add('walk-'+d,m[d][2:],160,'locomotion')
            add('move-start-'+d,[m[d][0],m[d][2]], [200,250],'locomotion',False,'shared idle and rolling endpoints')
            add('move-stop-'+d,[m[d][5],m[d][0]], [200,250],'locomotion',False,'shared rolling and idle endpoints')
            def chain(name,entry,loop,exit,ms=360):
                add(name+'-enter-'+d,entry,160,loop=False)
                add(name+'-'+d,loop,ms)
                add(name+'-exit-'+d,exit,160,loop=False)
            if who=='josh':
                chain('watch',[m[d][0],a[d][0]],[a[d][0],a[d][1],a[d][0],a[d][3],a[d][0]],[a[d][0],m[d][0]],550)
                # Reject the actions sheet's powered-off face drift; use the dedicated correction.
                chain('powerdown',[m[d][0],p[d][1],p[d][2],p[d][3]],[p[d][3]],
                      [p[d][3],p[d][2],p[d][1],m[d][0]],1200)
                w=sp[d]
                chain('torch',[m[d][0],w[0],w[1]],[w[2],w[3],w[2],w[4]],
                      [w[1],w[0],m[d][0]],180)
            else:
                # Columns3/7 turned too far in side rows; omit them, never mirror.
                chain('scan',[m[d][0],a[d][0]],[a[d][0],a[d][1],a[d][2],a[d][1]],
                      [a[d][0],m[d][0]],450)
                chain('inspect',[m[d][0],a[d][4],a[d][5]],[a[d][5],a[d][6],a[d][5]],
                      [a[d][5],a[d][4],m[d][0]],500)
                indices=[1,2,3,4,5] if d=='west' else [0,1,2,3,4,5]
                add('boot-'+d,[p[d][i] for i in indices],350,loop=False,
                    note='west front-facing first source cell omitted')
                add('boot-exit-'+d,[p[d][5],m[d][0]],150,loop=False)
                add('float-'+d,sp[d][:4],180,'water')
                add('float-idle-'+d,sp[d][4:],450,'water')
        quarters={}
        # Reviewed intermediate diagonals; generated grid endpoints sometimes face the wrong way.
        # Use exact locomotion cardinal endpoints and one actual diagonal per quarter.
        for i,d in enumerate(DIRS):
            to=DIRS[(i+1)%4]
            tile=diagonals[who][i];diagonal=register(tile,height/tile.height)
            q=[m[d][0],diagonal,m[to][0]]
            quarters[d,to]=q;quarters[to,d]=q[::-1]
            if who=='josh':
                add('turn-enter-'+d,q[:2],150,loop=False)
                add('turn-'+d,[q[1],q[2],q[1]],450)
                add('turn-exit-'+d,q[1::-1],150,loop=False)
        for d in DIRS:
            for to in DIRS:
                if d==to:continue
                q=quarters.get((d,to))
                if q is None:
                    mid=DIRS[(DIRS.index(d)+1)%4];q=quarters[d,mid]+quarters[mid,to][1:]
                add('turn-'+d+'-'+to,q,150,'locomotion',False,'authored diagonal; shared cardinal endpoints; reversed/composed quarters')
        stand=STANDING.get(who,148)
        manifest=dict(character=who,frameWidth=184,frameHeight=184,pivot=list(PIVOT),standingHeight=stand,
                      strideDistanceCells={'walk':.1},mirrored=False,status='installed-source',states=states)
        write(ROOT/who/'manifest.json',manifest)
        for group,rows in groups.items():
            if not rows:continue
            part={**manifest,'states':[{**s,'frameFiles':['../../../'+f for f in s['frameFiles']]} for s in rows]}
            write(ROOT/who/'packs'/group/'manifest.json',part)
        if who=='river':
            envelope={}
            for d in DIRS:
                boxes=[im.getbbox() for key,images in clips.items() if key.startswith('float-') and key.endswith('-'+d) for im in images]
                envelope[d]=[(min(b[0] for b in boxes)-92)*65.28/stand,(140-172)*65.28/stand,
                             (max(b[2] for b in boxes)-92)*65.28/stand,(max(b[3] for b in boxes)-172)*65.28/stand]
            write(ROOT/who/'clearance.json',{'bare':envelope,'helmet':envelope})
        # Freeze installed low-density baseline only once, before changing the consumer.
        basepath=ROOT/who/'baseline.json'
        if not basepath.exists():
            oldstates=[]
            paths=[REPO/'character/animation-expansion-v5'/name/'manifest.json' for name in [who,who+'-actions']]
            if who=='river':paths.append(REPO/'character/companion-water-v1/river/manifest.json')
            for path in paths:
                old=json.loads(path.read_text())
                for s in old['states']:
                    files=[]
                    for i,f in enumerate(s['frameFiles']):
                        rel=f'{who}/baseline/{s["id"]}/{i:03}.png';dest=ROOT/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path.parent/f,dest);files.append(rel)
                    oldstates.append({**s,'frameFiles':files})
            write(basepath,dict(character=who,frameWidth=92,frameHeight=92,pivot=[46,86],standingHeight=74,states=oldstates))
        baseline=json.loads(basepath.read_text());assert {s['id'] for s in baseline['states']}=={s['id'] for s in states}
        selected=['idle','walk','watch','torch','powerdown'] if who=='josh' else ['idle','walk','scan','inspect','boot','float']
        board=Image.new('RGB',(184*len(selected),210*4),'#18252b');draw=ImageDraw.Draw(board)
        for r,d in enumerate(DIRS):
            for c,key in enumerate(selected):
                im=clips[key+'-'+d][min(1,len(clips[key+'-'+d])-1)];board.paste(im,(c*184,r*210+20),im)
                draw.text((c*184+8,r*210+6),key+' / '+d,fill='#cbd4d8')
        board.save(ROOT/'review'/f'{who}-contact.png')
        report[who]={'states':len(states),'frameReferences':sum(len(s['frameFiles']) for s in states),'groups':{g:len(v) for g,v in groups.items()}}
        catalog[who]=dict(manifest=f'{who}/manifest.json',baseline=f'{who}/baseline.json')
    write(ROOT/'catalog.json',catalog);write(ROOT/'review/calibration.json',calibration)
    write(ROOT/'review/build-report.json',{'packs':report,'sources':{p.name:sha(p) for p in (ROOT/'sources').glob('*.png')}})
    print(json.dumps(report))
if __name__=='__main__':main()
