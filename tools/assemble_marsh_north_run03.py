"""Replace only whole passing slot4; preserve five run02 source files."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/assemble_marsh_north_run02.py').read_text().replace('passing-03-unselected/right-passing.png','passing-04-unselected/right-passing.png')
needle="exec(compile(source,"
source=source.replace(needle,"source = source.replace('candidate-02','candidate-03').replace('material-02','material-03').replace('Unselected02','Unselected03')\n"+needle)
exec(compile(source,str(ROOT/'tools/assemble_marsh_north_run03.py'),'exec'),{'__file__':str(ROOT/'tools/assemble_marsh_north_run03.py'),'__name__':'__main__'})
