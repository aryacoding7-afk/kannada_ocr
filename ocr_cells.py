import os
import json
from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

NAME_COLUMNS = [1]


def read_cell(image_path):

    try:
        img = Image.open(image_path)

        text = pytesseract.image_to_string(
            img,
            lang="kan+eng",
            config="--psm 7"
        )

        return text.strip()

    except:
        return ""


def translate_kannada(text):

    if not text.strip():
        return ""

    try:
        return GoogleTranslator(
            source="kn",
            target="en"
        ).translate(text)

    except:
        return text


with open(
    "output/cell_positions.json",
    "r",
    encoding="utf-8"
) as f:

    cells = json.load(f)

results = []

for cell in cells:

    image_path = os.path.join(
        "cells",
        cell["filename"]
    )

    text = read_cell(image_path)

    if cell["column"] in NAME_COLUMNS:

        translated = translate_kannada(text)

        cell["kannada_text"] = text
        cell["english_text"] = translated
        cell["text"] = translated

        print(
            f"Name: {text} -> {translated}"
        )

    else:

        cell["text"] = text

    results.append(cell)

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

print("Saved output/ocr_results.json")