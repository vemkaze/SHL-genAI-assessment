"""
Utility functions for logging and common operations
"""
import logging
import sys
from typing import Any, Dict, List
import json

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Setup a logger with consistent formatting
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

def save_json(data: Any, filepath: str) -> None:
    """Save data to JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(filepath: str) -> Any:
    """Load data from JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text.strip()

def format_assessment(assessment: Dict) -> str:
    """
    Format assessment data for embedding
    
    Args:
        assessment: Assessment dictionary
        
    Returns:
        Formatted text string
    """
    parts = [
        f"Assessment: {assessment.get('name', '')}",
        f"Type: {', '.join(assessment.get('test_type', []))}",
        f"Description: {assessment.get('description', '')}",
    ]
    
    if assessment.get('duration'):
        parts.append(f"Duration: {assessment['duration']} minutes")
    
    if assessment.get('adaptive_support'):
        parts.append(f"Adaptive: {assessment['adaptive_support']}")
    
    if assessment.get('remote_support'):
        parts.append(f"Remote: {assessment['remote_support']}")
    
    return " | ".join(parts)
