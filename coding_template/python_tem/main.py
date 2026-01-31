import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# SETUP LOGGING FIRST - before any other imports
from log_service.logger import setup_logging
setup_logging()