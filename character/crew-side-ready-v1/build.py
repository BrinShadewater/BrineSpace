from pathlib import Path
import json, shutil, hashlib
from PIL import Image, ImageDraw

P=Path(__file__).resolve().parent
C=P.parent
P.mkdir(exist_ok=True)
rows=[]
provenance=[]
for who,old in [('bill','major-bill-v3'),('branforth','chief-engineer-branforth-v2')]:
    dst=P/who; dst.mkdir(exist_ok=True)
    states=[]
    clips=[]
    for direction in ['east','west']:
        version='v2' if who=='branforth' and direction=='east' else 'v1'
        source=C/f'{who}-video-{direction}-{version}'
        # The accepted east recut may keep its standing source in the original pilot.
        master=source/'master-standing.png'
        if not master.exists(): master=C/f'{who}-video-{direction}-v1/master-standing.png'
        idle=dst/f'idle-{direction}.png'; shutil.copyfile(master,idle)
        states.append(dict(id=f'idle-{direction}',frameCount=1,frameFiles=[idle.name],frameDurationsMs=[1000],loop=True))
        provenance.append(dict(character=who,direction=direction,source=str(master.relative_to(C)),sha256=hashlib.sha256(master.read_bytes()).hexdigest(),method='Unmodified registered master hold; no synthetic breathing'))
        m=json.loads((source/'manifest.json').read_text());s=m['states'][0]
        frames=[Image.open(source/f).convert('RGBA') for f in s['frameFiles']]
        clips.append((Image.open(idle).convert('RGBA'),frames,s['frameDurationsMs']))
    (dst/'manifest.json').write_text(json.dumps(dict(name=f'{who} approved-master side idle holds',status='candidate_not_installed',frameWidth=184,frameHeight=184,pivot=[92,172],standingHeight=148,precomposed=True,states=states),indent=2))
    rows.append((who,clips))

out=[]
for tick in range(144):
    bg=Image.new('RGB',(960,840),'#263139');draw=ImageDraw.Draw(bg)
    for row,(who,clips) in enumerate(rows):
        for col,(idle,frames,durations) in enumerate(clips):
            t=tick*1000/24
            # 1s master hold, one unmodified source-speed loop, then master hold.
            if 1000<=t<1000+sum(durations):
                elapsed=t-1000;n=0
                while n<len(frames)-1 and elapsed>=durations[n]:elapsed-=durations[n];n+=1
                im=frames[n];label='WALK'
            else: im=idle;label='MASTER HOLD'
            x=col*480;y=row*420
            draw.text((x+12,y+10),f'{who.upper()} / {("EAST","WEST")[col]} / {label}',fill='white')
            large=im.resize((368,368),Image.Resampling.NEAREST);bg.paste(large,(x+56,y+28),large)
            small=im.resize((74,74),Image.Resampling.LANCZOS);bg.paste(small,(x+390,y+330),small)
    out.append(bg)
out[0].save(P/'idle-walk-review.gif',save_all=True,append_images=out[1:],duration=[40,40,50]*48,loop=0,optimize=False)
(P/'provenance.json').write_text(json.dumps(provenance,indent=2))

# Review current remaining cardinal walks before selecting another paid source.
remaining=[]
for who,old in [('bill','major-bill-v3'),('branforth','chief-engineer-branforth-v2')]:
    root=C/old;catalog=json.loads((root/'catalog.json').read_text())
    for rel in catalog['body']:
        mp=root/rel;m=json.loads(mp.read_text())
        for s in m['states']:
            if s['id'] in ['walk-north','walk-south']:
                remaining.append((who,s['id'],[Image.open(mp.parent/f).convert('RGBA') for f in s['frameFiles']],s['frameDurationsMs']))
contact=Image.new('RGB',(1104,len(remaining)*220),'#263139');d=ImageDraw.Draw(contact)
for row,(who,state,frames,durations) in enumerate(remaining):
    d.text((8,row*220+5),f'{who.upper()} / CURRENT {state} / {len(frames)} frames',fill='white')
    for col in range(min(6,len(frames))):
        im=frames[round(col*(len(frames)-1)/5)];contact.paste(im,(184*col,row*220+28),im)
contact.save(P/'remaining-walks.png')
print('Built four master idle holds, transition review, and remaining cardinal walk contact sheet.')
