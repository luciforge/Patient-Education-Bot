import os
import json
import faiss
import numpy as np
import re
import requests
from sentence_transformers import SentenceTransformer

#Config
API_KEY = "YOUR_API_KEY" 
MODEL_NAME = "models/gemini-2.0-flash"
INDEX_PATH = "data/medlineplus/nephrology_faiss.index"
LOOKUP_JSON = "data/medlineplus/nephrology_kb_lookup.json"
EMBED_MODEL = "cambridgeltl/SapBERT-from-PubMedBERT-fulltext"
TOP_K = 5
SIMILARITY_THRESHOLD = 250  # Lower = more similar (distance, not cosine)

API_URL = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:generateContent?key={API_KEY}"

#Load Models and Index
embedder = SentenceTransformer(EMBED_MODEL)
index = faiss.read_index(INDEX_PATH)

with open(LOOKUP_JSON, 'r', encoding='utf-8') as f:
    metadata = json.load(f)

#Input Normalization
def normalize_input(text):
    # Extracts lab terms like "GFR 45" or "Creatinine 2.0"
    lab_matches = re.findall(r"([a-zA-Z ]+?)\s*(\d+(\.\d+)?)", text)
    return text.strip(), lab_matches

#Embed Query
def embed_query(text):
    return embedder.encode([text], convert_to_numpy=True)

#Retrieve Context with Category Filtering and Threshold
def retrieve_context(query, k=TOP_K, category_filter="nephrology"):
    query_vec = embed_query(query)
    distances, ids = index.search(query_vec, k)

    print("\n[Debug] Retrieved distances and IDs:")
    context = []
    for idx, dist in zip(ids[0], distances[0]):
        if idx < len(metadata):
            entry = metadata[idx]
            entry_cat = entry.get("category", "").lower()

            print(f"→ ID {idx}, Distance: {round(dist, 4)}, Term: {entry['term']} | Category: {entry_cat}")

            # Check category match (if exists)
            if category_filter in entry_cat or entry_cat == "":
                context.append({
                    "text": f"{entry['term']}: {entry['definition']} (Source: {entry['source']})",
                    "score": dist
                })

    filtered = [ctx for ctx in context if ctx["score"] < SIMILARITY_THRESHOLD]

    if filtered:
        return sorted(filtered, key=lambda x: x["score"])
    else:
        print("[Debug] No contexts passed threshold — returning unfiltered top-K for fallback.")
        return sorted(context, key=lambda x: x["score"])

#Format Prompt
def build_prompt(user_input, context_list):
    context_str = "\n".join(
        f"- [{round(1 - ctx['score'], 3)} confidence] {ctx['text']}"
        for ctx in context_list
    )

    prompt = f"""
You are a trusted clinical assistant. Your job is to explain medical terms or lab results related to kidney health to patients.

Instructions:
1. Use the provided context as your primary source of information.
2. If the context is insufficient, you may also use your general medical knowledge to explain the concept or lab value.
3. If the input includes a lab value (e.g., "Creatinine 2.0", "GFR 45"), provide general interpretation ranges and what such a result could typically suggest.
4. Clearly explain that lab interpretation depends on the patient’s full clinical context, but give useful guidance when appropriate.
5. Be specific, use plain language, cite sources, and provide a confidence level (High / Medium / Low).
6. Do not give medical advice or a diagnosis — only interpret the meaning of terms or values as educational guidance.

USER INPUT:
\"{user_input}\"

RELEVANT CONTEXT:
{context_str}

Example:

Input: "My GFR is 45"
Explanation: A GFR of 45 typically suggests moderate to severe kidney impairment. This could indicate Stage 3b chronic kidney disease...
Sources: MedlinePlus - Kidney Tests, CKD
Confidence: Medium

FORMAT:
- Explanation:
- Sources:
- Confidence:
"""
    return prompt.strip()

#Gemini API Call
def call_gemini_api(prompt):
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(API_URL, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Gemini API Error {response.status_code}: {response.text}")
    
    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise ValueError("Invalid response from Gemini API")

#Main Function
def explain_medical_term(user_input):
    clean_input, _ = normalize_input(user_input)
    context = retrieve_context(clean_input)

    if not context:
        raise ValueError("No relevant context found. Try rephrasing your input.")

    prompt = build_prompt(clean_input, context)
    explanation = call_gemini_api(prompt)
    return {
        "input": clean_input,
        "explanation": explanation,
        "context_used": [ctx["text"] for ctx in context],
        "model": MODEL_NAME
    }

if __name__ == "__main__":
    query = input("Enter a medical term or lab result: ")
    try:
        result = explain_medical_term(query)
        print("\n--- Explanation ---")
        print(result["explanation"])
        print("\n--- Sources (via context) ---")
        for item in result["context_used"]:
            print(item)
    except Exception as e:
        print(f"Error: {e}")
