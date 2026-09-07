# Wall decoration style pass

Combined reviewed collection of 24 decorations from wall-dressing-v1 and v2.
Six new image-tool revisions replace the digital clock, comm panel, diver poster,
jellyfish poster, oxygen-mask rack and pressure gauges in this collection. The
other eighteen exports retain their previous artwork. Earlier packs are preserved.

## Visual review

Compared against `rooms/whole-room/crew-hab-card-activity-v1.png` for maintained
matte materials and room hierarchy, and `rooms/underwater/corner-card-dressing-v2-0.png`
for restrained wall detail. The airlock card was inspected as a construction
reference, not as an approved wall-height template.

The six original outliers had bright emission, glossy highlights, heavy rust
speckling or busy print texture. Revisions reduce those features while preserving
object identity and mounting construction. Posters have quieter ink fields; they
are not exact four-color indexed images. The clock remains a static illustration.

The eighteen retained pieces are acceptable as small supporting decorations at
the manifest's proposed sizes: pale paper and safety markings remain readable;
the lamp/beacon retain localized lit glass; botanical and personal items retain
department-appropriate warmth. This is a visual judgment at 1x/2x, not a claim
that every original source has identical pixel density or a locked shared palette.

`preview.png` shows all 24 at 1x/2x. `comparison.png` shows the six original/revised
pairs at the same height with room references. `review.gd` and `compare.gd` render
these natively; the comparison script requires the original packs and room files.

## Use and limits

Use `wall_sprites.gd` and `manifest.json` from this folder for the reviewed set.
The drawing helper loads the local PNG exports without stretching. These are
static decorative sprites, with no collision or gameplay functions.

The earlier 48-unit wall strips are mounting studies, not room integration
acceptance. The current bible requires low walls. Actual placement must fit the
host's current visible wall band, doors and occluders; do not raise walls to fit
these assets. No gameplay renderer or existing room has been changed by this pass.

## Provenance

Exact original and revision prompts are in `source/`. Six revised sources came
back as RGB with a painted pale checkerboard. The project neutral-background
cleanup removes connected exterior pixels and explicitly reviewed mounting-hole
gaps. Remaining eighteen RGBA sources use their previously reviewed alpha-128
cleanup. Original pixels remain in source files; the manifest records hashes,
native dimensions, cleanup methods and gap seeds.
