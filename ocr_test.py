import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

img = Image.open("cells/cell_106.png")

text = pytesseract.image_to_string(
    img,
    lang="kan",
    config="--psm 7"
)

print(text)