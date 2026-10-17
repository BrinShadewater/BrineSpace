# North master preparation

The original rear identity reference is an opaque512px image with a legacy
magenta background. The deterministic key test in build_master.py registered
the figure to148opaque pixels but left visible magenta contamination in the
hair, sleeve and boot edges. Its original-idle-master.png and comparison are
diagnostic only, rejected as animation/runtime source. Original RGB was retained
outside the key, which is not sufficient for a clean cutout.

Use the built-in edit in prompt-clean-master-v1.txt to prepare a faithful alpha
source. Inspect original-vs-prepared materials/proportions before using it for
idle generation. Successful generation does not certify pixel preservation.
Keep the original reference and both preparation results with their bindings.
