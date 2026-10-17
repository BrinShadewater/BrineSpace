"""Build a consolidated current-source review and native snapshot contract."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-consistency-review-v1'
def main():
    BASE.mkdir(parents=True,exist_ok=True);states={};catalog=json.loads((ROOT/'character/marsh-v2/catalog.json').read_text())
    for path in catalog['body']:
        manifest=ROOT/'character/marsh-v2'/path;data=json.loads(manifest.read_text())
        for s in data['states']:
            files=[(manifest.parent/f).resolve().relative_to(ROOT).as_posix() for f in s['frameFiles']]
            states[s['id']]={'files':files,'hashes':[hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files],'durations':s['frameDurationsMs'],'loop':s['loop'],'pivot':data['pivot'],'standingHeight':data.get('standingHeight',148)}
    review={k:v for k,v in states.items() if not k.startswith(('equip-helmet-','remove-helmet-'))}
    (BASE/'runtime-contract.json').write_text(json.dumps({'states':review},indent=2)+'\n')
    families=sorted({k.rsplit('-',1)[0] for k in review if all(a+'-'+d in review for d in ('south','north','east','west') for a in [k.rsplit('-',1)[0]])})
    for batch in range(0,len(families),6):
        actions=families[batch:batch+6];board=Image.new('RGB',(1472,220*len(actions)),'#293b40');draw=ImageDraw.Draw(board)
        for row,a in enumerate(actions):
            draw.text((4,row*220+4),a,fill='white')
            for c,d in enumerate(('south','north','east','west')):
                for j,key in enumerate(('idle-'+d,a+'-'+d)):
                    s=review[key];im=Image.open(ROOT/s['files'][len(s['files'])//2 if j else 0]).convert('RGBA');pivot=s['pivot'];board.paste(im,(c*368+j*184+92-round(pivot[0]),row*220+196-round(pivot[1])),im)
        board.save(BASE/f'comparison-{batch//6:02}.png')
    groups=[]
    recipes=[('Travel',['idle','walk','run','walk','idle']),('Diagnostics',['idle','kneel','repair','stand','idle','interact','idle']),('Inspection',['idle','inspect','idle']),('Galley',['idle','eat','drink','idle']),('Crew conversation',['idle','crew-chat','idle']),('Welding',['idle','torch-draw','weld','torch-stow','idle']),('Cargo',['idle','pickup','carry','unload','idle']),('Seated reading',['idle','sit-down','sit-idle','read-seated','sit-rise','idle']),('Rest',['idle','lie-down','sleep','get-up','idle']),('Swimming',['tread','swim-start','swim','swim-stop','tread']),('Loaded water',['tread','swim-pickup','swim-carry','cargo-drain','carry']),('Ground shutdown',['idle','death-ground']),('Water shutdown',['tread','death-water']),('Retained recovery',['idle','recover-air','idle']),('Retained water instability',['tread','swim-distress','tread'])]
    for title,actions in recipes:
        columns=[]
        for d in ('south','north','east','west'):
            keys=[a+'-'+d for a in actions]
            if all(k in review for k in keys):columns.append({'label':d,'keys':keys})
        if columns:groups.append({'title':title,'columns':columns})
    for prefix,title in [('swim-turn-','Swimming turns'),('swim-carry-turn-','Loaded swimming turns'),('carry-turn-','Cargo turns')]:
        keys=[k for k in review if k.startswith(prefix)]
        for batch in range(0,len(keys),4):groups.append({'title':title+' '+str(batch//4+1),'columns':[{'label':k[len(prefix):],'keys':[k]} for k in keys[batch:batch+4]]})
    for title,keys in [('Bought bunk',['bunk-enter-east','bunk-sleep-east','bunk-exit-east']),('Retained berth',['berth-lie-east','berth-sleep-east','berth-rise-east'])]:
        if all(k in review for k in keys):groups.append({'title':title,'columns':[{'label':'east','keys':keys}]})
    if all('injury-ground-'+d in review for d in ('south','north','east','west')):
        groups.append({'title':'Containment injury and recovery','columns':[{'label':d,'keys':['idle-'+d,'injury-ground-'+d,'injury-rise-'+d,'idle-'+d]} for d in ('south','north','east','west')]})
    if 'walk-start-north' in review:
        groups.append({'title':'North ground start','columns':[{'label':'north','keys':['idle-north','walk-start-north','walk-north']}]})
    for first in [0,3]:
        keys=[f'walk-stop-p{i}-north' for i in range(first,first+3)]
        if all(k in review for k in keys):groups.append({'title':f'North ground stops phases{first}-{first+2}','columns':[{'label':k,'keys':[k,'idle-north']} for k in keys]})
    data={'states':review,'groups':groups}
    html="""<!doctype html><meta charset="utf-8"><title>Marsh complete animation review</title><style>body{background:#17252a;color:#dde7e8;font:16px system-ui;max-width:1100px;margin:32px auto;padding:16px}h1{font-size:28px}select,button{font:inherit;padding:8px;background:#293b40;color:inherit;border:1px solid #637b80;border-radius:6px;margin-right:8px}canvas{max-width:100%;background:#293b40;border-radius:12px;margin-top:18px}p{line-height:1.5;color:#b9ccce}a{color:#a8d9cd}</style><h1>Marsh / complete animation review</h1><p>Compare identity and transitions across all four directions. Idle holds are shortened for review. Diagnostic suit brightness is matched to idle. Physical injury uses white synthetic fluid; battery shutdown stays dry.</p><select id="group"></select><select id="size"><option value="65.28">Station size</option><option value="148">Source size</option><option value="27">Far view</option></select><button id="pause">Pause</button><button id="restart">Restart</button><canvas id="view" width="1040" height="480"></canvas><p id="caption"></p><p>Furniture previews show sprite motion; room contact is reviewed separately. Distress and air-recovery are retained compatibility clips: Marsh does not need air.</p><p><a href="../marsh-run-carry-review-v1/index.html">Detailed clips and white-fluid injury preview</a></p><script>const DATA=__DATA__;const images={};for(const s of Object.values(DATA.states))for(const f of s.files)if(!images[f]){let im=new Image();im.src='../'+f.slice('character/'.length);images[f]=im}const choose=document.querySelector('#group'),size=document.querySelector('#size'),canvas=document.querySelector('#view'),ctx=canvas.getContext('2d');DATA.groups.forEach((g,i)=>choose.add(new Option(g.title,i)));let began=performance.now(),held=0,paused=false;document.querySelector('#pause').onclick=()=>{paused=!paused;if(paused)held=performance.now()-began;else began=performance.now()-held;document.querySelector('#pause').textContent=paused?'Play':'Pause'};function restart(){began=performance.now();held=0}choose.onchange=restart;document.querySelector('#restart').onclick=restart;function total(s,key){if(key.startsWith('idle-'))return 500;return s.durations.reduce((a,b)=>a+b,0)*(s.loop?2:1)+(key.startsWith('death-')?800:0)}function render(now){let g=DATA.groups[Number(choose.value)],time=paused?held:now-began;ctx.fillStyle='#293b40';ctx.fillRect(0,0,1040,480);ctx.fillStyle='#dbe6e8';ctx.font='16px system-ui';let captions=[];g.columns.forEach((col,i)=>{let length=col.keys.reduce((a,k)=>a+total(DATA.states[k],k),0),t=time%length,key=col.keys[col.keys.length-1];for(const k of col.keys){let n=total(DATA.states[k],k);if(t<n){key=k;break}t-=n}let s=DATA.states[key],cycle=s.durations.reduce((a,b)=>a+b,0),cursor=s.loop?t%cycle:Math.min(t,cycle),slot=0;while(slot<s.durations.length-1&&cursor>=s.durations[slot]){cursor-=s.durations[slot];slot++}let x=130+i*260,scale=Number(size.value)/s.standingHeight,img=images[s.files[slot]];ctx.fillText(col.label,x-95,40);ctx.fillText(key,x-110,70);ctx.strokeStyle='#62777b';ctx.beginPath();ctx.moveTo(x-115,390);ctx.lineTo(x+115,390);ctx.stroke();ctx.imageSmoothingEnabled=false;if(img.complete&&img.naturalWidth)ctx.drawImage(img,x-s.pivot[0]*scale,390-s.pivot[1]*scale,img.width*scale,img.height*scale);captions.push(key+' / '+slot)});document.querySelector('#caption').textContent=captions.join(' | ');requestAnimationFrame(render)}requestAnimationFrame(render);</script>"""
    (BASE/'index.html').write_text(html.replace('__DATA__',json.dumps(data)),encoding='utf8');(BASE/'groups.json').write_text(json.dumps(groups,indent=2)+'\n');print(len(review),'runtime states;',sum(len(s['files']) for s in review.values()),'source slots;',len(groups),'review chains')
if __name__=='__main__':main()
