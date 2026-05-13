import cv2
import numpy as np
import os

INPUT_PATH = "output/preprocessed.jpg"
ORIGINAL_PATH = "input/test.jpg"

os.makedirs("debug", exist_ok=True)
os.makedirs("cells", exist_ok=True)


def save(name, img):
    cv2.imwrite(f"debug/{name}", img)


binary = cv2.imread(INPUT_PATH, cv2.IMREAD_GRAYSCALE)
original = cv2.imread(ORIGINAL_PATH)

if binary is None:
    raise FileNotFoundError("output/preprocessed.jpg not found")

if original is None:
    raise FileNotFoundError("input/test.jpg not found")


# horizontal
horizontal_kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (40, 1)
)

horizontal = cv2.morphologyEx(
    binary,
    cv2.MORPH_OPEN,
    horizontal_kernel
)

save("06_horizontal.jpg", horizontal)


# vertical (balanced)
vertical_kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (1, 35)
)

vertical = cv2.morphologyEx(
    binary,
    cv2.MORPH_OPEN,
    vertical_kernel
)

# connect broken faint lines
vertical = cv2.dilate(
    vertical,
    cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5)),
    iterations=1
)

save("07_vertical.jpg", vertical)


# intersections
intersections = cv2.bitwise_and(horizontal, vertical)
save("08_intersections.jpg", intersections)


# visualization
grid = original.copy()

h_contours, _ = cv2.findContours(
    horizontal,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

for cnt in h_contours:
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.line(grid, (x, y), (x + w, y), (255, 0, 0), 1)

v_contours, _ = cv2.findContours(
    vertical,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

for cnt in v_contours:
    x, y, w, h = cv2.boundingRect(cnt)

    # reject tiny pen marks
    if h < 25:
        continue

    cv2.line(grid, (x, y), (x, y + h), (0, 255, 0), 1)

save("09_grid_lines.jpg", grid)


# cell extraction
table_mask = cv2.add(horizontal, vertical)

contours, _ = cv2.findContours(
    table_mask,
    cv2.RETR_TREE,
    cv2.CHAIN_APPROX_SIMPLE
)

cell_id = 0

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)

    if w < 20 or h < 15:
        continue

    if w > 500 or h > 200:
        continue

    cell = original[y:y+h, x:x+w]
    cv2.imwrite(f"cells/cell_{cell_id}.png", cell)
    cell_id += 1

print(f"Extracted {cell_id} cells")