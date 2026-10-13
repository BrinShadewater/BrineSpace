# Veld arm swing refinement

Updated: 2026-09-27. Project: Brine Space.

## Objective and acceptance
Owner says four-pose walk better, but arms move too much. Reduce swing only.

## Accepted decisions and constraints
Retain improved character and leg staging. East untouched, runtime unchanged.

## Current state
character/veld-west-walk-master-v3: imagegen edit of v2 four-frame source with
relaxed contact arms, forward hand down at hip/thigh rather than chest.
Exact prompt/source, local extraction, manifest and old/new GIF included.

## Verification
Source and contact sheet reviewed; arm excursion visibly reduced. Manifest
validator clean; common scale, 225ms per frame. Head/collar31-32px, body147-149px.
Leg silhouettes broadly retained but imagegen may alter other pixels; no exact
geometry preservation claim. No native foot-contact testing or installation.

## Next action
Owner review arm-before-after.gif; if rhythm accepted, add in-betweens with
restrained arms and same identity. No further palette changes requested.
