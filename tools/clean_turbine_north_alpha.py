"""Remove disconnected generation specks from the cleaned Turbine north candidate."""

from collections import deque
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/turbine-directional-v4/north-overhead-clean-v1.png"
OUTPUT = ROOT / "assets/turbine-directional-v4/north-overhead-v1.png"


def main() -> None:
    if OUTPUT.exists():
        raise SystemExit(f"Refusing to overwrite {OUTPUT}")
    image = Image.open(SOURCE).convert("RGBA")
    alpha = image.getchannel("A")
    seen: set[tuple[int, int]] = set()
    components: list[list[tuple[int, int]]] = []
    for y in range(image.height):
        for x in range(image.width):
            start = (x, y)
            if start in seen or alpha.getpixel(start) == 0:
                continue
            component: list[tuple[int, int]] = []
            queue = deque([start])
            seen.add(start)
            while queue:
                point = queue.popleft()
                component.append(point)
                px, py = point
                for neighbor in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                    nx, ny = neighbor
                    if not (0 <= nx < image.width and 0 <= ny < image.height):
                        continue
                    if neighbor in seen or alpha.getpixel(neighbor) == 0:
                        continue
                    seen.add(neighbor)
                    queue.append(neighbor)
            components.append(component)

    components.sort(key=len, reverse=True)
    if not components or len(components[0]) < 900_000:
        raise AssertionError("Expected one dominant connected turbine silhouette")
    removed = 0
    for component in components[1:]:
        if len(component) >= 10:
            raise AssertionError(f"Unexpected secondary component with {len(component)} pixels")
        for point in component:
            red, green, blue, _ = image.getpixel(point)
            image.putpixel(point, (red, green, blue, 0))
            removed += 1
    if removed != 25:
        raise AssertionError(f"Expected 25 disconnected pixels, removed {removed}")
    image.save(OUTPUT, optimize=True)
    print(f"PASS removed={removed} components={len(components)} alpha_bounds={image.getbbox()}")


if __name__ == "__main__":
    main()
