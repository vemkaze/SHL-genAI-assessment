"""
Generate predictions for test dataset
Outputs CSV in format: query,assessment_url
"""
import csv
import json
from pathlib import Path
from typing import List, Dict

from config import config
from utils import setup_logger, load_json
from vector_store import VectorStore
from retriever import AssessmentRetriever

logger = setup_logger(__name__)


def create_sample_test_data() -> List[Dict]:
    """Create sample test queries"""
    test_queries = [
        {
            "id": 1,
            "query": "Senior software engineer with expertise in machine learning and Python"
        },
        {
            "id": 2,
            "query": "Marketing manager with creative thinking and strategic planning skills"
        },
        {
            "id": 3,
            "query": "Financial analyst requiring advanced numerical and analytical abilities"
        },
        {
            "id": 4,
            "query": "Operations manager with process optimization and leadership capabilities"
        },
        {
            "id": 5,
            "query": "UX designer position needing creativity and user research skills"
        },
        {
            "id": 6,
            "query": "Project manager role requiring organization and stakeholder management"
        },
        {
            "id": 7,
            "query": "Data engineer with SQL, ETL, and database management expertise"
        },
        {
            "id": 8,
            "query": "Business analyst requiring analytical thinking and communication skills"
        },
        {
            "id": 9,
            "query": "Quality assurance engineer with attention to detail and testing skills"
        }
    ]
    
    return test_queries


def generate_predictions(retriever: AssessmentRetriever,
                        test_data: List[Dict],
                        output_file: str,
                        top_n: int = 10) -> None:
    """
    Generate predictions for test data
    
    Args:
        retriever: AssessmentRetriever instance
        test_data: List of test queries
        output_file: Output CSV file path
        top_n: Number of recommendations per query
    """
    logger.info(f"Generating predictions for {len(test_data)} queries...")
    
    predictions = []
    
    for item in test_data:
        query = item['query']
        query_id = item.get('id', item.get('query', query))
        
        logger.info(f"Processing: {query[:80]}...")
        
        # Get recommendations
        recommendations = retriever.retrieve(query, top_k=20, top_n=top_n)
        
        # Add to predictions
        for rec in recommendations:
            predictions.append({
                'query': query,
                'assessment_url': rec['url']
            })
        
        logger.info(f"  → Generated {len(recommendations)} recommendations")
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['query', 'assessment_url'])
        writer.writeheader()
        writer.writerows(predictions)
    
    logger.info(f"\n✓ Saved {len(predictions)} predictions to {output_file}")


def main():
    """Main execution"""
    import sys
    
    config.ensure_directories()
    
    # Get name from command line or use default
    if len(sys.argv) > 1:
        first_name = sys.argv[1]
        last_name = sys.argv[2] if len(sys.argv) > 2 else "lastname"
    else:
        logger.warning("Usage: python generate_predictions.py <firstname> <lastname>")
        logger.info("Using default name: john_doe")
        first_name = "john"
        last_name = "doe"
    
    output_filename = f"{first_name}_{last_name}.csv"
    output_path = config.DATA_DIR / output_filename
    
    # Load or create test data
    if config.TEST_DATA_PATH.exists():
        logger.info(f"Loading test data from {config.TEST_DATA_PATH}")
        test_data = load_json(config.TEST_DATA_PATH)
    else:
        logger.info("Creating sample test data...")
        test_data = create_sample_test_data()
        
        # Save for future use
        with open(config.TEST_DATA_PATH, 'w') as f:
            json.dump(test_data, f, indent=2)
        
        logger.info(f"✓ Saved test data to {config.TEST_DATA_PATH}")
    
    # Load vector store
    logger.info("Loading vector store...")
    store = VectorStore()
    
    if not (config.FAISS_INDEX_PATH / "index.faiss").exists():
        logger.error("Vector store not found. Please run vector_store.py first.")
        return
    
    store.load()
    
    # Initialize retriever with best configuration
    logger.info("Initializing retriever...")
    retriever = AssessmentRetriever(
        vector_store=store,
        use_reranker=True,  # Use reranker for best results
        use_llm_reranking=False
    )
    
    # Generate predictions
    generate_predictions(retriever, test_data, str(output_path), top_n=10)
    
    logger.info(f"\n{'='*80}")
    logger.info("PREDICTION GENERATION COMPLETE")
    logger.info(f"Output file: {output_path}")
    logger.info(f"Total queries: {len(test_data)}")
    logger.info('='*80)


if __name__ == "__main__":
    main()
