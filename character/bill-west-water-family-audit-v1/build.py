from pathlib import Path
import json, hashlib
from PIL import Image, ImageDraw
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
families = [
    ('Entry', 'bill-land-water-west-v15', ['Idle','Ready','Crouch','Push off','Levelling','Near prone','Swimming']),
    ('Swim', 'bill-swim-west-calibrated-v6', ['Extend','Sweep','Pull','Gather','Recover','Reach','Glide']),
    ('Exit', 'bill-water-exit-west-master-v13', ['Swimming','Lower hands','Low elbow','Palm push','Knee tuck','Half kneel','Rise','Standing']),
]
frozen, sequences, frames, diagnostics = {}, {}, {}, []
def freeze(path):
    frozen[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
for gear in ['bare', 'helmet']:
    sequences[gear] = []
    for family, bank, names in families:
        mp = ROOT / bank / gear / 'manifest.json'
        freeze(mp)
        m = json.loads(mp.read_text()); state = m['states'][0]
        assert [m['frameWidth'],m['frameHeight']] == [352,320]
        assert m['pivot'] == [160,224] and m['standingHeight'] == 148
        rows = []
        for i, (rel, hold) in enumerate(zip(state['frameFiles'],state['frameDurationsMs'])):
            path = mp.parent / rel; freeze(path)
            im = Image.open(path).convert('RGBA'); frames[gear,family,i] = im
            rows.append({'url':'../'+path.relative_to(ROOT).as_posix(),'hold':hold,'label':family+' / '+names[i]})
            a = np.array(im)
            mask = (a[:,:,3]>=250)&(a[:,:,1]>=a[:,:,0]*.8)&(a[:,:,2]>=a[:,:,0]*.8)&(a[:,:,:3].mean(2)>30)
            y = a[:,:,:3].mean(2)[mask]
            diagnostics.append({'gear':gear,'family':family,'pose':names[i],'greyPixels':int(mask.sum()),'greyMedian':round(float(np.median(y)),2),'greyP95':round(float(np.percentile(y,95)),2),'scope':'Whole grey diagnostic includes hardware; not textile or grade acceptance.'})
        sequences[gear] += rows * (2 if family == 'Swim' else 1)
for family, bank, names in families:
    board = Image.new('RGB',(352*len(names),696),(23,42,51)); draw=ImageDraw.Draw(board)
    for row, gear in enumerate(['bare','helmet']):
        for i, name in enumerate(names):
            draw.text((352*i+5,348*row+5),gear+' / '+name,fill='white')
            im=frames[gear,family,i]; board.paste(im,(352*i,348*row+28),im)
    board.save(OUT/(family.lower()+'-review.png'))
checks=[]
for gear in ['bare','helmet']:
    for aa,bb in [(('Entry',6),('Swim',0)),(('Swim',0),('Exit',0)),(('Exit',7),('Entry',0))]:
        assert frames[gear,*aa].tobytes()==frames[gear,*bb].tobytes()
        checks.append([gear,list(aa),list(bb)])
assert len(sequences['bare'])==len(sequences['helmet'])==29
assert sum(x['hold'] for x in sequences['bare'])==2920
master_path=ROOT/'bill-water-exit-west-master-v8/sources/master-west-reference.png'
freeze(master_path)
master=Image.open(master_path).convert('RGBA')
# Same documented original-master density; calibration comparison only.
master=master.resize((round(master.width*148/956),round(master.height*148/956)),Image.Resampling.LANCZOS)
master_canvas=Image.new('RGBA',(352,320));master_canvas.alpha_composite(master,(160-master.width//2,224-master.height))
board=Image.new('RGB',(352*6,696),(23,42,51));draw=ImageDraw.Draw(board)
for row,gear in enumerate(['bare','helmet']):
    items=[('Original West / bare authority',master_canvas),('Current idle',frames[gear,'Entry',0]),('Ready',frames[gear,'Entry',1]),('Push off',frames[gear,'Entry',3]),('Half kneel',frames[gear,'Exit',5]),('Rise',frames[gear,'Exit',6])]
    for i,(name,im) in enumerate(items):
        draw.text((352*i+5,348*row+5),name,fill='white');board.paste(im,(352*i,348*row+28),im)
board.save(OUT/'master-review.png')
report={'status':'cross_family_source_audit_unselected','frozenInputs':frozen,'frozenCount':len(frozen),'exactPairedContextJoins':checks,'sourceSequenceSlotsPerGear':29,'totalMs':2920,'brightnessDiagnostics':diagnostics,'normalSelected':False,'nativeAcceptance':False,'scope':'Original source pixels and clocks; two swim cycles then finite exit. No root movement or station overlay simulated.'}
(OUT/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
html='''<!doctype html><meta charset="utf-8"><title>Bill west water family consistency</title><style>body{background:#172a33;color:#e1e5e7;font:17px sans-serif;margin:24px}img.pose{width:352px;height:320px;background:#132630}.pair{display:flex;gap:20px}img.board{max-width:100%}button,select{font:inherit;margin:6px}</style><h1>Bill west — complete water family</h1><p>Current idle → entry → two swim cycles → exit → current idle. Original frames and timings. Grade, body motion and physical contact remain under review.</p><div class="pair"><div>Bare<br><img id="bare" class="pose"></div><div>Helmet<br><img id="helmet" class="pose"></div></div><select id="speed" aria-label="Playback speed"><option value="1">Normal speed</option><option value=".25">Quarter speed</option></select><button id="play">Play sequence</button><button id="prev">Previous pose</button><button id="next">Next pose</button><span id="phase"></span><h2>Entry</h2><img class="board" src="entry-review.png"><h2>Swimming</h2><img class="board" src="swim-review.png"><h2>Exit</h2><img class="board" src="exit-review.png"><script>const S=SEQUENCE;let i=0,timer=null;const $=x=>document.getElementById(x);function show(){for(const g of ['bare','helmet'])$(g).src=S[g][i].url;$('phase').textContent=S.bare[i].label+' / slot '+(i+1)+' of 29'}function stop(){clearTimeout(timer);timer=null;$('play').textContent='Play sequence'}function step(){show();timer=setTimeout(()=>{if(i<28){i++;step()}else stop()},S.bare[i].hold/Number($('speed').value))}$('play').onclick=()=>{if(timer!==null){stop()}else{i=0;$('play').textContent='Pause sequence';step()}};$('prev').onclick=()=>{stop();i=Math.max(0,i-1);show()};$('next').onclick=()=>{stop();i=Math.min(28,i+1);show()};show();</script>'''.replace('SEQUENCE',json.dumps(sequences))
(OUT/'index.html').write_text(html,encoding='utf-8')
print(json.dumps({'frozen':len(frozen),'joins':len(checks),'slots':29,'durationMs':2920}))
