"""Selected Veld east carry source rig; native validation is recorded separately."""
from pathlib import Path
import copy,json,hashlib,base64,io,argparse
import numpy as np
from PIL import Image
from rebuild_bill_art import chroma,binary
from repair_crew_walk import VELD_EAST,build

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'character/crew-action-detail-v2/sources/veld-carry-east-candidate-01.png'
OUT=ROOT/'character/crew-action-detail-v2/review/veld-carry-east-local-02'

def main(actor='veld',direction='east'):
    source_path=SOURCE if actor=='veld' else SOURCE.with_name('branforth-carry-east-donor-01.png')
    out=OUT if actor=='veld' else OUT.with_name('branforth-carry-east-local-01')
    if direction=='west':
        source_path=SOURCE.with_name(f'{actor}-carry-west-donor-01.png')
        out=OUT.with_name(f'{actor}-carry-west-local-01')
    out.mkdir(parents=True,exist_ok=True)
    raw=chroma(source_path);tile=raw.crop((0,0,raw.width//6,raw.height)) if actor=='veld' and direction=='east' else raw;bounds=tile.getbbox()
    reference=Image.open(ROOT/f'character/crew-action-detail-v2/sources/{actor}-idle-{direction}-reference-01.png')
    ref_bounds=reference.getbbox();scale=(ref_bounds[3]-ref_bounds[1])/(bounds[3]-bounds[1]);a=np.array(tile)
    _,xs=np.where(a[bounds[1]:bounds[1]+40,:,3]>0);anchor=float(xs.min()+xs.max()+1)/2
    dense=binary(tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX),True)
    donor=Image.new('RGBA',(184,184));donor.alpha_composite(dense,(round(92-anchor*scale),round(172-bounds[3]*scale)))
    rig=copy.deepcopy(VELD_EAST)
    rig['durations']=[140]*6 # Preserve the installed carry cadence, not walk timing.
    rig['sourceFrame']=0
    rig['direction']=direction
    rig['far'].update({'hip':(85,114),'knee':(74,138),'ankle':(63,157),'targetHip':(85,118),
        'upper':[(79,109),(92,112),(86,131),(80,143),(72,149),(62,140),(69,124)],
        'lower':[(67,132),(80,139),(73,151),(67,164),(55,163),(53,154)],
        'foot':[(55,150),(66,154),(67,161),(74,164),(79,169),(76,172),(64,171),(54,165)]})
    rig['near'].update({'hip':(94,114),'knee':(104,136),'ankle':(116,156),'targetHip':(94,118),
        'upper':[(86,108),(100,109),(107,123),(112,139),(105,147),(94,144),(86,130)],
        'lower':[(99,129),(111,133),(117,147),(122,158),(113,165),(103,153)],
        'foot':[(109,150),(121,151),(125,157),(132,157),(135,162),(131,169),(113,172),(105,168),(105,160)]})
    if actor=='branforth':
        rig['far'].update({'hip':(81,116),'knee':(66,135),'ankle':(49,152),'targetHip':(83,122),
            'upper':[(72,112),(89,115),(82,127),(73,142),(63,144),(54,136),(62,122)],
            'lower':[(57,130),(73,138),(64,147),(55,159),(42,161),(36,151),(46,140)],
            'foot':[(37,145),(51,148),(54,154),(58,157),(61,164),(57,171),(47,169),(38,160),(33,151)]})
        rig['near'].update({'hip':(94,116),'knee':(103,133),'ankle':(110,156),'targetHip':(94,127),
            'upper':[(86,110),(103,113),(112,124),(111,139),(101,145),(91,137),(85,125)],
            'lower':[(96,128),(111,131),(115,144),(116,157),(105,166),(97,154)],
            'foot':[(103,149),(115,149),(119,157),(130,158),(138,163),(137,170),(120,173),(103,171),(100,161)]})
    if direction=='west':
        rig['travel']=32
        rig['far'].update({'hip':(99,116),'knee':(116,139),'ankle':(132,158),'targetHip':(99,118),
            'upper':[(90,112),(105,114),(113,125),(124,141),(117,150),(102,139),(94,128)],
            'lower':[(109,132),(124,137),(132,147),(138,158),(128,168),(117,158),(111,147)],
            'foot':[(127,150),(138,151),(143,159),(138,169),(126,174),(119,173),(119,165),(129,161)]})
        rig['near'].update({'hip':(88,114),'knee':(77,128),'ankle':(75,158),'targetHip':(89,118),
            'upper':[(80,109),(97,112),(93,124),(85,134),(77,137),(68,132),(72,120)],
            'lower':[(70,122),(85,124),(86,139),(83,154),(82,162),(70,166),(66,149)],
            'foot':[(69,151),(82,152),(84,163),(80,172),(62,173),(54,169),(54,163),(68,160)]})
        if actor=='branforth':
            rig['far'].update({'hip':(100,115),'knee':(118,137),'ankle':(133,156),
                'upper':[(89,109),(107,110),(117,122),(128,139),(120,150),(104,141),(94,129)],
                'lower':[(109,128),(127,134),(138,148),(144,157),(135,168),(120,163),(111,146)],
                'foot':[(126,147),(141,148),(147,158),(141,169),(127,175),(117,174),(117,164),(128,159)]})
            rig['near'].update({'hip':(88,113),'knee':(77,126),'ankle':(72,157),
                'upper':[(78,107),(99,111),(94,125),(85,137),(75,138),(65,130),(71,117)],
                'lower':[(66,120),(86,122),(87,139),(81,157),(78,166),(64,167),(61,149)],
                'foot':[(62,150),(80,151),(82,165),(77,174),(59,174),(49,171),(48,163),(62,158)]})
    frames,joints=build(donor,rig)
    sheet=Image.new('RGB',(184*6,208),'#293b40')
    for i,frame in enumerate(frames):
        frame.save(out/f'{i:03}.png');sheet.paste(frame,(i*184,20),frame)
    donor.save(out/'donor.png');sheet.save(out/'contact.png')
    elapsed=np.r_[0,np.cumsum(rig['durations'])[:-1]]
    travel=elapsed/sum(rig['durations'])*rig['travel']*2*(1 if direction=='east' else -1)
    checks={}
    for leg,phases in [('near',[0,1,2]),('far',[3,4,5])]:
        contacts=[joints[i][leg]['ankle'][0]+travel[i] for i in phases]
        checks[leg+'StanceDriftPx']=float(max(contacts)-min(contacts))
        checks[leg+'SoleErrorPx']=max(abs(joints[i][leg]['soleActual']-172) for i in phases)
    assert max(checks.values())<=1,checks
    (out/'recipe.json').write_text(json.dumps({'status':'source_revision_selection_recorded_separately','source':source_path.relative_to(ROOT).as_posix(),
        'sha256':hashlib.sha256(source_path.read_bytes()).hexdigest(),'scale':scale,'headAnchorX':anchor,
        'rig':rig,'joints':joints,'checks':checks},indent=2)+'\n')
    def uri(im):
        stream=io.BytesIO();im.save(stream,format='PNG')
        return 'data:image/png;base64,'+base64.b64encode(stream.getvalue()).decode()
    pickup_revision='03' if actor=='veld' and direction=='east' else '01'
    pickup=Image.open(ROOT/f'character/crew-action-detail-v2/review/{actor}-pickup-{direction}-{pickup_revision}/005.png').convert('RGBA').crop((36,52,220,236))
    page='''<!doctype html><meta charset="utf-8"><title>Veld carry candidate</title>
<style>body{background:#293b40;color:#eee;font:16px system-ui}canvas{image-rendering:pixelated}</style>
<h1>Veld east cargo source revision</h1><p>Selected source revision; native checks recorded separately. Left: pickup endpoint. Middle: carry cycle. Right: carry at station scale. Inspect hips, crate size and hand contact.</p>
<button id="play">Pause</button><canvas id="view" width="700" height="240"></canvas>
<script>const sources=DATA,frames=sources.map(src=>{let im=new Image();im.src=src;return im});const durations=DURATIONS;let playing=true,t=0,last=performance.now();play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play'};
function draw(now){if(playing)t+=now-last;last=now;let time=t%durations.reduce((a,b)=>a+b,0),n=0;while(n<5&&time>=durations[n])time-=durations[n++];const c=view.getContext('2d');c.clearRect(0,0,700,240);c.imageSmoothingEnabled=false;if(frames.every(f=>f.complete)){c.drawImage(frames[0],40,20);c.drawImage(frames[n+1],280,20);const s=65.28/148;c.drawImage(frames[n+1],540,192-172*s,184*s,184*s)}requestAnimationFrame(draw)}requestAnimationFrame(draw)</script>'''
    page=page.replace('DATA',json.dumps([uri(pickup)]+[uri(f) for f in frames])).replace('DURATIONS',json.dumps(rig['durations']))
    page=page.replace('Veld',actor.title()).replace('Selected source revision;','Source revision; selection and')
    page=page.replace('east cargo',direction+' cargo')
    (out/'motion.html').write_text(page,encoding='utf-8')
    print(json.dumps(checks))
    print(out.relative_to(ROOT))
    return frames

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--actor',choices=['veld','branforth'],default='veld')
    parser.add_argument('--direction',choices=['east','west'],default='east')
    args=parser.parse_args();main(args.actor,args.direction)
