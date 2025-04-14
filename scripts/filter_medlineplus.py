import json

# Load the existing KB
with open(r"data\medlineplus\medical_kb.json", "r", encoding="utf-8") as f:
    kb = json.load(f)

# Define nephrology-specific keywords and categories
nephrology_keywords = [
    "kidney", "renal", "nephro", "gfr", "bun", "creatinine", "dialysis", "glomerular",
    "albumin", "electrolyte", "urine", "phosphorus", "potassium", "calcium", "acidosis", "esrd", "ckd"
]

# Function to check if an entry is nephrology-related
def is_nephrology_related(entry):
    text = f"{entry['term']} {entry['definition']}".lower()
    return any(kw in text for kw in nephrology_keywords)

# Filter KB entries
nephrology_kb = [entry for entry in kb if is_nephrology_related(entry)]

# Save filtered KB to new file
with open("medical_kb_nephrology.json", "w", encoding="utf-8") as f:
    json.dump(nephrology_kb, f, indent=2, ensure_ascii=False)

print(f"Filtered KB contains {len(nephrology_kb)} nephrology-related entries.")
