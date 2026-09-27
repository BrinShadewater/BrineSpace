# Comms portrait revisions

## Accepted matching portrait workflow — September 2026

Read `character/installed-portraits.json` and current consumers first. The accepted
seven cast masters are `character/portraits-brine-style-v1/` (Bill, Veld,
Branforth, Marsh, Margot, Josh and River). BRINE's style reference is
`character/brine-comms-v14/portrait.png`. Older pack READMEs can have stale
installation claims. The accepted pack's manifest, exact prompts and review.html
are the reproducible style record; use its closest matching peer as needed.

For revisions, supply the currently accepted character portrait as image 1 for
identity and BRINE as image 2 for style. For new characters, establish their identity
reference first, then use the same style contract. Use built-in imagegen by default;
do not silently substitute Higgsfield or a paid CLI/API workflow. Inspect all input
images before generation. Generate one separate portrait per character.

Style contract: fine painted realism, soft diffuse cool aquatic station light,
broad quiet tonal shapes, restrained contrast/highlights, delicate material detail
and a quieter role-specific background. Remove coarse block artifacts and harsh
etched texture without blurring away anatomy. Keep close square head-and-shoulders
framing, with the face dominant at 150px. Preserve age, skin/fur color, distinctive
markings, gaze, expression, head tilt, costume and mechanical geometry. BRINE's
submersion, bubbles, skin caustics and blue suit are her identity, not requirements
for the rest of the cast. Keep dry-room portraits dry.

Keep department colors subdued. Marsh retains his ivory suit and temple implant;
Margot retains her tabby/white markings and knitted frog hat; Josh and River retain
their specific cameras, sensors, joints and panels. Use matte robot materials and
localized wear rather than blanket crackle or bright edge strips. The accepted
robot masters still contain some crackle: do not claim this pass removed it all.

Save each output immediately into a new versioned project folder. Retain exact
prompts, reference paths/hashes, output hashes and original full-resolution PNGs.
Provide labeled previous/revised/BRINE comparisons and a small-size preview.
Distinguish agent visual review, owner acceptance and runtime installation.
Accepted masters remain unchanged; future edits create new versions.

When installation is requested, bind whole quoted paths in
`Architects.SELECTION_PORTRAITS` and `Companions.PORTRAIT_PATHS`, update
`character/installed-portraits.json` and the pack manifest, and record acceptance
in CURRENT_STATUS.md and the handoff. Crew comms shares the selection portrait
loader. Check other consumers rather than assuming every `portrait()` function
means a profile image. Keep PNG loading without editor imports and Git LFS coverage.
An existing game process caches textures; an existing export needs rebuilding.

### Native verification without touching owner saves

Every Godot test/probe must receive a scratch APPDATA before it starts. This
project pins user:// beneath APPDATA/Godot/app_userdata/BrineSpace, so changing only
a fixture's save_path is insufficient: comms can write a separate archive on startup.
Fingerprint the real save folder before and after. Copy room_layouts.json only if
needed; restore scratch copies of checkpoints and reset run_save_path after restore.
Never run the old portrait probe unchanged against the owner's real folder.

The September 26 unisolated portrait tests overwrote brine_loop.save.comms.json;
the owner-provided project instructions record its restoration from an F8 report
zip. Preserve this as a validation incident, not a successful save-safety check.

Validate crew through the real selection/comms loader at 1600x900 and 960x540.
Companions cannot transmit crew dialogue: validate their actual portrait loader
and selector instead of weakening transmit rules to make a probe pass. Inspect
native captures for framing and readability; a simple texture sheet proves loading
and small-size appearance, not full selector layout or reachable controls. Keep
logs and captures under a revision-specific output folder. Documentation-only
workflow changes require no Godot run or new generation.


Inspect runtime-selected artwork and actual peer portraits. Use the selected
portrait for identity/composition, peers for rendering style, and room art for
chamber construction only. Preserve expression corrections in later edits.

Keep versioned sources, exact prompts, reference paths and hashes. Install the
selected asset in the project and update its runtime consumer. Save native
captures per revision; shared output captures are overwritten by later tests.

For bubbles over flattened portraits, mask the foreground silhouette and map
effects to the fitted image rectangle. Revisit masking when hair or pose changes.
Check other speakers, small native sizes and initial visibility: long startup
gaps and subpixel outlines can make working animation appear absent. Adjust
size separately from brightness and cadence when the owner asks for smaller bubbles.

Buoyant hair and refracted light can establish submersion. Clearly distinguish
painted cues from animation; still captures do not establish hair motion.
Consult the project visual bible for current BRINE direction.


## Close framing and selector parity

Read the current portrait consumers before selecting a revision: crew_comms.gd,
Architects.SELECTION_PORTRAITS and Companions.portrait may select different paths
from a pack README. A generated review candidate is not an installed or approved
portrait. Check current source bindings separately from the frozen build.

For this cast, faces should fill the portrait window and remain recognizable at
small native size. Match peer rendering without replacing distinctive anatomy,
hair or equipment. Treat softer shadows, darker midtones and closer framing as
separate edits; do not increase face contrast merely to darken it. Preserve each
owner correction in subsequent revisions. Use role backgrounds as quieter context,
not competing subjects. Keep generative likeness review distinct from claims of
pixel-identical foreground preservation.

Companion selector portraits share the architects' 160x170 design-pixel area,
with aspect-preserving fit and linear filtering. Check the actual visible image,
not just the TextureRect minimum: aspect ratios, atlas crops and transparent margins
can change apparent size. Capture the scroll position that shows companions and
confirm selection controls remain reachable at 1600x900 and 960x540.

Check all procedural portrait effects in the current framing. Small background
bubbles must not obscure the face; a source-image edit can invalidate a foreground
mask. Painted caustics/source bubbles are separate from animated overlays.
