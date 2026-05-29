from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_angle_cls=False,
    lang="en"
)

print("Paddle loaded successfully")