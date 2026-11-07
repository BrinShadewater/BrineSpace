BRINE Core Animation Kit - first prototype

What is included:
- assets/brine_core_base.png: the current full room image as the static base.
- assets/brine_body_temp.png: a rough temporary BRINE cutout for testing bobbing. It is not final-clean.
- assets/tank_glow_overlay.png: transparent full-room glow overlay for the tank.
- assets/tank_glass_overlay_temp.png: rough transparent tank/glass highlight overlay.
- assets/bubble_particle.png: small bubble sprite.
- scripts/brine_float_sprite2d.gd: bobbing script for the temporary BRINE sprite.
- scripts/brine_float.gd: bobbing script for a later AnimatedSprite2D version.
- scripts/tank_glow_pulse.gd: slow alpha pulse for the tank glow.
- scenes/BRINECoreRoom.tscn: starter Godot 4 scene.

How to use:
1. Keep the brinecore-animation folder in your Godot project root.
2. Open brinecore-animation/scenes/BRINECoreRoom.tscn.
3. You may see double-BRINE because the original base image still has her baked into the tank. This is expected for prototype testing.
4. Once the motion feels right, replace brine_core_base.png with a cleaned version where BRINE has been removed from the tank.
5. Replace brine_body_temp.png with a real transparent 4-6 frame idle animation or spritesheet.

Recommended final pass:
- Keep the room base static.
- Put the animated BRINE body behind the tank glass overlay.
- Keep bubbles and glow between BRINE and glass.
- Add monitor flicker overlays later as small sprites, not as full-room animation frames.
