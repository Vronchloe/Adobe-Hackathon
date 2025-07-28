from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer, util
import torch
import os

# Offline path to the model folder (make sure all files are there)
MODEL_PATH = "./tinyllama_model"

# Option 1: Using SentenceTransformer-compatible version (preferred for semantic ranking)
try:
    model = SentenceTransformer(MODEL_PATH)
except Exception as e:
    print(f"[INFO] SentenceTransformer fallback failed: {e}")
    print("[INFO] Using manual tokenizer and encoder...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model_raw = AutoModel.from_pretrained(MODEL_PATH)

    def encode(texts):
        with torch.no_grad():
            inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
            outputs = model_raw(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)  # Mean pooling
            return embeddings

else:
    def encode(texts):
        return model.encode(texts, convert_to_tensor=True)

# Main ranking function
def rank_pages_by_relevance(pages, persona, job_to_be_done, top_k=5):
    context = f"{persona}. Task: {job_to_be_done}"
    query_embedding = encode([context])[0]

    ranked = []
    for page in pages:
        combined_text = (page.get("text") or "") + "\n" + (page.get("ocr_text") or "")
        if combined_text.strip():
            page_embedding = encode([combined_text])[0]
            score = util.pytorch_cos_sim(query_embedding, page_embedding).item()
            ranked.append({
                "page_number": page["page_number"],
                "score": round(score, 4),
                "section_title": combined_text[:100].strip().replace("\n", " ")
            })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked[:top_k]
