import cv2
import json
import os

IMAGE_PATH = "input/test.jpg"

os.makedirs("cells", exist_ok=True)

image = cv2.imread(IMAGE_PATH)

if image is None:
    raise FileNotFoundError(
        "input/test.jpg not found"
    )

with open(
    "output/grid.json",
    "r"
) as f:
    grid = json.load(f)

rows = grid["rows"]
cols = grid["columns"]

cell_data = []

cell_id = 0

for r in range(len(rows) - 1):

    y1 = rows[r]
    y2 = rows[r + 1]

    if y2 - y1 < 10:
        continue

    for c in range(len(cols) - 1):

        x1 = cols[c]
        x2 = cols[c + 1]

        if x2 - x1 < 10:
            continue

        cell = image[
            y1:y2,
            x1:x2
        ]

        if cell.size == 0:
            continue

        filename = (
            f"cell_{cell_id}.png"
        )

        cv2.imwrite(
            f"cells/{filename}",
            cell
        )

        cell_data.append({
            "id": cell_id,
            "filename": filename,
            "row": r,
            "column": c,
            "x": x1,
            "y": y1,
            "w": x2 - x1,
            "h": y2 - y1
        })

        cell_id += 1

with open(
    "output/cell_positions.json",
    "w"
) as f:

    json.dump(
        cell_data,
        f,
        indent=4
    )

print()
print(
    f"Extracted {cell_id} cells"
)
print(
    "Saved output/cell_positions.json"
)