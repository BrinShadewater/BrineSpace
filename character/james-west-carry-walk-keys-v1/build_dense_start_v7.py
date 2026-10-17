from pathlib import Path
p=Path(__file__).resolve().parent
source=(p/'build_dense_start_v6.py').read_text().replace("else f'walk{i:02d}-dense-carry-v6.png'","else 'walk03-contact-v7.png' if i==3 else f'walk{i:02d}-dense-carry-v6.png'")
source=source.replace('dense-start-v6-','dense-start-v7-')
exec(compile(source,str(p/'build_dense_start_v6.py'),'exec'))
