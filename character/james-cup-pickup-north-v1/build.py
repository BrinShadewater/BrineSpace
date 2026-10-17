"""Register cup source with bowl pipeline's one fixed ruler and matte curve."""
from pathlib import Path
P=Path(__file__).resolve().parent
base=P.parent/'james-meal-pickup-north-v1'
script=(base/'build.py').read_text()
script=script.replace('frames/eat/000.png','frames/drink/000.png').replace('pickup','cup pickup')
script=script.replace('held meal','held cup')
script=script.replace("'prompt.txt'","'prompt-v2.txt'").replace("'tool-prompt.txt'","'prompt-v2.txt'")
script=script.replace('exec-ebefe2c1-5dad-448e-aa7c-2cdd2bce7c29.png','exec-094a48dd-76e6-425b-9a77-47074b096849.png')
script=script.replace('Bowl rises near shoulder in authored reach; native hand/worktop contact and endpoint joins unproven. Staged, not installed.','Cup now uses image-left hand, opposite fixed belt wrench. Native contact and exact endpoint joins remain unproven. Staged, not installed.')
exec(compile(script,str(P/'build.py'),'exec'),{'__file__':str(P/'build.py'),'__name__':'__main__'})
