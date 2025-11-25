"""
Retrieval and reranking for assessment recommendations
"""
from typing import List, Dict, Tuple, Optional
import google.generativeai as genai
from sentence_transformers import CrossEncoder

from config import config
from utils import setup_logger
from vector_store import VectorStore

logger = setup_logger(__name__)


class AssessmentRetriever:
    """Retrieve and rerank assessments"""
    
    def __init__(self, 
                 vector_store: VectorStore = None,
                 use_reranker: bool = True,
                 use_llm_reranking: bool = False):
        """
        Initialize retriever
        
        Args:
            vector_store: VectorStore instance
            use_reranker: Whether to use cross-encoder reranking
            use_llm_reranking: Whether to use LLM for reranking
        """
        self.vector_store = vector_store
        self.use_reranker = use_reranker
        self.use_llm_reranking = use_llm_reranking and config.GEMINI_API_KEY
        
        # Initialize reranker
        if self.use_reranker and not self.use_llm_reranking:
            logger.info(f"Loading cross-encoder: {config.RERANKER_MODEL}")
            self.reranker = CrossEncoder(config.RERANKER_MODEL)
        else:
            self.reranker = None
        
        # Initialize Gemini for LLM reranking
        if self.use_llm_reranking:
            logger.info("Initializing Gemini for LLM reranking")
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.llm_model = genai.GenerativeModel('gemini-pro')
    
    def retrieve(self, 
                query: str,
                top_k: int = None,
                top_n: int = None) -> List[Dict]:
        """
        Retrieve and rerank assessments
        
        Args:
            query: Search query
            top_k: Number of initial candidates
            top_n: Number of final results
            
        Returns:
            List of recommended assessments
        """
        top_k = top_k or config.TOP_K_RETRIEVAL
        top_n = top_n or config.TOP_N_FINAL
        
        # Initial retrieval
        logger.info(f"Retrieving top {top_k} candidates for query: {query[:100]}...")
        candidates, scores = self.vector_store.search(query, top_k=top_k)
        
        if not candidates:
            logger.warning("No candidates found")
            return []
        
        # Rerank if enabled
        if self.use_reranker or self.use_llm_reranking:
            logger.info(f"Reranking {len(candidates)} candidates...")
            candidates, scores = self.rerank(query, candidates)
        
        # Apply domain balancing
        final_results = self._balance_domains(candidates[:top_n])
        
        logger.info(f"✓ Returning {len(final_results)} recommendations")
        return final_results
    
    def rerank(self, 
              query: str, 
              candidates: List[Dict]) -> Tuple[List[Dict], List[float]]:
        """
        Rerank candidates
        
        Args:
            query: Search query
            candidates: List of candidate assessments
            
        Returns:
            Tuple of (reranked assessments, scores)
        """
        if self.use_llm_reranking:
            return self._rerank_with_llm(query, candidates)
        elif self.reranker:
            return self._rerank_with_cross_encoder(query, candidates)
        else:
            # Return as-is with dummy scores
            return candidates, [1.0] * len(candidates)
    
    def _rerank_with_cross_encoder(self, 
                                   query: str,
                                   candidates: List[Dict]) -> Tuple[List[Dict], List[float]]:
        """Rerank using cross-encoder"""
        # Prepare pairs
        pairs = []
        for candidate in candidates:
            text = f"{candidate['name']}. {candidate['description']}"
            pairs.append([query, text])
        
        # Score pairs
        scores = self.reranker.predict(pairs)
        
        # Sort by scores
        sorted_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        
        reranked = [candidates[i] for i in sorted_indices]
        reranked_scores = [float(scores[i]) for i in sorted_indices]
        
        return reranked, reranked_scores
    
    def _rerank_with_llm(self,
                        query: str,
                        candidates: List[Dict]) -> Tuple[List[Dict], List[float]]:
        """
        Rerank using Gemini LLM
        
        Args:
            query: Search query
            candidates: Candidate assessments
            
        Returns:
            Reranked candidates with scores
        """
        # Create scoring prompt
        candidates_text = "\n".join([
            f"{i+1}. {c['name']}: {c['description'][:150]}"
            for i, c in enumerate(candidates[:10])  # Limit to top 10 for LLM
        ])
        
        prompt = f"""Given the job requirement: "{query}"

Rate each assessment's relevance on a scale of 1-10:

{candidates_text}

Return only a JSON list of scores, e.g., [9, 7, 5, 8, 6, 4, 3, 2, 1, 1]"""
        
        try:
            response = self.llm_model.generate_content(prompt)
            # Parse scores (simple parsing)
            import re
            import json
            
            score_text = response.text
            # Extract JSON array
            match = re.search(r'\[[\d,\s]+\]', score_text)
            if match:
                scores = json.loads(match.group())
                scores = scores[:len(candidates)]
                
                # Normalize scores
                max_score = max(scores) if scores else 1
                scores = [s / max_score for s in scores]
                
                # Sort by scores
                sorted_indices = sorted(range(len(scores)), 
                                      key=lambda i: scores[i], 
                                      reverse=True)
                
                reranked = [candidates[i] for i in sorted_indices]
                reranked_scores = [scores[i] for i in sorted_indices]
                
                return reranked, reranked_scores
        
        except Exception as e:
            logger.warning(f"LLM reranking failed: {e}, using original order")
        
        # Fallback to original order
        return candidates, [1.0] * len(candidates)
    
    def _balance_domains(self, assessments: List[Dict]) -> List[Dict]:
        """
        Balance assessment types (technical + behavioral mix)
        
        Args:
            assessments: List of assessments
            
        Returns:
            Balanced list of assessments
        """
        # Categorize
        technical = []  # K, P
        behavioral = []  # B, S
        other = []
        
        for assessment in assessments:
            test_types = assessment.get('test_type', [])
            if any(t in ['K', 'P'] for t in test_types):
                technical.append(assessment)
            elif any(t in ['B', 'S'] for t in test_types):
                behavioral.append(assessment)
            else:
                other.append(assessment)
        
        # Aim for ~70% technical, 30% behavioral
        target_technical = int(len(assessments) * 0.7)
        target_behavioral = len(assessments) - target_technical
        
        balanced = []
        balanced.extend(technical[:target_technical])
        balanced.extend(behavioral[:target_behavioral])
        
        # Fill remaining with other
        remaining = len(assessments) - len(balanced)
        if remaining > 0:
            balanced.extend(other[:remaining])
        
        # If we don't have enough, just return what we have
        if len(balanced) < len(assessments):
            balanced.extend(technical[target_technical:])
            balanced.extend(behavioral[target_behavioral:])
        
        return balanced[:len(assessments)]


def main():
    """Test retriever"""
    from vector_store import VectorStore
    
    # Load vector store
    logger.info("Loading vector store...")
    store = VectorStore()
    store.load()
    
    # Create retriever
    retriever = AssessmentRetriever(
        vector_store=store,
        use_reranker=True,
        use_llm_reranking=False
    )
    
    # Test queries
    test_queries = [
        "I need assessments for a software developer position requiring Python and data analysis",
        "Looking for personality and behavioral tests for a sales manager role",
        "Need cognitive ability tests for graduate recruitment"
    ]
    
    for query in test_queries:
        logger.info(f"\n{'='*80}")
        logger.info(f"Query: {query}")
        logger.info('='*80)
        
        results = retriever.retrieve(query, top_k=20, top_n=5)
        
        for i, assessment in enumerate(results, 1):
            logger.info(f"\n{i}. {assessment['name']}")
            logger.info(f"   Type: {', '.join(assessment['test_type'])}")
            logger.info(f"   Duration: {assessment.get('duration', 'N/A')} min")
            logger.info(f"   Description: {assessment['description'][:100]}...")


if __name__ == "__main__":
    main()
