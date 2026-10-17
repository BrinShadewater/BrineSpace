from pathlib import Path
p=Path(__file__).resolve().parent
source=(p/'inventory_full_set_v18.py').read_text()
source=source.replace("out=r/'character/james-full-set-review-2026-10-02';out.mkdir(exist_ok=True)",
    "out=r/'character/james-full-set-review-2026-10-02/current-selection-v27';out.mkdir(exist_ok=True)")
exec(compile(source,str(p/'inventory_full_set_v18.py'),'exec'))
