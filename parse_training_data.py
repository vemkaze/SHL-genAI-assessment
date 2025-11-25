"""
Parse real training data from Excel/CSV format
Converts the provided training data into the proper format for evaluation
"""
import json
from typing import List, Dict
from collections import defaultdict
from pathlib import Path

from config import config
from utils import setup_logger

logger = setup_logger(__name__)


def parse_training_data() -> List[Dict]:
    """
    Parse the real training data provided
    
    Returns:
        List of training examples with queries and relevant assessment URLs
    """
    
    # Real training data from the assignment
    raw_data = [
        ("I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.", "https://www.shl.com/solutions/products/product-catalog/view/automata-fix-new/"),
        ("I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.", "https://www.shl.com/solutions/products/product-catalog/view/core-java-entry-level-new/"),
        ("I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.", "https://www.shl.com/solutions/products/product-catalog/view/java-8-new/"),
        ("I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.", "https://www.shl.com/solutions/products/product-catalog/view/core-java-advanced-level-new/"),
        ("I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.", "https://www.shl.com/products/product-catalog/view/interpersonal-communications/"),
        
        ("I want to hire new graduates for a sales role in my company, the budget is for about an hour for each test. Give me some options", "https://www.shl.com/solutions/products/product-catalog/view/entry-level-sales-7-1/"),
        ("I want to hire new graduates for a sales role in my company, the budget is for about an hour for each test. Give me some options", "https://www.shl.com/solutions/products/product-catalog/view/entry-level-sales-sift-out-7-1/"),
        ("I want to hire new graduates for a sales role in my company, the budget is for about an hour for each test. Give me some options", "https://www.shl.com/solutions/products/product-catalog/view/entry-level-sales-solution/"),
        ("I want to hire new graduates for a sales role in my company, the budget is for about an hour for each test. Give me some options", "https://www.shl.com/solutions/products/product-catalog/view/sales-representative-solution/"),
        ("I want to hire new graduates for a sales role in my company, the budget is for about an hour for each test. Give me some options", "https://www.shl.com/products/product-catalog/view/business-communication-adaptive/"),
        ("I want to hire new graduates for a sales role in my company, the budget is for about an hour for each test. Give me some options", "https://www.shl.com/solutions/products/product-catalog/view/technical-sales-associate-solution/"),
        ("I want to hire new graduates for a sales role in my company, the budget is for about an hour for each test. Give me some options", "https://www.shl.com/solutions/products/product-catalog/view/svar-spoken-english-indian-accent-new/"),
        ("I want to hire new graduates for a sales role in my company, the budget is for about an hour for each test. Give me some options", "https://www.shl.com/products/product-catalog/view/interpersonal-communications/"),
        ("I want to hire new graduates for a sales role in my company, the budget is for about an hour for each test. Give me some options", "https://www.shl.com/solutions/products/product-catalog/view/english-comprehension-new/"),
        
        ("I am looking for a COO for my company in China and I want to see if they are culturally a right fit for our company. Suggest me an assessment that they can complete in about an hour", "https://www.shl.com/products/product-catalog/view/enterprise-leadership-report/"),
        ("I am looking for a COO for my company in China and I want to see if they are culturally a right fit for our company. Suggest me an assessment that they can complete in about an hour", "https://www.shl.com/products/product-catalog/view/occupational-personality-questionnaire-opq32r/"),
        ("I am looking for a COO for my company in China and I want to see if they are culturally a right fit for our company. Suggest me an assessment that they can complete in about an hour", "https://www.shl.com/solutions/products/product-catalog/view/opq-leadership-report/"),
        ("I am looking for a COO for my company in China and I want to see if they are culturally a right fit for our company. Suggest me an assessment that they can complete in about an hour", "https://www.shl.com/solutions/products/product-catalog/view/opq-team-types-and-leadership-styles-report"),
        ("I am looking for a COO for my company in China and I want to see if they are culturally a right fit for our company. Suggest me an assessment that they can complete in about an hour", "https://www.shl.com/products/product-catalog/view/enterprise-leadership-report-2-0/"),
        ("I am looking for a COO for my company in China and I want to see if they are culturally a right fit for our company. Suggest me an assessment that they can complete in about an hour", "https://www.shl.com/solutions/products/product-catalog/view/global-skills-assessment/"),
        
        ("Content Writer required, expert in English and SEO.", "https://www.shl.com/products/product-catalog/view/english-comprehension-new/"),
        ("Content Writer required, expert in English and SEO.", "https://www.shl.com/solutions/products/product-catalog/view/drupal-new/"),
        ("Content Writer required, expert in English and SEO.", "https://www.shl.com/solutions/products/product-catalog/view/written-english-v1/"),
        ("Content Writer required, expert in English and SEO.", "https://www.shl.com/solutions/products/product-catalog/view/occupational-personality-questionnaire-opq32r/"),
        ("Content Writer required, expert in English and SEO.", "https://www.shl.com/solutions/products/product-catalog/view/search-engine-optimization-new/"),
        
        ("ICICI Bank Assistant Admin, Experience required 0-2 years, test should be 30-40 mins long", "https://www.shl.com/solutions/products/product-catalog/view/administrative-professional-short-form/"),
        ("ICICI Bank Assistant Admin, Experience required 0-2 years, test should be 30-40 mins long", "https://www.shl.com/solutions/products/product-catalog/view/verify-numerical-ability/"),
        ("ICICI Bank Assistant Admin, Experience required 0-2 years, test should be 30-40 mins long", "https://www.shl.com/solutions/products/product-catalog/view/financial-professional-short-form/"),
        ("ICICI Bank Assistant Admin, Experience required 0-2 years, test should be 30-40 mins long", "https://www.shl.com/solutions/products/product-catalog/view/bank-administrative-assistant-short-form/"),
        ("ICICI Bank Assistant Admin, Experience required 0-2 years, test should be 30-40 mins long", "https://www.shl.com/solutions/products/product-catalog/view/general-entry-level-data-entry-7-0-solution/"),
        ("ICICI Bank Assistant Admin, Experience required 0-2 years, test should be 30-40 mins long", "https://www.shl.com/solutions/products/product-catalog/view/basic-computer-literacy-windows-10-new/"),
        
        ("I want to hire a Senior Data Analyst with 5 years of experience and expertise in SQL, Excel and Python. The assessment can be 1-2 hour long", "https://www.shl.com/solutions/products/product-catalog/view/sql-server-analysis-services-%28ssas%29-%28new%29/"),
        ("I want to hire a Senior Data Analyst with 5 years of experience and expertise in SQL, Excel and Python. The assessment can be 1-2 hour long", "https://www.shl.com/solutions/products/product-catalog/view/sql-server-new/"),
        ("I want to hire a Senior Data Analyst with 5 years of experience and expertise in SQL, Excel and Python. The assessment can be 1-2 hour long", "https://www.shl.com/solutions/products/product-catalog/view/automata-sql-new/"),
        ("I want to hire a Senior Data Analyst with 5 years of experience and expertise in SQL, Excel and Python. The assessment can be 1-2 hour long", "https://www.shl.com/solutions/products/product-catalog/view/python-new/"),
        ("I want to hire a Senior Data Analyst with 5 years of experience and expertise in SQL, Excel and Python. The assessment can be 1-2 hour long", "https://www.shl.com/solutions/products/product-catalog/view/tableau-new/"),
        ("I want to hire a Senior Data Analyst with 5 years of experience and expertise in SQL, Excel and Python. The assessment can be 1-2 hour long", "https://www.shl.com/solutions/products/product-catalog/view/microsoft-excel-365-new/"),
        ("I want to hire a Senior Data Analyst with 5 years of experience and expertise in SQL, Excel and Python. The assessment can be 1-2 hour long", "https://www.shl.com/solutions/products/product-catalog/view/microsoft-excel-365-essentials-new/"),
        ("I want to hire a Senior Data Analyst with 5 years of experience and expertise in SQL, Excel and Python. The assessment can be 1-2 hour long", "https://www.shl.com/solutions/products/product-catalog/view/professional-7-0-solution-3958/"),
        ("I want to hire a Senior Data Analyst with 5 years of experience and expertise in SQL, Excel and Python. The assessment can be 1-2 hour long", "https://www.shl.com/solutions/products/product-catalog/view/professional-7-1-solution/"),
        ("I want to hire a Senior Data Analyst with 5 years of experience and expertise in SQL, Excel and Python. The assessment can be 1-2 hour long", "https://www.shl.com/solutions/products/product-catalog/view/data-warehousing-concepts/"),
    ]
    
    # Group by query
    query_to_urls = defaultdict(list)
    for query, url in raw_data:
        query_to_urls[query].append(url)
    
    # Convert to training format
    training_data = []
    for query, urls in query_to_urls.items():
        training_data.append({
            "query": query,
            "relevant_assessments": [{"url": url} for url in urls]
        })
    
    logger.info(f"Parsed {len(training_data)} unique queries")
    logger.info(f"Total query-URL pairs: {len(raw_data)}")
    
    return training_data


def save_training_data(output_path: Path = None):
    """Save parsed training data to JSON"""
    if output_path is None:
        output_path = config.TRAIN_DATA_PATH
    
    training_data = parse_training_data()
    
    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✓ Saved training data to {output_path}")
    
    # Print summary
    logger.info("\nTraining Data Summary:")
    logger.info("="*80)
    for i, item in enumerate(training_data, 1):
        logger.info(f"\n{i}. Query: {item['query'][:100]}...")
        logger.info(f"   Relevant assessments: {len(item['relevant_assessments'])}")
    logger.info("="*80)
    
    return training_data


if __name__ == "__main__":
    config.ensure_directories()
    save_training_data()
