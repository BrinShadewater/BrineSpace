"""Build a local gallery of standardized material/scale records, not the whole art catalog."""
import hashlib
import html
import json
import os
from pathlib import Path
from urllib.parse import quote

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'output/material-review-gallery.html'


def discover_records(root):
    """Include single and multi-asset standardized records without guessing legacy schemas."""
    paths=set((root/'assets').glob('*/material-scale-review.json'))
    paths.update((root/'assets').glob('*/*-review.json'))
    records=[]
    exports={}
    for path in sorted(paths):
        data=json.loads(path.read_text(encoding='utf-8'))
        # A filename is not a schema. Legacy manifests need a deliberate adapter.
        if not all(key in data for key in ('asset_id','export_path','export_sha256','review')):
            continue
        if not isinstance(data['review'],dict):
            continue
        export=(root/data['export_path']).resolve()
        export.relative_to(root.resolve())
        if export in exports:
            raise ValueError(f'Duplicate export review: {path} and {exports[export]}')
        exports[export]=path
        records.append((path,data))
    return records


def review_findings(reviews):
    findings=[]
    for gate in ('materials','native_scale','alpha'):
        review=reviews.get(gate,{})
        findings.append(gate.replace('_',' ')+': '+str(review.get('verdict') or 'unreviewed'))
        findings.extend(str(item) for item in review.get('findings',[]))
    return findings


def contextual_reviews(reviews):
    """Preserve separate study scopes; a later pass must not erase a rejected host."""
    return [(gate, value) for gate, value in reviews.items()
            if gate not in ('materials', 'native_scale', 'alpha', 'integration')
            and isinstance(value, dict)]


def main():
    records=discover_records(ROOT)
    cards=[]
    checks=[]
    for path,data in records:
        label=data.get('asset_id') or path.parent.name
        export=ROOT/data['export_path']
        export.resolve().relative_to(ROOT)
        if not export.is_file():
            raise ValueError(f'Missing export for {label}: {export}')
        actual=hashlib.sha256(export.read_bytes()).hexdigest()
        current=actual==data.get('export_sha256')
        checks.append({'asset_id':label,'record':path.relative_to(ROOT).as_posix(),'export_hash_matches':current})
        esc=lambda value:html.escape(str(value),quote=True)
        link=lambda p:quote(os.path.relpath(p,OUTPUT.parent).replace('\\','/'),safe='/')
        width=data.get('proposed_display_width_world')
        height=data.get('proposed_display_height_world')
        scale=f'{width:.1f} units wide' if isinstance(width,(float,int)) else 'Scale unrecorded'
        if isinstance(height,(float,int)):
            scale+=f' × {height:.1f} high'
        reviews=data.get('review',{})
        findings=review_findings(reviews)
        contexts=contextual_reviews(reviews)
        context_html=[]
        for gate, study in contexts:
            title=gate.replace('_',' ')
            verdict=str(study.get('verdict') or 'unreviewed')
            links=[]
            for key in ('evidence','report'):
                if not study.get(key):
                    continue
                study_path=(ROOT/study[key]).resolve()
                study_path.relative_to(ROOT)
                if not study_path.is_file():
                    raise ValueError(f'Missing {gate} {key} for {label}')
                expected=data.get('evidence_hashes',{}).get(study[key])
                stale=expected is not None and hashlib.sha256(study_path.read_bytes()).hexdigest()!=expected
                links.append(f'<a href="{link(study_path)}">{esc(key)}</a>'+(' · STALE evidence' if stale else ''))
            context_html.append(f'<section class="context"><p><strong>{esc(title)}: {esc(verdict)}</strong></p>'
                                +'<ul>'+''.join('<li>'+esc(item)+'</li>' for item in study.get('findings',[]))+'</ul>'
                                +('<p>'+esc(study['scope'])+'</p>' if study.get('scope') else '')
                                +'<nav>'+''.join(links)+'</nav></section>')
        integration=reviews.get('integration',{})
        stage=integration.get('stage','unrecorded') if isinstance(integration,dict) else str(integration or 'unrecorded')
        owner='Owner review pending' if data.get('owner_acceptance') is None else 'Owner status: '+str(data['owner_acceptance'])
        evidence=reviews.get('native_scale',{}).get('evidence')
        preview=''
        if evidence:
            evidence_path=(ROOT/evidence).resolve()
            evidence_path.relative_to(ROOT)
            if not evidence_path.is_file():
                raise ValueError(f'Missing native evidence for {label}')
            preview=f'<a href="{link(evidence_path)}">Native-scale board</a>'
        status='Export hash matches record' if current else 'STALE: export hash differs from review'
        cards.append(f'''<article class="card" data-search="{esc(label+' '+str(data.get('department','')))}">
<a class="art" href="{link(export)}"><img loading="lazy" src="{link(export)}" alt="{esc(label)}"></a>
<h2>{esc(label)}</h2><p class="department">{esc(data.get('department','Unspecified'))}</p>
<p>{esc(scale)} · {esc(data.get('camera_and_facing','Facing unrecorded'))}</p>
<p class="status {'stale' if not current else ''}">{esc(status)}</p>
<p>{esc(owner)} · {esc(stage)}</p><details><summary>Review findings</summary>
<ul>{''.join('<li>'+esc(f)+'</li>' for f in findings)}</ul>
<p>{esc(data.get('runtime_behavior') or 'Runtime behavior unrecorded')}</p></details>
{''.join(context_html)}
<nav><a href="{link(export)}">PNG</a>{preview}<a href="{link(path)}">Record</a></nav></article>''')
    document='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>BrineSpace · Asset review</title><style>
