# Animation contract and packaging

Inspect `character/dr-veld-v1/final/manifest.json`, the pack README, and the actual
consumer before writing a new contract. Bill and Veld are examples with different
coverage, not mandatory frame-count targets.

## Record the required data

- Stable character/version ID and canonical reference/source paths.
- Canvas dimensions, foot pivot, intended standing scale, alpha/palette policy.
- Required states and directions, ordered frame paths and counts, per-frame
  duration, loop/one-shot behavior, and action meanings.
- Transition chains and compatible endpoints; locomotion stride distance where
  the player advances frames by movement rather than elapsed time.
  A full state/direction key may override the state-wide stride when authored gait
  reach differs; consumers must retain the state-wide fallback for other clips.
- Source hashes, authoring method, exact prompts for generated sources, build
  settings, and derived/mirrored/reversed-frame provenance.

Extend the current manifest deliberately when needed. Do not replace a working
schema with a generic engine export example. Keep playback metadata authoritative
in one place and derive exported timing and previews from it.

Legacy humanoid profile: 92 × 92 canvas, (46, 86) foot pivot, 74-pixel standing
height, 64-color base palette, binary alpha. Bill's selected `major-bill-v3`
declares standingHeight 148, with canvas/pivot profiles appropriate to each pose.
Inspect `character/ACTIVE_ASSETS.json` and the active loader before selecting a
reference or calibration. Keep legacy profiles for compatible crew. Do not
stretch individual poses to equal heights or center each frame independently.

Veld uses four-direction idle/walk, east-facing scanner interaction, and
idle → kneel → repair/sample inspection → stand → idle. Her 12 clips contain
72 frames. Bill's original base had 17 clips/102 frames; his complete selected
library has 175 bare states/1,134 frame references and 168 equipped states/1,080
references, including runtime joins. These are coverage counts, not unique authored
pose counts. Generate states needed by the requested controller, not the union of both.
Six frames per clip is a current choice, not a smoothness requirement.

## Production and revision

Prove representative poses and timing early. Inspect opposite views rather than
assuming mirroring is safe. Share compatible endpoint frames when it improves the
intended transition; reverse a kneel only if the resulting stand motion is credible.
Record reused frames so an export count is not mistaken for a generated-source count.

Preserve accepted regions/rows during repairs. Retiming an existing motion does
not necessarily require new art. Treat repeated identity drift or expensive pose
retakes as evidence to propose a different authoring method, not permission for
an unsolicited pipeline migration.

## Existing tools

From the checkout root, the selected complete Bill rebuild and read-only check are:

```powershell
python tools/rebuild_bill_art.py
python tools/validate_bill_art.py
```

The first writes the new revision from preserved sources; the second checks it.
The original native migration inventory is frozen in
`tools/bill-art-source-contract.json`; do not replace it with a dump of the new
consumer. The historical base-only rebuilds below do not update the selected Bill
revision:

```powershell
python character/dr-veld-v1/build_pack.py
python character/major-bill-v2/build_pack.py
```

These commands write the corresponding pack outputs. Use them for that pack's
authorized rebuild, not as read-only validation. They require Pillow and NumPy.
Veld's builder imports Bill's helpers; inspect that dependency before adapting
it. For a new character, give the builder its own source/output root so it cannot
overwrite Bill or Veld. Do not refactor game architecture to create a pack.

For a single-clip repair, note that the current Veld builder processes the whole
pack and recomputes its shared palette: one changed source can alter accepted
clips. Preserve the accepted palette/unrelated frame pixels or account for an
explicitly intended pack-wide change. Its `--partial` option skips missing sources;
it is not a selector for one animation. Verify affected and unaffected outputs.

When `sprite-animation-maker` is installed, locate its directory from the skill
catalog and run its existing validator:

```text
python <sprite-skill>/scripts/validate_sprite_manifest.py --manifest <pack>/final/manifest.json
```

Check its actual supported schema/options when adapting inputs. If unavailable,
perform equivalent image/manifest checks with project tools and identify that
the generic validator was not run. Do not assume a tool's success proves checks
outside its documented coverage.

Preserve sources, cleaned frames, strips/atlas, manifest, requested Godot resource,
contact sheet, and motion previews. Keep script/UID pairs and project LFS rules.
For Godot SpriteFrames conversion, durations are relative to animation FPS, not
milliseconds; verify absolute playback timing against the manifest. Existing raw
PNG consumers also need verification even if a generated `.tres` loads correctly.
