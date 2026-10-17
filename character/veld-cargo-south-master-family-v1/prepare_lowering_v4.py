from pathlib import Path
import json, shutil
P=Path(__file__).resolve().parent
study=P/'lowering-study-v3'
study.mkdir(exist_ok=True)
for name in ['extract_unload.py','build.py','extraction.json','registration.json','native-review-evidence.json','paired-master-cargo.png','bare-manifest.json','helmet-manifest.json']:
    shutil.copy2(P/name,study/name)
for name in ['frames','ungraded-unload']:
    shutil.copytree(P/name,study/name,dirs_exist_ok=True)
source=Path('C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/exec-04456277-79b9-4259-8335-49ae8f2f4e91.png')
shutil.copy2(source,P/'raw-unload-v4.png')
script=(P/'extract_unload.py').read_text(encoding='utf-8').replace('raw-unload-v3.png','raw-unload-v4.png')
(P/'extract_unload.py').write_text(script,encoding='utf-8')
print('Preserved v3 source package and copied v4 whole lowering-pose edit.')
