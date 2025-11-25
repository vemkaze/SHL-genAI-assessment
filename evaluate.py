"""
Evaluation script using labeled train dataset
Computes Recall@K metrics
"""
import json
from typing import List, Dict, Set
from pathlib import Path

from config import config
from utils import setup_logger, load_json
from vector_store import VectorStore
from retriever import AssessmentRetriever

logger = setup_logger(__name__)


class Evaluator:
    """Evaluate recommendation system"""
    
    def __init__(self, retriever: AssessmentRetriever):
        """
        Initialize evaluator
        
        Args:
            retriever: AssessmentRetriever instance
        """
        self.retriever = retriever
    
    def compute_recall_at_k(self,
                           query: str,
                           ground_truth_urls: Set[str],
                           k: int = 10) -> float:
        """
        Compute Recall@K for a single query
        
        Args:
            query: Search query
            ground_truth_urls: Set of relevant assessment URLs
            k: Number of recommendations to consider
            
        Returns:
            Recall@K score
        """
        # Get recommendations
        recommendations = self.retriever.retrieve(query, top_k=20, top_n=k)
        
        # Extract URLs from recommendations
        recommended_urls = {rec['url'] for rec in recommendations}
        
        # Compute recall
        if len(ground_truth_urls) == 0:
            return 0.0
        
        true_positives = len(recommended_urls & ground_truth_urls)
        recall = true_positives / len(ground_truth_urls)
        
        return recall
    
    def evaluate_dataset(self,
                        dataset: List[Dict],
                        k: int = 10) -> Dict[str, float]:
        """
        Evaluate on entire dataset
        
        Args:
            dataset: List of query/ground_truth pairs
            k: Number of recommendations to consider
            
        Returns:
            Dictionary of metrics
        """
        recalls = []
        
        logger.info(f"Evaluating {len(dataset)} queries at K={k}")
        
        for i, item in enumerate(dataset, 1):
            query = item['query']
            
            # Get ground truth URLs
            ground_truth_urls = set()
            for assessment in item.get('relevant_assessments', []):
                if isinstance(assessment, dict):
                    ground_truth_urls.add(assessment.get('url', ''))
                elif isinstance(assessment, str):
                    ground_truth_urls.add(assessment)
            
            # Compute recall
            recall = self.compute_recall_at_k(query, ground_truth_urls, k=k)
            recalls.append(recall)
            
            logger.info(f"Query {i}/{len(dataset)}: Recall@{k} = {recall:.3f}")
            logger.info(f"  Query: {query[:80]}...")
            logger.info(f"  Ground truth: {len(ground_truth_urls)} URLs")
        
        # Compute average metrics
        avg_recall = sum(recalls) / len(recalls) if recalls else 0.0
        
        metrics = {
            f'recall@{k}': avg_recall,
            'num_queries': len(dataset),
            'individual_recalls': recalls
        }
        
        return metrics
    
    def print_results(self, metrics: Dict[str, float]) -> None:
        """Print evaluation results"""
        logger.info("\n" + "="*80)
        logger.info("EVALUATION RESULTS")
        logger.info("="*80)
        
        for key, value in metrics.items():
            if key != 'individual_recalls':
                logger.info(f"{key}: {value:.4f}")
        
        logger.info("="*80 + "\n")


