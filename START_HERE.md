# 🎯 START HERE - Quick Setup Instructions

## For Windows Users (EASIEST)

### 1️⃣ One-Command Setup
```powershell
.\run_setup.bat
```

This will:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Prompt you for Gemini API key
- ✅ Build the entire system
- ✅ Start the server automatically

**Time**: ~10 minutes

---

## Manual Setup (If Batch Fails)

### Step 1: Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Configure API Key
```powershell
copy .env.example .env
notepad .env
```
Add your Gemini API key (get free key: https://makersuite.google.com/app/apikey)

### Step 4: Build System
```powershell
python setup.py
```

### Step 5: Start Server
```powershell
python main.py
```

### Step 6: Open Browser
Go to: **http://localhost:8000**

---

## For WSL/Linux Users

```bash
# Navigate to project
cd /mnt/c/Users/abhiv/Music/shl_assignment

# Run setup script
chmod +x run_setup.sh
./run_setup.sh
```

---

## 🧪 Quick Test

After setup, test the system:

```powershell
# Test 1: System health
python test_system.py

# Test 2: API health
curl http://localhost:8000/health

# Test 3: Generate predictions
python generate_predictions.py
```

---

## 📂 What Gets Created

After setup, you'll have:
```
data/
├── catalog.json          # 377+ scraped assessments
├── catalog.csv           # Same data in CSV format
├── train.json            # Real training data (6 queries, 46 pairs)
└── faiss_index/          # Vector database
    ├── index.faiss       # FAISS index file
    ├── metadata.pkl      # Assessment metadata
    └── config.pkl        # Index configuration
```

---

## 🎉 Success Indicators

You'll know setup worked when you see:

```
✓ Scraped 377 assessments
✓ Generated 377 embeddings  
✓ Built FAISS index
✓ Evaluation Results:
  Baseline Recall@10: 0.45
  Improved Recall@10: 0.68
  Improvement: +51%
✓ Server running at http://0.0.0.0:8000
```

---

## ❓ Common Issues

### Issue: "python not found"
**Fix**: Install Python 3.10+ from python.org

### Issue: "Execution policy error"
**Fix**: 
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "No module named 'dotenv'"
**Fix**: Activate virtual environment first!
```powershell
.\venv\Scripts\Activate.ps1
```

### Issue: Setup is slow
**Normal!** First run downloads ~500MB of models. Subsequent runs are fast.

---

## 🚀 What to Try First

Once the server is running at http://localhost:8000, try these queries:

1. **"I need Java developers with 5+ years experience"**
   - Should return Java assessments + collaboration tests

2. **"Entry level sales position for fresh graduates"**
   - Should return sales + communication assessments

3. **"Senior data analyst with SQL and Python skills"**
   - Should return technical assessments for SQL, Python, Excel

4. **"Content writer expert in English and SEO"**
   - Should return English comprehension + SEO tests

---

## 📚 Next Steps

After testing locally:

1. ✅ Read **APPROACH.md** (2-page technical document)
2. ✅ Run **evaluate.py** to see Recall@10 metrics
3. ✅ Generate predictions with **generate_predictions.py**
4. ✅ Deploy to cloud (see **DEPLOYMENT.md**)

---

## 💡 Pro Tip

For fastest setup experience:
1. Get Gemini API key ready: https://makersuite.google.com/app/apikey
2. Run `.\run_setup.bat` 
3. Paste API key when prompted
4. Wait ~10 minutes
5. System is ready! 🎉

---

**Need more help?** Check **SETUP_GUIDE.md** for detailed troubleshooting.
