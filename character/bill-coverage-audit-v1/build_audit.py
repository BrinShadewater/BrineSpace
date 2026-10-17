"""Resolve current Bill loader order; distinguish presence from matching revision."""
from pathlib import Path
import re,json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
ACTIONS=['sit-down','sit-rise','sit-idle','read-seated','read-seated-enter','read-seated-exit','lie-down','sleep','get-up','bunk-enter','bunk-sleep','bunk-exit','eat','drink','inspect','death-ground','death-water','recover-air']
def main():
    text=(ROOT/'scripts/grid_canvas.gd').read_text(encoding='utf-8')
    section=text.split('func _load_major_bill_animations()',1)[1].split('\nfunc ',1)[0]
    catalog_path=ROOT/'character/major-bill-v3/catalog.json';catalog=json.loads(catalog_path.read_text())
    order=[(gear,catalog_path.parent/name) for gear,names in [('bare',catalog['body']),('helmet',catalog['equipment'])] for name in names]
    for match in re.finditer(r'player\.load_(manifest|equipment_manifest)\((?:"diving-helmet",\s*)?"(res://[^"]+)"',section):
        order.append(('helmet' if match[1]=='equipment_manifest' else 'bare',ROOT/match[2].removeprefix('res://')))
    selected={'bare':{},'helmet':{}};bindings={}
    for gear,path in order:
        data=json.loads(path.read_text());bindings[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
        for s in data['states']:
            files=[ROOT/f.removeprefix('res://') if f.startswith('res://') else (path.parent/f).resolve() for f in s['frameFiles']]
            selected[gear][s['id']]={'manifest':path.relative_to(ROOT).as_posix(),'status':data.get('status',''),'files':[f.relative_to(ROOT).as_posix() for f in files],'timing':s['frameDurationsMs'],'loop':s['loop'],'pivot':data.get('pivot',[46,86]),'standingHeight':data.get('standingHeight',74),'precomposed':data.get('precomposed',False),'mirrored':False}
        for target,source in data.get('mirrorDirections',{}).items():
            for key,row in list(selected[gear].items()):
                if key.endswith('-'+source) and key[:-len(source)]+target not in selected[gear]:
                    selected[gear][key[:-len(source)]+target]={**row,'mirrored':True,'mirrorSource':key}
    rows=[]
    for action in ACTIONS:
        for direction in ['north','east','south','west']:
            key=action+'-'+direction
            for gear in ['bare','helmet']:
                row=selected[gear].get(key)
                rows.append({'action':action,'direction':direction,'gear':gear,'present':row is not None,**(row or {})})
    result={'scope':'current loader source resolution;visual acceptance and runtime journeys separate','loaderSha256':hashlib.sha256((ROOT/'scripts/grid_canvas.gd').read_bytes()).hexdigest(),'catalogSha256':hashlib.sha256(catalog_path.read_bytes()).hexdigest(),'manifestBindings':bindings,'stateCounts':{g:len(s) for g,s in selected.items()},'lifeRows':rows,'selected':selected}
    (P/'source-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    summary={a:sorted({r['manifest'] for r in rows if r['action']==a and r['present']}) for a in ACTIONS}
    print(json.dumps({'stateCounts':result['stateCounts'],'missingLifeRows':sum(not r['present'] for r in rows),'lifeSources':summary},indent=2))
if __name__=='__main__':main()
