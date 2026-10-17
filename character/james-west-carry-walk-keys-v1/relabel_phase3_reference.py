from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1');f=p/'package_local_material_stride.py';s=f.read_text();s=s.replace("s=s.replace('previous phase3','phase3 material anchor')","s=s.replace('previous phase3','phase3 prior provisional reference')");f.write_text(s,encoding='utf-8')
