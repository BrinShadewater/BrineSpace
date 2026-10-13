"""Publish actual staged stop interruption source/root diagnostic evidence."""
from pathlib import Path
import hashlib,json,argparse
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-north-stop-v1'
CAP=ROOT/'output/marsh-animation-audit/north-stop-interruptions-v2-2026-10-02'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--settled',action='store_true');parser.add_argument('--production',action='store_true');args=parser.parse_args()
    cap=ROOT/'output/marsh-animation-audit/north-stop-interruptions-v4-2026-10-02' if args.settled else CAP
    report=json.loads((cap/'report.json').read_text());assert report['failures']==0
    before=json.loads((cap/'profile-before.json').read_text());assert before==json.loads((cap/'profile-after.json').read_text())
    out=BASE/('interruption-settlement-review' if args.settled else 'interruption-review');out.mkdir(exist_ok=True)
    if args.production:
        cap=ROOT/'output/marsh-animation-audit/north-stop-production-interruptions-2026-10-02'
        report=json.loads((cap/'report.json').read_text());assert report['failures']==0
        before=json.loads((cap/'profile-before.json').read_text());assert before==json.loads((cap/'profile-after.json').read_text())
        out=BASE/'production-interruption-review';out.mkdir(exist_ok=True)
    bank=BASE/'phase-bank-v3/manifest.json'
    sources={s['id']:[(bank.parent/p).resolve() for p in s['frameFiles']] for s in json.loads(bank.read_text())['states']}
    normal=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
    kinds=['pause','not-running','power','suspension','injury','recharge','fire','water']
    board=Image.new('RGB',(6*260,8*190),(24,33,41));draw=ImageDraw.Draw(board)
    for c in report['captures']:
        source=sources[c['key']][c['slot']] if c['key'] in sources else ROOT/normal[c['key']]['files'][c['slot']]
        c.update(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha(source),captureSha256=sha(cap/c['file']))
        x=c['phase']*260+(0 if c['moment']=='before' else 130);y=kinds.index(c['case'])*190
        im=Image.open(cap/c['file']).convert('RGB').crop((485,305,575,430)).resize((117,163),Image.Resampling.NEAREST)
        board.paste(im,(x+5,y+25));draw.text((x+3,y+4),f"{c['case']} p{c['phase']} {c['moment']}",fill='white')
    board.save(out/'before-after-board.png')
    report['ownerFilesUnchanged']=len(before)
    report['visualScope']='Before-after native source/body/root samples. Diagnostic safety/host checks do not certify every visual join or full flooding renderer/world dynamics.'
    if args.settled:report['visualFinding']='Service loss retains North physical settlement with the work goal cleared; no immediate side-facing route choice. Pause/stopped host retain pose. Injury/fire/recharge supersede the stop. Flooding preserves deliberate underwater floor movement and finite settlement. Broader emergency art joins and natural traffic remain open.'
    (out/'native-report.json').write_text(json.dumps(report,indent=2)+'\n')
    files=['tools/review_marsh_north_stop_world.gd','tools/review_marsh_north_stop_world.gd.uid','character/marsh-north-stop-v1/stop_controller.gd','character/marsh-north-stop-v1/phase-bank-v3/manifest.json','scripts/room_flooding.gd','tools/publish_marsh_north_stop_interruptions.py']
    if args.production:files+=['scripts/marsh_npc.gd','scripts/marsh_npc.gd.uid','scripts/grid_canvas.gd','character/marsh-v2/catalog.json']
    (out/'verification.json').write_text(json.dumps({'inputs':{p:sha(ROOT/p) for p in files},'checks':report['checks'],'cases':48,'captures':96,'failures':0,'normalAdmission':args.production,'standardContinueVerified':False},indent=2)+'\n')
    page='<!doctype html><meta charset="utf-8"><title>Marsh staged North stop interruptions</title><style>body{background:#182129;color:#eee;font:16px sans-serif;margin:24px}img{max-width:100%}a{color:#9df}</style><h1>North stop interruption diagnostics</h1><p>'+report['scope']+'</p><p>'+report['visualScope']+'</p><p>Marsh deliberately walks underwater on the floor: real flooding coordinator keeps dry movement, applies0.55 speed and battery drain. Flooding retains this finite floor stop. Power/suspension cancel deferred service; injury/recharge/fire supersede the stop; pause/stopped-host freeze.</p><img src="before-after-board.png"><p><a href="native-report.json">Exact source/capture hashes and actor fields</a> · <a href="verification.json">Pinned inputs</a></p>'
    if args.settled:page+='<p>'+report['visualFinding']+'</p>'
    (out/'index.html').write_text(page,encoding='utf-8')
    print(f'Published48 interruption cases/{report["checks"]}checks/96captures;{len(before)}owner files unchanged')
if __name__=='__main__':main()
