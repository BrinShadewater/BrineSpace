"""Retain whole opposite contact with enlarged matching crate; no admission."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/build_marsh_east_carry_contact03.py').read_text().replace('contact-03','contact-07').replace('exec-1661ff9f-b710-4f30-ae90-3b6dc30c659a','exec-a022b5f8-98d9-4aef-a929-f145d7770f79')
s=s.replace('foreground thigh correctly backward/left, boot contact projection and crate variant remain provisional','opposite far contact retained, crate enlarged toward far05; packed cycle joins pending')
s=s.replace('Foreground near thigh correctly goes backward LEFT, darker far thigh forward RIGHT. Far front boot angled and projects above rear near boot; supporting sole not certified. Crate single-latch broad recessed panel differs from source01 rounded box; cannot assume cross-half consistency. Whole body/grade/crate/contact joins pending.','Correct foreground near thigh backward LEFT and darker far thigh forward RIGHT, front far boot flat. Crate enlarged toward far05 single-latch inset-panel projection. Whole body/cargo/registration joins require review; contact not certified.')
exec(compile(s,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
