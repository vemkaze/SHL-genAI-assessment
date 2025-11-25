"""
FastAPI backend for SHL Assessment Recommendation System
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import os
from pathlib import Path

from config import config
from utils import setup_logger
from vector_store import VectorStore
from retriever import AssessmentRetriever

logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="RAG-based assessment recommendation system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
vector_store = None
retriever = None


class RecommendationRequest(BaseModel):
    """Request model for recommendations"""
    query: str = Field(..., description="Job description or requirement query")
    top_k: Optional[int] = Field(None, description="Number of candidates to retrieve")
    top_n: Optional[int] = Field(None, description="Number of final recommendations")


class Assessment(BaseModel):
    """Assessment model"""
    name: str
    url: str
    description: str
    test_type: List[str]
    adaptive_support: str
    remote_support: str
    duration: Optional[int]


class RecommendationResponse(BaseModel):
    """Response model for recommendations"""
    recommended_assessments: List[Assessment]
    query: str
    count: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    global vector_store, retriever
    
    logger.info("Starting up API server...")
    logger.info(f"PORT environment variable: {os.environ.get('PORT', 'NOT SET')}")
    
    try:
        # Start setup in background if needed
        index_path = config.FAISS_INDEX_PATH / "index.faiss"
        
        if not index_path.exists():
            logger.warning("Vector store not found. Will build on first request.")
            logger.info("API server ready (setup will run on demand)")
        else:
            # Load vector store
            logger.info("Loading vector store...")
            vector_store = VectorStore()
            vector_store.load()
            
            # Initialize retriever
            logger.info("Initializing retriever...")
            retriever = AssessmentRetriever(
                vector_store=vector_store,
                use_reranker=True,
                use_llm_reranking=False  # Set to True to use Gemini for reranking
            )
            
            logger.info("✓ API server ready!")
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        logger.info("API will start anyway - setup on first request")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend"""
    static_dir = Path(__file__).parent / "static"
    index_file = static_dir / "index.html"
    
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(), status_code=200)
    else:
        return HTMLResponse(
            content="<h1>SHL Assessment API</h1><p>API is running. Frontend not found.</p>",
            status_code=200
        )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns:
        Health status
    """
    if vector_store is None or retriever is None:
        return HealthResponse(
            status="unhealthy",
            message="Models not loaded"
        )
    
    return HealthResponse(status="healthy")


@app.post("/recommend", response_model=RecommendationResponse)
async def recommend(request: RecommendationRequest):
    """
    Get assessment recommendations
    
    Args:
        request: Recommendation request with query
        
    Returns:
        List of recommended assessments
    """
    global vector_store, retriever
    
    # Auto-trigger setup if not done
    if retriever is None:
        logger.info("Triggering setup on first request...")
        try:
            import subprocess
            import sys
            # Run setup
            subprocess.run([sys.executable, "scraper.py"], check=True, timeout=180)
            subprocess.run([sys.executable, "vector_store.py"], check=True, timeout=300)
            
            # Load vector store
            vector_store = VectorStore()
            vector_store.load()
            
            # Initialize retriever
            retriever = AssessmentRetriever(
                vector_store=vector_store,
                use_reranker=True,
                use_llm_reranking=False
            )
            logger.info("Setup completed successfully!")
        except subprocess.TimeoutExpired:
            raise HTTPException(
                status_code=503,
                detail="Setup is taking too long. Please try again in a few minutes."
            )
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            raise HTTPException(
                status_code=503,
                detail=f"System setup failed: {str(e)}. Please contact support."
            )
    
    if not request.query or not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty"
        )
    
    try:
        # Get recommendations
        logger.info(f"Processing query: {request.query[:100]}...")
        
        results = retriever.retrieve(
            query=request.query,
            top_k=request.top_k,
            top_n=request.top_n
        )
        
        # Format response
        assessments = [
            Assessment(
                name=a['name'],
                url=a['url'],
                description=a['description'],
                test_type=a.get('test_type', []),
                adaptive_support=a.get('adaptive_support', 'unknown'),
                remote_support=a.get('remote_support', 'unknown'),
                duration=a.get('duration')
            )
            for a in results
        ]
        
        return RecommendationResponse(
            recommended_assessments=assessments,
            query=request.query,
            count=len(assessments)
        )
    
    except Exception as e:
        logger.error(f"Recommendation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    if vector_store is None:
        raise HTTPException(status_code=503, detail="Vector store not loaded")
    
    return {
        "total_assessments": len(vector_store.assessments),
        "index_size": vector_store.index.ntotal if vector_store.index else 0,
        "embedding_dimension": vector_store.dimension
    }


# Mount static files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {config.API_HOST}:{config.API_PORT}")
    
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True,
        log_level="info"
    )
