"""
Configuration management for SHL Assessment Recommendation System
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    MODELS_DIR = BASE_DIR / "models"
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Model configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    RERANKER_MODEL = os.getenv("RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
    
    # Data paths
    CATALOG_JSON = DATA_DIR / "catalog.json"
    CATALOG_CSV = DATA_DIR / "catalog.csv"
    FAISS_INDEX_PATH = DATA_DIR / "faiss_index"
    TRAIN_DATA_PATH = DATA_DIR / "train.json"
    TEST_DATA_PATH = DATA_DIR / "test.json"
    
    # Retrieval configuration
    TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", "20"))
    TOP_N_FINAL = int(os.getenv("TOP_N_FINAL", "10"))
    
    # API configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # SHL catalog URL
    SHL_CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.MODELS_DIR.mkdir(exist_ok=True)

config = Config()
