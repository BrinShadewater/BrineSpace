from pathlib import Path
p=Path(__file__).resolve().parent
script=(p/'build_arrival_review_v300.py').read_text(encoding='utf-8').replace('arrival-turn-chronology-v300','arrival-turn-chronology-v303').replace('study 300','study 303')
script=script.replace("exec(compile(script", "script=script.replace('arrival-turn-pose2-v297','arrival-turn-pose2-v302')\nexec(compile(script")
exec(compile(script,str(p/'build_arrival_review_v300.py'),'exec'))
