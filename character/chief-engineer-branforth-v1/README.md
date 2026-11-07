# Chief Engineer Branforth

Integrated prototype. Concept source generated with the built-in image tool on
September 6, 2026. Style references: Bill's approved concept and Veld's concept.
Exact prompt: `prompt.txt`. Source preserved as `concept-01.png`.

Identity: older stocky chief engineer, steel-grey receding hair, horseshoe
moustache, amber goggles on forehead, charcoal pressure suit with burnt-orange
Engineering panels and steel protection. Wrench on right hip, diagnostic meter
on left. Same crew family, distinct from Bill's beard and Veld's silhouette.

Requested end state: character concept, representative idle/walk/repair pilot,
complete required animation pack, and integrated engineer NPC. Remaining:
none within the integrated prototype scope.
Native gameplay-scale inspection is recorded below; owner approval is separate.

The full pack now contains four-direction idle/walk, east-facing diagnostic-meter
interaction, kneel, wrench repair and stand: 12 clips / 72 frames,
92 x 92 canvas, pivot (46, 86), shared 64-color palette. Raw generated rows remain
in `generated/`; exact prompts are in `animation-prompts.json` and the per-action
prompt text files. `python character/chief-engineer-branforth-v1/build_pack.py`
rebuilds the full pack locally, reusing Bill's extraction helpers. Standing reverses
kneeling; action endpoints share frames. Directions are not mirrored. The first
west-walk candidate was retained but rejected for insufficient pose separation;
revision two is the active source. Eleven source rows feed twelve exported clips.
The generic sprite validator passes with zero errors/warnings. Idle and walk
contact frames were inspected, followed by the complete pack contact sheet.
Timed-frame and sampled live playback review are complete. Native action and three-crew
integration checks pass as detailed below. `qa/validation.json` records the
generic validator result. `qa/engineering-sequence.gif` shows the action chain;
`qa/animation-preview.gif` contains the complete animation gallery.

The engineer controller is implemented in `scripts/branforth_npc.gd`, with
independent needs/random state, Engineering room preferences, equipment servicing
and diagnostic-meter activity. The station updates, layered rooms, corridors,
legacy rendering, connected doors and checkpoints now include Branforth.
`tests/test_branforth_pack.gd` passes in Godot 4.6.1: required directional/action
coverage, frame sizes/counts, exact action endpoints, independent controller data,
action meanings and snapshot validation.

`tests/test_branforth.gd` passes: autonomous actions, Engineering preferences,
station RNG isolation, swept movement, pause, independent playback and doors.
`tests/test_branforth_crew.gd` passes headless and native: three moving crew,
all-pair foot clearance, bounded movement, geometric clearance, traffic progress,
disk state/animation round trip, malformed engineer rejection and two-crew/crewless
save compatibility. Bill/Veld minimum separation was 20.61 canonical units; the
engineer's distances to both peers were checked against the same 19.99 tolerance.

`tests/playtest_branforth.gd` passes with autonomous four-direction walking,
kneel/repair/stand, diagnostic interaction and idle captures. Native evidence is
under `qa/native/` (local, ignored). Agent inspection of repair, diagnostic and
corridor captures finds a readable engineer silhouette, registered feet and
appropriate prop depth. Live gallery review supplements these still captures; see the review notes below.


Temporal verification now also exercises each of the six timed poses in every
clip through `CrewSpritePlayer`, over two cycles, including distance-driven walking
and one-shot endpoint clamping (144 samples; zero failures). The agent inspected
`qa/timed-movement.png` and `qa/timed-actions.png` chronologically with dwell times:
identity and ground registration remain consistent, walking alternates legs,
and the kneel/repair/stand chain preserves its shared endpoints. This is timed
frame inspection, not a claim of watching continuous playback. The subsequent live gallery review is recorded below.


Final review: `qa/review.html` plays all 12 clips from the packaged PNGs and
manifest durations. The agent inspected successive live browser snapshots with
changing frame counters and poses, supplementing the complete timed-frame review
and native Godot captures. This is sampled visual playback inspection, not human
owner approval or a claim of continuous video perception. Observed poses preserve
the stocky orange/charcoal identity, fixed ground contact and alternating gait.
The diagnostic action raises and lowers the handheld instrument; maintenance lowers
to a wrench-working pose and returns to standing. No blocking defect was found.

Limits: six-pose stylized motion; east-facing work actions; small equipment details
vary across generated poses; local three-crew avoidance rather than population-scale
crowd simulation. NPC needs remain visual, with no station resource consumption,
staffing bonuses or repair rewards. Export/release packaging is outside this scope.
`qa/completion-evidence.json` records current integration hashes and test summaries.
