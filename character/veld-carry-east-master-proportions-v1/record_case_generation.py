from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
items=[('21','17177c83-736e-4483-b788-3295b52d34d9',['raw-far-swing-v20.png','unified-identity-pose-guide.png']),('22','27f27d89-e019-4714-80d3-f2880efe4867',['raw-case-surface-v21.png'])]
for v,execution,refs in items:
 source=P/('raw-case-surface-v'+v+'.png')
 (P/('references-case-surface-v'+v+'.json')).write_text(json.dumps([{'path':r,'sha256':hashlib.sha256((P/r).read_bytes()).hexdigest()} for r in refs],indent=2)+'\n',encoding='utf-8')
 (P/('execution-case-surface-v'+v+'.json')).write_text(json.dumps({'tool':'builtin image_gen','execution':execution,'workspaceSource':source.name,'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'prompt':'prompt-case-surface-v'+v+'.txt','references':'references-case-surface-v'+v+'.json','status':'rejected_full_pose_material_edit','review':'Case diagonal pattern persists; complete generated output changes pixels outside equipment context and alpha. Preserve current registered body. Next localized equipment-source edit, protected surface extraction only.','scope':'Unselected source diagnostic; no native/runtime mutation.'},indent=2)+'\n',encoding='utf-8')
print('Recorded two rejected candidates and exact reference hashes.')
