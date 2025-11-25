"""
Embedding generation using sentence-transformers and Gemini API
"""
import numpy as np
from typing import List, Union, Optional
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

from config import config
from utils import setup_logger

logger = setup_logger(__name__)


class EmbeddingGenerator:
    """Generate embeddings for text using multiple backends"""
    
    def __init__(self, model_name: str = None, use_gemini: bool = False):
        """
        Initialize embedding generator
        
        Args:
            model_name: Name of sentence-transformer model
            use_gemini: Whether to use Gemini API for embeddings
        """
        self.use_gemini = use_gemini and config.GEMINI_API_KEY
        self.model_name = model_name or config.EMBEDDING_MODEL
        
        if self.use_gemini:
            logger.info("Initializing Gemini embeddings")
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.model = None
            self.dimension = 768  # Gemini embedding dimension
        else:
            logger.info(f"Loading sentence-transformer model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            self.dimension = self.model.get_sentence_embedding_dimension()
        
        logger.info(f"Embedding dimension: {self.dimension}")
    
    def encode(self, 
               texts: Union[str, List[str]], 
               batch_size: int = 32,
               show_progress: bool = False) -> np.ndarray:
        """
        Generate embeddings for texts
        
        Args:
            texts: Single text or list of texts
            batch_size: Batch size for processing
            show_progress: Show progress bar
            
        Returns:
            Numpy array of embeddings
        """
        if isinstance(texts, str):
            texts = [texts]
        
        if self.use_gemini:
            return self._encode_gemini(texts)
        else:
            return self._encode_sentence_transformer(texts, batch_size, show_progress)
    
    def _encode_sentence_transformer(self, 
                                     texts: List[str], 
                                     batch_size: int,
                                     show_progress: bool) -> np.ndarray:
        """Encode using sentence-transformers"""
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embeddings
    
    def _encode_gemini(self, texts: List[str]) -> np.ndarray:
        """
        Encode using Gemini API
        
        Args:
            texts: List of texts to embed
            
        Returns:
            Numpy array of embeddings
        """
        embeddings = []
        
        for text in texts:
            try:
                # Use Gemini embedding model
                result = genai.embed_content(
                    model="models/embedding-001",
                    content=text,
                    task_type="retrieval_document"
                )
                embeddings.append(result['embedding'])
            except Exception as e:
                logger.warning(f"Gemini API error, using zeros: {e}")
                embeddings.append([0.0] * self.dimension)
        
        embeddings = np.array(embeddings, dtype=np.float32)
        
        # Normalize embeddings
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1
        embeddings = embeddings / norms
        
        return embeddings
    
    def encode_query(self, query: str) -> np.ndarray:
        """
        Encode a search query
        
        Args:
            query: Search query text
            
        Returns:
            Query embedding
        """
        if self.use_gemini:
            try:
                result = genai.embed_content(
                    model="models/embedding-001",
                    content=query,
                    task_type="retrieval_query"
                )
                embedding = np.array([result['embedding']], dtype=np.float32)
                
                # Normalize
                norm = np.linalg.norm(embedding)
                if norm > 0:
                    embedding = embedding / norm
                
                return embedding
            except Exception as e:
                logger.error(f"Gemini query encoding failed: {e}")
                return np.zeros((1, self.dimension), dtype=np.float32)
        else:
            return self.encode(query)


def main():
    """Test embedding generation"""
    from utils import load_json, format_assessment
    
    # Load catalog
    catalog = load_json(config.CATALOG_JSON)
    
    # Initialize generator
    generator = EmbeddingGenerator()
    
    # Test on first few assessments
    test_assessments = catalog[:5]
    texts = [format_assessment(a) for a in test_assessments]
    
    logger.info(f"Generating embeddings for {len(texts)} assessments")
    embeddings = generator.encode(texts, show_progress=True)
    
    logger.info(f"✓ Generated embeddings with shape: {embeddings.shape}")
    
    # Test query encoding
    query = "I need a test for software developers"
    query_emb = generator.encode_query(query)
    logger.info(f"✓ Query embedding shape: {query_emb.shape}")


if __name__ == "__main__":
    main()
