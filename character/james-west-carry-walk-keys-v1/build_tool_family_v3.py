from pathlib import Path
p=Path(__file__).resolve().parent
source=(p/'build_eight_keys.py').read_text()
for index in (8,12,20,28,36,48):
    old=f"p/'walk{index:02d}-case-v2.png'" if index in (12,28,36) else f"p/'walk{index:02d}-carry.png'"
    source=source.replace(old,f"p/'walk{index:02d}-meter-occlusion-v3.png'")
source=source.replace('eight-key-','eight-key-tools-v3-')
source=source.replace('Earlier8..36meters still uncorrected.','Six new meter-removal source repairs. Hand/tool occlusion and wrench identity still provisional.')
exec(compile(source,str(p/'build_eight_keys.py'),'exec'))
