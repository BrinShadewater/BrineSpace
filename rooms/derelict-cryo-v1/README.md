# Derelict cryo recovery

The [architect identity pass](../architect-cryo-v1/README.md) supersedes the generic
occupants on new loops: the selected architect starts in BRINE Core, and the other
two occupy one derelict ward each. This original record describes the generic
one/two-pod system retained by legacy saves and its fixture.

New runs seed a one-pod ward at (19,18), facing north/south, and a two-pod ward at
(22,21), facing east/west. Existing checkpoints retain their existing map.

Connect a matching station door, select the ward and choose **Repair & Connect**.
The shared exterior rig spends 8 Metal once and takes 18 simulation seconds.
Pausing the job retains payment and progress. Completion absorbs that same
compartment as a Cryo Chamber, retaining its location, rotation and occupants.
It receives normal power evaluation on the next cycle; it is not a free blueprint.

Powered wards thaw one occupant at a time. Each seven-second sequence opens the
pod, sits the survivor up, brings their feet over the rim, steps out and stands.
Only the completed sequence adds a named survivor and increments living crew.
Full berths, missing food/oxygen, suspension, power loss and global pause retain
progress. Ordinary crew upkeep and failure rules apply after recovery. The journal
has a **Crew** tab; the HUD crew counter opens it. Named losses remain recorded.
Save/Continue preserves paid repairs, partial thaw, exhausted pods and the roster.
Restored wards cannot create extra occupants through repeated Safe Wake bonuses;
the existing discovery/stabilization graph and legacy blueprint rules are retained.

## Art and motion contract

Medical hull, compressor, diagnostics and empty pods reuse the registered cryo
room. Damage is localized code-rendered hull-seam wear; this is not a new wreck
illustration or a simulated flooding system. The one-pod variant removes the
second prop from rendering and navigation. Sockets rotate; props remain south-facing.
The inspector uses the occupied-pod art rather than the empty blueprint thumbnail.

The preserved generated source contains six new poses, using the existing pod
and Bill identity as references. Exact prompt and reference roles are in
`prompt.txt`; source hash, dimensions and registration are in `manifest.json`.
`build_pack.py` slices without inventing, mirroring or stretching poses. The
builder retains the connected pod/occupant subject and removes detached alpha
specks from frame exports, preserving the unmodified source. The generic
sprite-manifest validator checks dimensions, coverage and registration.
The shared casing base is (210,560) in each 418x627 frame; second-row origin is offset
586 pixels. Runtime renders at the registered pod width. Six equal timing stages
span seven seconds; the GIF repeats only for review. The actual recovery is one-shot.

Survivors currently share the generated rescue-suit appearance. They join the
population and named roster; this does not add individual wandering NPC controllers,
unique portraits, role bonuses or persistent meta-game character unlocks. On roster
entry, the occupied animation returns to the existing empty-pod presentation.
Bill, Veld and Branforth remain the independent visual NPC prototypes.

## Verification

- `tests/test_cryo_recovery.gd`: paid/blocked access, one and two pod recovery,
  pause/suspension/supply/berth gates, saved repair and mid-thaw, once-only roster,
  malformed/duplicate rejection and old checkpoints.
- `tests/playtest_cryo_recovery.gd`: actual station at 1280/1600/2560, all six
  poses in all four rotations, native pause pixels and roster UI.
- Native evidence: `output/cryo-recovery-v1/`; second capture pass corrects the
  first pass's clipped camera. Agent inspection confirms readable emergence and
  pod placement at station scale; it is not owner aesthetic approval.
- Save, wreck, rock, discovery, economy, balance and crew regressions are recorded
  under `output/cryo-*`. Existing raw-image loading warnings remain; no release
  export or packaging claim is made for this addition.
- `test_crew_polish.gd` passes. `test_bill_npc.gd` retains its pre-existing bend
  chord failure at step 3542, matching the earlier
  `output/batch-two/crew-bend-diagnostic-v1.log` trajectory hash
  `19c1d07e4956285bd65de2dfecb36aa6b354f7c4e0feafb8c229cc722fac0170` exactly.
  Both actually traversed bend segments report clear; that separate regression
  remains unresolved rather than being hidden or changed for this feature.

Prototype pacing values (two fixed wards, 8 Metal, 18-second repair and 7-second
thaw) need play feedback. Generated poses are stepped keyframes, not interpolated
skeletal animation. The room retains the inherited sparse furnishing layout.
