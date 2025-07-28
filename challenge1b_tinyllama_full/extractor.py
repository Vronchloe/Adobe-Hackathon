import fitz
from PIL import Image
import pytesseract
import io

def extract_text_and_images(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        images = page.get_images(full=True)
        ocr = []
        for img in images:
            base_img = doc.extract_image(img[0])
            image = Image.open(io.BytesIO(base_img["image"]))
            ocr.append(pytesseract.image_to_string(image))
        pages.append({
            "page_number": i+1,
            "text": page.get_text(),
            "ocr_text": "\n".join(ocr)
        })
    return pages