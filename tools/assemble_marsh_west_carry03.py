"""Assemble complete own West near/far contact/passing figures unchanged."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/assemble_marsh_east_carry02.py').read_text().replace('east','west').replace('East','West').replace("O=B/'candidate-02'","O=B/'candidate-03'").replace("B/'near-06-unselected/near-passing.png'","B/'near-08-unselected/near-passing.png'").replace('contact-04-unselected','contact-03-unselected').replace('candidate-01','candidate-02').replace('marsh-west-carry-material-02-unselected','marsh-west-carry-material-03-unselected')
exec(compile(s,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})

