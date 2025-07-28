import os, json, time
from extractor import extract_text_and_images
from ranker import rank_pages_by_relevance
from summarizer import summarize_text
import nltk
nltk.data.path.append("/app/nltk_data")

INPUT_JSON_DIR = "input_jsons"
INPUT_PDFS_DIR = "input_pdfs"
OUTPUT_DIR = "outputs"

def process_batch(input_json_file, pdf_subfolder):
    with open(input_json_file, "r") as f:
        schema = json.load(f)

    persona = schema["persona"]
    job = schema["job_to_be_done"]

    output = {
        "metadata": {
            "input_documents": [],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    pdf_folder = os.path.join(INPUT_PDFS_DIR, pdf_subfolder)
    for file in os.listdir(pdf_folder):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, file)
            pages = extract_text_and_images(pdf_path)
            top_sections = rank_pages_by_relevance(pages, persona, job)

            output["metadata"]["input_documents"].append(file)
            for section in top_sections:
                output["extracted_sections"].append({
                    "document": file,
                    "page_number": section["page_number"],
                    "section_title": section["section_title"],
                    "importance_rank": section["score"]
                })

                refined = summarize_text(section["section_title"])
                output["subsection_analysis"].append({
                    "document": file,
                    "page_number": section["page_number"],
                    "refined_text": refined
                })

    basename = os.path.splitext(os.path.basename(input_json_file))[0]
    output_file = os.path.join(OUTPUT_DIR, f"{basename}_output.json")
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for file in os.listdir(INPUT_JSON_DIR):
        if file.endswith(".json"):
            base = os.path.splitext(file)[0]
            pdf_subfolder = f"set_{base.split('_')[-1]}"  # e.g., input_1 → set_1
            print(f"Processing {file} with PDFs from {pdf_subfolder}")
            process_batch(os.path.join(INPUT_JSON_DIR, file), pdf_subfolder)

if __name__ == "__main__":
    main()
