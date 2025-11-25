#!/usr/bin/env python
"""
Complete setup and build script for SHL Assessment Recommendation System
Runs all necessary steps to get the system ready
"""
import sys
import subprocess
from pathlib import Path

from config import config
from utils import setup_logger

logger = setup_logger(__name__)


def run_command(command: str, description: str) -> bool:
    """
    Run a command and handle errors
    
    Args:
        command: Command to run
        description: Description of the step
        
    Returns:
        True if successful, False otherwise
    """
    logger.info(f"\n{'='*80}")
    logger.info(f"STEP: {description}")
    logger.info('='*80)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=False,
            text=True
        )
        logger.info(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ {description} failed: {e}")
        return False


def main():
    """Main setup workflow"""
    logger.info("""
╔══════════════════════════════════════════════════════════════════════╗
║  SHL Assessment Recommendation System - Setup & Build Script         ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Ensure directories exist
    config.ensure_directories()
    
    # Use the current Python interpreter (from venv if activated)
    python_exe = sys.executable
    
    # Check if running non-interactively (e.g., in CI/CD)
    is_interactive = sys.stdin.isatty()
    
    steps = [
        (f'"{python_exe}" scraper.py', "Scrape SHL catalog"),
        (f'"{python_exe}" vector_store.py', "Build vector store and embeddings"),
        (f'"{python_exe}" evaluate.py', "Run evaluation pipeline"),
    ]
    
    failed_steps = []
    
    for command, description in steps:
        if not run_command(command, description):
            failed_steps.append(description)
            if is_interactive:
                response = input(f"\n⚠️  Step failed. Continue anyway? (y/n): ")
                if response.lower() != 'y':
                    logger.error("Setup aborted by user")
                    sys.exit(1)
            else:
                logger.warning(f"Step failed (non-interactive mode): {description}")
                logger.warning("Continuing with next step...")
    
    logger.info("\n" + "="*80)
    logger.info("SETUP COMPLETE")
    logger.info("="*80)
    
    if failed_steps:
        logger.warning(f"Some steps failed: {', '.join(failed_steps)}")
        logger.warning("Please review the errors above")
    else:
        logger.info("✓ All steps completed successfully!")
    
    logger.info("\nNext steps:")
    logger.info("1. Review generated files in the 'data/' directory")
    logger.info("2. (Optional) Generate test predictions:")
    logger.info("   python generate_predictions.py <firstname> <lastname>")
    logger.info("3. Start the API server:")
    logger.info("   python main.py")
    logger.info("4. Open http://localhost:8000 in your browser")
    logger.info("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
