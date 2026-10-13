"""Verify frozen South geometry and publish coherent material source comparisons."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-walk-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    baseline=json.loads((BASE/'baseline.json').read_text());recipe=json.loads((BASE/'candidate-02/recipe.json').read_text());rows=[]
    board=Image.new('RGB',(1104,300),'#293b40');draw=ImageDraw.Draw(board)
    for r in baseline['states']:
        slot=r['slot'];path=ROOT/r['path'];assert sha(path)==r['sha256']
        old=Image.open(path).convert('RGBA');file=BASE/'candidate-02'/('%03d.png'%slot);new=Image.open(file).convert('RGBA')
        assert old.size==new.size==(184,184) and old.getchannel('A').tobytes()==new.getchannel('A').tobytes()
        # Detail board is a nearest-neighbour presentation of actual final pixels.
        boot=new.crop((62,113,126,180)).resize((128,134),Image.Resampling.NEAREST)
        torso=new.crop((62,23,126,113)).resize((128,180),Image.Resampling.NEAREST)
        x=slot*184;board.paste(torso,(x,18),torso);board.paste(boot,(x+36,166),boot);draw.text((x+2,2),f'gait{slot}',fill='white')
        rows.append({'slot':slot,'sha256':sha(file),'originalSha256':r['sha256'],'alphaExact':True,'size':[184,184],'materialCoverage':recipe['frames'][slot]['mappingCoverage']})
    start=BASE/'candidate-02/south-start'
    for i in range(4):assert (start/('%03d.png'%i)).read_bytes()==(ROOT/'character/marsh-south-start-v1/candidate-04'/('%03d.png'%i)).read_bytes()
    assert (start/'004.png').read_bytes()==(BASE/'candidate-02/004.png').read_bytes()
    manifest=json.loads((BASE/'candidate-02/manifest.json').read_text());assert manifest['frameWidth']==184 and manifest['frameHeight']==184 and manifest['pivot']==[92,172] and manifest['standingHeight']==148
    assert manifest['states'][0]['frameDurationsMs']==[150.0]*6 and manifest['states'][0]['loop']
    (BASE/'candidate-02/detail-board.png').parent.mkdir(exist_ok=True);board.save(BASE/'candidate-02/detail-board.png')
    report={'status':'unselected source material candidate; native motion review separate','frames':rows,'alphaPixelComparisons':6*184*184,'allOriginalGeometryExact':True,'startFirstFourByteIdentical':True,'startEndpointByteIdenticalToGait4':True,'timings':[150]*6,'pivot':[92,172],'standingHeight':148,'gain':recipe['sharedIvoryGain'],'rawSourceSha256':sha(BASE/'sources/south-walk-02.raw.png'),'normalSixFramesUnchanged':True,'limits':'Exact geometry and static detail checks do not establish master/style/native/full-cycle acceptance. Original rig motion retained, not newly authored anatomical motion.'}
    (BASE/'candidate-02/verification.json').write_text(json.dumps(report,indent=2)+'\n')
    (BASE/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Marsh South gait material repair</title><style>body{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1500px}img{max-width:100%;image-rendering:pixelated}</style><h1>South gait master/material repair: staged</h1><p>Six original alpha silhouettes retained exactly,150ms holds/p92,172/H148. Original pose geometry and existing rig motion remain. Standard palette, one shared ivory gain1.0. Matched start retains first four candidate04 poses and uses byte-identical revised gait4 endpoint. Source edit via built-in imagegen; raw/prompt/reference hashes retained.</p><p>Candidate01 rejected: internal calf/boot bands and retained original fragments despite exact alpha. Larger3x2input yields97.1–98.6%full-figure colour mapping; original pixels fill remaining mapped holes. Static candidate02 reads closer to master/start in face/panel detail, with improved shin alignment. Native cycle and joins require separate review; no normal selection or complete consistency claim.</p><img src="candidate-02/comparison.png"><h2>Actual final detail crops,2xnearest presentation</h2><img src="candidate-02/detail-board.png"><h2>Original South master</h2><img style="width:384px" src="../marsh-motion-polish-v1/sources/south-standing-identity-01.png"><h2>Edited larger grid, raw alpha retained</h2><img src="sources/south-walk-02.raw.png"><p><a href="sources/south-walk-02.prompt.txt">Exact prompt</a> · <a href="sources/south-walk-02.request.json">Ordered refs/provenance</a> · <a href="candidate-02/recipe.json">Recipe</a> · <a href="candidate-02/verification.json">Geometry verification</a> · <a href="motion-review-v1/index.html">Separate native motion evidence</a></p>')
    print('Six exact alpha comparisons:',6*184*184,'pixels; original six unchanged; start4 endpoint and first4 verified')
if __name__=='__main__':main()
