Here's an updated version that labels each planet's volume:

```python
# -*- coding: utf-8 -*-
import numpy as np

# Planet radii in kilometers (same order as the names below)
radii = np.array([2439.7, 6051.8, 6371, 3389.7, 69911, 58232, 25362, 24622])

# A list of planet names, matching the order of the radii above
planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

# Calculate the volume for every planet at once
volumes = 4 / 3 * np.pi * radii**3

# Loop through each planet and print its name with its volume
for i in range(len(planets)):
    # "i" is the position number (0 = Mercury, 1 = Venus, etc.)
    print(f"{planets[i]}: {volumes[i]:,.2f} km³")
```

**Output looks like this:**
```
Mercury: 60,827,515,880.76 km³
Venus: 928,413,436,727.75 km³
Earth: 1,083,206,916,845.78 km³
Mars: 163,114,706,192.49 km³
Jupiter: 1,431,281,810,739,360.50 km³
Saturn: 826,719,780,388,111.00 km³
Uranus: 68,295,517,194,794.70 km³
Neptune: 62,524,643,425,230.70 km³
```

**What's new — explained:**

| Code | What it does |
|---|---|
| `planets = [...]` | A list of names, one per planet, in the same order as the radii |
| `for i in range(len(planets))` | Loops 8 times; `i` goes 0 → 7 |
| `planets[i]` | Gets the planet name at position `i` |
| `volumes[i]` | Gets the volume at the same position `i` |
| `f"..."` | An **f-string** that lets you insert variables directly into text |
| `:,.2f` | Formats the number: commas for thousands, 2 decimal places |
| `km³` | Appends the unit (cubic kilometers) |

**A couple of tips:**
- You could also use `zip(planets, volumes)` to pair names with volumes — a cleaner alternative:
  ```python
  for planet, volume in zip(planets, volumes):
      print(f"{planet}: {volume:,.2f} km³")
  ```
- Notice how Jupiter's volume is over a **trillion times** larger than Mercury's — that's because volume scales with radius³ (cubed). Doubling the radius makes the volume 8× bigger!

Want me to also add the Earth-relative comparison (e.g., "Jupiter = 1,321 Earths")?