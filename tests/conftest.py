import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)


# python -m pytest backend/tests/ -v

# python -m pytest backend/tests/ --cov=backend --cov-report=html
