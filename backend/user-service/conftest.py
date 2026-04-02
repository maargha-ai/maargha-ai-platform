# conftest.py
import sys
from pathlib import Path

# Add user_service/ (the Django project root) to sys.path
# so that imports like "from user_service.monitoring.logger import ..."
# resolve to user_service/user_service/monitoring/logger.py
sys.path.insert(0, str(Path(__file__).parent / "user_service"))
