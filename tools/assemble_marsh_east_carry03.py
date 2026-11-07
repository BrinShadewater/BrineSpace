"""Replace complete far-contact only; three source poses stay byte identical."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/assemble_marsh_east_carry02.py').read_text().replace("O=B/'candidate-02'","O=B/'candidate-03'").replace('contact-04-unselected','contact-07-unselected').replace('marsh-east-carry-material-02-unselected','marsh-east-carry-material-03-unselected')
exec(compile(s,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
