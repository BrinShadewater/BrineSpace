# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: selective lossless effect storage and comparison fidelity

## Objective and acceptance

Reduce the observed mixed-room upload burst without frame/memory regression.
Native pixels/input/lifetime and repeated matched gameplay remain required.
Full release goal remains open; no provider admitted.

## Accepted decisions and constraints

Production unchanged; no global cache increase, art copies, lossy conversion or
quality changes. Reuse existing byte-verified R8 effect assets/hardened shared
Bank/Group. Select only West/North/South mining effects; body textures stay normal.
Do not interpret the combined private provider as isolated storage evidence.

## Current state

Builders/checker/pilot in `output/renderdoc-tools-2026-10-08/`:
`build-effects-only-provider.py`, `check-effects-only-bank.py`,
`run-effects-only-mixed-pilot.py`. Small private code/catalog/resource maps in
`benchmark-input-isolation/effects-only-provider/`. No normal game renderer changes.

## Verification

Unique trace-event census of previous110ms mixed-room stall: each of its three
sheets uploaded once in measured trace. Startup/warm-up excluded, so this does not
prove first-ever loading; repeated eviction is not established for that burst.
Two413.44MiB-burst effects sheets can use existing lossless R8: theoretical total
payload433520640→216760320bytes, plus shared palette1209344bytes. Storage arithmetic
only. Earlier standalone West/South native pixels and hardened21-source bank/Group
evidence reused, not rerun unchanged. New actual debug=false selective Bank18
checks pass: three R8 sources, segment/byte validation, cache identity, command
ownership/release and malformed-index fallback. No engine errors.

Matched mixed-room pilot2runs/2160frames/12 full states/cameras/labels exact:
mean30.562→31.023ms,p9545.569→46.303,p9953.525→53.743,max91.048→83.827,
>50ms21→24,>100ms0→0. Peak2928.086→3143.998MiB (above3GiB candidate target).
GPU query mean6.803→6.314ms; delayed scope, not current-frame causal timing.
No indexed ordinary duplicates or fallback draws. Candidate's ordinary cache
reaches723108752bytes alongside72253440 indexed bytes despite soft256MiB budget.
Cause of all higher retention remains unassigned. No FPS/memory admission.

Inspection discovers additional `prepare_collection(d,s)` in private Motion.draw,
absent from normal DroneAnimation.draw. It prepares/touches future collection
layers, including ordinary resources. This is a comparison confound; first pilot
is valid for that combined provider, not isolated effects-only attribution. The
builder now writes `motion-no-collection-lookahead.gd` and maps it. Corrected
variant not yet parsed/executed; retained pilot driver still overrides Motion to
old trace version and MUST be changed before another run.

All successful native logs clean, owner2938 unchanged; jobs terminal, override
restored. Bounded evidence/no screenshots/runtime copies. Original renderer intact.

## Next action

Use a NEW output folder and corrected driver that respects the new Motion mapping;
assert loaded source excludes the extra collection call. Preserve required worker
loading/readiness/filters and payload validation. Then one matched mixed-room pair
before broader repeated trials. Do not reuse cached combined-pilot results or
interpret rejection as proof about isolated R8 storage. If still worse, move to
another measured remedy. Complete remaining mixed mission/visual/hardware and
full FPS/loading/endurance/save/bug/PC-Mac release gates.

## Corrected pilot completed; alternative native storage identified

`run-effects-only-corrected-pilot.py` uses a new folder and respects Motion mapping.
Before gameplay, native source guard compares loaded Script bytes to corrected
file and rejects the extra draw call; `EFFECTS_SOURCE_GUARD_OK` verified.
Two native debug=false runs/2160 measured frames, all12 states/cameras/labels exact:
mean30.661→31.105ms,p9545.607→46.149,p9954.628→55.554,>50ms21→27,
>100ms1→0,max111.499→84.065. Peak2928.086→2777.143MiB; end1939.219→1940.756.
GPU query mean6.301→6.550ms. No runtime/missing-art errors, owner2938 unchanged,
jobs terminal/override restored. Corrected provider still not admitted: memory and
maximum improve, mean/tails do not. No repeated timing of this unchanged candidate.
Artifacts `effects-only-corrected-pilot/{comparison.json,*.json,*.log,owner.json}`.

Additional bounded inventory: all three original effect sheets contain only TWO
RGB values across every pixel, including transparent RGB: black and(135,139,125).
All nontransparent entries have the latter color.152 exact RGBA colors/source;
36,126,720 pixels each. Palette inventory confirmed by full original PNG color
census, saved `effects-only-provider/full-rgb-inventory.json`. Earlier no-grayscale
conclusion remains correct; colored constant RGB is a different representation.

Next test a lossless native LA8 representation: binary luminance mask encodes
black vs colored RGB, original alpha retained, constant RGB supplied by draw tint.
That can reconstruct all source RGBA bytes without palette fetch/shader/command
backend, but native output/filter/modulation equivalence is UNPROVEN. First build
bounded derived PNGs and reconstruct every original byte, then native nearest/
linear, tint/parent modulation, flood, mirror/frame/alpha oracles. Preserve explicit
original-image fallback for any unsupported context and PNG runtime loading.
Do not install it or claim performance until actual matched source/visual/timing
acceptance. Keep all original release gates and owner protections.
