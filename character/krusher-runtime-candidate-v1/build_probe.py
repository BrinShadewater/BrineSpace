from pathlib import Path
p=Path(__file__).resolve().parent/'native'
(p/'review.gd').write_text('extends SceneTree\n\n'+(p/'stage.inc').read_text()+'\n'+(p/'probe.inc').read_text())
(p/'motion.gd').write_text('extends SceneTree\n\n'+(p/'stage.inc').read_text()+'\n'+(p/'motion.inc').read_text())
