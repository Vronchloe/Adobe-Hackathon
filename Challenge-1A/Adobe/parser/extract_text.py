import pdfplumber

def extract_text_elements(pdf_path):
    elements = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            lines = page.extract_text(layout=True, x_tolerance=3, y_tolerance=3)
            if not lines:
                continue
            for block in lines.split('\n'):
                words = block.strip().split()
                if not words:
                    continue
                text = ' '.join(words)
                char_details = page.chars
                relevant_chars = [c for c in char_details if c['text'].strip() in words]
                size = max([round(c.get('size', 12), 1) for c in relevant_chars], default=12)
                bold = 1 if any('Bold' in c.get('fontname', '') for c in relevant_chars) else 0
                y0 = min([c['top'] for c in relevant_chars], default=0)

                elements.append({
                    "text": text,
                    "size": size,
                    "bold": bold,
                    "y0": round(y0, 2),
                    "page": page_num + 1
                })
    return elements