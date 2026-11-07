"""Retain and pack complete near-support figures against current far cargo."""
from pathlib import Path
p=Path(__file__).with_name('build_marsh_east_carry_half02.py')
s=p.read_text(encoding='utf-8')
s=s.replace('exec-2557b186-1649-4014-be99-f397cd83811a','exec-fdd5fddf-e75f-4039-b86d-114cf92dd814').replace('half-02','near-06')
s=s.replace('far-near-06-rejected','near-06-unselected').replace('wrong-near-contact.png','near-contact.png').replace('wrong-near-passing.png','near-passing.png')
s=s.replace('Retained rejected: contact/passing both near support; crate front projection/latch count differs from near-half','Retained unselected near contact and passing: correct foreground near support, current inset-panel single-latch crate; whole-cycle joins pending')
s=s.replace('Both raw contact/passing repeat foreground thigh forward/right and near support. Crate now shows two latches/front face instead of previous single-latch side projection. Rejected correction; no assembled accepted cycle/native claim.','Both raw figures show intended foreground near support, rear darker far boot raised. Current inset-panel single-latch crate matches far05 concept; body grade/width and whole-cycle joins require review. No normal admission or native claim.')
s=s.replace("'rejected':True","'rejected':False")
exec(compile(s,str(p),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
