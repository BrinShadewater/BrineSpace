"""Publish normal render and same-scene disk evidence, distinct from title Continue."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'output/marsh-animation-audit/north-step-production-2026-10-02'
DEST=ROOT/'character/marsh-north-step-v1/production-review-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    report=json.loads((RUN/'report.json').read_text());assert report['checks']==141 and report['failures']==0 and report['checkpoints']==6 and len(report['captures'])==18
    frozen=json.loads((RUN/'inputs-before.json').read_text());assert frozen==json.loads((RUN/'inputs-after.json').read_text())
    for p,d in frozen.items():assert sha(ROOT/p)==d,p
    owner=json.loads((RUN/'owner-before.json').read_text());assert owner==json.loads((RUN/'owner-after.json').read_text())
    for n in ['unit.log','native.log']:assert 'ERROR:' not in (RUN/n).read_text(encoding='utf-8-sig')
    assert '1525 checks,0 failures' in (RUN/'unit.log').read_text(encoding='utf-8-sig')
    DEST.mkdir(exist_ok=True);captures=[];groups={};crop=(400,200,550,355)
    board=Image.new('RGB',(1080,1500),'#293b40');draw=ImageDraw.Draw(board)
    for i,r in enumerate(report['captures']):
        native=Image.open(RUN/r['file']).convert('RGB').crop(crop);source=Image.open(RUN/r['sourceFile']).convert('RGBA')
        path=ROOT/'character/marsh-north-step-v1/sequence-v2'/('%03d.png'%r['slot']) if r['key']=='walk-step-north' else ROOT/'character/marsh-v2/frames/bare/idle-north/000.png'
        expected=Image.open(path).convert('RGBA');assert source.size==expected.size and source.tobytes()==expected.tobytes()
        groups.setdefault((r['kind'],r['phase']),[]).append(r)
        x=(i%3)*360;y=(i//3)*250;board.paste(native,(x,y+40));matte=Image.new('RGBA',source.size,'#293b40');matte.alpha_composite(source);board.paste(matte.convert('RGB'),(x+160,y+40))
        draw.text((x+3,y+3),f"{r['kind']} @{r['phase']:.2f} {r['moment']}",fill='white');draw.text((x+3,y+19),f"{r['key']} #{r['slot']} / {r['goal']}",fill='white')
        captures.append({**r,'nativeSha256':sha(RUN/r['file']),'submittedSourceSha256':sha(RUN/r['sourceFile']),'crop':crop})
    assert len(groups)==6
    for rows in groups.values():
        a,b,_=rows
        assert sha(RUN/a['sourceFile'])==sha(RUN/b['sourceFile']) and a['foot']==b['foot'] and a['drawOffset']==b['drawOffset']
    board.save(DEST/'native-board.png')
    for i in [0,3]:board.crop((0,i*250,1080,(i+3)*250)).save(DEST/f'native-board-{i}.png')
    contract=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states'];assert len(contract)==212 and sum(len(s['files']) for s in contract.values())==1100
    assert contract['walk-step-north']['files']==['character/marsh-north-step-v1/sequence-v2/%03d.png'%i for i in range(7)]
    evidence={**report,'controllerChecks':1525,'captures':captures,'targetedInputs':frozen,'targetedInputsUnchanged':True,'ownerNonLogFiles':len(owner),'ownerUnchanged':True,'normalAdmission':True,'titleFreshMainVerified':False,'normalStates':212,'normalSlots':1100,'inputFreezeScope':'32 targeted inputs before/after/publication; not recursive world freeze.','rebuildScope':'Explicit state_override plus refreshed source contract; full raster batch intentionally not run.','logs':{n:sha(RUN/n) for n in ['unit.log','native.log']}}
    if (RUN/'title.log').exists():
        log=(RUN/'title.log').read_text(encoding='utf-8-sig');assert '78 checks,0 failures' in log and 'ERROR:' not in log
        evidence.update({'titleFreshMainVerified':True,'titleChecks':78,'titleCases':6,'titleTestSha256AtPublication':sha(ROOT/'tests/test_marsh_north_step_continue.gd')})
        evidence['logs']['title.log']=sha(RUN/'title.log')
    (DEST/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    html='<!doctype html><meta charset="utf-8"><title>Marsh North step normal integration</title><style>body{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1200px}img{max-width:100%;image-rendering:pixelated}</style><h1>North short step: normal integration</h1><p>1525 controller checks;141 native checks,6 actual disk restores/18 captures,0 failures. Exact normal main, Marsh, grid, catalog and strict validator; no staged actor/render/source injection. Fresh and cancelled curiosity routes saved at entry/transfer/settle. Full actor/player/source/contact preservation, pause and finite completion pass.</p><p>Normal paid/failure flags and real core wake; explicit furnished cold-store fixture, prescribed routes, paused peers/world. Same-scene RunSave restore; fresh title Continue, older saves and natural traffic remain separate.32 targeted hashes and2931 owner files unchanged.212 selected states/1100 source slots; other selected sources unchanged. Full raster rebuild not run.</p><img src="native-board.png"><p>Unscaled native context with exact submitted source on matte. <a href="verification.json">Bound evidence</a> · <a href="../motion-review-v2/index.html">Sampled motion/registration polish</a></p>'
    if evidence['titleFreshMainVerified']:html=html.replace('fresh title Continue, older saves and natural traffic remain separate.','fresh title Continue also passes78 checks across6 checkpoints. Older saves and natural moving traffic remain separate.')
    (DEST/'index.html').write_text(html);print('141 native/1525 controller checks;6 normal disk restores;18 source/native pairs;212 states/1100 slots')
if __name__=='__main__':main()
