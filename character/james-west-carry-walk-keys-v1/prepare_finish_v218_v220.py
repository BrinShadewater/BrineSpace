from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_finish_v215_v216.py').read_text(encoding='utf-8')
s=s.replace('[(35,215),(36,216)]','[(37,218),(38,219),(39,220)]')
s=s.replace('The feet are separating: the boot on the left points left, while the boot on the right retains its diagonal down-left toe and raised up-right heel.', 'The feet are separated in this exact walking phase. Preserve the existing pitch of each boot independently: toe and heel heights and all sole angles must stay exactly as in Image1.')
exec(compile(s,str(p/'prepare_finish_v218_v220.py'),'exec'))
