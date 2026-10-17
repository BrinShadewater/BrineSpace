from pathlib import Path
p=Path(__file__).resolve().parent
source=(p/'build_six_keys.py').read_text()
source=source.replace("r/'character/james-west-carry-depth-v1/walk12-carry.png'","p/'walk12-case-v2.png'").replace("p/'walk28-tool-fix.png'","p/'walk28-case-v2.png'").replace("p/'walk36-tool-fix.png'","p/'walk36-case-v2.png'")
for suffix in ['full.png','upper.png','station.png','review.json']:
    source=source.replace('six-key-'+suffix,'six-key-case-v2-'+suffix)
exec(compile(source,str(p/'build_six_keys.py'),'exec'))
