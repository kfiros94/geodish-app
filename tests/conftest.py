# tests/conftest.py
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print(f"✅ conftest.py loaded - project root: {project_root}")