def create_sample_train_data():
    """Create sample training data if not exists"""
    train_data = [
        {
            "query": "Software developer position requiring Python programming and problem-solving skills",
            "relevant_assessments": [
                {"url": "https://www.shl.com/solutions/products/assessment-0"},
                {"url": "https://www.shl.com/solutions/products/assessment-6"}
            ]
        },
        {
            "query": "Sales manager role with leadership and communication requirements",
            "relevant_assessments": [
                {"url": "https://www.shl.com/solutions/products/assessment-4"},
                {"url": "https://www.shl.com/solutions/products/assessment-7"}
            ]
        },
        {
            "query": "Graduate trainee program needing cognitive ability tests",
            "relevant_assessments": [
                {"url": "https://www.shl.com/solutions/products/assessment-1"},
                {"url": "https://www.shl.com/solutions/products/assessment-2"}
            ]
        },
        {
            "query": "Customer service representative with problem-solving and communication skills",
            "relevant_assessments": [
                {"url": "https://www.shl.com/solutions/products/assessment-7"},
                {"url": "https://www.shl.com/solutions/products/assessment-5"}
            ]
        },
        {
            "query": "Technical support engineer requiring mechanical reasoning and troubleshooting",
            "relevant_assessments": [
                {"url": "https://www.shl.com/solutions/products/assessment-3"},
                {"url": "https://www.shl.com/solutions/products/assessment-6"}
            ]
        },
        {
            "query": "Finance analyst position requiring numerical reasoning and data analysis",
            "relevant_assessments": [
                {"url": "https://www.shl.com/solutions/products/assessment-1"},
            ]
        },
        {
            "query": "HR manager role needing personality assessment and situational judgment",
            "relevant_assessments": [
                {"url": "https://www.shl.com/solutions/products/assessment-4"},
                {"url": "https://www.shl.com/solutions/products/assessment-5"}
            ]
        },
        {
            "query": "Data scientist with advanced analytical and programming capabilities",
            "relevant_assessments": [
                {"url": "https://www.shl.com/solutions/products/assessment-6"},
                {"url": "https://www.shl.com/solutions/products/assessment-1"}
            ]
        },
        {
            "query": "Team leader position requiring interpersonal skills and decision-making ability",
            "relevant_assessments": [
                {"url": "https://www.shl.com/solutions/products/assessment-5"},
            ]
        },
        {
            "query": "Entry-level administrative assistant with typing and organizational skills",
            "relevant_assessments": [
                {"url": "https://www.shl.com/solutions/products/assessment-7"},
            ]
        }
    ]
    
    return train_data


def main():
    """Main evaluation workflow"""
    config.ensure_directories()
    
    # Load or create train data
    if config.TRAIN_DATA_PATH.exists():
        logger.info(f"Loading train data from {config.TRAIN_DATA_PATH}")
        train_data = load_json(config.TRAIN_DATA_PATH)
    else:
        logger.info("Parsing real training data from assignment...")
        try:
            from parse_training_data import save_training_data
            train_data = save_training_data()
        except Exception as e:
            logger.error(f"Failed to parse training data: {e}")
            logger.info("Falling back to sample training data...")
            train_data = create_sample_train_data()
            
            # Save for future use
            with open(config.TRAIN_DATA_PATH, 'w') as f:
                json.dump(train_data, f, indent=2)
            
            logger.info(f"✓ Saved train data to {config.TRAIN_DATA_PATH}")
    
    # Load vector store
    logger.info("Loading vector store...")
    store = VectorStore()
    
    if not (config.FAISS_INDEX_PATH / "index.faiss").exists():
        logger.error("Vector store not found. Please run vector_store.py first.")
        return
    
    store.load()
    
    # Initialize retriever
    logger.info("\n" + "="*80)
    logger.info("BASELINE EVALUATION (without reranker)")
    logger.info("="*80)
    
    retriever_baseline = AssessmentRetriever(
        vector_store=store,
        use_reranker=False,
        use_llm_reranking=False
    )
    
    evaluator = Evaluator(retriever_baseline)
    metrics_baseline = evaluator.evaluate_dataset(train_data, k=10)
    evaluator.print_results(metrics_baseline)
    
    # Improved evaluation with reranker
    logger.info("\n" + "="*80)
    logger.info("IMPROVED EVALUATION (with cross-encoder reranker)")
    logger.info("="*80)
    
    retriever_improved = AssessmentRetriever(
        vector_store=store,
        use_reranker=True,
        use_llm_reranking=False
    )
    
    evaluator_improved = Evaluator(retriever_improved)
    metrics_improved = evaluator_improved.evaluate_dataset(train_data, k=10)
    evaluator_improved.print_results(metrics_improved)
    
    # Compare results
    logger.info("\n" + "="*80)
    logger.info("IMPROVEMENT SUMMARY")
    logger.info("="*80)
    
    baseline_recall = metrics_baseline['recall@10']
    improved_recall = metrics_improved['recall@10']
    improvement = ((improved_recall - baseline_recall) / baseline_recall * 100) if baseline_recall > 0 else 0
    
    logger.info(f"Baseline Recall@10:  {baseline_recall:.4f}")
    logger.info(f"Improved Recall@10:  {improved_recall:.4f}")
    logger.info(f"Improvement:         {improvement:+.2f}%")
    logger.info("="*80 + "\n")
    
    # Save results
    results_file = config.DATA_DIR / "evaluation_results.json"
    results = {
        "baseline": metrics_baseline,
        "improved": metrics_improved,
        "improvement_percent": improvement
    }
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"✓ Results saved to {results_file}")


if __name__ == "__main__":
    main()
