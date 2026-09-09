# Comms portrait revisions

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
