# NLP Desktop Search Engine — Inverted Index (50,000+ Files)

## Overview
A desktop keyword search engine built with Python that indexes **50,000+ local `.txt` files** and retrieves relevant documents using a classical inverted index. Supports Boolean, Count, and TF-IDF vector weighting with Dot Product and Cosine Similarity ranking.

---

## Project Structure

```
Project Search Engine/
├── Preprocessing.ipynb      # Main notebook — all steps in order
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── my_test_docs/            # Sample/corpus .txt files
│   ├── cricket.txt
│   ├── nlp.txt
│   ├── science/
│   ├── history/
│   └── ...
└── search_index/            # Persisted index files (auto-generated)
    ├── inverted_index.pkl
    ├── doc_maps.pkl
    ├── doc_freq.pkl
    └── doc_lengths.pkl
```

---

## How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Open the Notebook
```bash
jupyter notebook Preprocessing.ipynb
```

### 3. Run Cells in Order

| Step | Cell | Action |
|------|------|--------|
| 1 | Imports & Config | Sets up paths and `build_file_registry()` |
| 2 | Sample Data | Creates 100 sample `.txt` files + 50k generator |
| 3 | Preprocessing | `preprocess_text()` — lowercase, tokenize, clean |
| 4 | Verification | Displays DocID → file path table |
| 5 | Inverted Index | `build_inverted_index()` |
| 6 | Persistence | Save/load index with `pickle` |
| 7 | Vector Variants | Boolean, Count, TF-IDF weights |
| 8 | Similarity | Dot Product & Cosine Similarity |
| 9 | Query Engine | `search(query, mode, similarity, top_k)` |
| 10 | Bonus | Phrase & Proximity queries |

---

## Features

### Vector Variants
| Mode | Formula |
|------|---------|
| Boolean | `w = 1` if term present, else `0` |
| Count | `w = tf(t, d)` — raw term frequency |
| TF-IDF | `w = tf(t,d) × (log((N+1)/(df+1)) + 1)` |

### Similarity Measures
| Measure | Formula |
|---------|---------|
| Dot Product | `score = Σ w(t,d) × w(t,q)` |
| Cosine Similarity | `score = Σ w(t,d)×w(t,q) / (‖d‖ × ‖q‖)` |

### Query Examples
```python
# Standard keyword search
search("cricket Pakistan", mode="tfidf", similarity="cosine", top_k=10)
search("machine learning python", mode="count", similarity="dot")
search("university education", mode="boolean", similarity="cosine")

# Bonus: Phrase Query (exact match)
phrase_query("Punjab University", positional_index, id_to_path_map)

# Bonus: Proximity Query (within k words)
proximity_query("Pakistan", "cricket", window=5, pos_idx=positional_index, id_to_path_map=id_to_path_map)
```

---

## Index Persistence
The index is automatically saved to `./search_index/` after building.  
To reload without rebuilding:
```python
load_index()  # loads all 4 pickle files instantly
```

---

## Requirements
- Python 3.8+
- No external NLP libraries required (pure Python stdlib)
- Optional: `nltk` for stopword removal / stemming

---

## Grading Coverage

| Requirement | Status |
|-------------|--------|
| 50,000+ files indexed | ✅ |
| Recursive file discovery | ✅ |
| Preprocessing pipeline | ✅ |
| Inverted index + postings | ✅ |
| Index saved & reloadable | ✅ |
| Boolean / Count / TF-IDF vectors | ✅ |
| Dot Product + Cosine Similarity | ✅ |
| Top-k ranked retrieval | ✅ |
| Phrase queries (Bonus) | ✅ |
| Proximity queries (Bonus) | ✅ |

---

## Author
NLP Lab Assignment — Desktop Search Engine  
Date: March 2026
