"""Refine the measured 48..56 depth boundary for empty and grasp poses."""
from pathlib import Path
P=Path(__file__).resolve().parent
s=(P/'native-contact-depth.gd').read_text().replace('native-contact-depth','native-contact-depth-fine').replace('depth-captures','depth-fine-captures')
s=s.replace('index==4 and','index in [3,4] and').replace('[0,8,16,24,32,40,48,56,64]','[49,50,51,52,53,54,55,56,64]')
s=s.replace('"index":4,"depthOffset":depth','"index":index,"depthOffset":depth')
s=s.replace('"contact-depth-%02d"%depth','"contact-%02d-depth-%02d"%[index,depth]')
s=s.replace('JAMES SOUTH CONTACT DEPTH','JAMES SOUTH CONTACT DEPTH FINE')
(P/'native-contact-depth-fine.gd').write_text(s)
print('Fine boundary samples for both empty and grasp contact, unchanged actors.')
