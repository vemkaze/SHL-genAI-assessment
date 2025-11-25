"""Test if all imports work"""
import sys

print("Testing imports...")

try:
    print("1. FastAPI...")
    from fastapi import FastAPI
    print("   ✓ FastAPI OK")
except Exception as e:
    print(f"   ✗ FastAPI failed: {e}")
    sys.exit(1)

try:
    print("2. Config...")
    from config import config
    print("   ✓ Config OK")
except Exception as e:
    print(f"   ✗ Config failed: {e}")
    sys.exit(1)

try:
    print("3. Utils...")
    from utils import setup_logger
    print("   ✓ Utils OK")
except Exception as e:
    print(f"   ✗ Utils failed: {e}")
    sys.exit(1)

try:
    print("4. VectorStore...")
    from vector_store import VectorStore
    print("   ✓ VectorStore OK")
except Exception as e:
    print(f"   ✗ VectorStore failed: {e}")
    sys.exit(1)

try:
    print("5. Retriever...")
    from retriever import AssessmentRetriever
    print("   ✓ Retriever OK")
except Exception as e:
    print(f"   ✗ Retriever failed: {e}")
    sys.exit(1)

print("\nAll imports successful!")
