import cv2
import numpy as np
import json
import os

INPUT_BINARY = "output/preprocessed.jpg"
INPUT_ORIGINAL = "input/test.jpg"

os.makedirs("output", exist_ok=True)
os.makedirs("debug", exist_ok=True)

binary = cv2.imread(INPUT_BINARY, cv2.IMREAD_GRAYSCALE)
original = cv2.imread(INPUT_ORIGINAL)

if binary is None:
    raise FileNotFoundError("output/preprocessed.jpg not found")

if original is None:
    raise FileNotFoundError("input/test.jpg not found")

# ==========================================
# HORIZONTAL LINES
# ==========================================

horizontal_kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (40, 1)
)

horizontal = cv2.morphologyEx(
    binary,
    cv2.MORPH_OPEN,
    horizontal_kernel
)

cv2.imwrite(
    "debug/06_horizontal.jpg",
    horizontal
)

# ==========================================
# VERTICAL LINES
# ==========================================

vertical_kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (1, 35)
)

vertical = cv2.morphologyEx(
    binary,
    cv2.MORPH_OPEN,
    vertical_kernel
)

vertical = cv2.dilate(
    vertical,
    cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (1, 5)
    ),
    iterations=1
)

cv2.imwrite(
    "debug/07_vertical.jpg",
    vertical
)

# ==========================================
# FIND HORIZONTAL POSITIONS
# ==========================================

h_contours, _ = cv2.findContours(
    horizontal,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

rows = []

for cnt in h_contours:

    x, y, w, h = cv2.boundingRect(cnt)

    if w > 300:
        rows.append(y)

rows = sorted(rows)

filtered_rows = []

for y in rows:

    if (
        len(filtered_rows) == 0
        or abs(y - filtered_rows[-1]) > 8
    ):
        filtered_rows.append(y)

rows = filtered_rows

# ==========================================
# FIND VERTICAL POSITIONS
# ==========================================

v_contours, _ = cv2.findContours(
    vertical,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

columns = []

for cnt in v_contours:

    x, y, w, h = cv2.boundingRect(cnt)

    if h > 120:
        columns.append(x)

columns = sorted(columns)

filtered_columns = []

for x in columns:

    if (
        len(filtered_columns) == 0
        or abs(x - filtered_columns[-1]) > 8
    ):
        filtered_columns.append(x)

columns = filtered_columns

# ==========================================
# SAVE GRID
# ==========================================

grid = {
    "rows": rows,
    "columns": columns
}

with open(
    "output/grid.json",
    "w"
) as f:
    json.dump(
        grid,
        f,
        indent=4
    )

# ==========================================
# DEBUG OVERLAY
# ==========================================

overlay = original.copy()

for y in rows:

    cv2.line(
        overlay,
        (0, y),
        (overlay.shape[1], y),
        (255, 0, 0),
        2
    )

for x in columns:

    cv2.line(
        overlay,
        (x, 0),
        (x, overlay.shape[0]),
        (0, 255, 0),
        2
    )

cv2.imwrite(
    "debug/09_grid_lines.jpg",
    overlay
)

# ==========================================
# PRINT RESULTS
# ==========================================

print("\nDetected rows:\n")

for i, y in enumerate(rows):
    print(f"Row {i+1}: y={y}")

print("\nDetected columns:\n")

for i, x in enumerate(columns):
    print(f"Column {i+1}: x={x}")

print("\nTotal rows:", len(rows))
print("Total columns:", len(columns))

print("\nSaved:")
print("output/grid.json")
print("debug/09_grid_lines.jpg")