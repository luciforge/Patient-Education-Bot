import os
import json
import csv
import re
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Configuration
INPUT_JSON_PATH = "data/medlineplus/medical_kb_nephrology.json"
OUTPUT_DIR = "data/medlineplus"
MODEL_NAME = "cambridgeltl/SapBERT-from-PubMedBERT-fulltext"

def clean_text(text):
    """Remove HTML tags and normalize spacing"""
    text = re.sub(r"<[^>]+>", "", text)  # strip HTML
    return text.strip().lower()

def load_knowledge_base(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    terms, definitions, sources = [], [], []
    for entry in data:
        terms.append(entry["term"].strip().lower())
        definitions.append(clean_text(entry["definition"]))
        sources.append(entry["source"])
    return terms, definitions, sources

def embed_texts(texts, model_name=MODEL_NAME):
    model = SentenceTransformer(model_name)
    return model.encode(texts, convert_to_numpy=True)

def save_faiss_index(embeddings, output_path):
    dimension = embeddings.shape[1]
    index = faiss.IndexIDMap(faiss.IndexFlatL2(dimension))
    ids = np.arange(len(embeddings))
    index.add_with_ids(embeddings, ids)
    faiss.write_index(index, os.path.join(output_path, 'nephrology_faiss.index'))

def save_metadata_csv(terms, definitions, sources, output_path):
    csv_path = os.path.join(output_path, 'nephrology_metadata.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'term', 'definition', 'source'])
        for i, (term, definition, source) in enumerate(zip(terms, definitions, sources)):
            writer.writerow([i, term, definition, source])

def save_metadata_json(terms, definitions, sources, output_path):
    json_path = os.path.join(output_path, 'nephrology_kb_lookup.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump([
            {"id": i, "term": term, "definition": definition, "source": source}
            for i, (term, definition, source) in enumerate(zip(terms, definitions, sources))
        ], f, indent=2, ensure_ascii=False)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load and clean
    terms, definitions, sources = load_knowledge_base(INPUT_JSON_PATH)
    texts = [f"{term}: {definition}" for term, definition in zip(terms, definitions)]

    # Embed
    embeddings = embed_texts(texts)

    # Save
    save_faiss_index(embeddings, OUTPUT_DIR)
    save_metadata_csv(terms, definitions, sources, OUTPUT_DIR)
    save_metadata_json(terms, definitions, sources, OUTPUT_DIR)

    print(f"Embedded {len(terms)} terms and saved FAISS index + metadata to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