*{box-sizing:border-box}body{margin:0;background:#142126;color:#d5dcd9;font:15px/1.5 system-ui,sans-serif}main{max-width:1440px;margin:auto;padding:32px}h1{font-size:30px;margin:0}header p{max-width:850px;color:#aebcba}input{width:min(100%,600px);padding:12px;background:#203238;color:#fff;border:1px solid #627670;border-radius:6px;font:inherit;margin:12px 0 28px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(285px,1fr));gap:18px}.card{background:#1e3035;border:1px solid #41565a;border-radius:8px;padding:16px;min-width:0}.card[hidden]{display:none}.art{height:205px;display:flex;align-items:center;justify-content:center;background:#53615f;border-radius:4px;padding:12px}.art img{max-width:100%;max-height:100%;object-fit:contain;image-rendering:pixelated}h2{font-size:18px;margin:16px 0 4px;overflow-wrap:anywhere}.department{color:#bcb296;margin:0}.card p{font-size:13px}.status{color:#acc4b6}.stale{color:#ffbd91}a{color:#afd8d1}nav{display:flex;gap:14px;flex-wrap:wrap;margin-top:15px}summary{cursor:pointer}details{font-size:13px}#count{color:#bac7c4;margin-bottom:15px}
</style><main><header><h1>BrineSpace asset review</h1><p>Standardized material/scale records only; this is not the complete room-art inventory. Thumbnails fit their cards and are not gameplay scale. Open each native-scale board to judge size. A matching hash does not establish visual or owner acceptance.</p></header>
<label for="filter">Find an asset or department</label><br><input id="filter" type="search" placeholder="Try galley, engineering, or laboratory"><div id="count"></div><section class="grid">'''+''.join(cards)+'''</section></main><script>
const cards=[...document.querySelectorAll('.card')];const input=document.getElementById('filter');function filter(){const q=input.value.trim().toLowerCase();let n=0;for(const card of cards){card.hidden=!card.dataset.search.toLowerCase().includes(q);if(!card.hidden)n++}document.getElementById('count').textContent=n+' of '+cards.length+' recorded candidates'}input.addEventListener('input',filter);filter();</script></html>'''
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(document,encoding='utf-8')
    (OUTPUT.with_suffix('.audit.json')).write_text(json.dumps(checks,indent=2)+'\n')
    print(f'{len(cards)} records; {sum(not item["export_hash_matches"] for item in checks)} stale hashes; {OUTPUT.relative_to(ROOT)}')


if __name__=='__main__':
    main()
