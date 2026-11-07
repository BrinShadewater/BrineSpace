"""Use same whole-guide packager with explicit own rear-view identity."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/prepare_marsh_west_run_guides.py').read_text().replace('west','north').replace('West','North')
source=source.replace('Own original North master, visible near temple BARE; implant on far right temple. Never mirror East or add visible temple hardware.','Own original North rear master: back plate, harness and blond hair whorl authority. Raised charcoal soles legitimate; boot uppers warm ivory. Preserve rear view, no invented front face.')
exec(compile(source,str(ROOT/'tools/prepare_marsh_north_run_guides.py'),'exec'),{'__file__':str(ROOT/'tools/prepare_marsh_north_run_guides.py'),'__name__':'__main__'})
