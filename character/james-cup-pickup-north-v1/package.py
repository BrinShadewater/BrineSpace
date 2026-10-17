from pathlib import Path
P=Path(__file__).resolve().parent
script=(P.parent/'james-meal-pickup-north-v1/package.py').read_text()
script=script.replace('frames/eat/000.png','frames/drink/000.png').replace('meal-acquire-north','cup-acquire-north').replace('bowl','cup').replace('held meal','held cup')
exec(compile(script,str(P/'package.py'),'exec'),{'__file__':str(P/'package.py'),'__name__':'__main__'})
