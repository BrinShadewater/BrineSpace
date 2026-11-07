"""Retain correct far support, with passing stride still too extended."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/build_marsh_east_carry_contact03.py').read_text().replace('east','west').replace('East','West').replace('contact-03','passing-04').replace('far-contact.png','far-passing.png').replace('exec-1661ff9f-b710-4f30-ae90-3b6dc30c659a','exec-f5f1fe86-8160-45b6-b09d-acf55eb61fe6')
s=s.replace('foreground thigh correctly backward/left, boot contact projection and crate variant remain provisional','far support correct but foreground near rear leg remains extended like contact; passing refinement pending')
s=s.replace('Foreground near thigh correctly goes backward LEFT, darker far thigh forward RIGHT. Far front boot angled and projects above rear near boot; supporting sole not certified. Crate single-latch broad recessed panel differs from source01 rounded box; cannot assume cross-half consistency. Whole body/grade/crate/contact joins pending.','Correct far support and foreground near rear boot RIGHT, but near thigh/shin remain extended and passing does not compress enough relative contact03. Current crate concept close, projection/grade and connected arm joins provisional; not accepted passing cycle.')
exec(compile(s,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
