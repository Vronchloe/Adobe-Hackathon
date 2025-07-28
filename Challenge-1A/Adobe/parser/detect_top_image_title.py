from pdf2image import convert_from_path
import pytesseract
from PIL import Image, ImageOps
import re

def detect_top_image_title(pdf_path):
    try:
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        img = images[0]
        w, h = img.size
        crop_area = (w*0.1, 0, w*0.9, h*0.3)
        cropped = img.crop(crop_area).convert("L")
        enhanced = ImageOps.invert(cropped.resize((cropped.width*2, cropped.height*2)))
        text = pytesseract.image_to_string(enhanced).strip()
        for line in text.split("\n"):
            clean = re.sub(r"[^A-Za-z0-9: ]+", "", line).strip()
            if len(clean.split()) <= 10 and len(clean) >= 4:
                return {"level": "H1", "text": clean, "page": 1}
    except Exception as e:
        print("OCR Title detection failed:", e)
    return None