import json, os

def write_output_json(title, headings, images, out_path):
    combined = headings + images
    combined = sorted(combined, key=lambda x: (x['page'], x['level']))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    json.dump({"title": title, "outline": combined}, open(out_path, "w", encoding="utf-8"), indent=2)
