from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'character/veld-cardinal-actions-shared-original-helmet-v1/prepare_review.py').read_text()
s=s.replace('output/veld-cardinal-actions-shared-original-helmet-v1','output/veld-idle-north-original-master-v1').replace('558','282').replace("['north','east','west']","['north']")
s=s.replace('30 chronological boards','12 chronological boards').replace('Standalone N/E/W shared helmet action families','Standalone North original-guided idle and cargo joins')
s=s.replace('Veld cardinal shared original helmet','Veld North original master idle').replace('Veld North, East and West - shared original helmet','Veld North - original master idle')
s=s.replace('North, East and West pickup, unload, carrying and start/stop share the original-master turn helmets. Held-case and turn endpoints match exactly. Whole bodies and action clocks are preserved. Master grading, full idle and gameplay integration remain in progress.','Quiet North breathing follows the prepared original rear master, with planted boots and a fixed shared helmet. Pickup and unload share its exact resting endpoint. Broader body grading and gameplay transitions remain in progress.')
s=s.replace('Carry loops in the engine','Carry and idle loop in the engine').replace('unload-west-comparison.png','paired-original-idle.png').replace('Six overviews cover','Two overviews cover')
# Execute the maintained review builder here so its __file__ resolves to this package.
exec(compile(s,str(P/'prepare_review.py'),'exec'),{'__file__':str(P/'prepare_review.py')})
parts=['# Built-in generation prompts\n\nOriginal master governs identity, proportions, camera and grade. All four executions use the built-in tool.\n']
for name in ['prompt-clean-master-v1.txt','prompt-idle-v1.txt','prompt-idle-v2.txt','prompt-idle-v3.txt']:
 parts.append('\n## '+name+'\n\n'+(P/name).read_text()+'\n')
(P/'PROMPTS.md').write_text(''.join(parts))
