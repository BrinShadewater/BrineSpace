from pathlib import Path
p=Path(__file__).resolve().parent
source=(p/'build_eight_keys.py').read_text()
start=source.index('sources=[')
end=source.index('\n',start)
source=source[:start]+"sources=[p/f'walk{index:02d}-belt-anatomy-v4.png' for index in indices]"+source[end:]
source=source.replace('eight-key-','eight-key-belt-v4-')
source=source.replace('Earlier8..36meters still uncorrected.','False near-side silver hardware removal; original-location tool occlusion and material continuity remain provisional.')
exec(compile(source,str(p/'build_eight_keys.py'),'exec'))
