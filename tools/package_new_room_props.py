from pathlib import Path
import json,shutil,hashlib,html
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/new-room-props-2026-09-26'
SOURCE=Path(r'C:/Users/Alex/Desktop/Projects/Gaming/Brine Space Art/BrineSpace Clean Prop Exports/New Room Art - Organized 2026-09-26')
records=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))['records']
for source,target in [
 (SOURCE/'03-animation-studies/aquarium',OUT/'animation-studies/aquarium'),
 (SOURCE/'03-animation-studies/survey-probe',OUT/'animation-studies/four-wall-probe'),
 (SOURCE/'04-ocean-reuse-candidates',OUT/'ocean-reuse')]:
 shutil.copytree(source,target,dirs_exist_ok=True)
cards=[]
for r in records:
 path=Path(r['export']).relative_to(OUT.relative_to(ROOT)).as_posix()
 cards.append('<article data-category="'+r['category']+'"><div class="art"><a href="'+path+'"><img src="'+path+'" style="width:calc('+str(r['display_width'])+'px * var(--zoom))" alt="'+html.escape(r['label'])+'"></a></div><h3>'+html.escape(r['label'])+'</h3><p>'+str(r['native_size'][0])+' × '+str(r['native_size'][1])+' export · '+str(round(r['display_width'],1))+' world units wide</p></article>')
doc='''<!doctype html><html lang="en"><meta charset="utf-8"><title>BrineSpace new room props</title><style>
:root{--zoom:2;--back:#263139}*{box-sizing:border-box}body{font:15px system-ui;background:#152126;color:#e3e9e7;margin:0;padding:32px}h1{font-weight:500}p{color:#aebec2}nav{display:flex;gap:18px;flex-wrap:wrap;position:sticky;top:0;background:#152126;padding:16px 0;z-index:1}select,input{accent-color:#94b9b5;background:#304148;color:#e4e9e7;padding:8px;border:1px solid #627478}a{color:#acd9dc}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:16px}article{border:1px solid #405158;padding:12px}article[hidden]{display:none}.art{height:330px;display:flex;align-items:flex-end;justify-content:center;overflow:auto;background:var(--back);padding:10px}img{image-rendering:pixelated;max-width:none}h3{font-size:15px;font-weight:500}small{color:#aebec2}details{margin:24px 0}details img{width:min(100%,1500px)}.links{display:flex;flex-wrap:wrap;gap:16px}
</style><h1>BrineSpace · New room props</h1><p>154 individual props from 28 room concepts and their additions. Installed in Layout Studio by department. Existing room layouts preserved.</p>
<div class="links"><a href="animation-studies/aquarium/aquarium-preview/index.html">Aquarium animation</a><a href="animation-studies/four-wall-probe/index.html">Four-wall launcher study</a><a href="../survey-probe-v1-2026-09-26/index.html">Latest survey mission</a><a href="README.md">Production notes</a></div>
<details><summary>Native crew, footprint and transparency review — 8 pages</summary>'''+''.join('<a href="review/native-%02d-dark.png"><img loading="lazy" src="review/native-%02d-dark.png" alt="Native review page %d"></a>'%(i,i,i+1) for i in range(8))+'''</details>
<nav><label>Department <select id="department"><option value="">All departments</option>'''+''.join('<option>'+c+'</option>' for c in sorted(set(r['category'] for r in records)))+'''</select></label><label>Background <select id="background"><option value="#263139">Dark</option><option value="#e8e3d8">Light</option><option value="#737b7f">Neutral</option></select></label><label>World-scale zoom <select id="zoom"><option value="1">1×</option><option value="2" selected>2×</option><option value="3">3×</option></select></label><span id="count">154 props</span></nav><main>'''+''.join(cards)+'''</main><script>
document.querySelector('#department').onchange=e=>{let n=0;document.querySelectorAll('article').forEach(a=>{a.hidden=!!e.target.value&&a.dataset.category!==e.target.value;if(!a.hidden)n++});document.querySelector('#count').textContent=n+' props'};
document.querySelector('#background').onchange=e=>document.documentElement.style.setProperty('--back',e.target.value);
document.querySelector('#zoom').onchange=e=>document.documentElement.style.setProperty('--zoom',e.target.value);
</script></html>'''
(OUT/'index.html').write_text(doc,encoding='utf-8')
# Selection/export status is explicit and separate from supplied sheet history.
manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
manifest['scope']='154 static Studio props. Selected concepts authorized for preparation on September 26. Native isolated fixture and agent visual review passed; owner has not yet reviewed these derived exports.'
for r in manifest['records']:
 r['stage']='installed-studio';r['native_review']='agent reviewed with production Bill and .34 world units per export pixel; isolated floor fixture'
manifest['animation_authority']='../survey-probe-v1-2026-09-26/manifest.json is newer than the retained four-wall study. Animations remain standalone.'
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
protected=json.loads((OUT/'protected-before.json').read_text(encoding='utf-8'))
result=[]
for item in protected[1:]:
 actual=hashlib.sha256(Path(item['path']).read_bytes()).hexdigest();assert actual==item['sha256'],item['path'];result.append(item['path'])
old=json.loads((OUT/'before-install/0-props.json').read_text(encoding='utf-8'));installed=json.loads((ROOT/'rooms/station-props-v2/props.json').read_text(encoding='utf-8'))
assert installed[:len(old)]==old
for r in records:
 f=ROOT/r['export'];assert hashlib.sha256(f.read_bytes()).hexdigest()==r['export_sha256']
(OUT/'review/integrity.json').write_text(json.dumps({'exports_verified':len(records),'existing_catalog_entries_unchanged':len(old),'protected_files_unchanged':result},indent=2),encoding='utf-8')
# Deliver a portable reviewed export bundle beside the organized source collection.
bundle=SOURCE/'06-production-exports'
for folder in ['game-size','masters','review','ocean-reuse']:
 shutil.copytree(OUT/folder,bundle/folder,dirs_exist_ok=True)
for name in ['catalog.json','manifest.json','cleanup-provenance.json']:
 shutil.copy2(OUT/name,bundle/name)
(SOURCE/'PRODUCTION-EXPORTS.md').write_text('Production exports: 06-production-exports. 154 props registered in the project Layout Studio.\n\nLive review gallery: http://127.0.0.1:8780/new-room-props-2026-09-26/\n\nThe original sheets and historical approvals remain intact. See the project production README for scope and remaining gameplay work.\n',encoding='utf-8')
print(json.dumps({'exports':len(records),'original_catalog_preserved':len(old),'protected_files':len(result)}))

