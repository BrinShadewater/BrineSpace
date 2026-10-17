# Habitat refresh — September 29, 2026

Original habitat replacements: overhead cold-water lace coral, low vase sponges,
radial cup corals, spreading sea fans and quiet coral sediment. Generated with
built-in imagegen; exact prompts
in prompts.json/prompt-additions.json and immutable masters are preserved. The accepted September 26 prop board guides
painted material treatment, overhead projection and controlled detail density.

Installed through the explicit whole paths in sub_biome_view.gd SELECTED_PATHS:
coral-lace-coral, sponge-vase-sponges, coral-cup-corals, sponge-sea-fans and
coral-ground. Original sprites remain.
All 21 habitat textures load. No region positions, decorative placement seeds,
sizes, tints, collisions, clearance stages or gameplay rules change.

bake.py produces four 512px-wide props and a 1024px square continuous ground field.
Prop fitting uses alpha>=16 bounds plus two source pixels of padding to prevent
near-invisible generator specks distorting scale. Pixel color/alpha is preserved
within the crop; no recoloring or alpha threshold is applied to the image itself.
Ground uses the existing feathered world-space mesh and continuous field UVs.
Mirrored panels are diagnostic only; runtime ground remains ordinary sampling.

validate.py confirms immutable hashes, actual alpha and byte-identical rebakes:
5 identities / 10 source and runtime PNGs. Raster files use Git LFS.
Runtime environment: 66 checks, zero failures. Native fixture checks 21 textures,
five replacement bindings and deterministic decoration. Native comparisons show
old/new props at 120 physical pixels, source/tint on pale/dark ground, and normal/
mirrored sediment panels. Station capture uses 1600x900, 0.35 zoom, production
lights/fog and an explicitly authored decorative field below the station.
This is art review, not a paid expedition or seamless repeating-tile certificate.

Evidence: output/habitat-refresh-v1/native-comparison-v2.png and native-station-v2.png.
Logs: output/habitat-refresh-20260929-224004 (runtime PASS; first native FAILED)
and output/habitat-refresh-20260929-224202 (corrected native PASS). First fixture
released its mesh before rendering and drew mirrored rectangles out of bounds;
the v2 fixture retains the mesh and uses a proper reflected transform. Failed
logs/captures are retained. Scratch APPDATA/LOCALAPPDATA used for every process;
both before/after fingerprints match all 2753 owner files.

Companion addition: output/habitat-refresh-v1/native-comparison-v3.png compares the
old/new cup corals and sea fans; native-station-v3.png shows all four species with
the installed sediment. All six earlier master/runtime hashes remain unchanged.
output/habitat-refresh-20260929-230800 records raster 5/10, runtime 66 checks and
native 21 textures/deterministic placement/5 bindings passing. The wrapper exits 1
because the full 2761-file owner fingerprint detects only rotated Godot logs;
all non-log profile files match. Processes use scratch APPDATA/LOCALAPPDATA.

Installed locally and agent-reviewed. Owner review and release packaging remain
pending. No export, commit or push. Next: remaining habitat species, low-rock/timber
alternatives, then full-cell basalt/wrecks retaining authoritative clearance geometry.
