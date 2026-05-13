import cv2
import numpy as np
import os

INPUT_PATH = "input/test.jpg"

os.makedirs("output", exist_ok=True)
os.makedirs("debug", exist_ok=True)


def save(name, img):
    cv2.imwrite(f"debug/{name}", img)


img = cv2.imread(INPUT_PATH)

if img is None:
    raise FileNotFoundError("input/test.jpg not found")

save("01_original.jpg", img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# gentle denoise
gray = cv2.GaussianBlur(gray, (3, 3), 0)

# shadow removal without killing lines
bg = cv2.medianBlur(gray, 31)
shadow_removed = cv2.divide(gray, bg, scale=255)

save("02_shadow_removed.jpg", shadow_removed)

# adaptive threshold tuned for faint lines
binary = cv2.adaptiveThreshold(
    shadow_removed,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    31,
    8
)

save("03_binary.jpg", binary)

# light cleanup only
kernel = np.ones((2, 2), np.uint8)
clean = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

save("04_cleaned.jpg", clean)
cv2.imwrite("output/preprocessed.jpg", clean)

print("Preprocessing complete")