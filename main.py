"""
FastAPI backend for SHL Assessment Recommendation System
"""
import os
import sys
from pathlib import Path

# Add proper error handling for startup
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import HTMLResponse
    from pydantic import BaseModel, Field
    from typing import List, Dict, Optional
    
    from config import config
    from utils import setup_logger
    from vector_store import VectorStore
    from retriever import AssessmentRetriever
except Exception as e:
    print(f"FATAL ERROR during imports: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)

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
    """Initialize models on startup - Quick start, load in background"""
    global vector_store, retriever
    
    try:
        logger.info("="*80)
        logger.info("Starting up API server...")
        logger.info(f"Python version: {sys.version}")
        logger.info(f"PORT environment variable: {os.environ.get('PORT', 'NOT SET')}")
        logger.info(f"Working directory: {os.getcwd()}")
        
        # Check if vector store exists
        index_path = config.FAISS_INDEX_PATH / "index.faiss"
        logger.info(f"Looking for vector store at: {index_path}")
        logger.info(f"Vector store exists: {index_path.exists()}")
        
        if index_path.exists():
            logger.info(f"Vector store file size: {index_path.stat().st_size} bytes")
        else:
            logger.error(f"Vector store NOT FOUND at {index_path}")
            logger.error(f"Directory contents of {config.FAISS_INDEX_PATH}:")
            if config.FAISS_INDEX_PATH.exists():
                for item in config.FAISS_INDEX_PATH.iterdir():
                    logger.error(f"  - {item.name}")
            else:
                logger.error(f"  Directory does not exist!")
        
        logger.info("Server starting immediately (vector store will load on first request)")
        logger.info("="*80)
    except Exception as e:
        print(f"Error in startup logging: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
    
    # Don't load anything here - let the port bind quickly
    # Loading will happen on first request to /recommend


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
    
    # Lazy load on first request
    if retriever is None:
        logger.info("Loading vector store on first request...")
        try:
            index_path = config.FAISS_INDEX_PATH / "index.faiss"
            
            if not index_path.exists():
                raise HTTPException(
                    status_code=503,
                    detail="System not ready. Vector store not found. Please contact support."
                )
            
            # Load vector store
            logger.info("Loading FAISS index...")
            vector_store = VectorStore()
            vector_store.load(load_embedding_model=False)  # Don't load embedding model yet
            logger.info(f"✓ Loaded {len(vector_store.assessments)} assessments")
            
            # Initialize retriever (without reranker for faster startup)
            logger.info("Initializing retriever...")
            retriever = AssessmentRetriever(
                vector_store=vector_store,
                use_reranker=False,  # Disabled for faster startup
                use_llm_reranking=False
            )
            
            logger.info("✓ System ready!")
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to load vector store: {e}", exc_info=True)
            raise HTTPException(
                status_code=503,
                detail=f"Failed to initialize system: {str(e)}"
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


@app.get("/setup")
async def run_setup():
    """
    Trigger system setup (scraping + vector store building)
    This endpoint runs setup and returns immediately while work continues in background
    """
    global vector_store, retriever
    
    index_path = config.FAISS_INDEX_PATH / "index.faiss"
    
    if index_path.exists():
        return {"status": "already_setup", "message": "System is already configured"}
    
    # Run setup inline (this will take time but we're already past startup)
    try:
        logger.info("Starting setup process...")
        
        # Import and run scraper
        from scraper import scrape_all_assessments
        logger.info("Scraping assessments...")
        assessments = scrape_all_assessments()
        logger.info(f"Scraped {len(assessments)} assessments")
        
        # Build vector store
        logger.info("Building vector store...")
        vector_store = VectorStore()
        vector_store.build_from_assessments(assessments)
        vector_store.save()
        logger.info("Vector store saved")
        
        # Initialize retriever
        logger.info("Initializing retriever...")
        retriever = AssessmentRetriever(
            vector_store=vector_store,
            use_reranker=True,
            use_llm_reranking=False
        )
        
        logger.info("✓ Setup completed successfully!")
        
        return {
            "status": "success",
            "message": f"Setup complete. Indexed {len(assessments)} assessments.",
            "total_assessments": len(assessments)
        }
        
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Setup failed: {str(e)}"
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
