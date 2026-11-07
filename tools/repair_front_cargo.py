"""Front/rear cargo cycle from its pickup endpoint; selection recorded separately."""
from pathlib import Path
import argparse,contextlib,io,json,hashlib,base64
from PIL import Image
from extract_veld_cargo_study import main as pickup_build
from repair_crew_walk import build_axial

ROOT=Path(__file__).resolve().parents[1]

def main(actor='veld',direction='south'):
    with contextlib.redirect_stdout(io.StringIO()):pickup=pickup_build(actor,direction=direction)
    donor=pickup[-1].crop((36,52,220,236))
    rig={'projection':'axial','direction':direction,'travel':36,'durations':[140]*6,
         'bodyBob':[0,-1,0,0,-1,0],'solePath':[172,168,164,160,156,164],
         'legs':{'left':{'box':[52,121,92,184]},'right':{'box':[92,121,132,184]}}}
    residual=donor.copy()
    for leg in rig['legs'].values():residual.paste((0,0,0,0),tuple(leg['box']))
    if residual.crop((0,121,184,184)).getbbox() is not None:
        raise ValueError('Leg masks leave stationary lower-body pixels')
    frames,joints=build_axial(donor,rig)
    out=ROOT/f'character/crew-action-detail-v2/review/{actor}-carry-{direction}-local-01'
    out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(7*184,208),'#293b40')
    sheet.paste(donor,(0,20),donor)
    for i,frame in enumerate(frames):
        frame.save(out/f'{i:03}.png');sheet.paste(frame,((i+1)*184,20),frame)
    donor.save(out/'donor.png');sheet.save(out/'contact.png')
    error=max(abs(p['soleActual']-p['soleTarget']) for row in joints for p in row.values())
    source=ROOT/f'character/crew-action-detail-v2/sources/{actor}-pickup-{direction}-candidate-01.png'
    (out/'recipe.json').write_text(json.dumps({'status':'source_revision_selection_recorded_separately','source':source.relative_to(ROOT).as_posix(),
        'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'rig':rig,'joints':joints,
        'checks':{'projectedSoleErrorPx':error},'limitations':'Image-space registration, not world-space contact proof'},indent=2)+'\n')
    def uri(im):
        stream=io.BytesIO();im.save(stream,format='PNG');return 'data:image/png;base64,'+base64.b64encode(stream.getvalue()).decode()
    page='''<!doctype html><meta charset="utf-8"><title>Front cargo study</title><style>body{background:#293b40;color:#eee;font:16px system-ui}canvas{image-rendering:pixelated}</style>
<h1>Front cargo source revision</h1><p>Selection and native checks are recorded in the action handoff. Pickup endpoint / carry / station scale. Projected limb lengths, with original upper body and grip.</p><button id="play">Pause</button><canvas id="view" width="700" height="240"></canvas>
<script>const frames=DATA.map(src=>{let im=new Image();im.src=src;return im});let t=0,last=performance.now(),playing=true;play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play'};function draw(now){if(playing)t+=now-last;last=now;let n=Math.floor(t/140)%6,c=view.getContext('2d');c.clearRect(0,0,700,240);c.imageSmoothingEnabled=false;if(frames.every(f=>f.complete)){c.drawImage(frames[0],40,20);c.drawImage(frames[n+1],280,20);const s=65.28/148;c.drawImage(frames[n+1],540,192-172*s,184*s,184*s)}requestAnimationFrame(draw)}requestAnimationFrame(draw)</script>'''
    page=page.replace('Front cargo',direction.title()+' cargo')
    (out/'motion.html').write_text(page.replace('DATA',json.dumps([uri(donor)]+[uri(f) for f in frames])),encoding='utf-8')
    print(json.dumps({'actor':actor,'frames':len(frames),'projectedSoleErrorPx':error}))
    return frames

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--actor',choices=['veld','branforth'],default='veld')
    p.add_argument('--direction',choices=['south','north'],default='south')
    args=p.parse_args();main(args.actor,args.direction)
