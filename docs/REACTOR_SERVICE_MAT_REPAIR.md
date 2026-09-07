# Reactor service mat repair

The service-table mat is now 84x38, down from 104x38, retaining offset (-4,-5)
and its existing colors. Its 76-unit host remains unchanged. The mat no longer
extends into the east wall in the reviewed q3 image. Source art, prop placement,
cooler mounting platform, walls, doors and collision are untouched.

## Evidence

- Before: `output/catalog-mat-review-v1/reactor-q3.png`, visually inspected;
  fresh catalog audit also flagged q2 and q3.
- `output/reactor-mat-contained-v2.log`: child 0, all four mats contained.
- `output/reactor-mat-review-v2`: four native room captures; q3 inspected.
- `output/reactor-mat-effects-v2.log`: child 0, no engine errors, 48 host
  operation comparisons and four actual main-clock pause/resume pairs pass.
  Measurements deliberately remove crew occlusion; not crew-depth evidence.
- Native 512-square card `reactor-card-mat-v2.png` baked and visually inspected;
  child 0, no engine errors, LFS attribute verified. Both station mappings
  (including alternate-art list), card consumer and export manifest select it.
  The old card is retained, and the composition manifest hash is updated.

Profile SHA256: `553B3CF4F6A9B2DC9BD9292CC3820357A5B0D366C283E4E022B2BE8BA4CFEAE2`.
Card SHA256: `A9FE326B2D116667626C12E18AC0ABB952E3469DAF169F84C1E27AFCFA7F246F`.

Fresh packaging for this mat revision remains pending with the other batch
repairs. Earlier Reactor package/lighting evidence describes its earlier mat.
The established host-fitted mat rule was sufficient; no bible change is needed.
