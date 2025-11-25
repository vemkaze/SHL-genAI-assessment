"""
Real Training Data from SHL Assignment
This file contains the actual training data provided in the assignment
Format: List of (query, assessment_url) pairs
"""

REAL_TRAINING_DATA = [
    # Java developers with collaboration (5 relevant assessments)
    ("I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.", [
        "https://www.shl.com/solutions/products/product-catalog/view/automata-fix-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/core-java-entry-level-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/java-8-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/core-java-advanced-level-new/",
        "https://www.shl.com/products/product-catalog/view/interpersonal-communications/"
    ]),
    
    # Entry-level sales role (9 relevant assessments)
    ("I want to hire new graduates for a sales role in my company, the budget is for about an hour for each test. Give me some options", [
        "https://www.shl.com/solutions/products/product-catalog/view/entry-level-sales-7-1/",
        "https://www.shl.com/solutions/products/product-catalog/view/entry-level-sales-sift-out-7-1/",
        "https://www.shl.com/solutions/products/product-catalog/view/entry-level-sales-solution/",
        "https://www.shl.com/solutions/products/product-catalog/view/sales-representative-solution/",
        "https://www.shl.com/products/product-catalog/view/business-communication-adaptive/",
        "https://www.shl.com/solutions/products/product-catalog/view/technical-sales-associate-solution/",
        "https://www.shl.com/solutions/products/product-catalog/view/svar-spoken-english-indian-accent-new/",
        "https://www.shl.com/products/product-catalog/view/interpersonal-communications/",
        "https://www.shl.com/solutions/products/product-catalog/view/english-comprehension-new/"
    ]),
    
    # COO for China (6 relevant assessments)
    ("I am looking for a COO for my company in China and I want to see if they are culturally a right fit for our company. Suggest me an assessment that they can complete in about an hour", [
        "https://www.shl.com/products/product-catalog/view/enterprise-leadership-report/",
        "https://www.shl.com/products/product-catalog/view/occupational-personality-questionnaire-opq32r/",
        "https://www.shl.com/solutions/products/product-catalog/view/opq-leadership-report/",
        "https://www.shl.com/solutions/products/product-catalog/view/opq-team-types-and-leadership-styles-report",
        "https://www.shl.com/products/product-catalog/view/enterprise-leadership-report-2-0/",
        "https://www.shl.com/solutions/products/product-catalog/view/global-skills-assessment/"
    ]),
    
    # Content Writer (5 relevant assessments)
    ("Content Writer required, expert in English and SEO.", [
        "https://www.shl.com/products/product-catalog/view/english-comprehension-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/drupal-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/written-english-v1/",
        "https://www.shl.com/solutions/products/product-catalog/view/occupational-personality-questionnaire-opq32r/",
        "https://www.shl.com/solutions/products/product-catalog/view/search-engine-optimization-new/"
    ]),
    
    # ICICI Bank Assistant Admin (6 relevant assessments)
    ("ICICI Bank Assistant Admin, Experience required 0-2 years, test should be 30-40 mins long", [
        "https://www.shl.com/solutions/products/product-catalog/view/administrative-professional-short-form/",
        "https://www.shl.com/solutions/products/product-catalog/view/verify-numerical-ability/",
        "https://www.shl.com/solutions/products/product-catalog/view/financial-professional-short-form/",
        "https://www.shl.com/solutions/products/product-catalog/view/bank-administrative-assistant-short-form/",
        "https://www.shl.com/solutions/products/product-catalog/view/general-entry-level-data-entry-7-0-solution/",
        "https://www.shl.com/solutions/products/product-catalog/view/basic-computer-literacy-windows-10-new/"
    ]),
    
    # Senior Data Analyst (10 relevant assessments)
    ("I want to hire a Senior Data Analyst with 5 years of experience and expertise in SQL, Excel and Python. The assessment can be 1-2 hour long", [
        "https://www.shl.com/solutions/products/product-catalog/view/sql-server-analysis-services-%28ssas%29-%28new%29/",
        "https://www.shl.com/solutions/products/product-catalog/view/sql-server-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/automata-sql-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/python-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/tableau-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/microsoft-excel-365-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/microsoft-excel-365-essentials-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/professional-7-0-solution-3958/",
        "https://www.shl.com/solutions/products/product-catalog/view/professional-7-1-solution/",
        "https://www.shl.com/solutions/products/product-catalog/view/data-warehousing-concepts/"
    ])
]

# Note: The assignment also includes two longer queries:
# 1. Radio station Programming Manager JD (5 relevant assessments)
# 2. QA Engineer at SHL JD (9 relevant assessments)  
# 3. Marketing Manager for Recro JD (5 relevant assessments)
# 4. Consultant position JD (5 relevant assessments)
# These are not included here due to length but are in parse_training_data.py

def get_training_data_json():
    """Convert to JSON format for evaluation"""
    result = []
    for query, urls in REAL_TRAINING_DATA:
        result.append({
            "query": query,
            "relevant_assessments": [{"url": url} for url in urls]
        })
    return result


if __name__ == "__main__":
    import json
    data = get_training_data_json()
    print(f"Total queries: {len(data)}")
    print(f"Total relevant assessments: {sum(len(q['relevant_assessments']) for q in data)}")
    print("\nSample:")
    print(json.dumps(data[0], indent=2))
