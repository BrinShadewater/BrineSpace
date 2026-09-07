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
- Source hashes, authoring method, exact prompts for generated sources, build
  settings, and derived/mirrored/reversed-frame provenance.

Extend the current manifest deliberately when needed. Do not replace a working
schema with a generic engine export example. Keep playback metadata authoritative
in one place and derive exported timing and previews from it.

Current humanoid defaults: 92 × 92 canvas, (46, 86) foot pivot, 74-pixel standing
height, 64-color pack palette, binary alpha. These describe existing packs; keep
them for compatible crew unless the task calls for a different profile. Do not
stretch individual poses to equal heights or center each frame independently.

Veld uses four-direction idle/walk, east-facing scanner interaction, and
idle → kneel → repair/sample inspection → stand → idle. Her 12 clips contain
72 frames. Bill has 17 clips/102 frames, including running and an extra diagonal
walk. Generate states needed by the requested controller, not the union of both.
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

From the checkout root, existing pack rebuilds are:

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
