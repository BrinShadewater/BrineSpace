"""Retain good near contact and rejected far-like requested near passing."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/build_marsh_east_carry_half02.py').read_text().replace('east','west').replace('East','West').replace('half-02','near-06').replace('far-near-06-rejected','near-06-unselected').replace('exec-2557b186-1649-4014-be99-f397cd83811a','exec-d4ddf953-e306-4917-b0f6-db8ab815ca73')
s=s.replace('wrong-near-contact.png','near-contact.png').replace('wrong-near-passing.png','requested-near-passing-wrong-far.png')
s=s.replace('Retained rejected: contact/passing both near support; crate front projection/latch count differs from near-half','Retained partial: near contact correct, requested near passing repeats far support from cargo reference; no complete cycle')
s=s.replace('Both raw contact/passing repeat foreground thigh forward/right and near support. Crate now shows two latches/front face instead of previous single-latch side projection. Rejected correction; no assembled accepted cycle/native claim.','Near contact foreground near thigh forward LEFT correct. Requested near passing instead has foreground near knee RIGHT,near rear boot RIGHT raised and darker far shin LEFT flat: repeats far support. Current plain inset-panel single-left-block-latch crate closer to far05; no complete opposite cycle/native acceptance.')
exec(compile(s,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
