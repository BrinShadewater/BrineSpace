from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];rev=P/'revisions/staged-before-selection-v1';rev.mkdir(parents=True,exist_ok=True)
for rel in ['bare-manifest.json','helmet-manifest.json','source-bindings.json','verification.json','candidate-evidence.json','HANDOFF.md','index.html','build_family.py']:
    f=P/rel;target=rev/rel
    if f.exists() and not target.exists():shutil.copy2(f,target)
active=R/'character/ACTIVE_ASSETS.json';target=rev/'ACTIVE_ASSETS.json'
if not target.exists():shutil.copy2(active,target)
s=(P/'build_family.py').read_text(encoding='utf-8').replace("'status':'staged_candidate'","'status':'selected_runtime'").replace("'normalSelection':False","'normalSelection':True").replace('staged family','selected family')
s=s.replace("offset=[round((center[j]-[128,224][j])*65.28/148,6) for j in range(2)]","offset=[round((center[j]-[128,224][j])*65.28/148+(14.592 if j==1 else 0),6) for j in range(2)]")
s=s.replace('anatomical bare or component helmet center, furniture integration pending','anatomical bare or component helmet center including14.592world draw lift; furniture integration proof distinct')
(P/'build_family.py').write_text(s,encoding='utf-8')
s=(P/'verify_family.py').read_text(encoding='utf-8').replace("'normalSelection':False","'normalSelection':True");(P/'verify_family.py').write_text(s,encoding='utf-8')
data=json.loads(active.read_text());data['actionOverrides']['veld-generic-rest-family']='character/veld-rest-family-v1/bare-manifest.json';data['equipmentOverrides']['veld-generic-rest-family']='character/veld-rest-family-v1/helmet-manifest.json';active.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('Selected paired cardinal generic rest; retained staged metadata revision.')
