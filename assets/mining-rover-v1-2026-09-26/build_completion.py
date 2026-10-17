"""Complete rover work, cargo and power-state review clips from registered art."""
from pathlib import Path
import json,math,hashlib,sys
from PIL import Image
R=Path(__file__).resolve().parent;O=R/'completion';O.mkdir(exist_ok=True)
cargo_only='--cargo-only' in sys.argv
D=json.loads((R/'manifest.json').read_text());D['states']=[e for e in D['states'] if not e.get('completionSupplement') or (cargo_only and e['state'] not in ['carry','collect','unload'])]
original={e['id']:e for e in D['states']};SIZE=448
source=R.parent/'drone-motion-v2-2026-09-26/cargo/job-collect-south/090.png'
ore=Image.open(source).convert('RGBA');ore=ore.crop(ore.getbbox());ore=ore.resize((max(1,round(ore.width*18/ore.height)),18),Image.Resampling.LANCZOS)
ore.save(O/'ore-source.png')
dirs={'north':(0,-1),'east':(1,0),'south':(0,1),'west':(-1,0),'northeast':(.707,-.707),'southeast':(.707,.707),'southwest':(-.707,.707),'northwest':(-.707,-.707)}
def save(im,path):path.parent.mkdir(parents=True,exist_ok=True);im.save(path,compress_level=3);return path.relative_to(R).as_posix()
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def cargo(h,progress=1,unloading=False):
    im=Image.new('RGBA',(SIZE,SIZE));u=dirs[h];v=(-u[1],u[0])
    for j in range(5):
        t=smooth((progress*1.6-j*.12)/1.12);t=1-t if unloading else t
        start=125+j*2;end=(j-2)*7
        along=start*(1-t)+end*t;side=(((j%3)-1)*7+(j//3)*2)*(1-t)+((j%2)*2-1)*3*t
        x=224+u[0]*along+v[0]*side;y=224+u[1]*along+v[1]*side
        im.alpha_composite(ore,(round(x-ore.width/2),round(y-ore.height/2)))
    return im
empty=Image.new('RGBA',(SIZE,SIZE));emptyPath=save(empty,O/'empty.png')
checks=[]
for h in D['headings']:
    pose=D['headings'][h]['pose'];drive=original['drive-'+h]
    D['headings'][h]['cargoPose']=save(cargo(h),O/'cargo-poses'/f'{h}.png')
    states=['start','stop','carry','power-on','power-off','charging','disabled']
    if h in ['north','east','south','west']:states+=['collect','unload','blocked']
    if cargo_only:states=[state for state in states if state in ['carry','collect','unload']]
    for state in states:
        count=120 if state in ['collect','unload','blocked'] else 60
        frames=[];effects=[];cargos=[];phases=[];lamp=[];distances=[]
        for n in range(count):
            t=n/30;path=pose;effect=emptyPath;phase=state;distance=0
            if state=='carry':path=drive['frameFiles'][n]
            elif state in ['start','stop']:
                speed=drive['travelWorldUnitsPerSecond'];ramp=speed/50
                distance=25*min(t,ramp)**2+speed*max(0,t-ramp) if state=='start' else speed*min(t,ramp)-25*min(t,ramp)**2
                path=drive['frameFiles'][math.floor(distance/speed*30)%60]
                phase=('Accelerating' if t<ramp else 'Rolling') if state=='start' else ('Braking' if t<ramp else 'Stopped')
            elif state=='blocked':
                # Brace/deploy, short jam, then recover using the authored retraction.
                index=n if n<45 else 44 if n<60 else min(179,135+n-60)
                path=original['mine-'+h]['frameFiles'][index]
                phase='Brace' if n<15 else 'Deploy' if n<45 else 'Blocked' if n<60 else 'Retract' if n<90 else 'Ready'
            elif state in ['collect','unload']:phase=('Intake' if state=='collect' else 'Discharge') if n<105 else ('Loaded' if state=='collect' else 'Deposited')
            elif state=='power-on':phase='Boot' if n<45 else 'Ready'
            elif state=='power-off':phase='Powering down' if n<45 else 'Off'
            elif state=='charging':phase='Charging'
            elif state=='disabled':phase='Stopped / disabled'
            pulse=.35+.65*(.5+.5*math.cos(t/.85*math.tau))
            intensity=smooth(n/44) if state=='power-on' else 1-smooth(n/44) if state=='power-off' else pulse
            lamp.append(intensity);phases.append(phase);frames.append(path);effects.append(effect);distances.append(distance)
            if state in ['collect','unload','carry']:
                im=cargo(h,1 if state=='carry' else min(1,n/104),state=='unload')
                cargos.append(save(im,O/'cargo'/f'{state}-{h}'/f'{n:03}.png'))
        atlas=Image.new('RGBA',(SIZE*6,SIZE*math.ceil(count/6)));fx=Image.new('RGBA',atlas.size);ca=Image.new('RGBA',atlas.size)
        for n,path in enumerate(frames):
            xy=(n%6*SIZE,n//6*SIZE);atlas.paste(Image.open(R/path),xy)
            if cargos:ca.paste(Image.open(R/cargos[n]),xy)
        entry={'id':state+'-'+h,'state':state,'heading':h,'frameFiles':frames,'effectFiles':effects,'frameCount':count,'fps':30,'loop':state in ['carry','charging','disabled'],'holdFrame':count-1,'phases':phases,'atlas':{'path':save(atlas,O/'atlases'/f'{state}-{h}.png'),'columns':6},'effectAtlas':{'path':save(fx,O/'atlases'/f'empty-{count}.png'),'columns':6},'travelWorldUnitsPerSecond':drive['travelWorldUnitsPerSecond'] if state in ['carry','start','stop'] else 0,'rootDistanceWorld':distances,'lampSamples':lamp,'lampColor':'charging' if state=='charging' else 'stopped' if state in ['disabled','blocked'] else 'operational','completionSupplement':True}
        if state not in ['power-on','power-off']:entry.pop('lampSamples',None)
        if cargos:entry.update(cargoFiles=cargos,cargoAtlas={'path':save(ca,O/'atlases'/f'{state}-{h}-cargo.png'),'columns':6})
        D['states'].append(entry);checks.append({'clip':entry['id'],'frames':count})
    print(h,'complete',flush=True)
D['scope']='Complete Mining rover animation review set: eight-way travel and lifecycle, four cardinal mining/intake/unload/blocked jobs, cargo and independent power lights. Review only; no game integration.'
D['statusClips']=[{'id':key,'color':value,'frameCount':51,'fps':30,'loop':True,'alpha':[.35+.65*(.5+.5*math.cos(n/30/.85*math.tau)) for n in range(51)]} for key,value in D['lamp']['colors'].items()]
D['completion']={'oreSource':str(source),'oreSourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'bodyMethod':'reuse registered authored poses/tyre frames; no whole-rover rotations','startStopPlayback':'rootDistanceWorld records matching travel; interactive player integrates the same acceleration','cargoMethod':'existing generated ore pixels; intake along front tool axis into the central processing bay','powerMethod':'stationary chassis with separate lampSamples; no extra machinery invented'}
D['completion']['completeCycle']=['mine','collect','carry for 3 seconds','unload','idle; deposited ore persists']
(R/'manifest.json').write_text(json.dumps(D,indent=2));(O/'build-checks.json').write_text(json.dumps(checks,indent=2));print('TOTAL',len(D['states']),'clips',flush=True)
