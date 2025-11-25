"""
Quick test script to verify the system is working
"""
import sys
from pathlib import Path

from config import config
from utils import setup_logger

logger = setup_logger(__name__)


def test_imports():
    """Test that all required modules can be imported"""
    logger.info("Testing imports...")
    
    try:
        import requests
        import bs4
        import numpy
        import faiss
        import sentence_transformers
        import fastapi
        import google.generativeai
        logger.info("✓ All required packages imported successfully")
        return True
    except ImportError as e:
        logger.error(f"✗ Import failed: {e}")
        logger.error("Please run: pip install -r requirements.txt")
        return False


def test_config():
    """Test configuration"""
    logger.info("\nTesting configuration...")
    
    try:
        config.ensure_directories()
        logger.info(f"✓ Data directory: {config.DATA_DIR}")
        logger.info(f"✓ Models directory: {config.MODELS_DIR}")
        
        if config.GEMINI_API_KEY:
            logger.info("✓ Gemini API key configured")
        else:
            logger.warning("⚠ Gemini API key not configured (optional)")
        
        return True
    except Exception as e:
        logger.error(f"✗ Configuration test failed: {e}")
        return False


def test_data_files():
    """Test if data files exist"""
    logger.info("\nChecking data files...")
    
    files_to_check = [
        (config.CATALOG_JSON, "Catalog JSON", False),
        (config.CATALOG_CSV, "Catalog CSV", False),
        (config.FAISS_INDEX_PATH / "index.faiss", "FAISS Index", False),
    ]
    
    all_exist = True
    for file_path, name, required in files_to_check:
        if file_path.exists():
            logger.info(f"✓ {name} exists: {file_path}")
        else:
            if required:
                logger.error(f"✗ {name} missing: {file_path}")
                all_exist = False
            else:
                logger.warning(f"⚠ {name} not found (will be created): {file_path}")
    
    return all_exist


def test_api_health():
    """Test if API can start"""
    logger.info("\nTesting API initialization...")
    
    try:
        from main import app
        logger.info("✓ FastAPI app initialized successfully")
        return True
    except Exception as e:
        logger.error(f"✗ API initialization failed: {e}")
        return False


def main():
    """Run all tests"""
    logger.info("""
╔══════════════════════════════════════════════════════════════════════╗
║           SHL Assessment System - Quick Test Suite                   ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Data Files", test_data_files),
        ("API Initialization", test_api_health),
    ]
    
    results = []
    
    for name, test_func in tests:
        logger.info(f"\n{'='*80}")
        logger.info(f"TEST: {name}")
        logger.info('='*80)
        
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            logger.error(f"Test '{name}' raised exception: {e}")
            results.append((name, False))
    
    # Summary
    logger.info("\n" + "="*80)
    logger.info("TEST SUMMARY")
    logger.info("="*80)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status}: {name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    logger.info(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("\n✓ All tests passed! System is ready.")
        logger.info("\nNext steps:")
        logger.info("1. Run: python setup.py (to build data and models)")
        logger.info("2. Run: python main.py (to start the server)")
    else:
        logger.warning("\n⚠ Some tests failed. Please review the errors above.")
        logger.info("\nQuick fixes:")
        logger.info("- Install dependencies: pip install -r requirements.txt")
        logger.info("- Build system: python setup.py")
        logger.info("- Configure API key: edit .env file")
    
    logger.info("\n" + "="*80 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
