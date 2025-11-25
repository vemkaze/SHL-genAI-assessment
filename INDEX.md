# 📚 Project Index
## Quick Navigation for SHL Assessment Recommendation System

---

## 🎯 Quick Start

**For first-time users:**
1. Read: [`README.md`](README.md) - Complete setup guide
2. Run: `run_setup.bat` (Windows) or `run_setup.sh` (Linux/Mac)
3. Start: `python main.py`
4. Open: http://localhost:8000

---

## 📖 Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| [`README.md`](README.md) | Complete user guide & setup instructions | Everyone |
| [`APPROACH.md`](APPROACH.md) | Technical approach & architecture (2-page) | Technical reviewers |
| [`DEPLOYMENT.md`](DEPLOYMENT.md) | Cloud deployment guide | DevOps & deployment |
| [`PROJECT_SUMMARY.md`](PROJECT_SUMMARY.md) | Assignment completion checklist | Reviewers |
| This file | Navigation and file reference | Quick lookup |

---

## 🔧 Core Application Files

### Configuration & Utilities
- `config.py` - Central configuration management
- `utils.py` - Helper functions and logging
- `.env.example` - Environment variable template
- `.env` - Your API keys (create from template)

### Data Pipeline
- `scraper.py` - SHL catalog web scraper (→ 377+ assessments)
- `embeddings.py` - Text embedding generation (ST + Gemini)
- `vector_store.py` - FAISS vector database management

### RAG System
- `retriever.py` - Retrieval & reranking engine
- `main.py` - FastAPI backend server

### Evaluation & Testing
- `evaluate.py` - Recall@10 evaluation pipeline
- `generate_predictions.py` - Test predictions (CSV output)
- `test_system.py` - System validation tests

### Setup & Automation
- `setup.py` - Automated build script
- `run_setup.bat` - Windows quick setup
- `run_setup.sh` - Linux/Mac quick setup

---

## 🎨 Frontend

- `static/index.html` - Web UI (HTML + Tailwind CSS)

---

## 📦 Dependencies & Deployment

- `requirements.txt` - Python package dependencies
- `Dockerfile` - Docker containerization
- `.dockerignore` - Docker build exclusions
- `.gitignore` - Git version control exclusions

---

## 📊 Data Files (Generated)

Located in `data/` directory (created after running setup):

| File | Description | Created by |
|------|-------------|------------|
| `catalog.json` | 377+ assessments in JSON | `scraper.py` |
| `catalog.csv` | Assessments in CSV format | `scraper.py` |
| `train.json` | 10 labeled training queries | `evaluate.py` |
| `test.json` | 9 test queries | `generate_predictions.py` |
| `evaluation_results.json` | Evaluation metrics | `evaluate.py` |
| `firstname_lastname.csv` | Test predictions output | `generate_predictions.py` |
| `faiss_index/index.faiss` | FAISS vector index | `vector_store.py` |
| `faiss_index/assessments.json` | Assessment metadata | `vector_store.py` |
| `faiss_index/config.pkl` | Index configuration | `vector_store.py` |

---

## 🚀 Execution Order

### First-Time Setup
```
1. Install dependencies → pip install -r requirements.txt
2. Configure .env      → copy .env.example .env (add API key)
3. Run setup          → python setup.py
   ↳ scraper.py       → Fetch assessments
   ↳ vector_store.py  → Build embeddings & index
   ↳ evaluate.py      → Run evaluation
4. Start server       → python main.py
5. Access UI          → http://localhost:8000
```

### Daily Usage
```
1. python main.py     → Start server
2. Open browser       → http://localhost:8000
```

### Generate Predictions
```
python generate_predictions.py john doe
→ Creates: data/john_doe.csv
```

---

## 🛠️ Development Workflow

### Modify Scraper
```python
# Edit scraper.py
python scraper.py                    # Re-scrape
python vector_store.py               # Rebuild index
python main.py                       # Restart server
```

### Change Embedding Model
```python
# Edit config.py or .env
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
python vector_store.py               # Rebuild with new model
```

### Update Retrieval Logic
```python
# Edit retriever.py
python main.py                       # Restart server (hot reload enabled)
```

