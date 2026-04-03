#!/usr/bin/env python3
"""
Streamlit Cloud Deployment Verification Script
Verifies all deployment files are correctly configured before pushing to GitHub
"""

import os
import sys
from pathlib import Path

print("\n" + "="*70)
print("STREAMLIT CLOUD DEPLOYMENT VERIFICATION")
print("="*70 + "\n")

# Color codes for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

checks_passed = 0
checks_total = 0

def check(condition, message, details=""):
    global checks_passed, checks_total
    checks_total += 1
    status = f"{GREEN}✓{RESET}" if condition else f"{RED}✗{RESET}"
    print(f"{status} {message}")
    if details and not condition:
        print(f"  {YELLOW}→ {details}{RESET}")
    if condition:
        checks_passed += 1
    return condition

# Check 1: runtime.txt exists
print("[1] Python Version Configuration")
print("-" * 70)
runtime_file = Path("runtime.txt")
if check(runtime_file.exists(), "runtime.txt exists"):
    with open(runtime_file, encoding='utf-8') as f:
        content = f.read().strip()
        check(content.startswith("python-3"), 
              f"Python version specified: {content}",
              "Should be python-3.x.x format")

# Check 2: .streamlit/config.toml exists
print("\n[2] Streamlit Configuration")
print("-" * 70)
config_file = Path(".streamlit/config.toml")
if check(config_file.exists(), ".streamlit/config.toml exists"):
    with open(config_file, encoding='utf-8') as f:
        content = f.read()
        check("headless = true" in content, 
              "Headless mode enabled (better for cloud)",
              "Add 'headless = true' in [server] section")
        check("caching" in content.lower(), 
              "Caching configuration present",
              "Add [client.caching] for better performance")

# Check 3: frontend/requirements.txt
print("\n[3] Frontend Dependencies")
print("-" * 70)
frontend_reqs = Path("frontend/requirements.txt")
if check(frontend_reqs.exists(), "frontend/requirements.txt exists"):
    with open(frontend_reqs, encoding='utf-8') as f:
        content = f.read()
        required_packages = ["streamlit", "pandas", "numpy", "plotly", "requests"]
        for pkg in required_packages:
            check(pkg.lower() in content.lower(), 
                  f"✓ {pkg} specified",
                  f"Missing {pkg} in frontend requirements")

# Check 4: backend/requirements.txt
print("\n[4] Backend Dependencies")
print("-" * 70)
backend_reqs = Path("backend/requirements.txt")
if check(backend_reqs.exists(), "backend/requirements.txt exists"):
    with open(backend_reqs, encoding='utf-8') as f:
        content = f.read()
        required_packages = ["fastapi", "uvicorn", "pandas", "numpy", "scikit-learn"]
        for pkg in required_packages:
            check(pkg.lower() in content.lower(), 
                  f"✓ {pkg} specified",
                  f"Missing {pkg} in backend requirements")

# Check 5: .gitignore
print("\n[5] Git Configuration")
print("-" * 70)
gitignore_file = Path(".gitignore")
if check(gitignore_file.exists(), ".gitignore exists"):
    with open(gitignore_file, encoding='utf-8') as f:
        content = f.read()
        check("__pycache__" in content, 
              "__pycache__/ ignored",
              "Add '__pycache__/' to .gitignore")
        check(".venv" in content, 
              "Virtual environment ignored",
              "Add '.venv' to .gitignore")
        check(".env" in content, 
              "Environment files ignored",
              "Add '.env' to .gitignore")

# Check 6: frontend/app.py
print("\n[6] Frontend Application")
print("-" * 70)
frontend_app = Path("frontend/app.py")
if check(frontend_app.exists(), "frontend/app.py exists"):
    with open(frontend_app, encoding='utf-8') as f:
        content = f.read()
        check("import streamlit" in content, 
              "Streamlit imported",
              "File should contain 'import streamlit as st'")
        check("st." in content, 
              "Streamlit functions used",
              "File should use st.* functions")

# Check 7: README
print("\n[7] Documentation")
print("-" * 70)
readme_file = Path("README.md")
check(readme_file.exists(), "README.md exists", "Add project documentation")

# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"\nTests passed: {GREEN}{checks_passed}/{checks_total}{RESET}")

if checks_passed == checks_total:
    print(f"\n{GREEN}✓ ALL CHECKS PASSED - Ready for deployment!{RESET}\n")
    print("Next steps:")
    print("  1. git add .")
    print("  2. git commit -m 'Optimize deployment for Streamlit Cloud'")
    print("  3. git push")
    print("  4. Go to https://streamlit.io/cloud")
    print("  5. Deploy with main file: frontend/app.py")
    sys.exit(0)
else:
    failed = checks_total - checks_passed
    print(f"\n{RED}✗ {failed} checks failed - Fix issues before deployment{RESET}\n")
    sys.exit(1)
