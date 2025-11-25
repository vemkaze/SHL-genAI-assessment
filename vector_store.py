"""
FAISS vector store for efficient similarity search
"""
import numpy as np
import faiss
import pickle
from pathlib import Path
from typing import List, Tuple, Optional, Dict

from config import config
from utils import setup_logger, load_json, save_json, format_assessment
from embeddings import EmbeddingGenerator

logger = setup_logger(__name__)


class VectorStore:
    """FAISS-based vector store for assessments"""
    
    def __init__(self, dimension: int = 384):
        """
        Initialize vector store
        
        Args:
            dimension: Embedding dimension
        """
        self.dimension = dimension
        self.index = None
        self.assessments = []
        self.embedding_generator = None
    
    def build_index(self, 
                   assessments: List[Dict],
                   embedding_generator: EmbeddingGenerator = None) -> None:
        """
        Build FAISS index from assessments
        
        Args:
            assessments: List of assessment dictionaries
            embedding_generator: EmbeddingGenerator instance
        """
        logger.info(f"Building index for {len(assessments)} assessments")
        
        self.assessments = assessments
        
        # Initialize embedding generator
        if embedding_generator is None:
            self.embedding_generator = EmbeddingGenerator()
        else:
            self.embedding_generator = embedding_generator
        
        self.dimension = self.embedding_generator.dimension
        
        # Format assessments for embedding
        texts = [format_assessment(a) for a in assessments]
        
        # Generate embeddings
        logger.info("Generating embeddings...")
        embeddings = self.embedding_generator.encode(
            texts, 
            batch_size=32, 
            show_progress=True
        )
        
        # Create FAISS index (Flat L2 for simplicity and accuracy)
        logger.info("Creating FAISS index...")
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner Product (cosine similarity)
        
        # Add embeddings to index
        self.index.add(embeddings.astype(np.float32))
        
        logger.info(f"✓ Index built with {self.index.ntotal} vectors")
    
    def search(self, 
              query: str, 
              top_k: int = 20) -> Tuple[List[Dict], List[float]]:
        """
        Search for similar assessments
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            Tuple of (assessments, scores)
        """
        if self.index is None:
            raise ValueError("Index not built. Call build_index first.")
        
        # Generate query embedding
        query_embedding = self.embedding_generator.encode_query(query)
        
        # Search
        scores, indices = self.index.search(
            query_embedding.astype(np.float32), 
            min(top_k, self.index.ntotal)
        )
        
        # Get results
        results = []
        result_scores = []
        
        for idx, score in zip(indices[0], scores[0]):
            if idx < len(self.assessments):
                results.append(self.assessments[idx])
                result_scores.append(float(score))
        
        return results, result_scores
    
    def save(self, path: str = None) -> None:
        """
        Save index and metadata
        
        Args:
            path: Directory path to save to
        """
        if path is None:
            path = config.FAISS_INDEX_PATH
        
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        index_file = path / "index.faiss"
        faiss.write_index(self.index, str(index_file))
        
        # Save assessments metadata
        metadata_file = path / "assessments.json"
        save_json(self.assessments, str(metadata_file))
        
        # Save config
        config_file = path / "config.pkl"
        with open(config_file, 'wb') as f:
            pickle.dump({
                'dimension': self.dimension,
                'model_name': self.embedding_generator.model_name,
                'use_gemini': self.embedding_generator.use_gemini
            }, f)
        
        logger.info(f"✓ Vector store saved to {path}")
    
    def load(self, path: str = None) -> None:
        """
        Load index and metadata
        
        Args:
            path: Directory path to load from
        """
        if path is None:
            path = config.FAISS_INDEX_PATH
        
        path = Path(path)
        
        # Load FAISS index
        index_file = path / "index.faiss"
        self.index = faiss.read_index(str(index_file))
        
        # Load assessments metadata
        metadata_file = path / "assessments.json"
        self.assessments = load_json(str(metadata_file))
        
        # Load config
        config_file = path / "config.pkl"
        with open(config_file, 'rb') as f:
            stored_config = pickle.load(f)
        
        self.dimension = stored_config['dimension']
        
        # Initialize embedding generator with same config
        self.embedding_generator = EmbeddingGenerator(
            model_name=stored_config['model_name'],
            use_gemini=stored_config.get('use_gemini', False)
        )
        
        logger.info(f"✓ Vector store loaded from {path}")
        logger.info(f"  - {self.index.ntotal} vectors")
        logger.info(f"  - {len(self.assessments)} assessments")


def main():
    """Build and save vector store"""
    config.ensure_directories()
    
    # Load catalog
    logger.info("Loading catalog...")
    assessments = load_json(config.CATALOG_JSON)
    
    # Create vector store
    store = VectorStore()
    
    # Build index
    store.build_index(assessments)
    
    # Save
    store.save()
    
    # Test search
    logger.info("\nTesting search...")
    test_query = "I need a test for software developers with Python skills"
    results, scores = store.search(test_query, top_k=5)
    
    logger.info(f"\nTop 5 results for: '{test_query}'")
    for i, (assessment, score) in enumerate(zip(results, scores), 1):
        logger.info(f"{i}. {assessment['name']} (score: {score:.3f})")
    
    logger.info("\n✓ Vector store build complete!")


if __name__ == "__main__":
    main()
