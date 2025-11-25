# 🚀 Deployment Guide
## SHL Assessment Recommendation System

---

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Render Deployment](#render-deployment)
4. [Railway Deployment](#railway-deployment)
5. [HuggingFace Spaces](#huggingface-spaces)
6. [Environment Variables](#environment-variables)
7. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites
- Python 3.10 or higher
- 4GB RAM minimum (8GB recommended)
- ~2GB disk space

### Setup Steps

1. **Clone/Extract the project**
   ```bash
   cd shl_assignment
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Copy template
   copy .env.example .env    # Windows
   cp .env.example .env      # Linux/Mac

   # Edit .env and add your Gemini API key
   GEMINI_API_KEY=your_actual_api_key_here
   ```

5. **Build the system**
   ```bash
   # Automated (recommended)
   python setup.py

   # OR Manual
   python scraper.py
   python vector_store.py
   python evaluate.py
   ```

6. **Start the server**
   ```bash
   python main.py
   ```

7. **Access the application**
   - Open browser: http://localhost:8000
   - API docs: http://localhost:8000/docs

---

## Docker Deployment

### Build and Run Locally

1. **Build the Docker image**
   ```bash
   docker build -t shl-recommender .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 \
     -e GEMINI_API_KEY=your_key_here \
     -v ${PWD}/data:/app/data \
     shl-recommender
   ```

3. **Access the application**
   - Open: http://localhost:8000

### Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - API_HOST=0.0.0.0
      - API_PORT=8000
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Run with:
```bash
docker-compose up -d
```

---

## Render Deployment

### Method 1: Web Service (Recommended)

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO
   git push -u origin main
   ```

2. **Create Render account**
   - Go to: https://render.com
   - Sign up / Log in

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `shl_assignment` repository

4. **Configure Service**
   ```
   Name: shl-recommender
   Environment: Python 3
   Build Command: pip install -r requirements.txt && python setup.py
   Start Command: python main.py
   ```

5. **Add Environment Variables**
   - Click "Environment"
   - Add: `GEMINI_API_KEY` = `your_key_here`
   - Add: `API_HOST` = `0.0.0.0`
   - Add: `API_PORT` = `8000`

6. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (~5 minutes)
   - Access your app at: `https://your-app-name.onrender.com`

### Method 2: Docker on Render

1. **Use Dockerfile deployment**
   - Select "Docker" as environment
   - Render automatically detects Dockerfile
   - Configure environment variables
   - Deploy!

---

## Railway Deployment

1. **Push code to GitHub** (if not already done)

2. **Create Railway account**
   - Go to: https://railway.app
   - Sign up with GitHub

3. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `shl_assignment` repository

4. **Railway auto-detects**
   - Automatically finds Dockerfile
   - Starts build process

5. **Add Environment Variables**
   - Click on your service
   - Go to "Variables" tab
   - Add: `GEMINI_API_KEY`

6. **Generate Domain**
   - Go to "Settings"
   - Click "Generate Domain"
   - Access your app!

---

## HuggingFace Spaces

### Using Docker

1. **Create HuggingFace account**
   - Go to: https://huggingface.co
   - Sign up / Log in

2. **Create New Space**
   - Click on your profile → "Spaces"
   - Click "Create new Space"
   - Name: `shl-assessment-recommender`
   - License: Apache 2.0
   - SDK: **Docker**
   - Hardware: CPU Basic (free) or GPU (if available)

3. **Upload Files**
   ```bash
   # Clone the space
   git clone https://huggingface.co/spaces/YOUR_USERNAME/shl-assessment-recommender
   cd shl-assessment-recommender

   # Copy all project files
   cp -r ../shl_assignment/* .

   # Create README.md for Space
   cat > README.md << 'EOF'
   ---
   title: SHL Assessment Recommender
   emoji: 🎯
   colorFrom: blue
   colorTo: green
   sdk: docker
   pinned: false
   ---

   # SHL Assessment Recommendation System

   AI-powered assessment recommendations using RAG.
   EOF

   # Commit and push
   git add .
   git commit -m "Initial deployment"
   git push
   ```

4. **Add Secrets**
   - Go to Space Settings
   - Click "Repository secrets"
   - Add: `GEMINI_API_KEY`

5. **Wait for Build**
   - HuggingFace builds Docker image
   - Space becomes available at: `https://huggingface.co/spaces/YOUR_USERNAME/shl-assessment-recommender`

### Using Gradio (Alternative)

If you prefer Gradio interface, create `app.py`:

```python
import gradio as gr
from retriever import AssessmentRetriever
from vector_store import VectorStore

# Load models
store = VectorStore()
store.load()
retriever = AssessmentRetriever(store, use_reranker=True)

def recommend(query):
    results = retriever.retrieve(query, top_n=10)
    formatted = []
    for r in results:
        formatted.append([
            r['name'],
            ', '.join(r['test_type']),
            r.get('duration', 'N/A'),
            r['description'][:200] + '...'
        ])
    return formatted

iface = gr.Interface(
    fn=recommend,
    inputs=gr.Textbox(lines=3, label="Job Description"),
    outputs=gr.Dataframe(headers=["Assessment", "Type", "Duration", "Description"]),
    title="SHL Assessment Recommender",
    description="Get AI-powered assessment recommendations"
)

iface.launch()
```

---

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | `AIza...` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `API_HOST` | API host address | `0.0.0.0` |
| `API_PORT` | API port | `8000` |
| `EMBEDDING_MODEL` | Sentence transformer model | `sentence-transformers/all-MiniLM-L6-v2` |
| `RERANKER_MODEL` | Cross-encoder model | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| `TOP_K_RETRIEVAL` | Initial retrieval count | `20` |
| `TOP_N_FINAL` | Final results count | `10` |

### How to Get Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Add to your `.env` file

---

## Troubleshooting

### Build Failures

**Problem**: `pip install` fails
```bash
# Solution: Upgrade pip
pip install --upgrade pip
pip install -r requirements.txt
```

**Problem**: Out of memory during build
```bash
# Solution: Build models locally, then deploy data folder
python vector_store.py
# Deploy the generated data/ folder with your app
```

### Runtime Errors

**Problem**: "Vector store not found"
```bash
# Solution: Run setup before starting server
python setup.py
python main.py
```

**Problem**: "Gemini API error"
```bash
# Solution: Check API key is set correctly
echo $GEMINI_API_KEY  # Linux/Mac
echo %GEMINI_API_KEY% # Windows
```

### Performance Issues

**Problem**: Slow response times
```bash
# Solution: Use sentence-transformers instead of Gemini embeddings
# In embeddings.py, set use_gemini=False
```

**Problem**: High memory usage
```bash
# Solution: Reduce batch size in vector_store.py
# Change batch_size=32 to batch_size=16
```

### Deployment-Specific

**Render**: 
- Free tier spins down after inactivity
- First request after wake-up takes ~30 seconds
- Solution: Use paid tier for production

**Railway**:
- Automatically sleeps after 24h on free tier
- Solution: Add uptime monitor or upgrade

**HuggingFace**:
- Docker build timeout on complex projects
- Solution: Pre-build models and include in repo

---

## Production Checklist

Before deploying to production:

- [ ] Set strong `GEMINI_API_KEY`
- [ ] Enable HTTPS (usually automatic on platforms)
- [ ] Set up monitoring (uptimerobot.com)
- [ ] Configure proper CORS settings
- [ ] Add rate limiting
- [ ] Set up logging aggregation
- [ ] Create backup of vector store
- [ ] Document API endpoints
- [ ] Add authentication if needed
- [ ] Set up CI/CD pipeline
- [ ] Configure auto-scaling
- [ ] Set up error tracking (Sentry)

---

## Monitoring & Maintenance

### Health Checks

```bash
# Check API health
curl https://your-app.com/health

# Expected response:
# {"status":"healthy"}
```

### Logs

```bash
# Render: View in dashboard
# Railway: Click on service → Logs
# Docker: docker logs CONTAINER_ID
```

### Updates

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Rebuild vector store with new data
python scraper.py
python vector_store.py

# Deploy changes
git push origin main  # Auto-deploys on most platforms
```

---

## Support & Resources

- **Documentation**: See `README.md` and `APPROACH.md`
- **API Docs**: Visit `/docs` endpoint when server is running
- **Issues**: Check logs and `test_system.py`
- **Community**: Refer to respective platform documentation

---

**🎉 Happy Deploying!**
