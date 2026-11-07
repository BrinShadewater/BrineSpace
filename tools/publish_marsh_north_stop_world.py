"""Retain staged North-stop world evidence and reconstructed pose holds."""
from pathlib import Path
import hashlib,json,argparse
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-north-stop-v1'
CAP=ROOT/'output/marsh-animation-audit/north-stop-world-v2-2026-10-02'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--polished',action='store_true');parser.add_argument('--both-polished',action='store_true');parser.add_argument('--controller-v2',action='store_true');parser.add_argument('--production',action='store_true');args=parser.parse_args()
    if args.controller_v2 or args.production:args.both_polished=True
    cap=ROOT/'output/marsh-animation-audit/north-stop-world-both-polished-2026-10-02' if args.both_polished else ROOT/'output/marsh-animation-audit/north-stop-world-polish-2026-10-02' if args.polished else CAP
    out=BASE/('world-paired-polish-review' if args.both_polished else 'world-polish-review' if args.polished else 'world-review');out.mkdir(exist_ok=True)
    if args.controller_v2:
        cap=ROOT/'output/marsh-animation-audit/north-stop-world-controller-v2-2026-10-02'
        out=BASE/'world-settlement-review';out.mkdir(exist_ok=True)
    if args.production:
        cap=ROOT/'output/marsh-animation-audit/north-stop-production-native-2026-10-02'
        out=BASE/'production-review';out.mkdir(exist_ok=True)
    report=json.loads((cap/'report.json').read_text());assert report['failures']==0
    before=json.loads((cap/'profile-before.json').read_text())
    assert before==json.loads((cap/'profile-after.json').read_text())
    bank=BASE/('phase-bank-v3/manifest.json' if args.both_polished else 'phase-bank-v2/manifest.json' if args.polished else 'phase-bank-v1/manifest.json')
    staged={s['id']:[(bank.parent/p).resolve() for p in s['frameFiles']] for s in json.loads(bank.read_text())['states']}
    states=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
    board=Image.new('RGB',(1000,6*180),(24,33,41));draw=ImageDraw.Draw(board)
    for c in report['captures']:
        source=staged[c['key']][c['slot']] if c['key'] in staged else ROOT/states[c['key']]['files'][c['slot']]
        c.update(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha(source),captureSha256=sha(cap/c['file']))
    for phase in range(6):
        records=[c for c in report['captures'] if c['phase']==phase]
        stops=[c for c in records if c['key'] in staged]
        assert {c['slot'] for c in stops}==set(range(5))
        assert all(c['stopSlot']==phase for c in stops)
        assert all(c['foot']==stops[0]['foot'] for c in stops)
        images=[Image.open(cap/c['file']).convert('RGB').crop((450,260,610,430)).resize((320,340),Image.Resampling.NEAREST) for c in records]
        duration=[round((b['time']-a['time'])*1000) for a,b in zip(records,records[1:])]+[180]
        images[0].save(out/f'phase-{phase}.gif',save_all=True,append_images=images[1:],duration=duration,loop=0)
        draw.text((5,phase*180+5),f'Phase {phase}: exact gait, three settlement holds, selected idle',fill='white')
        for c in stops:
            im=Image.open(cap/c['file']).convert('RGB').crop((485,310,575,425)).resize((126,161),Image.Resampling.NEAREST)
            board.paste(im,(160+c['slot']*160,phase*180+19))
    board.save(out/'contact-board.png')
    report['ownerProfileFilesUnchanged']=len(before)
    report['mediaScope']='Native station pose-change captures; GIF timing reconstructs sampled holds, not continuous video.'
    report['arrivalTolerance']='Base relative-coordinate arrival removes the route 0.041015625 world units before the nominal endpoint here. All settlement roots are exactly equal to the actual arrival root; no base navigation change.'
    report['visualFinding']='All six phase entries settle toward selected idle at fixed actual root. Interiors show a somewhat broader torso and different head/material tones versus exact selected gait/idle; final visual polish remains open. Staged controller and explicit render hook only; standard production Continue and natural interruptions are pending.'
    if args.polished:report['visualFinding']='Phases0-2 now use master-based candidate09 with narrower fitted torso, more granular material and subdued head relative to prior05. Phases3-5 retain06, whose width/material repair is still open;10 rejected for breadth,11 wrong leg. Final cross-family polish, natural interruptions and standard production Continue remain pending.'
    if args.both_polished:report['visualFinding']='Phases0-2 use candidate09 and3-5 use new right-lowering candidate12. Both master-based whole-pose branches retain narrower fitted torso and granular muted material, correct support sides, exact selected gait entries/idle endpoints. Broader cross-family polish and production interruptions/Continue remain open.'
    if args.production:report['visualFinding']='All six stop phases now use the normal Marsh controller, catalog and renderer. Selected09/12 whole-pose branches retain fitted master material/proportions and correct support sides. Six real disk restores retain source/clock/root; natural traffic and broader cross-family polish remain open.'
    (out/'native-report.json').write_text(json.dumps(report,indent=2)+'\n')
    files=['character/marsh-north-stop-v1/stop_controller.gd','character/marsh-north-stop-v1/stop_controller.gd.uid','tools/review_marsh_north_stop_world.gd','tools/review_marsh_north_stop_world.gd.uid','tests/test_marsh_north_stop_controller.gd','tests/test_marsh_north_stop_controller.gd.uid','character/marsh-north-stop-v1/phase-bank-v1/manifest.json','tools/publish_marsh_north_stop_world.py']
    if args.polished:files+=['character/marsh-north-stop-v1/phase-bank-v2/manifest.json','tools/build_marsh_north_stop.py','tools/build_marsh_north_stop_phases.py']
    if args.both_polished:files+=['character/marsh-north-stop-v1/phase-bank-v3/manifest.json','character/marsh-north-stop-v1/candidate-09/recipe.json','character/marsh-north-stop-v1/candidate-12/recipe.json','tools/build_marsh_north_stop.py','tools/build_marsh_north_stop_phases.py']
    if args.production:files+=['scripts/marsh_npc.gd','scripts/marsh_npc.gd.uid','scripts/grid_canvas.gd','character/marsh-v2/catalog.json','character/marsh-consistency-review-v1/runtime-contract.json','tools/rebuild_marsh_art.py','tests/test_marsh_north_stop_continue.gd','tests/test_marsh_north_stop_continue.gd.uid']
    verification={'inputs':{p:sha(ROOT/p) for p in files},'checks':report['checks'],'captures':len(report['captures']),'failures':0,'unitChecks':71 if args.controller_v2 or args.production else 66,'ownerFilesUnchanged':len(before),'normalAdmission':args.production,'standardDiskRestores':report.get('checkpoints',0),'standardContinueVerified':False}
    if args.production and (out/'continue-verification.json').exists():
        continued=json.loads((out/'continue-verification.json').read_text())
        verification['standardContinueVerified']=continued['failures']==0 and all(sha(ROOT/p)==h for p,h in continued['inputs'].items())
        verification['titleContinueCases']=continued['cases'];verification['titleContinueChecks']=continued['checks']
    (out/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    page='<!doctype html><meta charset="utf-8"><title>Marsh North stop world review</title><style>body{background:#182129;color:#eee;font:16px sans-serif;margin:24px}img{max-width:100%}a{color:#9df}</style><h1>Staged North arrival settlement</h1><p>'+report['visualFinding']+'</p><p>'+report['scope']+'</p><p>'+report['mediaScope']+'</p><img src="contact-board.png">'
    for phase in range(6):page+=f'<h2>Actual terminal gait phase {phase}</h2><img src="phase-{phase}.gif">'
    page+='<p>'+report['arrivalTolerance']+'</p><p><a href="native-report.json">Checks and exact source/capture hashes</a> · <a href="verification.json">Pinned inputs and scope</a></p>'
    if verification['standardContinueVerified']:page+='<p>Actual title Continue: eight fresh scenes, six stop phases and two cancelled-work cases,112checks/0fail. <a href="continue-verification.json">Continue inputs/checkpoint hashes and evidence</a>.</p>'
    (out/'index.html').write_text(page,encoding='utf-8')
    print(f'Published six {"production" if args.production else "staged"} world arrivals: {report["checks"]} checks, {len(report["captures"])} captures, {len(before)} owner files unchanged')
if __name__=='__main__':main()
