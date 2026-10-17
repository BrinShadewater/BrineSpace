from pathlib import Path
# Same deterministic whole-body registration/protection as the independently
# authored middle trial. Keep its source and evidence separate and unchanged.
p=Path(__file__).resolve().parent
source=(p/'package_middle.py').read_text(encoding='utf-8')
source=source.replace('middle-','guided-middle-')
exec(compile(source,str(p/'package_guided_middle.py'),'exec'))
