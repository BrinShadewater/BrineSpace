# Veld v9 - east exposure correction
Candidate only. Corrected idle-east, walk-east and interact-east fabric exposure.
Old 0.43 measurement ceiling omitted bright fabric, while 0.72 minimum gain
prevented adequate correction. New east-only thigh measurement targets 0.272,
matching the retained front idle. Skin/blue retain independent targets.
42 alpha masks unchanged; 24 non-east frames byte-identical. Exact idle/action
joins preserved. 160 native checks pass, manifest validator clean, all 2670 real
profile hashes unchanged. See exposure-audit.json and east-brightness-comparison.png.
No production selection changed. Held walk drafts remain in v8, excluded here.
