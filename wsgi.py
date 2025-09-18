import sys
import os

# Add your project directory to Python path
path = '/home/yourusername/mysite'
if path not in sys.path:
    sys.path.insert(0, path)

# Import your Flask app
from app import app as application

if __name__ == "__main__":
    application.run()
