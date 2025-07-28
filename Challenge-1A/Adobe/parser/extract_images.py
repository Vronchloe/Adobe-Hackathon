import fitz  # PyMuPDF

def extract_image_titles(pdf_path):
    titles = []
    doc = fitz.open(pdf_path)
    for page_number in range(len(doc)):
        page = doc[page_number]
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for line in b["lines"]:
                    for span in line["spans"]:
                        if "figure" in span["text"].lower():
                            titles.append({
                                "level": "ImageTitle",
                                "text": span["text"],
                                "page": page_number + 1
                            })
    return titles
