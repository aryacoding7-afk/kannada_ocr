import os
import json
from PIL import Image
from paddleocr import PaddleOCR
import pytesseract

# ---------------------------------
# TESSERACT SETUP
# ---------------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# ---------------------------------
# PADDLE OCR SETUP
# ---------------------------------

paddle = PaddleOCR(
    use_angle_cls=False,
    lang="en"
)

# ---------------------------------
# TABLE CONFIGURATION
# ---------------------------------

# Student name column
NAME_COLUMNS = [1]

# Header rows
HEADER_ROWS = [0, 1, 2]

# ---------------------------------
# OCR FUNCTIONS
# ---------------------------------

def paddle_read(image_path):
    try:
        result = paddle.ocr(image_path)

        if not result:
            return ""

        if not result[0]:
            return ""

        return result[0][0][1][0].strip()

    except Exception:
        return ""


def tesseract_read(image_path):
    try:
        img = Image.open(image_path)

        text = pytesseract.image_to_string(
            img,
            lang="kan+eng",
            config="--psm 6"
        )

        return text.strip()

    except Exception:
        return ""


def read_cell(image_path, row, column):

    # Header rows
    if row in HEADER_ROWS:
        return tesseract_read(image_path)

    # Student names
    if column in NAME_COLUMNS:
        return tesseract_read(image_path)

    # Numeric columns
    return paddle_read(image_path)


# ---------------------------------
# LOAD CELL POSITIONS
# ---------------------------------

with open(
    "output/cell_positions.json",
    "r",
    encoding="utf-8"
) as f:

    cells = json.load(f)

# ---------------------------------
# OCR ALL CELLS
# ---------------------------------

results = []

total_cells = len(cells)

for index, cell in enumerate(cells):

    filename = cell["filename"]

    image_path = os.path.join(
        "cells",
        filename
    )

    row = cell["row"]
    column = cell["column"]

    text = read_cell(
        image_path,
        row,
        column
    )

    cell["text"] = text

    results.append(cell)

    print(
        f"[{index + 1}/{total_cells}] "
        f"R{row} C{column} -> {text}"
    )

# ---------------------------------
# SAVE RESULTS
# ---------------------------------

os.makedirs("output", exist_ok=True)

with open(
    "output/ocr_results.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        results,
        f,
        ensure_ascii=False,
        indent=2
    )

print()
print("=" * 50)
print("OCR COMPLETE")
print("Saved: output/ocr_results.json")
print("=" * 50)