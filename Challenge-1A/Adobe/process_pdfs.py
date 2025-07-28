import os
from parser.extract_text import extract_text_elements
from parser.classify_headings import classify_headings
from parser.detect_top_image_title import detect_top_image_title
from parser.json_writer import write_output_json

PDF_FOLDER = "sample_dataset/pdfs"
OUT_FOLDER = "sample_dataset/outputs"

def process_pdf(pdf_path, output_path):
    print("\n📄", os.path.basename(pdf_path))
    elements = extract_text_elements(pdf_path)
    headings, title = classify_headings(elements)
    ocr_title = detect_top_image_title(pdf_path)
    if ocr_title:
        headings.insert(0, ocr_title)
        if not title or title == "Untitled":
            title = ocr_title['text']
    write_output_json(title, headings, [], output_path)

def main():
    for file in os.listdir(PDF_FOLDER):
        if file.endswith(".pdf"):
            process_pdf(
                os.path.join(PDF_FOLDER, file),
                os.path.join(OUT_FOLDER, file.replace(".pdf", ".json"))
            )
    print("\n✅ Done")

if __name__ == "__main__":
    main()
