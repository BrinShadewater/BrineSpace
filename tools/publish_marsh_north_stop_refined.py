"""Publish refined sources and six native phase entries separately from old trials."""
from pathlib import Path
import json,hashlib,html
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-north-stop-v1'
CAP=ROOT/'output/marsh-animation-audit/north-stop-phases-native-2026-10-02'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    output=BASE/'refined-review';output.mkdir(parents=True,exist_ok=True)
    report=json.loads((CAP/'report.json').read_text());assert report['failures']==0
    before=json.loads((CAP/'profile-before.json').read_text());assert before==json.loads((CAP/'profile-after.json').read_text())
    manifests=json.loads((BASE/'phase-bank-v1/manifest.json').read_text())['states']
    sources={s['id']:[(BASE/'phase-bank-v1'/p).resolve() for p in s['frameFiles']] for s in manifests}
    selected=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
    for c in report['captures']:
        p=sources[c['key']][c['slot']] if c['key'] in sources else ROOT/selected[c['key']]['files'][c['slot']]
        c['source']=p.relative_to(ROOT).as_posix();c['sourceSha256']=sha(p);c['captureSha256']=sha(CAP/c['file'])
    for phase in range(6):
        key=f'walk-stop-p{phase}-north';rows=[c for c in report['captures'] if c['branch']==key]
        assert rows[0]['slot']==phase and rows[0]['key']=='walk-north'
        images=[Image.open(CAP/c['file']).convert('RGB') for c in rows]
        durations=[round((b['time']-a['time'])*1000) for a,b in zip(rows,rows[1:])]+[150]
        images[0].save(output/f'phase-{phase}.gif',save_all=True,append_images=images[1:],duration=durations,loop=0)
    report['ownerProfileFilesUnchanged']=len(before)
    report['scope']='Actual selected loader with six explicitly staged stop phase manifests;20ms source clock, exact outgoing gait slot checked inside hold, five400ms source slots each,148/65.28display. No actor/world root/arrival/interruptions/production Continue or normal admission.'
    report['visualFinding']='Refined05/06 reduce the sharp added knee lift. Both distinct support-side identities retained; near-neutral phases2/5 omit lifted-leg interiors and use settlement holds. Master-referenced material/density retained; natural stopping root/contact and final owner motion acceptance remain unproven.'
    report['mediaScope']='Native source/pivot pose-change samples reconstructed with recorded holds; not continuous native video.'
    (output/'native-report.json').write_text(json.dumps(report,indent=2)+'\n')
    provenance={}
    for version in ['05','06']:
        recipe=json.loads((BASE/f'candidate-{version}/recipe.json').read_text());provenance[version]=recipe
    (output/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    page='<!doctype html><meta charset="utf-8"><title>Marsh refined North stop</title><style>body{background:#17212a;color:#eee;font:16px sans-serif;margin:24px}img{max-width:100%}a{color:#8bd}</style><h1>Marsh North stop — refined unselected phases</h1><p>'+html.escape(report['visualFinding'])+'</p><p>'+html.escape(report['scope'])+'</p><img src="../phase-bank-v1/comparison.png">'
    for phase in range(6):page+=f'<h2>Outgoing gait{phase}</h2><img src="phase-{phase}.gif">'
    page+='<p><a href="native-report.json">Native checks/source/capture hashes</a> · <a href="provenance.json">Exact new sources/prompts/references</a> · <a href="../index.html">Earlier retained trials</a></p>'
    (output/'index.html').write_text(page,encoding='utf-8')
    print(f"Published six checked gait-to-stop phases,{len(report['captures'])}native samples,{report['checks']}checks;normal admission remains off")
if __name__=='__main__':main()
