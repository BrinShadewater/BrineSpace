from pathlib import Path
P=Path(__file__).resolve().parent;OLD=P.parent/'bill-land-water-material-west-v2'
s=(OLD/'build_review.py').read_text(encoding='utf-8').replace('bill-land-water-material-west-v2','bill-land-water-material-west-v3')
start=s.index('normal=json.loads(');end=s.index("for study in [",start)
s=s[:start]+"normal=json.loads((P/'source-inventory.json').read_text(encoding='utf-8'));candidate={}\n"+s[end:]
s=s.replace("['bill-land-water-west-v4/bare','bill-land-water-west-v4/helmet']", "['bill-land-water-west-v4/bare','bill-land-water-west-v4/helmet','bill-water-exit-west-v1/bare','bill-water-exit-west-v1/helmet']")
s=s.replace("[('enter',60,105)]","[('enter',60,105),('exit',410,460)]")
s=s.replace('West exit remains normal source; checkpoints/Continue and continuous motion/master material acceptance pending.','Independent West exit source now staged; entry and exit takeovers captured. Checkpoints/Continue, actual continuous motion and full master material acceptance pending.')
s=s.replace('90 advancing60Hz entry boundary presentations/180original source-room files;4APNGs verify180decoded capture intervals','190 advancing60Hz entry/exit boundary presentations/380original source-room files;8APNGs verify380decoded capture intervals')
start=s.index("e=json.loads((P/'review.json')");end=s.index('print(json.dumps',start)
s=s[:start]+"e=json.loads((P/'review.json').read_text(encoding='utf-8'))\ne['normalInventoryScope']='Prelaunch frozen current entry/exit and normal walking/swimming banks; every advancing capture identified by exact RGBA plus manifest registration, no historical fallback or inferred pivot.'\n(P/'review.json').write_text(json.dumps(e,indent=2)+'\\n',encoding='utf-8')\n"+s[end:]
(P/'build_review.py').write_text(s,encoding='utf-8')
print('Prepared focused current-inventory entry/exit review publisher.')
