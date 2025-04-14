# 🧠 Patient Education Bot

A plain-language chatbot that explains lab results or medical terms — especially for kidney health — using retrieval-augmented generation (RAG) and Gemini API.

---

## 🚀 Features

- ✅ Explains terms like **"Creatinine 2.0"**, **"GFR 45"**, etc.
- 📂 Upload PDF/TXT lab reports and get breakdowns
- 🔗 Uses trusted sources (MedlinePlus)
- 📊 Confidence Score + Source Attribution
- 🌐 Runs offline with local embeddings
- 🛡️ Privacy-friendly: designed to run on personal laptops

---

## 🧱 Architecture

- **Embedding Model**: `cambridgeltl/SapBERT-from-PubMedBERT-fulltext`
- **Vector Store**: FAISS
- **LLM**: Gemini Pro (via API)
- **Frontend**: Gradio

---

## 💻 Setup

### 1. Clone Repo

```bash
git clone https://github.com/yourusername/patient-education-bot.git
cd patient-education-bot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Fill in your [Gemini API key](https://ai.google.dev/gemini-api/docs/quickstart) in `.env` file.

---

## 🧪 Run the App

### Terminal mode

```bash
python scripts/gradio_ui.py
```

### Or for PDF upload:

```bash
python scripts/gradio_pdf.py
```

---

## 📂 Directory Structure

```bash
PATIENT_EDUCATION_BOT/
├── data/                      # MedlinePlus KB and FAISS index
│   └── medlineplus/
├── scripts/                   # All processing + UI files
├── .env                       # API key
├── requirements.txt           # Dependencies
├── README.md
```

---

## 📜 License

MIT – Free to use and modify.

---

## 🙌 Author

Made with ❤️ to support AI for kidney health!