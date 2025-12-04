import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import FastAPI app
from app.main import app

# Vercel requires the app to be accessible
# This is the handler that Vercel will use

