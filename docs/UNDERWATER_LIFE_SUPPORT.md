# Underwater Life Support presentation

Owner approved the generated direction. Integrated as a dedicated subclass so
Hydroponics, Reactor, Medical and historical connected-room studies retain their
own artwork. Existing Life Support ID, cost, production, consumption, unlock and
socket metadata are unchanged.

Primary department: Life Support; maintained grey industrial construction,
insulated service equipment and restrained cyan identification. Four south-facing
assemblies: ventilation cabinet, three-vessel filter skid, transparent treatment
tank with attached pump, and diagnostic console. Replaces the repeated fan unit.
Equipment centres rotate while source silhouettes, height and effect orientation
remain fixed; containment adjustment includes complete registered silhouettes.

Source: life-support-underwater-source-v1.png (1254 square, requested 1280).
Exact built-in generation prompt and SHA-256 are in the adjacent generation JSON.
Raw art and prior versions are preserved. Engine geometry owns walls/doors, not
the source illustration. New grey wall strips use their own source coordinates;
the first card incorrectly reused the nursery wall sample and remains archived.

Current consumers: grid_canvas.gd uses underwater_life_support_view.gd; both
card maps use life-support-underwater-card-v3.png. Room lights are cool white.
Four independently gated effects: fan rotation cues, filter flow marks, bubbles
inside treatment glass, and console traces. Static cyan glass/identification is
part of the source; this is not a fully separated emissive-mask asset.

Verification:

- underwater-life-station-v1: four-room circuit (1,616 walker samples), 404
  distinct-neighbor samples, complete prop containment/non-overlap, 32 room state
  comparisons and 40-room fit; passed before final white-light adjustment.
- underwater-life-effects-v2: each of four machines compared independently in
  four rotations; active motion, inactive stillness, pause and source-effect
  envelope checks pass with final white lighting. No engine errors.
- Card v3 is baked through the same embedded renderer. Source/card LFS rules
  remain active. No gameplay balance changes, save migration or publication.

The isolated corridor pilot still uses the historical Life Support study; its
earlier media is not evidence for this redesign. Production station uses the new
subclass. Future corridor review should explicitly select the production class.
