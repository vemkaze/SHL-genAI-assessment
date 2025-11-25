# Real Training Data Documentation

## Overview

This system uses **REAL training data** provided in the SHL GenAI Assessment Recommendation assignment. The data was extracted from an Excel file containing actual query-assessment pairs used by SHL.

## Dataset Statistics

- **Total Queries**: 6 unique queries
- **Total Query-Assessment Pairs**: 46 pairs
- **Average Assessments per Query**: 7.7
- **Format**: Query → List of relevant assessment URLs

## Training Queries

### 1. Java Developer with Collaboration (5 assessments)
```
Query: "I am hiring for Java developers who can also collaborate effectively 
        with my business teams. Looking for an assessment(s) that can be 
        completed in 40 minutes."

Relevant Assessments:
- automata-fix-new
- core-java-entry-level-new
- java-8-new
- core-java-advanced-level-new
- interpersonal-communications
```

### 2. Entry-Level Sales (9 assessments)
```
Query: "I want to hire new graduates for a sales role in my company, 
        the budget is for about an hour for each test. Give me some options"

Relevant Assessments:
- entry-level-sales-7-1
- entry-level-sales-sift-out-7-1
- entry-level-sales-solution
- sales-representative-solution
- business-communication-adaptive
- technical-sales-associate-solution
- svar-spoken-english-indian-accent-new
- interpersonal-communications
- english-comprehension-new
```

### 3. COO for China - Cultural Fit (6 assessments)
```
Query: "I am looking for a COO for my company in China and I want to see 
        if they are culturally a right fit for our company. Suggest me an 
        assessment that they can complete in about an hour"

Relevant Assessments:
- enterprise-leadership-report
- occupational-personality-questionnaire-opq32r
- opq-leadership-report
- opq-team-types-and-leadership-styles-report
- enterprise-leadership-report-2-0
- global-skills-assessment
```

### 4. Content Writer - English & SEO (5 assessments)
```
Query: "Content Writer required, expert in English and SEO."

Relevant Assessments:
- english-comprehension-new
- drupal-new
- written-english-v1
- occupational-personality-questionnaire-opq32r
- search-engine-optimization-new
```

### 5. ICICI Bank Assistant Admin (6 assessments)
```
Query: "ICICI Bank Assistant Admin, Experience required 0-2 years, 
        test should be 30-40 mins long"

Relevant Assessments:
- administrative-professional-short-form
- verify-numerical-ability
- financial-professional-short-form
- bank-administrative-assistant-short-form
- general-entry-level-data-entry-7-0-solution
- basic-computer-literacy-windows-10-new
```

### 6. Senior Data Analyst (10 assessments)
```
Query: "I want to hire a Senior Data Analyst with 5 years of experience 
        and expertise in SQL, Excel and Python. The assessment can be 1-2 hour long"

Relevant Assessments:
- sql-server-analysis-services-(ssas)-(new)
- sql-server-new
- automata-sql-new
- python-new
- tableau-new
- microsoft-excel-365-new
- microsoft-excel-365-essentials-new
- professional-7-0-solution-3958
- professional-7-1-solution
- data-warehousing-concepts
```

## Additional Training Data

The assignment also included 4 longer queries with detailed job descriptions:

1. **Radio Station Programming Manager** (5 assessments)
2. **QA Engineer at SHL** (9 assessments)
3. **Marketing Manager for Recro** (5 assessments)
4. **Consultant Position** (5 assessments)

These queries contain full job descriptions with responsibilities, skills, and qualifications.

## Data Format

### Raw Format (Excel)
```
Query | Assessment_url
------|----------------
I am hiring for... | https://www.shl.com/solutions/products/product-catalog/view/java-8-new/
I am hiring for... | https://www.shl.com/solutions/products/product-catalog/view/automata-fix-new/
```

### Processed Format (JSON)
```json
[
  {
    "query": "I am hiring for Java developers...",
    "relevant_assessments": [
      {"url": "https://www.shl.com/solutions/products/product-catalog/view/java-8-new/"},
      {"url": "https://www.shl.com/solutions/products/product-catalog/view/automata-fix-new/"}
    ]
  }
]
```

## Usage in System

1. **Training Data Location**: `data/train.json`
2. **Parser Script**: `parse_training_data.py`
3. **Evaluation**: Used in `evaluate.py` to compute Recall@10

### Loading Training Data

```python
from parse_training_data import parse_training_data

# Get parsed training data
training_data = parse_training_data()

# Each item has structure:
# {
#   "query": str,
#   "relevant_assessments": [{"url": str}, ...]
# }
```

### Evaluation Metrics

The system computes **Recall@10** on this training data:

```
Recall@10 = (Number of relevant assessments in top 10) / (Total relevant assessments)
```

## Key Insights

### Query Characteristics
- Mix of technical and behavioral requirements
- Duration constraints (30-40 mins, 1 hour, 1-2 hours)
- Experience levels (entry-level, 5+ years)
- Domain-specific (banking, tech, sales, leadership)

### Assessment Patterns
- Technical roles → Multiple technical skill tests
- Leadership roles → Personality + leadership assessments
- Entry-level → General ability + domain basics
- Senior roles → Advanced skills + comprehensive solutions

### Challenge Areas
1. **Duration Filtering**: Queries specify time constraints
2. **Multi-Domain**: Technical + soft skills (e.g., Java + collaboration)
3. **Geographic/Cultural**: China COO role with cultural fit
4. **Specificity**: Some queries very specific (ICICI Bank), others generic (Content Writer)

## Validation

To validate the system's performance:

```bash
# Run evaluation on real training data
python evaluate.py

# Expected output:
# - Recall@10 for baseline (vector search only)
# - Recall@10 for improved (with reranking)
# - Improvement percentage
```

## Notes

- All URLs point to real SHL assessment pages
- Some assessments appear in multiple queries (e.g., "interpersonal-communications")
- The data represents realistic usage patterns of the SHL catalog
- No synthetic or generated data - this is 100% real-world data

## References

- Original data source: Excel file provided in assignment
- Parser implementation: `parse_training_data.py`
- Data storage: `data/real_training_data.py` (Python format)
- JSON format: `data/train.json` (generated by parser)
