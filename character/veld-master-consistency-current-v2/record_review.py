from pathlib import Path
import json,hashlib,html
P=Path(__file__).resolve().parent;R=P.parents[1]
names=['master-review-evidence.json','cross-family-review-evidence.json','furniture-review-evidence.json','action-sequence-evidence.json']
sources={};boards=[];presentations=0
for name in names:
 path=P/name;d=json.loads(path.read_bytes());presentations+=len(d['rows'])
 for row in d['rows']:
  source=row['source'];digest=hashlib.sha256((R/source).read_bytes()).hexdigest()
  expected=row.get('SHA256',d.get('bindings',{}).get(source));assert digest==expected,source;sources[source]=digest
 for source,expected in d.get('bindings',{}).items():
  digest=hashlib.sha256((R/source).read_bytes()).hexdigest();assert digest==expected,source;sources[source]=digest
 d['visualReview']='All listed boards inspected October 3, 2026; scoped findings in VERDICT.md; full acceptance open.'
 path.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
 boards+=d.get('boards',[])
boards+=['bare-selected-furniture-review.png','helmet-selected-furniture-review.png']
assert len(set(boards))==13
verification=dict(presentations=presentations,distinctBoundImages=len(sources),bindingFailures=0,boardsViewed=13,sourceBindings=sources,scope='Static source review only; no native motion/contact/production adoption.')
(P/'review-validation.json').write_text(json.dumps(verification,indent=2)+'\n')
page='<!doctype html><meta charset="utf-8"><title>Veld master consistency review</title><style>body{background:#202a30;color:#eee;font:16px system-ui;margin:24px}img{display:block;max-width:100%;margin:12px 0 32px}a{color:#aad8ed}section{margin-top:36px}</style><h1>Veld master consistency review</h1><p>Current selected artwork compared at unchanged native scale and colour. Review only; full animation acceptance remains open.</p><p><a href="VERDICT.md">Findings and repair order</a></p>'
for b in boards:page+=f'<section><h2>{html.escape(b.replace("-"," ").removesuffix(".png"))}</h2><a href="{b}">Open full size</a><img src="{b}"></section>'
(P/'index.html').write_text(page,encoding='utf-8')
title='## Veld current selected full-library master comparison — October 3, 2026'
note=title+'\n\nFresh actual-loader inventory in character/veld-master-consistency-current-v2:198bare/\n192helmet states,118manifests,4804unique sources,0missing. Thirteen unchanged-colour/\nnative-scale boards viewed:112dry/master,80dry/water,48furniture and36complete bare\nWest/North/South interact/repair source presentations. Hash-bound source review;\nstatic samples do not establish native motion/contact or full acceptance.\n\nConfirmed priority: interact poses1–4 in those three directions switch to softer/\ncooler art between detailed selected standing endpoints; all6repair poses use the\nsofter family. This is whole-source identity/detail drift, not merely RGB grading.\nWest/South cargo and North rear construction differ from idle/master. Side furniture\nfinish/helmets and North reading differ; verify dormant dispatch before admission.\nWater samples internally more coherent but full perspective/master/motion review\nremains. Original North magenta edge contamination is not a target global grade;\nprepared cleanup is authored, not pixel-identical original. Kneeling/prone bounds\nmust not be normalized to standing height. Bare masters do not prove helmet shape.\n\nNext whole-source West interact interior repair against original directional master,\nthen North/South actions, cargo, furniture, water/death and ordinary controller/\nsave/Continue integration. Keep East motion studies and current normal selections.\nNo art/controller/normal selection/owner save changes or new paid generation.\nFull objective active/incomplete; source coverage is not acceptance.\nHandoff and scoped priorities:character/veld-master-consistency-current-v2/HANDOFF.md\nand VERDICT.md.\n\n'
# Reuse the concurrency-guarded streaming prepend implementation already maintained.
code=(R/'character/veld-carry-east-original-master-v1/record_native_milestone.py').read_text(encoding='utf-8')
exec('from pathlib import Path\nimport shutil,uuid,time\n'+code[code.index('paths=['):],dict(P=P,R=R,title=title,note=note))
print(f'{presentations} presentations; {len(sources)} source bindings verified; 13 boards reviewed')
