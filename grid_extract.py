import cv2
import numpy as np
import os

INPUT = "input/test.jpg"
OUTPUT = "final_output"

os.makedirs(OUTPUT, exist_ok=True)

# =========================
# LOAD IMAGE
# =========================

img = cv2.imread(INPUT)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Contrast improvement
gray = cv2.createCLAHE(
    clipLimit=2.0,
    tileGridSize=(8, 8)
).apply(gray)

# =========================
# BINARIZE
# =========================

binary = cv2.adaptiveThreshold(
    gray,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    21,
    10
)

# Save
cv2.imwrite(f"{OUTPUT}/01_binary.jpg", binary)

# =========================
# HORIZONTAL LINE DETECTION
# =========================

h_kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (120, 1)
)

horizontal = cv2.morphologyEx(
    binary,
    cv2.MORPH_OPEN,
    h_kernel,
    iterations=2
)

cv2.imwrite(f"{OUTPUT}/02_horizontal.jpg", horizontal)

# =========================
# VERTICAL LINE DETECTION
# =========================

v_kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (1, 80)
)

vertical = cv2.morphologyEx(
    binary,
    cv2.MORPH_OPEN,
    v_kernel,
    iterations=2
)

cv2.imwrite(f"{OUTPUT}/03_vertical.jpg", vertical)

contours_v, _ = cv2.findContours(
    vertical,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

vertical_positions = []

for c in contours_v:

    x, y, w, h = cv2.boundingRect(c)

    if h > 150:
        vertical_positions.append(x)

vertical_positions = sorted(vertical_positions)

# remove duplicates
filtered_v = []

for x in vertical_positions:
    if not filtered_v or abs(x - filtered_v[-1]) > 12:
        filtered_v.append(x)

vertical_positions = filtered_v

# =========================
# HORIZONTAL POSITIONS
# =========================

contours, _ = cv2.findContours(
    horizontal,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

horizontal_positions = []

for c in contours:

    x, y, w, h = cv2.boundingRect(c)

    if w > 200:
        horizontal_positions.append(y)

horizontal_positions = sorted(horizontal_positions)

# Remove near duplicates
filtered_h = []

for y in horizontal_positions:

    if not filtered_h or abs(y - filtered_h[-1]) > 10:
        filtered_h.append(y)

horizontal_positions = filtered_h

# =========================
# DRAW GRID
# =========================

overlay = img.copy()

# Draw horizontal lines
for y in horizontal_positions:

    cv2.line(
        overlay,
        (0, y),
        (img.shape[1], y),
        (255, 0, 0),
        2
    )

# Draw vertical lines
for x in vertical_positions:

    cv2.line(
        overlay,
        (x, 0),
        (x, img.shape[0]),
        (0, 255, 0),
        2
    )

cv2.imwrite(f"{OUTPUT}/04_grid_overlay.jpg", overlay)

# =========================
# CELL EXTRACTION
# =========================

cells_dir = f"{OUTPUT}/cells"
os.makedirs(cells_dir, exist_ok=True)

count = 0

for i in range(len(horizontal_positions) - 1):

    y1 = horizontal_positions[i]
    y2 = horizontal_positions[i + 1]

    if y2 - y1 < 20:
        continue

    for j in range(len(vertical_positions) - 1):

        x1 = vertical_positions[j]
        x2 = vertical_positions[j + 1]

        if x2 - x1 < 15:
            continue

        cell = img[y1:y2, x1:x2]

        if cell.size == 0:
            continue

        cv2.imwrite(
            f"{cells_dir}/cell_{i}_{j}.jpg",
            cell
        )

        count += 1

print("Cells extracted:", count)
print("DONE")