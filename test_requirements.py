#!/usr/bin/env python3
"""
Test script to verify all requirements are compatible
Run this before deploying to Binder
"""

import sys
import importlib
import subprocess
from pathlib import Path

def test_package_import(package_name, import_name=None):
    """Test if a package can be imported"""
    if import_name is None:
        import_name = package_name
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✅ {package_name}: {version}")
        return True
    except ImportError as e:
        print(f"❌ {package_name}: {e}")
        return False
    except Exception as e:
        print(f"⚠️ {package_name}: {e}")
        return False

def main():
    print("🧪 Testing Binder Requirements Compatibility")
    print("=" * 50)
    
    # Core packages to test
    packages_to_test = [
        # Core Framework
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("pydantic", "pydantic"),
        
        # Quantum Computing
        ("qutip", "qutip"),
        ("numpy", "numpy"),
        ("scipy", "scipy"),
        
        # Visualization
        ("matplotlib", "matplotlib"),
        ("seaborn", "seaborn"),
        ("plotly", "plotly"),
        
        # Web & API
        ("httpx", "httpx"),
        ("websockets", "websockets"),
        ("aiofiles", "aiofiles"),
        
        # Jupyter
        ("jupyter", "jupyter"),
        ("ipywidgets", "ipywidgets"),
        ("notebook", "notebook"),
        
        # AI & Chatbot
        ("openai", "openai"),
        ("markdown", "markdown"),
        
        # Utilities
        ("click", "click"),
        ("rich", "rich"),
        ("pandas", "pandas"),
        ("pyyaml", "yaml"),
        
        # Security
        ("cryptography", "cryptography"),
        ("pycryptodome", "Crypto"),
        
        # System
        ("psutil", "psutil"),
        ("python-dotenv", "dotenv"),
    ]
    
    success_count = 0
    total_count = len(packages_to_test)
    
    print(f"Testing {total_count} packages...")
    print()
    
    for package_name, import_name in packages_to_test:
        if test_package_import(package_name, import_name):
            success_count += 1
    
    print()
    print("=" * 50)
    print(f"Results: {success_count}/{total_count} packages working")
    
    if success_count == total_count:
        print("🎉 All packages are compatible!")
        return 0
    else:
        print("⚠️ Some packages have issues")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
