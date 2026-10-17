# Frozen-release live-object attribution

Keep build `brinespace-b0b5d1b031c6ec29` and its Windows/Mac deliveries intact.
The two-hour soak showed live ObjectDB growth after texture/Node counts settled;
neither observer ownership nor a production leak has been established.

1. Run a separate physical Windows QA copy against isolated scratch saves,
   fingerprinting the owner's files and checking delivery/fixture hashes.
2. Compare two repeated normal 4× play/Return-to-Title episodes using a minimal
   observer and the prior full soak recorder. Count objects, cached resources,
   scene Nodes and processed Tweens; verify the old gameplay Node is freed.
3. Use the resulting lifetime and rate evidence to choose one focused diagnostic
   experiment. Do not infer that release orphan-counter zero means no orphans,
   or that cached-resource count enumerates all procedural Resources.
4. If a production defect is demonstrated, make the narrowest behavior-preserving
   fix and run focused regression and native lifetime validation. Otherwise record
   the measured limit and next useful diagnostic, without claiming leak acceptance.

All native runs are serial, visible on secondary screen 2, silent, with guarded
scratch APPDATA and at least 20 GiB free. No visual, crew, gameplay, architecture,
renderer or delivery changes are authorized by this diagnostic plan.

Completed: minimal/full baselines, demonstrated stale router WeakRefs, failing
lifetime regression, narrow cleanup, five focused passing tests including native
pixels, exact private Windows package audits and 600-second release validation.
All 121 fixed censuses have zero expired references; late objects settle. Original
deliveries and all player files verified unchanged. See
`docs/OBJECT_LIFETIME_2026-10-16.md` for results and separate remaining release gates.
