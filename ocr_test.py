# ocr_test.py

from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

img = Image.open("cells/cell_100.png")

text = pytesseract.image_to_string(
    img,
    config="--psm 7"
)

print(repr(text))