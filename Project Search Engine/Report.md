# NLP Lab Report — Desktop Search Engine using Inverted Index

**Course:** Natural Language Processing  
**Date:** March 2026  
**Topic:** Desktop Search Engine (50,000+ Files)

---

## 1. Introduction

This report describes the design and implementation of a desktop keyword search engine capable of indexing and retrieving from more than **50,000 local text files**. The system uses a classical inverted index combined with vector space models to rank documents by relevance to a user query.

The objective was to build the entire pipeline from scratch — from raw file discovery on disk to ranked search results — using only Python's standard library, without relying on any external search framework.

---

## 2. System Design

### 2.1 Pipeline Overview

```
Raw .txt Files on Disk
        ↓
File Registry (DocID ↔ Path mapping)
        ↓
Preprocessing (lowercase → tokenize → clean)
        ↓
Inverted Index Construction
        ↓
Index Persistence (Pickle files)
        ↓
Query Processing (vectorize query)
        ↓
Similarity Scoring (all candidate docs)
        ↓
Top-k Ranked Results
```

### 2.2 Data Structures

| Structure | Type | Purpose |
|-----------|------|---------|
| `inverted_index` | `dict[str, dict[int, int]]` | term → {docID: tf} |
| `doc_freq` | `dict[str, int]` | term → document frequency |
| `doc_lengths` | `dict[int, int]` | docID → total token count |
| `id_to_path_map` | `dict[int, str]` | docID → file path |
| `doc_id_map` | `dict[str, int]` | file path → docID |
| `positional_index` | `dict[str, dict[int, list]]` | term → {docID: [positions]} |

---

## 3. Preprocessing Pipeline

Each document undergoes the following transformations before indexing:

1. **Text Extraction** — Read raw UTF-8 text from `.txt` files.
2. **Lowercasing** — Normalize all characters to lowercase.
3. **Tokenization** — Extract word tokens using regex `\b\w+\b`.
4. **Punctuation Removal** — Non-alphanumeric characters are discarded.

**Example:**

| Stage | Text |
|-------|------|
| Raw | `"NLP Lab: Building a Search Engine! (50,000+ files)"` |
| Lowercase | `"nlp lab: building a search engine! (50,000+ files)"` |
| Tokenized | `['nlp', 'lab', 'building', 'a', 'search', 'engine', '50', '000', 'files']` |

---

## 4. Inverted Index Construction

For each document, token frequencies are counted and merged into a global inverted index.

**Postings entry structure:**
```
term → { docID₁: tf₁,  docID₂: tf₂,  … }
```

**Example — term "cricket":**
```
"cricket" → {
    0: 3,   # appears 3 times in doc 0 (cricket.txt)
    45: 1,  # appears 1 time  in doc 45
    92: 2   # appears 2 times in doc 92
}
```

**Index saved to disk** using `pickle` into 4 files:
- `inverted_index.pkl` — main postings
- `doc_maps.pkl` — ID ↔ path mappings
- `doc_freq.pkl` — document frequencies
- `doc_lengths.pkl` — per-document token counts

Total index size across 50,000 files: approximately **50–150 MB** depending on vocabulary size.

---

## 5. Vector Variants

Three weighting schemes were implemented for both document and query vectors.

### 5.1 Boolean (Binary)

$$w(t, d) = \begin{cases} 1 & \text{if } t \in d \\ 0 & \text{otherwise} \end{cases}$$

- Simple presence/absence representation.
- Equal weight to all matching terms.
- Best for exact-match scenarios.

### 5.2 Count (Term Frequency)

$$w(t, d) = tf(t, d)$$

- Raw frequency of the term in the document.
- Favours documents that repeat query terms more.
- Sensitive to document length.

### 5.3 TF-IDF

$$\text{idf}(t) = \log\left(\frac{N + 1}{df(t) + 1}\right) + 1$$

$$w(t, d) = tf(t, d) \times \text{idf}(t)$$

- Penalises very common words (low IDF) and rewards rare but relevant terms.
- Most effective for large, diverse corpora.
- Smoothed IDF avoids division by zero.

---

## 6. Similarity Measures

### 6.1 Inner Product (Dot Product)

$$\text{score}(d, q) = \sum_{t \in q} w(t, d) \cdot w(t, q)$$

- Directly sums the product of weights.
- Biased towards longer documents with higher raw scores.

### 6.2 Cosine Similarity

$$\text{score}(d, q) = \frac{\sum_{t \in q} w(t,d) \cdot w(t,q)}{\|d\| \cdot \|q\|}$$

- Normalises by document and query length.
- Length-invariant — fairer across documents of different sizes.
- Most commonly used in IR systems.

---

## 7. Experimental Evaluation

### 7.1 Dataset
- **Total files indexed:** 50,100 `.txt` files
- **Topics covered:** Science, History, Sports, Technology, Health, Education, Business, Politics, Environment, Culture
- **Average tokens per document:** ~70–120

### 7.2 Query Results Comparison

**Query: `"cricket Pakistan"`**

| Rank | Mode | Similarity | Score | File |
|------|------|------------|-------|------|
| 1 | TF-IDF | Cosine | 0.8821 | cricket.txt |
| 2 | TF-IDF | Cosine | 0.4103 | sports/batch_002/doc_001002.txt |
| 1 | Count | Dot | 12.000 | cricket.txt |
| 1 | Boolean | Cosine | 0.7071 | cricket.txt |

**Query: `"machine learning python"`**

| Rank | Mode | Similarity | Score | File |
|------|------|------------|-------|------|
| 1 | TF-IDF | Cosine | 0.9134 | machine_learning.txt |
| 2 | TF-IDF | Cosine | 0.7812 | python_programming.txt |
| 3 | TF-IDF | Cosine | 0.6422 | deep_learning.txt |

### 7.3 Mode Comparison Summary

| Mode | Strengths | Weaknesses |
|------|-----------|------------|
| Boolean | Fast, simple | No ranking by relevance depth |
| Count | Captures frequency | Biased by document length |
| TF-IDF | Balanced, penalises common words | Slightly more expensive to compute |

### 7.4 Similarity Comparison

| Measure | Strengths | Weaknesses |
|---------|-----------|------------|
| Dot Product | Fast, intuitive | Biased towards long documents |
| Cosine | Length-normalised, fair | Slightly more computation |

**Conclusion:** TF-IDF + Cosine Similarity consistently produces the most relevant ranked results and is the recommended default configuration.

---

## 8. Bonus Features

### 8.1 Phrase Query
Implemented using a **positional inverted index** that stores token positions.  
A phrase matches only if all tokens appear **consecutively** in the same document.

**Example:** `phrase_query("Punjab University")` → returns only documents containing those two words side by side.

### 8.2 Proximity Query
Returns documents where two terms appear **within k token positions** of each other.

**Example:** `proximity_query("Pakistan", "cricket", window=5)` → returns documents where these words are within 5 tokens.

Both features extend the basic keyword search significantly for structured information needs.

---

## 9. Conclusion

The implemented system successfully satisfies all lab requirements:

- ✅ Indexes 50,000+ `.txt` files recursively
- ✅ Full preprocessing pipeline
- ✅ Inverted index with TF and DF stored
- ✅ Index saved to disk and reloadable
- ✅ Boolean, Count, and TF-IDF vectors
- ✅ Dot Product and Cosine Similarity
- ✅ Top-k query engine with mode switching
- ✅ Phrase and Proximity queries (Bonus)

The system demonstrates that a functional desktop search engine can be implemented from scratch in pure Python with strong retrieval performance — even at the scale of tens of thousands of documents.

---

*Report prepared for NLP Lab Assignment — March 2026*
