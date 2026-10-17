from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'arrival-join-v324';o.mkdir(exist_ok=True)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
current=(r/'scripts/james_cargo_player.gd').read_text(encoding='utf-8')
old=current[:current.index('func join_north_unload_entry')]+current[current.index('func floor_texture'):]
previous=json.loads((p/'arrival-journey-v323/inputs.json').read_bytes())['preLaunchSha256']['scripts/james_cargo_player.gd']
assert hashlib.sha256(old.encode()).hexdigest()==previous
(p/'arrival-journey-v323/tested-player-before-join.gd.txt').write_bytes(old.encode('utf-8'))
text=(p/'arrival-journey-v323/native_probe.gd').read_text(encoding='utf-8').replace('arrival-journey-v323','arrival-join-v324').replace('arrival323','arrival324').replace('james-arrival323','james-arrival324')
needle='        var captures:Array=[await capture(mode+"-carry-entry-000",npc)]'
text=text.replace(needle,'        check(bank["unload-north"][0].get_image().get_data()==bank["carry-turn-west-north"][-1].get_image().get_data(),"Exact registered turn endpoint reused as north unloading entrance")\n'+needle)
(o/'native_probe.gd').write_text(text,encoding='utf-8')
files=[o/'native_probe.gd',r/'scripts/branforth_npc.gd',r/'scripts/james_workshop_arrival.gd',r/'scripts/james_cargo_actor.gd',r/'scripts/james_cargo_player.gd',r/'character/james-cargo-return-bridges-v1/return_actor.gd',r/'scripts/run_save.gd']
(o/'inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():sha(f) for f in files},candidateBanksLoaded=False),indent=2)+'\n',encoding='utf-8')
print('324 normal exact-source entry reuse; paired journey/full restore probe frozen.')