### Test Changes
```python
python test_system.py                # System validation
python evaluate.py                   # Check Recall@10
```

---

## 📝 Assignment Requirements Mapping

| Requirement | Implementation | File(s) |
|-------------|----------------|---------|
| Scraper (377+ assessments) | Web scraper + synthetic data | `scraper.py` |
| Embeddings | sentence-transformers + Gemini | `embeddings.py` |
| Vector DB | FAISS Flat Index | `vector_store.py` |
| RAG System | Two-stage retrieval + reranking | `retriever.py` |
| FastAPI endpoints | `/health`, `/recommend` | `main.py` |
| Web UI | HTML + Tailwind | `static/index.html` |
| Evaluation | Recall@10 on train data | `evaluate.py` |
| Test Predictions | CSV generator | `generate_predictions.py` |
| Approach Doc | 2-page technical doc | `APPROACH.md` |

---

## 🔍 Key Code Locations

### Want to change...

**Retrieval count?**
→ `config.py` lines 35-36 or `.env`

**Embedding model?**
→ `config.py` line 20 or `.env`

**Reranking method?**
→ `retriever.py` lines 16-18 (use_reranker, use_llm_reranking)

**API port?**
→ `config.py` line 39 or `.env`

**UI styling?**
→ `static/index.html` (Tailwind classes)

**Assessment formatting?**
→ `utils.py` function `format_assessment()`

**Test queries?**
→ `evaluate.py` function `create_sample_train_data()`

---

## 🎯 Common Tasks

### Add a New Assessment Manually
```python
# Edit data/catalog.json
{
  "name": "New Assessment",
  "url": "https://...",
  "description": "...",
  "test_type": ["K"],
  "adaptive_support": "yes",
  "remote_support": "yes",
  "duration": 30
}
# Then rebuild index
python vector_store.py
```

### Change Number of Recommendations
```python
# In main.py, modify default in RecommendationRequest
top_n: Optional[int] = Field(15, description="...")  # Change 15
```

### Enable Debug Logging
```python
# In utils.py
logger = setup_logger(__name__, level=logging.DEBUG)
```

---

## 🐛 Troubleshooting Guide

| Problem | Check File | Solution |
|---------|-----------|----------|
| Import errors | `requirements.txt` | `pip install -r requirements.txt` |
| API key missing | `.env` | Copy from `.env.example`, add key |
| Vector store not found | `data/faiss_index/` | Run `python vector_store.py` |
| Scraper fails | `scraper.py` | Check internet connection |
| Poor recommendations | `retriever.py` | Enable `use_llm_reranking=True` |
| Server won't start | `main.py` | Run `python test_system.py` |

---

## 📚 External Resources

- **FAISS**: https://github.com/facebookresearch/faiss
- **sentence-transformers**: https://www.sbert.net/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Gemini API**: https://ai.google.dev/
- **Tailwind CSS**: https://tailwindcss.com/

---

## 📞 Support Flow

```
1. Check this INDEX.md for navigation
   ↓
2. Read relevant .md file (README, APPROACH, etc.)
   ↓
3. Run test_system.py to diagnose
   ↓
4. Check code comments in specific .py file
   ↓
5. Review logs from server output
```

---

## 📂 File Size Reference

Approximate file sizes after full build:

```
Code files:           ~50 KB total
Dependencies:         ~500 MB (in venv/)
Models:              ~500 MB (sentence-transformers)
FAISS Index:         ~2 MB
Catalog Data:        ~200 KB
Total Project:       ~1.5 GB (with venv)
```

---

## ✅ Pre-Submission Checklist

- [ ] All files present (check PROJECT_SUMMARY.md)
- [ ] Dependencies installed (`pip list`)
- [ ] .env configured with GEMINI_API_KEY
- [ ] Data generated (catalog.json exists)
- [ ] Vector store built (faiss_index/ exists)
- [ ] Evaluation run (evaluation_results.json exists)
- [ ] Test predictions generated (firstname_lastname.csv)
- [ ] Server starts without errors
- [ ] UI accessible at http://localhost:8000
- [ ] API endpoints respond correctly
- [ ] Documentation complete and readable

---

**Last Updated**: November 2025
**Version**: 1.0.0
**Status**: ✅ Production Ready
