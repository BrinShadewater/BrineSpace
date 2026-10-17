# Whole gather source provenance

All via builtin image generation. Raw outputs, exact prompts and rejection evidence retained. Deterministic extraction/registration only; no anatomical strips or output RGB edits.

- 8aad1cc0-9579-4185-8057-fbcb5dbeb2e7: raw-interiors-v1.png, prompt-interiors-v1.txt. Original held and old gathered refs. Diagnostic only: first planted left foot moves4.5px inward before its lift; torso58-59 vs61, boots shrink, cloth brighter. Not selected motion.
- 8316497f-2020-432a-b800-53114aa4131b: raw-corrected-gather-v1.png, direct original held stance edit. Still18/20px boots, rejected as physical footwear correction.
- efabbf86-99df-4e87-b169-76d7230cdf10: raw-corrected-gather-v2.png, targeted whole-source boot breadth edit. Restores22/23px, torso61/head23/H148/sole224, but cloth median88 vs original78. Material study, not final match.
- 576c1e79-57d5-4166-addb-65a9c144507a: raw-corrected-gather-v3.png, focused cloth darkening fromv2 with original material ref. Keeps22/23 boots but cloth65 vs78; overcorrected, rejected material.
- 405dcb8b-5881-4d57-b526-1a788435ce7f: raw-corrected-gather-v4.png, requested subtle midtone increase fromv3. Keeps22/24 boots but cloth92; overcorrected, rejected material.

original-cloth-detail-reference.png is an unchanged crop(86,285,170,355) of original whole-held-source.png, used solely as a material reference, never output anatomy. Cropped master evidence doesn't replace full-body review.

- ebb8d200-d578-4e1e-a1c8-a09e7104a666: raw-corrected-gather-v5.png, prompt-corrected-gather-v5.txt. Whole v2 breadth target plus unchanged original cloth detail reference ONLY. Selected SOURCE FOUNDATION: boots22/23, torso61/head23/H148/sole224, neutral cloth quartiles63/77.33/87 versus original61/78/92.67. No deterministic body RGB edits. Paired whole original rear shell; transition not authored/accepted.
