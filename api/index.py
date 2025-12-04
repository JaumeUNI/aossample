import sys
import os
from pathlib import Path

# Get the project root directory (parent of api/)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import the FastAPI app
from app.main import app

# Vercel will use this app object
__all__ = ["app"]

