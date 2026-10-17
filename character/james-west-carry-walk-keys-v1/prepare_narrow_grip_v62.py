from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_narrow_grip_v61.py').read_text().replace('v61','v62').replace('V61','V62').replace('[(90,128,134,155),(107,122,119,128)]','[(90,129,126,155),(126,137,138,152),(107,122,119,128)]').replace('64276','64348')
exec(compile(s,str(__file__),'exec'))
