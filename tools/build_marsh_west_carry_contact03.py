"""Pack correct whole West opposite contact with one own neutral calibration."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/build_marsh_east_carry_contact03.py').read_text().replace('east','west').replace('East','West').replace('exec-1661ff9f-b710-4f30-ae90-3b6dc30c659a','exec-9c21d53b-efb4-469c-bab9-4e15245b3abb')
s=s.replace('foreground thigh correctly backward/left, boot contact projection and crate variant remain provisional','foreground near thigh backward/right and darker far leg forward/left correctly achieved; crate/grade joins provisional')
s=s.replace('Foreground near thigh correctly goes backward LEFT, darker far thigh forward RIGHT. Far front boot angled and projects above rear near boot; supporting sole not certified. Crate single-latch broad recessed panel differs from source01 rounded box; cannot assume cross-half consistency. Whole body/grade/crate/contact joins pending.','Foreground near thigh slopes backward RIGHT; darker far leg forward LEFT supports flat front boot. Correct opposite whole anatomy. Crate now broader recessed two-section panel/single block left latch; source02 cargo/body joins cannot be assumed. Packed material and physical sole/contact remain provisional.')
exec(compile(s,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
