from pathlib import Path
import copy,hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent;ACTION=P.parent/'krusher-terminal-action-study-v5';BODY=P.parent/'krusher-moving-equipment-test-v2'
for folder in ['frames/bare','frames/helmet','review']:(P/folder).mkdir(parents=True,exist_ok=True)
base=json.loads((ACTION/'action-manifest.json').read_text());masters={v:BODY/f'frames/{v}/idle-west/000.png' for v in ['bare','helmet']};arrays={v:np.array(Image.open(f).convert('RGBA')) for v,f in masters.items()}
assert np.array_equal(arrays['bare'][62:],arrays['helmet'][62:]),'Bodies do not share exact lower geometry/material'
records=[];source_hashes={};images={v:{} for v in masters}
for variant,master in masters.items():
    manifest=copy.deepcopy(base);manifest['name']=f'Krusher Dom / west terminal action / {variant} pair';manifest['status']='unselected gear pair; native and continuous motion review pending';manifest['canonicalIdleSource']=str(master.relative_to(R));manifest['canonicalIdleSha256']=hashlib.sha256(master.read_bytes()).hexdigest()
    for path in set(path for s in base['states'] for path in s['frameFiles']):
        src=ACTION/path;source_hashes[str(src.relative_to(R))]=hashlib.sha256(src.read_bytes()).hexdigest();a=np.array(Image.open(src).convert('RGBA'));out=a.copy()
        if variant=='helmet':out[:62]=arrays['helmet'][:62]
        name=Path(path).name;output=f'frames/{variant}/{name}'
        if name=='idle.png':shutil.copyfile(master,P/output);im=Image.open(master).convert('RGBA')
        else:im=Image.fromarray(out);im.save(P/output)
        images[variant][name]=im;records.append({'variant':variant,'source':str(src.relative_to(R)),'output':output,'helmetUpperRegionExact':bool(np.array_equal(np.array(im)[:62],arrays[variant][:62])),'bodyMatchesBareActionExact':bool(np.array_equal(np.array(im)[62:],a[62:]))})
    for state in manifest['states']:
        state['frameFiles']=[f'frames/{variant}/{Path(path).name}' for path in state['frameFiles']]
        frames=[images[variant][Path(path).name] for path in state['frameFiles']]
        frames[0].save(P/f'review/{variant}-{state["id"]}.png',save_all=True,append_images=frames[1:],duration=state['frameDurationsMs'],loop=0,disposal=1,blend=0)
    manifest['gearDerivation']='Exact shared body below row62; existing helmet upper region retained byte-for-byte, no scaling/mirroring/warping';manifest['limitations']=['West terminal role action only; other views remain','Native art rendering does not establish station/controller integration or owner acceptance']
    (P/f'{variant}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
report={'records':records,'sourceHashes':source_hashes,'masters':{v:{'path':str(f.relative_to(R)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for v,f in masters.items()},'bodyPixelsBelow62ExactAcrossMasters':True,'method':'Deterministic gear composition from exact compatible bodies; no new generation or anatomy'}
(P/'provenance.json').write_text(json.dumps(report,indent=2)+'\n')
board=Image.new('RGB',(1000,820),'#272b2e');d=ImageDraw.Draw(board);d.text((16,12),'KRUSHER / WEST TERMINAL ACTION / EXISTING BODY AND HELMET REUSE',fill='white')
for row,variant in enumerate(['bare','helmet']):
    for col,name in enumerate(['idle.png','key-004.png','release.png']):
        im=images[variant][name].resize((290,290),Image.Resampling.NEAREST);board.paste(im,(col*330+20,row*350+40),im);d.text((col*330+20,row*350+340),variant+' / '+name,fill='white')
        small=images[variant][name].resize((92,92),Image.Resampling.LANCZOS)
        if row==1:board.paste(small,(col*330+110,710),small)
board.save(P/'review/gear-pair.png');print(json.dumps({'uniqueFrames':len(records),'bodyCompatible':True,'helmetUpperRegionsExact':all(r['helmetUpperRegionExact'] for r in records),'bodyMatchesBareAction':all(r['bodyMatchesBareActionExact'] for r in records)}))
