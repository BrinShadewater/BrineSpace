from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'character/james-inspect-tablet-v1/validate.gd').read_text(encoding='utf-8').replace('james-inspect-tablet-v1','james-inspect-material-continuity-v1')
s=s.replace('func _init() -> void:\n    call_deferred','func _init() -> void:\n    print("JAMES MATERIAL BOOT")\n    call_deferred')
s=s.replace('check(absf(elapsed-(6.0))<0.00001,"Authored inspection duration")','check(absf(elapsed-float(state.frameDurationsMs.reduce(func(a,b): return a+b,0))/1000.0)<0.00001,"Unchanged source clock duration")')
s=s.replace('for state in pack.states:\n        for index in','for state in pack.states:\n        if not String(state.id).begins_with("inspect-"): continue\n        for index in')
s=s.replace('print("JAMES TABLET INSPECTION INSTALLED:', 'var report := {"checks":checks,"failures":failures,"captures":captures,"scope":"All selected inspection, diagnostic and sealed meal substitute source references through normal loader; clocks/pivots/density and inspection loop/life policy. Native route/gear journeys not exercised."}\n    var report_file := FileAccess.open("res://character/james-inspect-material-continuity-v1/validate-evidence.json",FileAccess.WRITE)\n    report_file.store_string(JSON.stringify(report,"  "))\n    print("JAMES TABLET MATERIAL CONTINUITY:')
(P/'validate.gd').write_text(s,encoding='utf-8')
print('Native loader fixture prepared; isolated wrapper required.')
