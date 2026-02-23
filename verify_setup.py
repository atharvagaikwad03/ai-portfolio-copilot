#!/usr/bin/env python3
"""Script to verify the setup is correct."""
import sys
from pathlib import Path

def check_imports():
    """Check if all required packages can be imported."""
    print("Checking Python imports...")
    
    try:
        import langchain
        print("✅ langchain")
    except ImportError:
        print("❌ langchain - Run: pip install -r requirements.txt")
        return False
    
    try:
        import langchain_openai
        print("✅ langchain-openai")
    except ImportError:
        print("❌ langchain-openai - Run: pip install -r requirements.txt")
        return False
    
    try:
        import pinecone
        print("✅ pinecone-client")
    except ImportError:
        print("❌ pinecone-client - Run: pip install -r requirements.txt")
        return False
    
    try:
        import fastapi
        print("✅ fastapi")
    except ImportError:
        print("❌ fastapi - Run: pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists and has required keys."""
    print("\nChecking .env file...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found - Copy from .env.example")
        return False
    
    with open(env_file) as f:
        content = f.read()
    
    required_keys = ["OPENAI_API_KEY", "PINECONE_API_KEY"]
    missing = []
    
    for key in required_keys:
        if key not in content or f"{key}=your_" in content:
            missing.append(key)
    
    if missing:
        print(f"⚠️  Missing or incomplete keys: {', '.join(missing)}")
        return False
    
    print("✅ .env file configured")
    return True

def check_structure():
    """Check if project structure is correct."""
    print("\nChecking project structure...")
    
    required_dirs = [
        "backend/python/agents",
        "backend/python/rag",
        "backend/python/api",
        "backend/nodejs",
        "data",
        "frontend"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} - Missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all checks."""
    print("🔍 Verifying AI Portfolio Copilot Setup\n")
    
    checks = [
        ("Project Structure", check_structure),
        ("Python Imports", check_imports),
        ("Environment File", check_env_file)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")
            results.append((name, False))
    
    print("\n" + "="*50)
    print("Verification Summary:")
    print("="*50)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
        if not result:
            all_passed = False
    
    print("="*50)
    
    if all_passed:
        print("\n✨ All checks passed! Setup is complete.")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
